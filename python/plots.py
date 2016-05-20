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
import CMSDIJET.QCDAnalysis.simulation_config
from CMSDIJET.QCDAnalysis.simulation_config import *

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

def MakeFatJetComparison(hist_pf, hist_fat, save_tag, x_range=None, log=False):
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
	hist_pf.SetMarkerColor(seaborn.GetColorRoot("dark", 1))
	hist_pf.SetLineColor(seaborn.GetColorRoot("dark", 1))
	hist_pf.SetMarkerSize(1)
	hist_pf.Draw("p e1 same")
	l.AddEntry(hist_pf, "PF jets", "pl")

	hist_fat.SetMarkerStyle(24)
	hist_fat.SetMarkerColor(seaborn.GetColorRoot("dark", 2))
	hist_fat.SetLineColor(seaborn.GetColorRoot("dark", 2))
	hist_fat.SetMarkerSize(1)
	hist_fat.Draw("p e1 same")
	l.AddEntry(hist_fat, "Fat jets", "pl")

	l.Draw()
	# Write RMS on canvas
	pf_mean = hist_pf.GetMean()
	fat_mean = hist_fat.GetMean()
	pf_rms = hist_pf.GetRMS()
	fat_rms = hist_fat.GetRMS()
	Root.myText(0.15, 0.85, kBlack, "Mean/RMS (PF) = " + str(round(pf_mean, 2)) + "/" + str(round(pf_rms, 2)), 0.4)
	Root.myText(0.15, 0.8, kBlack, "Mean/RMS (Fat) = " + str(round(fat_mean, 2)) + "/" + str(round(fat_rms, 2)), 0.4)

	c.SaveAs("/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/Results/figures/" + save_tag + ".pdf")

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description = 'Dijet mass spectrum fits')
	parser.add_argument('--mjj', action='store_true', help='Make mjj plot with fits')
	parser.add_argument('--nmo', action='store_true', help='Make N-1 plots')
	parser.add_argument('--peaks', action='store_true', help='Make signal peak plots')
	parser.add_argument('--unblind', action='store_true', help='Unblind 750 region')
	args = parser.parse_args()


	f_data = TFile("/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/Results/InclusiveBHistograms_2012.root", "READ")
	signal_mass_points = [500., 750., 1000., 1200.]
	f_signal = {}
	f_signal["RSG"] = {}
	f_signal["Zprime"] = {}
	for signal_mass_point in signal_mass_points:
		f_signal["RSG"][signal_mass_point] = TFile("/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/Results/InclusiveBHistograms_RSGravitonToBBbar_M_" + str(int(signal_mass_point)) + "_TuneZ2star_8TeV_pythia6_FASTSIM.root", "READ")
		f_signal["Zprime"][signal_mass_point] = TFile("/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/Results/InclusiveBHistograms_ZprimeToBB_M_" + str(int(signal_mass_point)) + "_TuneD6T_8TeV_pythia6_FASTSIM.root", "READ")

	if args.mjj:
		save_file = TFile("/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/Results/mjj_fits.root", "RECREATE")
		fit_minima = {"fatjet":550., "pfjet":500.}
		for jet_type in ["fatjet", "pfjet"]:

			data_hist = f_data.Get("inclusive/h_" + jet_type + "_mjj")
			data_hist.SetName(data_hist.GetName() + "_data")
			data_hist.Rebin(20)
			data_hist.SetDirectory(0)

			signal_histograms = []
			signal_names = []
			for signal_mass_point in [500., 750., 1000.]:
				input_nevents = (f_signal["RSG"][signal_mass_point].Get("inclusive/h_input_nevents")).Integral()
				signal_histograms.append(f_signal["RSG"][signal_mass_point].Get("inclusive/h_" + jet_type + "_mjj"))
				signal_histograms[-1].SetDirectory(0)
				signal_histograms[-1].SetName(signal_histograms[-1].GetName() + "_signal" + str(signal_mass_point))
				signal_histograms[-1].Scale(19700 * signal_cross_sections["RSG"][signal_mass_point] / input_nevents)
				signal_histograms[-1].Rebin(20)
				signal_names.append("RSG to bb, m=" + str(int(signal_mass_point)) + " GeV")
			MakeMjjPlot(data_hist, signal_histograms=signal_histograms, signal_names=signal_names, x_range=[0., 2000.], save_tag=jet_type + "_mjj", log=False, fit_min=fit_minima[jet_type], fit_max=1500., save_file=save_file, blind=(not args.unblind))

			# For more plots, no need to redo fits
			this_fit_results = {}
			this_fit_results["fit"] = save_file.Get(jet_type + "_mjj_fit")
			this_fit_results["fit_ratio"] = save_file.Get(jet_type + "_mjj_fit_ratio")
			MakeMjjPlot(data_hist, signal_histograms=signal_histograms, signal_names=signal_names, x_range=[0., 2000.], save_tag=jet_type + "_mjj_log", log=True, fit_min=fit_minima[jet_type], fit_max=1500., cached_fit_results=this_fit_results, blind=(not args.unblind))
			MakeMjjPlot(data_hist, signal_histograms=signal_histograms, signal_names=signal_names, x_range=[500., 1000.], save_tag=jet_type + "_mjj_zoom", log=False, fit_min=fit_minima[jet_type], fit_max=1500., cached_fit_results=this_fit_results, blind=(not args.unblind))
			MakeMjjPlot(data_hist, signal_histograms=signal_histograms, signal_names=signal_names, x_range=[500., 1000.], save_tag=jet_type + "_mjj_log_zoom", log=True, fit_min=fit_minima[jet_type], fit_max=1500., cached_fit_results=this_fit_results, blind=(not args.unblind))

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
		f_data.cd("inclusive")
		for key in gDirectory.GetListOfKeys():
			if "nminusone" in key.GetName():
				nmo_histogram_names.append(key.GetName())
		print "Making N-1 plots for: "
		print nmo_histogram_names
		for signal_model in ["RSG", "Zprime"]:
			for nmo_histogram_name in nmo_histogram_names:
				variable_name = nmo_histogram_name.replace("h_nminusone_", "")
				data_hist = f_data.Get("inclusive/" + nmo_histogram_name)
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
				for signal_mass_point in [500., 750., 1000.]:
					signal_histograms.append(f_signal[signal_model][signal_mass_point].Get("inclusive/" + nmo_histogram_name))
					signal_histograms[-1].SetDirectory(0)
					signal_histograms[-1].SetName(signal_histograms[-1].GetName() + "_signal" + str(signal_mass_point))
					if variable_name in rebin.keys():
						signal_histograms[-1].Rebin(rebin[variable_name])
					if signal_histograms[-1].Integral() > 0:
						signal_histograms[-1].Scale(1. / signal_histograms[-1].Integral())
					if signal_model == "RSG":
						signal_names.append("RS G#rightarrowb#bar{b}, m=" + str(int(signal_mass_point)) + " GeV")
					elif signal_model == "Zprime":
						signal_names.append("Z'#rightarrowb#bar{b}, m=" + str(int(signal_mass_point)) + " GeV")
				if variable_name in x_axis_titles.keys():
					this_x_title = x_axis_titles[variable_name]
				else:
					this_x_title=None
				MakeNMinusOnePlot(data_hist, nmo_histogram_name[2:] + "_" + signal_model, signal_histograms=signal_histograms, signal_names=signal_names, x_title=this_x_title)

	if args.peaks:
		for signal_model in ["RSG", "Zprime"]:
			for signal_mass_point in [500., 750., 1000., 1200.]:
				input_nevents = (f_signal[signal_model][signal_mass_point].Get("inclusive/h_input_nevents")).Integral()
				hist_pf = f_signal[signal_model][signal_mass_point].Get("inclusive/h_pfjet_mjj")
				hist_pf.SetDirectory(0)
				hist_pf.SetName(hist_pf.GetName() + "_pf")
				hist_pf.Rebin(20)
				hist_pf.Scale(19700 * signal_cross_sections[signal_model][signal_mass_point] / input_nevents)
				hist_fat = f_signal[signal_model][signal_mass_point].Get("inclusive/h_fatjet_mjj")
				hist_fat.SetDirectory(0)
				hist_fat.SetName(hist_fat.GetName() + "_fat")
				hist_fat.Rebin(20)
				hist_fat.Scale(19700 * signal_cross_sections[signal_model][signal_mass_point] / input_nevents)

				MakeFatJetComparison(hist_pf, hist_fat, "mjj_pf_vs_fat_" + signal_model + "_" + str(int(signal_mass_point)), x_range=[signal_mass_point-400., signal_mass_point+400.], log=False)