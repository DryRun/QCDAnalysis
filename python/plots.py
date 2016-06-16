import os
import sys
import re
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
import CMSDIJET.QCDAnalysis.simulation_configuration_8TeV
from CMSDIJET.QCDAnalysis.simulation_configuration_8TeV import *
import CMSDIJET.QCDAnalysis.analysis_configuration_8TeV as analysis_config

def Blind(hist, center=750., half_width=75.):
	hist_blind = hist.Clone()
	for bin in xrange(1, hist_blind.GetNbinsX() + 1):
		if TMath.Abs(hist_blind.GetBinCenter(bin) - center) < half_width:
			hist_blind.SetBinContent(bin, 0.)
			hist_blind.SetBinError(bin, 0.)
	return hist_blind

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
	frame.GetYaxis().SetTitle("Events / " + str(int(data_hist.GetXaxis().GetBinWidth(1))) + " GeV")
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

def JetHTComparisonPlot(hist_bjetplusx, hist_jetht, save_tag, x_range=None, log=False):
	print "Welcome to JetHTComparisonPlot"

	if x_range:
		x_min = x_range[0]
		x_max = x_range[1]
	else:
		x_min = hist_bjetplusx.GetXaxis().GetXmin()
		x_max = hist_bjetplusx.GetXaxis().GetXmax()

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
	bin_width = hist_bjetplusx.GetXaxis().GetBinWidth(1)
	frame_top.GetYaxis().SetTitle("Events / " + str(int(bin_width)) + " GeV")
	if log:
		frame_top.SetMaximum(hist_jetht.GetMaximum() * 5.)
		frame_top.SetMinimum(5.)
	else:
		frame_top.SetMaximum(hist_jetht.GetMaximum() * 1.7)
	frame_top.Draw("axis")

	hist_bjetplusx.SetMarkerStyle(20)
	hist_bjetplusx.SetMarkerColor(seaborn.GetColorRoot("dark", 0))
	hist_bjetplusx.SetLineColor(seaborn.GetColorRoot("dark", 0))
	hist_bjetplusx.SetMarkerSize(1)
	hist_bjetplusx.Draw("p e1 same")
	l.AddEntry(hist_bjetplusx, "BJetPlusX", "pl")

	hist_jetht.SetMarkerStyle(24)
	hist_jetht.SetMarkerColor(seaborn.GetColorRoot("dark", 2))
	hist_jetht.SetLineColor(seaborn.GetColorRoot("dark", 2))
	hist_jetht.SetMarkerSize(1)
	hist_jetht.Draw("p e1 same")
	l.AddEntry(hist_jetht, "JetHT", "pl")
	l.Draw()

	c.cd()
	bottom.cd()
	# Make frame
	frame_bottom = TH1D("frame_bottom", "frame_bottom", 100, x_min, x_max)
	frame_bottom.SetMinimum(-0.2)
	frame_bottom.SetMaximum(1.2)
	frame_bottom.GetXaxis().SetTitle("m_{jj} [GeV]")
	frame_bottom.GetYaxis().SetTitle("BJetsPlusX / JetHT")

	frame_bottom.GetXaxis().SetLabelSize(0.04)
	frame_bottom.GetXaxis().SetTitleSize(0.06)
	frame_bottom.GetXaxis().SetLabelOffset(0.01)
	frame_bottom.GetXaxis().SetTitleOffset(1.1)

	frame_bottom.GetYaxis().SetLabelSize(0.04)
	frame_bottom.GetYaxis().SetTitleSize(0.04)
	frame_bottom.GetYaxis().SetTitleOffset(0.85)

	frame_bottom.Draw("axis")

	unity = TLine(x_min, 1., x_max, 1.)
	unity.SetLineColor(kGray)
	unity.SetLineStyle(2)
	unity.SetLineWidth(2)
	unity.Draw("same")

	zero = TLine(x_min, 0., x_max, 0.)
	zero.SetLineColor(kBlack)
	zero.SetLineStyle(1)
	zero.SetLineWidth(2)
	zero.Draw("same")

	# Ratio histogram with no errors (not so well defined, since this isn't a well-defined efficiency)
	hist_ratio = hist_bjetplusx.Clone()
	hist_ratio.Divide(hist_jetht)
	hist_ratio.Draw("hist same")

	c.SaveAs(analysis_config.figure_directory + "/" + save_tag + ".pdf")

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
		ratio_hists[name].Divide(ratio_hists[name], mjj_histograms[denominator_name], 1, 1, "B")
		ratio_hists[name].SetMarkerStyle(20 + styles[name])
		ratio_hists[name].SetMarkerColor(seaborn.GetColorRoot("dark", styles[name]))
		ratio_hists[name].SetLineColor(seaborn.GetColorRoot("dark", styles[name]))
		ratio_hists[name].Draw("p same")

	c.SaveAs(analysis_config.figure_directory + "/" + save_tag + ".pdf")

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description = 'Dijet mass spectrum fits')
	parser.add_argument('--analyses', type=str, required=True, help='Analyses to plot')
	parser.add_argument('--data_samples', type=str, required=True, help='Samples to plot')
	parser.add_argument('--signal_samples', type=str, required=True, help='Samples to plot')
	parser.add_argument('--mjj', action='store_true', help='Make mjj plot with fits')
	parser.add_argument('--nmo', action='store_true', help='Make N-1 plots')
	parser.add_argument('--peaks', action='store_true', help='Make signal peak plots')
	parser.add_argument('--unblind', action='store_true', help='Unblind 750 region')
	parser.add_argument('--jetht', action='store_true', help='BJetPlusX over JetHT plot')
	parser.add_argument('--btwp', action='store_true', help='Plot comparing B tagging working points')
	args = parser.parse_args()

	analyses = args.analyses.split(",")
	samples = args.samples.split(",")

	#for analysis in analyses:
	#	for sample in data_samples:


	#f_data = TFile("/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/Results/InclusiveBHistograms_2012.root", "READ")
	f_data = TFile(analysis_config.get_b_histogram_filename(args.analysis, "BJetPlusX_2012"), "READ")

	signal_models = ["Hbb", "RSG"]
	signal_mass_points = [300, 600, 900, 1200]

	f_signal = {}
	for model in signal_models:
		f_signal[model] = {}
		for signal_mass_point in signal_mass_points:
			print "Output tag = " + GetOutputTag(model, signal_mass_point, "FULLSIM")
			print "Opening " + analysis_config.get_b_histogram_filename(args.analysis, GetOutputTag(model, signal_mass_point, "FULLSIM"))
			f_signal[model][signal_mass_point] = TFile(analysis_config.get_b_histogram_filename(args.analysis, GetOutputTag(model, signal_mass_point, "FULLSIM")), "READ")

	if args.mjj:
		save_file = TFile("/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/Results/mjj_fits.root", "RECREATE")
		fit_minima = {"fatjet":600., "pfjet":500.}
		for jet_type in ["fatjet", "pfjet"]:

			data_hist = f_data.Get("BHistograms/h_" + jet_type + "_mjj")
			data_hist.SetName(data_hist.GetName() + "_data")
			data_hist.Rebin(20)
			data_hist.SetDirectory(0)

			signal_histograms = []
			signal_names = []
			for signal_mass_point in signal_mass_points:
				input_nevents = (f_signal["RSG"][signal_mass_point].Get("BHistograms/h_input_nevents")).Integral()
				signal_histograms.append(f_signal["RSG"][signal_mass_point].Get("BHistograms/h_" + jet_type + "_mjj"))
				signal_histograms[-1].SetDirectory(0)
				signal_histograms[-1].SetName(signal_histograms[-1].GetName() + "_signal" + str(signal_mass_point))
				signal_histograms[-1].Scale(19700 * signal_cross_sections["RSG"][signal_mass_point] / input_nevents)
				signal_histograms[-1].Rebin(20)
				signal_names.append("RSG to bb, m=" + str(int(signal_mass_point)) + " GeV")
			MakeMjjPlot(data_hist, signal_histograms=signal_histograms, signal_names=signal_names, x_range=[0., 2000.], save_tag=jet_type + "_mjj_" + args.analysis, log=False, fit_min=fit_minima[jet_type], fit_max=1500., save_file=save_file, blind=(not args.unblind))

			# For more plots, no need to redo fits
			this_fit_results = {}
			this_fit_results["fit"] = save_file.Get(jet_type + "_mjj_" + args.analysis + "_fit")
			this_fit_results["fit_ratio"] = save_file.Get(jet_type + "_mjj_" + args.analysis + "_fit_ratio")
			MakeMjjPlot(data_hist, signal_histograms=signal_histograms, signal_names=signal_names, x_range=[0., 2000.], save_tag=jet_type + "_mjj_log_" + args.analysis, log=True, fit_min=fit_minima[jet_type], fit_max=1500., cached_fit_results=this_fit_results, blind=(not args.unblind))
			MakeMjjPlot(data_hist, signal_histograms=signal_histograms, signal_names=signal_names, x_range=[500., 1000.], save_tag=jet_type + "_mjj_zoom_" + args.analysis, log=False, fit_min=fit_minima[jet_type], fit_max=1500., cached_fit_results=this_fit_results, blind=(not args.unblind))
			MakeMjjPlot(data_hist, signal_histograms=signal_histograms, signal_names=signal_names, x_range=[500., 1000.], save_tag=jet_type + "_mjj_log_zoom_" + args.analysis, log=True, fit_min=fit_minima[jet_type], fit_max=1500., cached_fit_results=this_fit_results, blind=(not args.unblind))

	if args.nmo:
		rebin = {}
		rebin["PFFatDijetMaxDeltaEta"] = 4
		rebin["MinLeadingPFJetPt"] = 20
		rebin["MinSubleadingPFJetPt"] = 20
		x_axis_titles = {}
		x_axis_titles["PFFatDijetMaxDeltaEta"] = "#Delta#eta"
		x_axis_titles["MinLeadingPFJetPt"] = "Leading jet p_{T} [GeV]"
		x_axis_titles["MinSubleadingPFJetPt"] = "Subleading jet p_{T} [GeV]"


		# Get all N-1 histogram names
		nmo_histogram_names = []
		f_data.cd("BHistograms")
		for key in gDirectory.GetListOfKeys():
			if "nminusone" in key.GetName():
				nmo_histogram_names.append(key.GetName())
		print "Making N-1 plots for: "
		print nmo_histogram_names
		for signal_model in ["RSG", "Hbb"]:
			for nmo_histogram_name in nmo_histogram_names:
				variable_name = nmo_histogram_name.replace("h_nminusone_", "")
				data_hist = f_data.Get("BHistograms/" + nmo_histogram_name)
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
				for signal_mass_point in signal_mass_points:
					signal_histograms.append(f_signal[signal_model][signal_mass_point].Get("BHistograms/" + nmo_histogram_name))
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
				MakeNMinusOnePlot(data_hist, nmo_histogram_name[2:] + "_" + signal_model + "_" + args.analysis, signal_histograms=signal_histograms, signal_names=signal_names, x_title=this_x_title)

	if args.peaks:
		for signal_model in ["RSG", "Hbb"]:
			for signal_mass_point in signal_mass_points:
		
				input_nevents = (f_signal[signal_model][signal_mass_point].Get("BHistograms/h_input_nevents")).Integral()
				hist_pf = f_signal[signal_model][signal_mass_point].Get("BHistograms/h_pfjet_mjj")
				hist_pf.SetDirectory(0)
				hist_pf.SetName(hist_pf.GetName() + "_pf")
				hist_pf.Rebin(20)
				hist_pf.Scale(19700 * signal_cross_sections[GetOutputTag(signal_model, signal_mass_point, "FULLSIM")] / input_nevents)
				hist_fat = f_signal[signal_model][signal_mass_point].Get("BHistograms/h_fatjet_mjj")
				hist_fat.SetDirectory(0)
				hist_fat.SetName(hist_fat.GetName() + "_fat")
				hist_fat.Rebin(20)
				hist_fat.Scale(19700 * signal_cross_sections[GetOutputTag(signal_model, signal_mass_point, "FULLSIM")] / input_nevents)

				MakeFatJetComparison(hist_pf, hist_fat, "mjj_pf_vs_fat_" + signal_model + "_" + str(int(signal_mass_point)) + "_" + args.analysis, x_range=[signal_mass_point-400., signal_mass_point+400.], fit_range=[signal_mass_point - 300., signal_mass_point + 200.], log=False)

	if args.jetht:
		f_bjetplusx = TFile(analysis_config.files_InclusiveBHistograms["BJetPlusX_2012BCD"], "READ")
		f_jetht = TFile(analysis_config.files_InclusiveBHistograms["JetHT_2012BCD"], "READ")
		hist_pfjet_bjetplusx = f_bjetplusx.Get("BHistograms/h_pfjet_mjj")
		hist_pfjet_bjetplusx.Rebin(20)
		hist_pfjet_bjetplusx.SetName("hist_pfjet_bjetplusx")
		hist_pfjet_jetht = f_jetht.Get("BHistograms/h_pfjet_mjj")
		hist_pfjet_jetht.Rebin(20)
		hist_pfjet_jetht.SetName("hist_pfjet_jetht")
		JetHTComparisonPlot(hist_pfjet_bjetplusx, hist_pfjet_jetht, "BJetPlusX_over_JetHT_pfjet", log=True, x_range=[500., 3000.])

		hist_fatjet_bjetplusx = f_bjetplusx.Get("BHistograms/h_fatjet_mjj")
		hist_fatjet_bjetplusx.Rebin(20)
		hist_fatjet_bjetplusx.SetName("hist_fatjet_bjetplusx")
		hist_fatjet_jetht = f_jetht.Get("BHistograms/h_fatjet_mjj")
		hist_fatjet_jetht.Rebin(20)
		hist_fatjet_jetht.SetName("hist_fatjet_jetht")
		JetHTComparisonPlot(hist_fatjet_bjetplusx, hist_fatjet_jetht, "BJetPlusX_over_JetHT_fatjet", log=True, x_range=[750., 2000.])
		f_bjetplusx.Close()
		f_jetht.Close()

		# With tight B tagging
		f_bjetplusx_tight = TFile(analysis_config.files_InclusiveBHistograms["BJetPlusX_tight_2012BCD"], "READ")
		f_jetht_tight = TFile(analysis_config.files_InclusiveBHistograms["JetHT_tight_2012BCD"], "READ")
		hist_pfjet_bjetplusx_tight = f_bjetplusx_tight.Get("BHistograms/h_pfjet_mjj")
		hist_pfjet_bjetplusx_tight.Rebin(20)
		hist_pfjet_bjetplusx_tight.SetName("hist_pfjet_bjetplusx_tight")
		hist_pfjet_jetht_tight = f_jetht_tight.Get("BHistograms/h_pfjet_mjj")
		hist_pfjet_jetht_tight.Rebin(20)
		hist_pfjet_jetht_tight.SetName("hist_pfjet_jetht_tight")
		JetHTComparisonPlot(hist_pfjet_bjetplusx_tight, hist_pfjet_jetht_tight, "BJetPlusX_over_JetHT_pfjet_tight", log=True, x_range=[500., 3000.])

		hist_fatjet_bjetplusx_tight = f_bjetplusx_tight.Get("BHistograms/h_fatjet_mjj")
		hist_fatjet_bjetplusx_tight.Rebin(20)
		hist_fatjet_bjetplusx_tight.SetName("hist_fatjet_bjetplusx_tight")
		hist_fatjet_jetht_tight = f_jetht_tight.Get("BHistograms/h_fatjet_mjj")
		hist_fatjet_jetht_tight.Rebin(20)
		hist_fatjet_jetht_tight.SetName("hist_fatjet_jetht_tight")
		JetHTComparisonPlot(hist_fatjet_bjetplusx_tight, hist_fatjet_jetht_tight, "BJetPlusX_over_JetHT_fatjet_tight", log=True, x_range=[500., 3000.])
		f_bjetplusx_tight.Close()
		f_jetht_tight.Close()

	if args.btwp:
		wps = ["tight", "medium", "loose"]
		hists = {}
		for wp in wps:
			if wp == "loose":
				f = TFile("InclusiveBHistograms_2012.root", "READ")
				h = f.Get("BHistograms/h_pfjet_mjj")
			else:
				f = TFile("BJetPlusX_" + wp + "_2012.root", "READ")
				h = f.Get("BHistograms/h_pfjet_mjj")
			if not h:
				print "Couldn't find BHistograms/h_pfjet_mjj for wp " + wp
				sys.exit(1)
			h.Rebin(20)
			hists[wp] = Blind(h)
			hists[wp].SetName(hists[wp].GetName() + "_" + wp)
			hists[wp].SetDirectory(0)
			f.Close()
		BTagWPPlot(hists, "loose", "btwp", log=True, x_range=[0., 3000.])
