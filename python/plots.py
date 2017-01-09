import os
import sys
import re
import array
import ROOT
from ROOT import *

gROOT.SetBatch(True)
gSystem.Load("~/Dijets/CMSSW_5_3_32_patch3/lib/slc6_amd64_gcc472/libMyToolsRootUtils.so")
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
seaborn = Root.SeabornInterface()
seaborn.Initialize()
import CMSDIJET.QCDAnalysis.mjj_fits
from CMSDIJET.QCDAnalysis.mjj_fits import *
#import CMSDIJET.QCDAnalysis.simulation_configuration_8TeV
#from CMSDIJET.QCDAnalysis.simulation_configuration_8TeV import *
import CMSDIJET.QCDAnalysis.analysis_configuration_8TeV as analysis_config
import CMSDIJET.QCDAnalysis.mjj_common as mjj_common

# Attempt at a generic plot to compare stuff.
def plot_compare(names, histograms, save_tag, nominal_name=None, legend_entries=None, log=True, log_ratio=False, x_range=None, y_range=None):
	c = TCanvas(save_tag, save_tag, 800, 1200)
	top = TPad("top", "top", 0., 0.5, 1., 1.)
	top.SetBottomMargin(0.02)
	top.Draw()
	top.cd()
	l = TLegend(0.6, 0.6, 0.85, 0.8)
	if log:
		top.SetLogy()

	if not nominal_name:
		nominal_name = names[0]

	if x_range:
		x_min = x_range[0]
		x_max = x_range[1]
	else:
		x_min = histograms[nominal_name].GetXaxis().GetXmin()
		x_max = histograms[nominal_name].GetXaxis().GetXmax()

	if y_range:
		y_min = y_range[0]
		y_max = y_range[1]
	else:
		y_max = -1.
		for name in names:
			if histograms[name].GetMaximum() > y_max:
				y_max = histograms[name].GetMaximum()
		if log:
			y_min = 0.05
			y_max = y_max * 10
		else:
			y_min = 0.
			y_max = y_max * 1.3

	frame_top = TH1F("frame_top", "frame_top", 100, x_min, x_max)
	frame_top.SetMinimum(y_min)
	frame_top.SetMaximum(y_max)
	frame_top.GetXaxis().SetLabelSize(0)
	frame_top.GetXaxis().SetTitleSize(0)
	frame_top.GetYaxis().SetLabelSize(0.04)
	frame_top.GetYaxis().SetTitleSize(0.04)
	frame_top.Draw("axis")

	style_counter = 0
	for name in names:
		histograms[name].SetLineColor(seaborn.GetColorRoot("dark", style_counter))
		histograms[name].SetLineWidth(2)
		histograms[name].Draw("hist same")
		if legend_entries.has_key(name):
			l.AddEntry(histograms[name], legend_entries[name], "l")
		else:
			l.AddEntry(name, legend_entries[name], "l")
		style_counter += 1
	l.Draw()

	c.cd()
	bottom = TPad("bottom", "bottom", 0., 0., 1., 0.5)
	bottom.SetTopMargin(0.03)
	bottom.SetBottomMargin(0.2)
	bottom.Draw()
	bottom.cd()
	if log_ratio:
		bottom.SetLogy()
	frame_bottom = TH1F("frame_bottom", "frame_bottom", 100, x_min, x_max)
	if log_ratio:
		frame_bottom.SetMinimum(1.e-3)
		frame_bottom.SetMaximum(5.)
	else:
		frame_bottom.SetMinimum(-0.2)
		frame_bottom.SetMaximum(1.2)
	frame_bottom.GetXaxis().SetTitle(histograms[nominal_name].GetXaxis().GetTitle())
	frame_bottom.GetYaxis().SetTitle(histograms[nominal_name].GetYaxis().GetTitle())
	frame_bottom.GetXaxis().SetLabelSize(0.04)
	frame_bottom.GetXaxis().SetTitleSize(0.06)
	frame_bottom.GetXaxis().SetLabelOffset(0.01)
	frame_bottom.GetXaxis().SetTitleOffset(1.1)

	frame_bottom.GetYaxis().SetLabelSize(0.04)
	frame_bottom.GetYaxis().SetTitleSize(0.037)
	frame_bottom.GetYaxis().SetTitleOffset(0.7)

	frame_bottom.Draw("axis")

	ratio_histograms = {}
	for name in names:
		if name == nominal_name:
			continue
		ratio_histograms[name] = histograms[name].Clone()
		ratio_histograms[name].Divide(histograms[name], histograms[nominal_name], 1, 1, "B")
		ratio_histograms[name].SetLineColor(histograms[name].GetLineColor())
		ratio_histograms[name].SetLineWidth(histograms[name].GetLineWidth())
		ratio_histograms[name].Draw("hist same")

	c.cd()
	c.SaveAs(analysis_config.figure_directory + "/CSVX/" + c.GetName() + ".pdf")

def MakeMjjPlot(data_hist, cached_fit_results=None, signal_histograms=None, signal_names=None, save_tag="c_mjj", x_range=None, log=False, fit_min=500., fit_max=1500., save_file=None, blind=True):
	print "[MakeMjjPlot] INFO : Welcome to MakeMjjPlot with save_tag=" + save_tag

	if blind:
		for bin in xrange(1, data_hist.GetNbinsX() + 1):
			if TMath.Abs(data_hist.GetBinCenter(bin) - 750.) < 75.:
				data_hist.SetBinContent(bin, 0.)
				data_hist.SetBinError(bin, 0.)

	if not cached_fit_results:
		print "[MakeMjjPlot] INFO : Launching background fits"
		fit_results = DoMjjBackgroundFit(data_hist, fit_min=fit_min, fit_max=fit_max, rebin=20, blind=blind)
	else:
		print "[MakeMjjPlot] INFO : Using cached fit results"


	# Get histogram limits
	if x_range:
		x_min = x_range[0]
		x_max = x_range[1]
	else:
		x_min = data_hist.GetXaxis().GetXmin()
		x_max = data_hist.GetXaxis().GetXmax()
	y_min = 1.e20
	y_max = -1.e20
	for bin in xrange(1, data_hist.GetNbinsX() + 1):
		if data_hist.GetBinContent(bin) == 0:
			continue
		if data_hist.GetXaxis().GetBinCenter(bin) < x_min or data_hist.GetXaxis().GetBinCenter(bin) > x_max:
			continue
		if data_hist.GetBinContent(bin) < y_min:
			y_min = data_hist.GetBinContent(bin)
		if data_hist.GetBinContent(bin) > y_max:
			y_max = data_hist.GetBinContent(bin)
	print "X axis range: " + str(x_min) + " - " + str(x_max)
	print "Y axis range: " + str(y_min) + " - " + str(y_max)

	c = TCanvas(save_tag, save_tag, 800, 1200)
	l = TLegend(0.55, 0.6, 0.88, 0.88)
	l.SetFillColor(0)
	l.SetBorderSize(0)
	top = TPad("top", "top", 0., 0.5, 1., 1.)
	top.SetBottomMargin(0.03)
	top.Draw()
	if log:
		top.SetLogy()
	c.cd()
	bottom = TPad("bottom", "bottom", 0., 0., 1., 0.5)
	bottom.SetTopMargin(0.02)
	bottom.SetBottomMargin(0.2)
	bottom.Draw()
	ROOT.SetOwnership(c, False)
	ROOT.SetOwnership(top, False)
	ROOT.SetOwnership(bottom, False)

	top.cd()
	data_hist.SetLineColor(ROOT.kBlack)
	data_hist.SetMarkerColor(ROOT.kBlack)
	data_hist.SetMarkerStyle(20)
	
	frame = TH1D("frame", "frame", 100, x_min, x_max)
	#frame.GetYaxis().SetTitle("Events / " + str(int(data_hist.GetXaxis().GetBinWidth(1))) + " GeV")
	frame.GetYaxis().SetTitle("Events / 1 GeV")
	frame.GetXaxis().SetTitleSize(0)
	frame.GetXaxis().SetLabelSize(0)
	if log:
		frame.SetMaximum(y_max * 10.)
		frame.SetMinimum(y_min / 100.)
	else:
		frame.SetMaximum(y_max * 1.3)
		frame.SetMinimum(0.)
	frame.Draw()

	data_hist.GetXaxis().SetTitleSize(0)
	data_hist.GetXaxis().SetLabelSize(0)

	data_hist.Draw("p e1 same")
	l.AddEntry(data_hist, "Data", "pl")
	if cached_fit_results:
		cached_fit_results["fit"].SetLineColor(seaborn.GetColorRoot("dark", 2))
		cached_fit_results["fit"].Draw("same")
		l.AddEntry(cached_fit_results["fit"], "Fit", "l")
	else:
		fit_results["fit"].SetLineColor(seaborn.GetColorRoot("dark", 2))
		fit_results["fit"].Draw("same")
		l.AddEntry(fit_results["fit"], "Fit", "l")

	if signal_histograms:
		for i in xrange(len(signal_histograms)):
			signal_histograms[i].SetLineColor(seaborn.GetColorRoot("dark", 3+i))
			signal_histograms[i].SetLineWidth(2)
			signal_histograms[i].Draw("hist same")
			l.AddEntry(signal_histograms[i], signal_names[i], "l")
	l.Draw()
	c.cd()
	bottom.cd()
	# Make frame
	frame_bottom = TH1D("frame_bottom", "frame_bottom", 100, x_min, x_max)
	frame_bottom.SetMinimum(-5.)
	frame_bottom.SetMaximum(5.)
	frame_bottom.GetXaxis().SetTitle("m_{jj} [GeV]")
	frame_bottom.GetYaxis().SetTitle("#frac{Data - Fit}{#sigma(Data)}")

	frame_bottom.GetXaxis().SetLabelSize(0.04)
	frame_bottom.GetXaxis().SetTitleSize(0.06)
	frame_bottom.GetXaxis().SetLabelOffset(0.01)
	frame_bottom.GetXaxis().SetTitleOffset(1.1)

	frame_bottom.GetYaxis().SetLabelSize(0.04)
	frame_bottom.GetYaxis().SetTitleSize(0.037)
	frame_bottom.GetYaxis().SetTitleOffset(0.7)

	frame_bottom.Draw("axis")


	if cached_fit_results:
		cached_fit_results["fit_ratio"].SetLineColor(ROOT.kBlack)
		cached_fit_results["fit_ratio"].SetFillColor(seaborn.GetColorRoot("dark", 2))
		cached_fit_results["fit_ratio"].SetFillStyle(1001)
		cached_fit_results["fit_ratio"].Draw("fhist same")
	else:
		fit_results["fit_ratio"].SetLineColor(ROOT.kBlack)
		fit_results["fit_ratio"].SetFillColor(seaborn.GetColorRoot("dark", 2))
		fit_results["fit_ratio"].SetFillStyle(1001)
		fit_results["fit_ratio"].Draw("fhist same")



	c.SaveAs("/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/Results/figures/" + save_tag + ".pdf")
	if save_file:
		print "[MakeMjjPlot] INFO : Saving data histogram and fit results to " + save_file.GetPath()
		save_file.cd()
		data_hist.Write()
		if not cached_fit_results:
			fit_results["fit"].Write(save_tag + "_fit")
			fit_results["fit_ratio"].Write(save_tag + "_fit_ratio")


def MakeNMinusOnePlot(data_hist, save_tag, signal_histograms=None, signal_names=None, log=False, x_range=None, x_title=None, y_range=None, y_title=None):
	# Get histogram limits
	if x_range:
		x_min = x_range[0]
		x_max = x_range[1]
	else:
		x_min = data_hist.GetXaxis().GetXmin()
		x_max = data_hist.GetXaxis().GetXmax()
	y_min = 1.e20
	y_max = -1.e20
	for bin in xrange(1, data_hist.GetNbinsX() + 1):
		if data_hist.GetBinContent(bin) != 0:
			if data_hist.GetXaxis().GetBinCenter(bin) > x_min and data_hist.GetXaxis().GetBinCenter(bin) < x_max:
				if data_hist.GetBinContent(bin) < y_min:
					y_min = data_hist.GetBinContent(bin)
				if data_hist.GetBinContent(bin) > y_max:
					y_max = data_hist.GetBinContent(bin)
		for signal_histogram in signal_histograms:
			if signal_histogram.GetBinContent(bin) != 0:
				if signal_histogram.GetXaxis().GetBinCenter(bin) > x_min and signal_histogram.GetXaxis().GetBinCenter(bin) < x_max:
					if signal_histogram.GetBinContent(bin) < y_min:
						y_min = signal_histogram.GetBinContent(bin)
					if signal_histogram.GetBinContent(bin) > y_max:
						y_max = signal_histogram.GetBinContent(bin)
	print "X axis range: " + str(x_min) + " - " + str(x_max)
	print "Y axis range: " + str(y_min) + " - " + str(y_max)


	c = TCanvas("c_" + save_tag, "c_" + save_tag, 800, 600)
	if log:
		c.SetLogy()
	l = TLegend(0.6, 0.7, 0.88, 0.88)
	l.SetFillColor(0)
	l.SetBorderSize(0)
	frame = TH1F("frame", "frame", 100, x_min, x_max)
	frame.SetMinimum(0.)
	frame.SetMaximum(y_max * 1.2)
	if x_title:
		frame.GetXaxis().SetTitle(x_title)
	else:
		frame.GetXaxis().SetTitle(data_hist.GetXaxis().GetTitle())
	if y_title:
		frame.GetYaxis().SetTitle(y_title)
	else:
		frame.GetYaxis().SetTitle(data_hist.GetYaxis().GetTitle())
	frame.Draw("axis")

	data_hist.SetMarkerStyle(20)
	data_hist.SetMarkerSize(1)
	data_hist.SetMarkerColor(1)
	data_hist.Draw("p e1 same")
	l.AddEntry(data_hist, "Data", "p")

	for i_signal in xrange(len(signal_histograms)):
		signal_histograms[i_signal].SetLineColor(seaborn.GetColorRoot("dark", i_signal+1))
		signal_histograms[i_signal].SetLineWidth(2)
		signal_histograms[i_signal].SetLineStyle(1)
		signal_histograms[i_signal].Draw("hist same")
		l.AddEntry(signal_histograms[i_signal], signal_names[i_signal], "l")
	l.Draw()

	c.SaveAs("/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/Results/figures/" + save_tag + ".pdf")

def MakeFatJetComparison(hist_pf, hist_fat, save_tag, fit_range=None, x_range=None, log=False):
	print "Welcome to MakeFatJetComparison"
	# Fits
	fit_results_pf = DoSignalFit(hist_pf, fit_range=fit_range)
	fit_results_fat = DoSignalFit(hist_fat, fit_range=fit_range)


	if x_range:
		x_min = x_range[0]
		x_max = x_range[1]
	else:
		x_min = hist_pf.GetXaxis().GetXmin()
		x_max = hist_pf.GetXaxis().GetXmax()

	c = TCanvas("c_" + save_tag, "c_" + save_tag, 800, 600)
	if log:
		c.SetLogy()
	l = TLegend(0.65, 0.7, 0.88, 0.83)
	l.SetBorderSize(0)
	l.SetFillColor(0)

	frame = TH1D("frame", "frame", 100, x_min, x_max)
	frame.GetXaxis().SetTitle(hist_pf.GetXaxis().GetTitle())
	frame.GetYaxis().SetTitle(hist_pf.GetYaxis().GetTitle())
	if log:
		frame.SetMaximum(hist_pf.GetMaximum() * 5.)
	else:
		frame.SetMaximum(hist_pf.GetMaximum() * 1.7)
	frame.Draw("axis")

	hist_pf.SetMarkerStyle(20)
	hist_pf.SetMarkerColor(seaborn.GetColorRoot("dark", 0))
	hist_pf.SetLineColor(seaborn.GetColorRoot("dark", 0))
	hist_pf.SetMarkerSize(1)
	hist_pf.Draw("p e1 same")
	l.AddEntry(hist_pf, "ak5 jets", "pl")

	fit_results_pf["fit"].SetLineColor(seaborn.GetColorRoot("pastel", 0))
	fit_results_pf["fit"].SetLineWidth(2)
	fit_results_pf["fit"].Draw("same")
	l.AddEntry(fit_results_pf["fit"], "ak5 jets fit", "l")

	hist_fat.SetMarkerStyle(24)
	hist_fat.SetMarkerColor(seaborn.GetColorRoot("dark", 2))
	hist_fat.SetLineColor(seaborn.GetColorRoot("dark", 2))
	hist_fat.SetMarkerSize(1)
	hist_fat.Draw("p e1 same")
	l.AddEntry(hist_fat, "Fat jets", "pl")

	fit_results_fat["fit"].SetLineColor(seaborn.GetColorRoot("pastel", 2))
	fit_results_fat["fit"].SetLineWidth(2)
	fit_results_fat["fit"].Draw("same")
	l.AddEntry(fit_results_fat["fit"], "Fat jets fit", "l")

	l.Draw()
	
	# Write RMS on canvas
	Root.myText(0.15, 0.85, kBlack, "#bar{x}/#sigma (ak5) = " + str(round(fit_results_pf["fit"].GetParameter(2), 2)) + "/" + str(round(fit_results_pf["fit"].GetParameter(3), 2)), 0.4)
	Root.myText(0.15, 0.8, kBlack, "#bar{x}/#sigma (Fat) = " + str(round(fit_results_fat["fit"].GetParameter(2), 2)) + "/" + str(round(fit_results_fat["fit"].GetParameter(3), 2)), 0.4)
	#pf_mean = hist_pf.GetMean()
	#fat_mean = hist_fat.GetMean()
	#pf_rms = hist_pf.GetRMS()
	#fat_rms = hist_fat.GetRMS()
	#Root.myText(0.15, 0.85, kBlack, "Mean/RMS (PF) = " + str(round(pf_mean, 2)) + "/" + str(round(pf_rms, 2)), 0.4)
	#Root.myText(0.15, 0.8, kBlack, "Mean/RMS (Fat) = " + str(round(fat_mean, 2)) + "/" + str(round(fat_rms, 2)), 0.4)

	c.SaveAs("/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/Results/figures/" + save_tag + ".pdf")
	
class AnalysisComparisonPlotMultiple:
	def __init__(self, hists_num, hists_den, names, name_num, name_den, save_tag, x_range=None, log=False, x_title=None, y_title=None):
		self.hists_num = hists_num
		self.hists_den = hists_den
		print "[debug] hists_num = ",
		print self.hists_num
		print "[debug] hists_den = ",
		print self.hists_den
		self.names = names
		self.name_num = name_num
		self.name_den = name_den
		self.save_tag = save_tag
		self.log = log
		self.ratio_min = -0.2
		self.ratio_max = 1.2
		self.lines = []
		if x_range:
			self.x_min = x_range[0]
			self.x_max = x_range[1]
		else:
			self.x_min = 1e20
			self.x_max = -1e20
			for name, hist in hists_num.iteritems():
				if hist.GetXaxis().GetXmin() < self.x_min:
					self.x_min = hist.GetXaxis().GetXmin()
				if hist.GetXaxis().GetXmax() > self.x_max:
					self.x_max = hist.GetXaxis().GetXmax()
		self.x_title = x_title
		self.y_title = y_title

		self.canvas = TCanvas("c_" + save_tag, "c_" + save_tag, 800, 1000)
		self.legend = TLegend(0.6, 0.45, 0.88, 0.88)
		self.legend.SetFillColor(0)
		self.legend.SetBorderSize(0)
		self.top = TPad("top_" + save_tag, "top", 0., 0.5, 1., 1.)
		self.top.SetBottomMargin(0.03)
		self.top.Draw()
		if self.log:
			self.top.SetLogy()
		self.canvas.cd()
		self.bottom = TPad("bottom_" + save_tag, "bottom", 0., 0., 1., 0.5)
		self.bottom.SetTopMargin(0.02)
		self.bottom.SetBottomMargin(0.2)
		self.bottom.Draw()
		ROOT.SetOwnership(self.canvas, False)
		ROOT.SetOwnership(self.top, False)
		ROOT.SetOwnership(self.bottom, False)

		self.draw_done = False

	def draw(self):
		self.top.cd()

		self.frame_top = TH1D("frame_top_" + self.save_tag, "frame_top", 100, self.x_min, self.x_max)
		self.frame_top.GetXaxis().SetTitleSize(0)
		self.frame_top.GetXaxis().SetLabelSize(0)
		self.frame_top.GetYaxis().SetLabelSize(0.04)
		self.frame_top.GetYaxis().SetTitleSize(0.04)
		#self.frame_top.GetYaxis().SetTitleOffset(0.85)
		print "[debug] At the point of error, self.hists_num = ",
		print self.hists_num
		bin_width = self.hists_num[self.names[0]].GetXaxis().GetBinWidth(1)
		if self.y_title:
			self.frame_top.GetYaxis().SetTitle(self.y_title)
		else:
			self.frame_top.GetYaxis().SetTitle("Events / " + str(int(bin_width)) + " GeV")
		if self.log:
			self.frame_top.SetMaximum(self.hists_den[self.names[0]].GetMaximum() * 5.)
			self.frame_top.SetMinimum(0.5)
		else:
			self.frame_top.SetMaximum(self.hists_den[self.names[0]].GetMaximum() * 1.2)
		self.frame_top.Draw("axis")

		style_counter = 0
		for name in self.names:
			self.hists_num[name].SetMarkerStyle(20)
			self.hists_num[name].SetMarkerColor(seaborn.GetColorRoot("dark", style_counter))
			self.hists_num[name].SetLineColor(seaborn.GetColorRoot("dark", style_counter))
			self.hists_num[name].SetMarkerSize(1)
			self.hists_num[name].Draw("p e1 same")
			#print "[plots] DEBUG : self.hists_num[name] integral = " + str(self.hists_num[name].Integral())
			self.legend.AddEntry(self.hists_num[name], str(name) + " / " + self.name_num, "pl")

			self.hists_den[name].SetMarkerStyle(24)
			self.hists_den[name].SetMarkerColor(seaborn.GetColorRoot("pastel", style_counter))
			self.hists_den[name].SetLineColor(seaborn.GetColorRoot("pastel", style_counter))
			self.hists_den[name].SetMarkerSize(1)
			self.hists_den[name].Draw("p e1 same")
			self.legend.AddEntry(self.hists_den[name], str(name) + " / " + self.name_den, "pl")
			style_counter += 1
		self.legend.Draw()

		self.canvas.cd()
		self.bottom.cd()
		# Make frame
		self.frame_bottom = TH1D("frame_bottom_" + self.save_tag, "frame_bottom", 100, self.x_min, self.x_max)
		self.frame_bottom.SetMinimum(self.ratio_min)
		self.frame_bottom.SetMaximum(self.ratio_max)
		if self.x_title:
			self.frame_bottom.GetXaxis().SetTitle(self.x_title)
		else:
			self.frame_bottom.GetXaxis().SetTitle("m_{jj} [GeV]")
		self.frame_bottom.GetYaxis().SetTitle("Ratio")

		self.frame_bottom.GetXaxis().SetLabelSize(0.04)
		self.frame_bottom.GetXaxis().SetTitleSize(0.06)
		self.frame_bottom.GetXaxis().SetLabelOffset(0.01)
		self.frame_bottom.GetXaxis().SetTitleOffset(1.1)

		self.frame_bottom.GetYaxis().SetLabelSize(0.04)
		self.frame_bottom.GetYaxis().SetTitleSize(0.04)
		self.frame_bottom.GetYaxis().SetTitleOffset(1.0)

		self.frame_bottom.Draw("axis")

		unity = TLine(self.x_min, 1., self.x_max, 1.)
		unity.SetLineColor(kGray)
		unity.SetLineStyle(2)
		unity.SetLineWidth(2)
		unity.Draw("same")

		zero = TLine(self.x_min, 0., self.x_max, 0.)
		zero.SetLineColor(kBlack)
		zero.SetLineStyle(1)
		zero.SetLineWidth(2)
		zero.Draw("same")

		# Ratio histogram with no errors (not so well defined, since this isn't a well-defined efficiency)
		self.hist_ratio = {}
		style_counter = 0
		for name in self.names:
			self.hist_ratio[name] = self.hists_num[name].Clone()
			#print "[debug] Num bins = " + str(self.hist_num.GetNbinsX())
			#print "[debug] Den bins = " + str(self.hist_den.GetNbinsX())
			self.hist_ratio[name].Divide(self.hists_num[name], self.hists_den[name], 1, 1, "B")
			for bin in xrange(1, self.hist_ratio[name].GetNbinsX() + 1):
				if self.hists_den[name].GetBinContent(bin) == 0 or self.hist_ratio[name].GetBinContent(bin) == 0:
					self.hist_ratio[name].SetBinContent(bin, 0)
					self.hist_ratio[name].SetBinError(bin, 0)
			self.hist_ratio[name].SetFillStyle(3002)
			self.hist_ratio[name].SetFillColor(seaborn.GetColorRoot("dark", style_counter))
			self.hist_ratio[name].Draw("p e4 same")
			self.hist_ratio[name].Draw("p e1 same")
			style_counter += 1

		self.canvas.cd()
		self.draw_done = True

	def draw_line(self, pad, x1, y1, x2, y2, style=2, color=kGray, width=1):
		if not self.draw_done:
			print "[AnalysisComparisonPlot::draw_line] ERROR : draw() must be called first"
			return

		if pad == "top":
			self.top.cd()
		elif pad == "bottom":
			self.bottom.cd()
		else:
			print "[AnalysisComparisonPlot::draw_line] ERROR : pad must be top or bottom"
		self.lines.append(TLine(x1, y1, x2, y2))
		self.lines[-1].SetLineStyle(style)
		self.lines[-1].SetLineColor(color)
		self.lines[-1].SetLineWidth(width)
		self.lines[-1].Draw("same")

	def save(self):
		self.canvas.cd()
		self.canvas.SaveAs(analysis_config.figure_directory + "/" + self.save_tag + ".pdf")


class AnalysisComparisonPlot:
	def __init__(self, hist_num, hist_den, name_num, name_den, save_tag, x_range=None, log=False, x_title=None, y_title=None):
		self.hist_num = hist_num
		self.hist_den = hist_den
		self.name_num = name_num
		self.name_den = name_den
		self.save_tag = save_tag
		self.log = log
		self.ratio_min = -0.2
		self.ratio_max = 1.2
		self.lines = []
		if x_range:
			self.x_min = x_range[0]
			self.x_max = x_range[1]
		else:
			self.x_min = hist_num.GetXaxis().GetXmin()
			self.x_max = hist_num.GetXaxis().GetXmax()
		self.x_title = x_title
		self.y_title = y_title

		self.canvas = TCanvas("c_" + save_tag, "c_" + save_tag, 800, 1000)
		self.legend = TLegend(0.6, 0.6, 0.88, 0.88)
		self.legend.SetFillColor(0)
		self.legend.SetBorderSize(0)
		self.top = TPad("top_" + save_tag, "top", 0., 0.5, 1., 1.)
		self.top.SetBottomMargin(0.03)
		self.top.Draw()
		if self.log:
			self.top.SetLogy()
		self.canvas.cd()
		self.bottom = TPad("bottom_" + save_tag, "bottom", 0., 0., 1., 0.5)
		self.bottom.SetTopMargin(0.02)
		self.bottom.SetBottomMargin(0.2)
		self.bottom.Draw()
		ROOT.SetOwnership(self.canvas, False)
		ROOT.SetOwnership(self.top, False)
		ROOT.SetOwnership(self.bottom, False)

		self.draw_done = False

	def draw(self):
		self.top.cd()

		self.frame_top = TH1D("frame_top_" + self.save_tag, "frame_top", 100, self.x_min, self.x_max)
		self.frame_top.GetXaxis().SetTitleSize(0)
		self.frame_top.GetXaxis().SetLabelSize(0)
		self.frame_top.GetYaxis().SetLabelSize(0.04)
		self.frame_top.GetYaxis().SetTitleSize(0.04)
		#self.frame_top.GetYaxis().SetTitleOffset(0.85)
		bin_width = self.hist_num.GetXaxis().GetBinWidth(1)
		if self.y_title:
			self.frame_top.GetYaxis().SetTitle(self.y_title)
		else:
			self.frame_top.GetYaxis().SetTitle("Events / " + str(int(bin_width)) + " GeV")
		if self.log:
			self.frame_top.SetMaximum(self.hist_den.GetMaximum() * 5.)
			self.frame_top.SetMinimum(5.)
		else:
			self.frame_top.SetMaximum(self.hist_den.GetMaximum() * 1.2)
		self.frame_top.Draw("axis")

		self.hist_num.SetMarkerStyle(20)
		self.hist_num.SetMarkerColor(seaborn.GetColorRoot("dark", 0))
		self.hist_num.SetLineColor(seaborn.GetColorRoot("dark", 0))
		self.hist_num.SetMarkerSize(1)
		self.hist_num.Draw("p e1 same")
		print "[plots] DEBUG : self.hist_num integral = " + str(self.hist_num.Integral())
		self.legend.AddEntry(self.hist_num, self.name_num, "pl")

		self.hist_den.SetMarkerStyle(24)
		self.hist_den.SetMarkerColor(seaborn.GetColorRoot("dark", 2))
		self.hist_den.SetLineColor(seaborn.GetColorRoot("dark", 2))
		self.hist_den.SetMarkerSize(1)
		self.hist_den.Draw("p e1 same")
		self.legend.AddEntry(self.hist_den, self.name_den, "pl")
		self.legend.Draw()

		self.canvas.cd()
		self.bottom.cd()
		# Make frame
		self.frame_bottom = TH1D("frame_bottom_" + self.save_tag, "frame_bottom", 100, self.x_min, self.x_max)
		self.frame_bottom.SetMinimum(self.ratio_min)
		self.frame_bottom.SetMaximum(self.ratio_max)
		if self.x_title:
			self.frame_bottom.GetXaxis().SetTitle(self.x_title)
		else:
			self.frame_bottom.GetXaxis().SetTitle("m_{jj} [GeV]")
		self.frame_bottom.GetYaxis().SetTitle(self.name_num + " / " + self.name_den)

		self.frame_bottom.GetXaxis().SetLabelSize(0.04)
		self.frame_bottom.GetXaxis().SetTitleSize(0.06)
		self.frame_bottom.GetXaxis().SetLabelOffset(0.01)
		self.frame_bottom.GetXaxis().SetTitleOffset(1.1)

		self.frame_bottom.GetYaxis().SetLabelSize(0.04)
		self.frame_bottom.GetYaxis().SetTitleSize(0.04)
		self.frame_bottom.GetYaxis().SetTitleOffset(1.0)

		self.frame_bottom.Draw("axis")

		unity = TLine(self.x_min, 1., self.x_max, 1.)
		unity.SetLineColor(kGray)
		unity.SetLineStyle(2)
		unity.SetLineWidth(2)
		unity.Draw("same")

		zero = TLine(self.x_min, 0., self.x_max, 0.)
		zero.SetLineColor(kBlack)
		zero.SetLineStyle(1)
		zero.SetLineWidth(2)
		zero.Draw("same")

		# Ratio histogram with no errors (not so well defined, since this isn't a well-defined efficiency)
		self.hist_ratio = self.hist_num.Clone()
		print "[debug] Num bins = " + str(self.hist_num.GetNbinsX())
		print "[debug] Den bins = " + str(self.hist_den.GetNbinsX())
		self.hist_ratio.Divide(self.hist_num, self.hist_den, 1, 1, "B")
		self.hist_ratio.Draw("p same")

		self.canvas.cd()
		self.draw_done = True

	def draw_line(self, pad, x1, y1, x2, y2, style=2, color=kGray, width=1):
		if not self.draw_done:
			print "[AnalysisComparisonPlot::draw_line] ERROR : draw() must be called first"
			return

		if pad == "top":
			self.top.cd()
		elif pad == "bottom":
			self.bottom.cd()
		else:
			print "[AnalysisComparisonPlot::draw_line] ERROR : pad must be top or bottom"
		self.lines.append(TLine(x1, y1, x2, y2))
		self.lines[-1].SetLineStyle(style)
		self.lines[-1].SetLineColor(color)
		self.lines[-1].SetLineWidth(width)
		self.lines[-1].Draw("same")

	def save(self):
		self.canvas.cd()
		self.canvas.SaveAs(analysis_config.figure_directory + "/" + self.save_tag + ".pdf")

def BTagWPPlot(mjj_histograms, denominator_name, save_tag, x_range=None, log=False):
	print "Welcome to BTagWPPlot"

	if x_range:
		x_min = x_range[0]
		x_max = x_range[1]
	else:
		x_min = mjj_histograms[denominator_name].GetXaxis().GetXmin()
		x_max = mjj_histograms[denominator_name].GetXaxis().GetXmax()

	c = TCanvas("c_" + save_tag, "c_" + save_tag, 800, 1000)
	l = TLegend(0.55, 0.6, 0.88, 0.88)
	l.SetFillColor(0)
	l.SetBorderSize(0)
	top = TPad("top", "top", 0., 0.5, 1., 1.)
	top.SetBottomMargin(0.03)
	top.Draw()
	if log:
		top.SetLogy()
	c.cd()
	bottom = TPad("bottom", "bottom", 0., 0., 1., 0.5)
	bottom.SetTopMargin(0.02)
	bottom.SetBottomMargin(0.2)
	bottom.Draw()
	ROOT.SetOwnership(c, False)
	ROOT.SetOwnership(top, False)
	ROOT.SetOwnership(bottom, False)

	top.cd()

	frame_top = TH1D("frame_top", "frame_top", 100, x_min, x_max)
	frame_top.GetXaxis().SetTitleSize(0)
	frame_top.GetXaxis().SetLabelSize(0)
	frame_top.GetYaxis().SetLabelSize(0.04)
	frame_top.GetYaxis().SetTitleSize(0.04)
	#frame_top.GetYaxis().SetTitleOffset(0.85)
	bin_width = mjj_histograms[denominator_name].GetXaxis().GetBinWidth(1)
	frame_top.GetYaxis().SetTitle("Events / " + str(int(bin_width)) + " GeV")
	if log:
		frame_top.SetMaximum(mjj_histograms[denominator_name].GetMaximum() * 5.)
		frame_top.SetMinimum(0.5)
	else:
		frame_top.SetMaximum(mjj_histograms[denominator_name].GetMaximum() * 1.7)
	frame_top.Draw("axis")

	style_counter = 0
	styles = {}
	for name, hist in mjj_histograms.iteritems():
		styles[name] = style_counter
		hist.SetMarkerStyle(20 + style_counter)
		hist.SetMarkerColor(seaborn.GetColorRoot("dark", style_counter))
		hist.SetLineColor(seaborn.GetColorRoot("dark", style_counter))
		hist.SetMarkerSize(1)
		hist.Draw("p e1 same")
		l.AddEntry(hist, name, "pl")
		style_counter += 1
	l.Draw()

	c.cd()
	bottom.cd()
	bottom.SetLogy()
	# Make frame
	frame_bottom = TH1D("frame_bottom", "frame_bottom", 100, x_min, x_max)
	frame_bottom.SetMinimum(1.e-3)
	frame_bottom.SetMaximum(1.5)
	frame_bottom.GetXaxis().SetTitle("m_{jj} [GeV]")
	frame_bottom.GetYaxis().SetTitle("WP / " + denominator_name)

	frame_bottom.GetXaxis().SetLabelSize(0.04)
	frame_bottom.GetXaxis().SetTitleSize(0.06)
	frame_bottom.GetXaxis().SetLabelOffset(0.01)
	frame_bottom.GetXaxis().SetTitleOffset(1.1)

	frame_bottom.GetYaxis().SetLabelSize(0.04)
	frame_bottom.GetYaxis().SetTitleSize(0.04)
	frame_bottom.GetYaxis().SetTitleOffset(0.85)

	frame_bottom.Draw("axis")

	# Make and draw ratio histograms
	ratio_hists = {}
	for name, hist in mjj_histograms.iteritems():
		ratio_hists[name] = hist.Clone()
		ratio_hists[name].SetName(name + "_ratio")
		print "[debug] Num bins = " + str(ratio_hists[name].GetNbinsX())
		print "[debug] Den bins = " + str(mjj_histograms[denominator_name])
		ratio_hists[name].Divide(ratio_hists[name], mjj_histograms[denominator_name], 1, 1, "B")
		ratio_hists[name].SetMarkerStyle(20 + styles[name])
		ratio_hists[name].SetMarkerColor(seaborn.GetColorRoot("dark", styles[name]))
		ratio_hists[name].SetLineColor(seaborn.GetColorRoot("dark", styles[name]))
		ratio_hists[name].Draw("p same")

	c.SaveAs(analysis_config.figure_directory + "/" + save_tag + ".pdf")

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description = 'Dijet mass spectrum fits')
	parser.add_argument('--analyses', type=str, default="trigbbh_CSVL", help='Analyses to plot')
	parser.add_argument('--data_samples', type=str, default="BJetPlusX_2012", help='Data sample to plot')
	parser.add_argument('--signal_samples', type=str, default=None, help='Signal samples to plot')
	#parser.add_argument('--data_samples', type=str, required=True, help='Samples to plot')
	#parser.add_argument('--signal_samples', type=str, required=True, help='Samples to plot')
	parser.add_argument('--mjj', action='store_true', help='Make mjj plot with fits')
	parser.add_argument('--nmo', action='store_true', help='Make N-1 plots')
	parser.add_argument('--peaks', action='store_true', help='Make signal peak plots')
	parser.add_argument('--unblind', action='store_true', help='Unblind 750 region')
	parser.add_argument('--compare', type=str, nargs=4, help='Plot comparing two analyses. Arg = analysis(num), sample(num), analysis(den), sample(den).')
	parser.add_argument('--csv', action='store_true', help='Plot comparing B tagging working points')
	args = parser.parse_args()

	analyses = args.analyses.split(",")
	data_samples = args.data_samples.split(",")
	signal_samples = []
	if args.signal_samples == "all":
		for signal_model in ["Hbb", "RSG"]:
			for mass in [600, 750, 900, 1200]:
				signal_samples.append(analysis_config.simulation.get_signal_tag(signal_model, mass, "FULLSIM"))
	elif args.signal_samples:
		signal_samples = args.signal_samples.split(",")
	

	f_data = {}
	f_signal = {}
	for analysis in analyses:
		f_data[analysis] = {}
		for data_sample in data_samples:
			f_data[analysis][data_sample] = TFile(analysis_config.get_b_histogram_filename(analysis, data_sample), "READ")

		f_signal[analysis] = {}
		for signal_sample in signal_samples:
			f_signal[analysis][signal_sample] = TFile(analysis_config.get_b_histogram_filename(analysis, signal_sample), "READ")

	if args.mjj:
		for analysis in analyses:
			for data_sample in data_samples:
				save_file = TFile("/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/Results/mjj_fits_" + analysis + "_" + data_sample + ".root", "RECREATE")
				if "trigbbl" in analysis:
					fit_minima = {"pfjet":419.1}
				elif "trigbbh" in analysis:
					fit_minima = {"pfjet":526.1}
				for jet_type in ["pfjet"]:
					data_hist = f_data[analysis][data_sample].Get("BHistograms/h_" + jet_type + "_mjj")
					data_hist.SetName(data_hist.GetName() + "_rebin" + analysis + data_sample)
					bins = array.array('d', [1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325, 354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 4509, 4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808, 7060, 7320, 7589, 7866, 8000])
					data_hist = data_hist.Rebin(len(bins) - 1, data_hist.GetName(), bins)
					x_bin_width = 1
					for bin in xrange(1, data_hist.GetNbinsX() + 1):
						data_hist.SetBinContent(bin, data_hist.GetBinContent(bin) / data_hist.GetXaxis().GetBinWidth(bin))
						data_hist.SetBinError(bin, data_hist.GetBinError(bin) / data_hist.GetXaxis().GetBinWidth(bin))
					#data_hist.Rebin(20)
					data_hist.SetDirectory(0)

					signal_histograms = []
					for signal_sample in signal_samples:
						signal_histograms.append(f_signal[signal_sample].Get("BHistograms/h_" + jet_type + "_mjj"))
						input_nevents = (f_signal[signal_sample].Get("BHistograms/h_input_nevents")).Integral()
						signal_histograms[-1].SetDirectory(0)
						signal_histograms[-1].SetName(signal_histograms[-1].GetName() + "_signal" + str(signal_mass_point))
						signal_histograms[-1].Scale(19700 * signal_cross_sections["RSG"][signal_mass_point] / input_nevents)
						signal_histograms[-1].Rebin(20)
						signal_names.append("RSG to bb, m=" + str(int(signal_mass_point)) + " GeV")
					MakeMjjPlot(data_hist, signal_histograms=signal_histograms, signal_names=signal_samples, x_range=[0., 1500.], save_tag=jet_type + "_mjj_" + analysis, log=False, fit_min=fit_minima[jet_type], fit_max=1200., save_file=save_file, blind=(not args.unblind))

					# For more plots, no need to redo fits
					this_fit_results = {}
					this_fit_results["fit"] = save_file.Get(jet_type + "_mjj_" + analysis + "_fit")
					this_fit_results["fit_ratio"] = save_file.Get(jet_type + "_mjj_" + analysis + "_fit_ratio")
					MakeMjjPlot(data_hist, signal_histograms=signal_histograms, signal_names=signal_samples, x_range=[0., 1500.], save_tag=jet_type + "_mjj_log_" + analysis, log=True, fit_min=fit_minima[jet_type], fit_max=1200., cached_fit_results=this_fit_results, blind=(not args.unblind))
					MakeMjjPlot(data_hist, signal_histograms=signal_histograms, signal_names=signal_samples, x_range=[250., 1250.], save_tag=jet_type + "_mjj_zoom_" + analysis, log=False, fit_min=fit_minima[jet_type], fit_max=1200., cached_fit_results=this_fit_results, blind=(not args.unblind))
					MakeMjjPlot(data_hist, signal_histograms=signal_histograms, signal_names=signal_samples, x_range=[250., 1250.], save_tag=jet_type + "_mjj_log_zoom_" + analysis, log=True, fit_min=fit_minima[jet_type], fit_max=1200., cached_fit_results=this_fit_results, blind=(not args.unblind))

	if args.nmo:
		rebin = {}
		rebin["PFDijetMaxDeltaEta"] = 4
		rebin["MinLeadingPFJetPt"] = 20
		rebin["MinSubleadingPFJetPt"] = 20
		x_axis_titles = {}
		x_axis_titles["PFFatDijetMaxDeltaEta"] = "#Delta#eta"
		x_axis_titles["MinLeadingPFJetPt"] = "Leading jet p_{T} [GeV]"
		x_axis_titles["MinSubleadingPFJetPt"] = "Subleading jet p_{T} [GeV]"

		for analysis in analyses:
			for data_sample in data_samples:
				# Get all N-1 histogram names
				nmo_histogram_names = []
				f_data[analysis][data_sample].cd("BHistograms")
				for key in gDirectory.GetListOfKeys():
					if "nminusone" in key.GetName():
						nmo_histogram_names.append(key.GetName())
				print "Making N-1 plots for: "
				print nmo_histogram_names
				for signal_model in ["RSG", "Hbb"]:
					for nmo_histogram_name in nmo_histogram_names:
						variable_name = nmo_histogram_name.replace("h_nminusone_", "")
						data_hist = f_data[analysis][data_sample].Get("BHistograms/" + nmo_histogram_name)
						data_hist.SetDirectory(0)
						data_hist.SetName(data_hist.GetName() + "_data")
						if variable_name in rebin.keys():
							data_hist.Rebin(rebin[variable_name])
						if data_hist.Integral() > 0:
							data_hist.Scale(1. / data_hist.Integral())
						else:
							continue
						signal_histograms = []
						signal_names = []
						for signal_mass_point in [600, 750, 900, 1200]:
							signal_sample = analysis_config.simulation.get_signal_tag(signal_model, signal_mass_point, "FULLSIM")
							signal_histograms.append(f_signal[analysis][signal_sample].Get("BHistograms/" + nmo_histogram_name))
							if not signal_histograms[-1]:
								print "ERROR : Couldn't find histogram BHistograms/" + nmo_histogram_name + " in file " + f_signal[signal_model][signal_mass_point].GetPath()
							signal_histograms[-1].SetDirectory(0)
							signal_histograms[-1].SetName(signal_histograms[-1].GetName() + "_signal" + str(signal_mass_point))
							if variable_name in rebin.keys():
								signal_histograms[-1].Rebin(rebin[variable_name])
							if signal_histograms[-1].Integral() > 0:
								signal_histograms[-1].Scale(1. / signal_histograms[-1].Integral())
							if signal_model == "RSG":
								signal_names.append("RS G#rightarrowb#bar{b}, m=" + str(int(signal_mass_point)) + " GeV")
							elif signal_model == "Hbb":
								signal_names.append("S#rightarrowb#bar{b}, m=" + str(int(signal_mass_point)) + " GeV")
						if variable_name in x_axis_titles.keys():
							this_x_title = x_axis_titles[variable_name]
						else:
							this_x_title=None
						MakeNMinusOnePlot(data_hist, nmo_histogram_name[2:] + "_" + signal_model + "_" + analysis + "_" + data_sample, signal_histograms=signal_histograms, signal_names=signal_names, x_title=this_x_title)

	if args.peaks:
		for analysis in analyses:
			for signal_model in ["RSG", "Hbb"]:
				for signal_mass_point in [600, 750, 900, 1200]:
					signal_sample = analysis_config.simulation.get_signal_tag(signal_model, signal_mass_point, "FULLSIM")
					input_nevents = (f_signal[analysis][signal_sample].Get("BHistograms/h_input_nevents")).Integral()
					hist_pf = f_signal[analysis][signal_sample].Get("BHistograms/h_pfjet_mjj")
					hist_pf.SetDirectory(0)
					hist_pf.SetName(hist_pf.GetName() + "_pf")
					hist_pf.Rebin(20)
					hist_pf.Scale(19700 * analysis_config.simulation.signal_cross_sections[signal_sample] / input_nevents)
					hist_fat = f_signal[analysis][signal_sample].Get("BHistograms/h_fatjet_mjj")
					hist_fat.SetDirectory(0)
					hist_fat.SetName(hist_fat.GetName() + "_fat")
					hist_fat.Rebin(20)
					hist_fat.Scale(19700 * analysis_config.simulation.signal_cross_sections[signal_sample] / input_nevents)

					MakeFatJetComparison(hist_pf, hist_fat, "mjj_pf_vs_fat_" + signal_model + "_" + str(int(signal_mass_point)) + "_" + analysis, x_range=[signal_mass_point-400., signal_mass_point+400.], fit_range=[signal_mass_point - 300., signal_mass_point + 200.], log=False)

	if args.compare:
		legend_entries = []
		for i in [0, 2]:
			if "trigbbh" in args.compare[i]:
				legend_entries.append("BJetPlusX, high mass")
			elif "trigbbl" in args.compare[i]:
				legend_entries.append("BJetPlusX, low mass")
			elif "jetht" in args.compare[i]:
				legend_entries.append("JetHT")
		print legend_entries

		f_num = TFile(analysis_config.get_b_histogram_filename(args.compare[0], args.compare[1]), "READ")
		f_den = TFile(analysis_config.get_b_histogram_filename(args.compare[2], args.compare[3]), "READ")
		hist_pfjet_num = f_num.Get("BHistograms/h_pfjet_mjj")
		hist_pfjet_num.SetName("hist_pfjet_num")
		hist_pfjet_num = mjj_common.apply_dijet_binning(hist_pfjet_num)
		hist_pfjet_den = f_den.Get("BHistograms/h_pfjet_mjj")
		hist_pfjet_den.SetName("hist_pfjet_den")
		hist_pfjet_den = mjj_common.apply_dijet_binning(hist_pfjet_den)
		save_tag = args.compare[0] + "_" + args.compare[1] + "_over_" + args.compare[2] + "_" + args.compare[3] + "_pfjet"
		AnalysisComparisonPlot(hist_pfjet_num, hist_pfjet_den, legend_entries[0], legend_entries[1], save_tag, log=True, x_range=[0., 2000.])

		hist_fatjet_num = f_num.Get("BHistograms/h_fatjet_mjj")
		hist_fatjet_num.SetName("hist_fatjet_num")
		hist_fatjet_num = mjj_common.apply_dijet_binning(hist_fatjet_num)
		hist_fatjet_den = f_den.Get("BHistograms/h_fatjet_mjj")
		hist_fatjet_den.SetName("hist_fatjet_den")
		hist_fatjet_den = mjj_common.apply_dijet_binning(hist_fatjet_den)
		save_tag = args.compare[0] + "_" + args.compare[1] + "_over_" + args.compare[2] + "_" + args.compare[3] + "_fatjet"
		AnalysisComparisonPlot(hist_fatjet_num, hist_fatjet_den, legend_entries[0], legend_entries[1], save_tag, log=True, x_range=[0., 2000.])
		f_num.Close()
		f_den.Close()


	if args.csv:
		analyses = ["trigbbh_CSVL", "trigbbh_CSVM", "trigbbh_CSVT"]
		legend_entries = {"trigbbh_CSVL":"CSVL", "trigbbh_CSVM":"CSVM", "trigbbh_CSVT":"CSVT"}
		data_histograms = {}
		for analysis in analyses:
			f = TFile(analysis_config.get_b_histogram_filename(analysis, "BJetPlusX_2012"), "READ")
			data_histograms[analysis] = f.Get("BHistograms/h_pfjet_mjj")
			if not data_histograms[analysis]:
				print "Failed to get histogram BHistograms/h_pfjet_mjj from file " + analysis_config.get_b_histogram_filename(analysis, "BJetPlusX_2012")
			data_histograms[analysis].SetDirectory(0)

		plot_compare(analyses, data_histograms, "CSVX_data", nominal_name="trigbbh_CSVL", legend_entries=legend_entries, log=True, log_ratio=True, x_range=[0., 1500.])

		for signal_model in ["Hbb", "RSG"]:
			for mass_point in [300, 600, 900, 1200]:
				signal_histograms = {}
				for analysis in analyses:
					f = TFile(analysis_config.get_b_histogram_filename(analysis, analysis_config.simulation.get_signal_tag(signal_model, mass_point, "FULLSIM")), "READ")
					signal_histograms[analysis] = f.Get("BHistograms/h_pfjet_mjj")
				plot_compare(analyses, signal_histograms, "CSVX_" + signal_model + "_" + str(mass_point), nominal_name="trigbbh_CSVL", legend_entries=legend_entries, log=True, log_ratio=False, x_range=[0., 1500.])



