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

def MakeMjjPlot(data_hist, signal_histograms=None, signal_names=None, save_tag="c_mjj", x_min=0., x_max=1500., log=False, fit_min=500., fit_max=1500.):
	fit_results = DoMjjBackgroundFit(data_hist, fit_min=fit_min, fit_max=fit_max, rebin=20, blind=True)

	c = TCanvas(save_tag, save_tag, 800, 1200)
	l = TLegend(0.6, 0.6, 0.93, 0.9)
	l.SetFillColor(0)
	l.SetBorderSize(0)
	top = TPad(0., 0.5, 1., 1.)
	top.SetBottomMargin(0.03)
	top.Draw()
	c.cd()
	bottom = TPad(0., 0., 1., 0.5)
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
	data_hist.GetYaxis().SetTitle("Events / " + str(int(data_hist.GetXaxis().GetBinWidth(1))) + " GeV")
	data_hist.GetXaxis().SetTitleSize(0)
	data_hist.GetXaxis().SetLabelSize(0)
	data_hist.Draw("p e1")
	fit_results["fit"].SetLineColor(seaborn.GetColorRoot("dark", 2))
	fit_results["fit"].Draw("same")
	l.Add(data_hist, "Data", "pl")
	l.Add(fit_results["fit"], "Fit", "l")

	if signal_histograms:
		for i in xrange(len(signal_histograms)):
			signal_histograms[i].SetLineColor(seaborn.GetColorRoot("dark", 3+i))
			signal_histograms[i].SetLineWidth(2)
			signal_histograms[i].Draw("hist same")
			l.AddEntry(signal_histograms[i], signal_names[i], "l")
	l.Draw()
	c.cd()
	bottom.cd()
	fit_results["fit_ratio"].SetLineColor(ROOT.kBlack)
	fit_results["fit_ratio"].SetFillColor(seaborn.GetColorRoot("dark", 2))
	fit_results["fit_ratio"].SetFillStyle(1001)
	fit_results["fit_ratio"].GetXaxis().SetTitle("m_{jj} [GeV]")
	fit_results["fit_ratio"].GetYaxis().SetTitle("#frac{Data - Fit}{#sigma(Data)}")
	fit_results["fit_ratio"].Draw("fhist")

	c.SaveAs("/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/Results/figures/" + save_tag + ".pdf")


def VarPlots(input_file, output_tag, plot_log=False, signal_file=None, signal_xs=None):
	f_in = TFile(input_file, "READ")
	tdf = f_in.Get("inclusive")
	variables = ["nevents", "pf_mjj", "pf_deltaeta", "pf_eta1", "pf_eta2", "pf_pt1", "pf_pt2", "pf_btag_csv1", "pf_btag_csv2"]
	rebin = {"pf_mjj":20, "pf_mjj_160_120":20, "pf_mjj_80_70":20, "pf_deltaeta":1, "pf_eta1":2, "pf_eta2":2, "pf_pt1":20, "pf_pt2":20, "pf_btag_csv1":1, "pf_btag_csv2":1}

	if signal_file:
		f_signal = TFile(signal_file, "READ")
		tdf_signal = f_signal.Get("inclusive")

	for var in variables:
		if "mjj" in var or "pt" in var:
			c = ROOT.TCanvas("c_" + var, "c_" + var, 800, 600)
			l = ROOT.TLegend(0.4, 0.7, 0.9, 0.9)
		elif "btag" in var:
			c = ROOT.TCanvas("c_" + var, "c_" + var, 800, 600)
			l = ROOT.TLegend(0.21, 0.5, 0.7, 0.8)
		elif "eta" in var:
			c = ROOT.TCanvas("c_" + var, "c_" + var, 800, 600)
			l = ROOT.TLegend(0.2, 0.75, 0.85, 0.9)
		else:
			c = ROOT.TCanvas("c_" + var, "c_" + var, 1200, 600)
			c.SetRightMargin(0.25)
			l = ROOT.TLegend(0.76, 0.4, 0.99, 0.7)
		if plot_log:
			c.SetLogy()
		l.SetFillColor(0)
		l.SetBorderSize(0)
		style_counter = 0
		hist = {}
		hist_signal = {}
		ymax = -1.
		for trigger in test_triggers:
			hist[trigger] = tdf.Get("h_ref" + trigger + "_" + var)
			hist[trigger].SetDirectory(0)
			if signal_file:
				hist_signal[trigger] = tdf.Get("h_ref" + trigger + "_" + var)
				hist_signal[trigger].SetDirectory(0)
				# Normalize
				hist_signal[trigger].Scale(1. / tdf_signal.Get("h_ref" + trigger + "_nevents").Integral() * 19700. * signal_xs)

			if var in rebin.keys():
				hist[trigger].Rebin(rebin[var])
				if signal_file:
					hist_signal[trigger].Rebin(rebin[var])
			blind = False
			if blind:
				if "mjj" in var:
					for bin in xrange(1, hist[trigger].GetNbinsX() + 1):
						if TMath.Abs(hist[trigger].GetBinCenter(bin) - 750.) < 75.:
							hist[trigger].SetBinContent(bin, 0.)
							hist[trigger].SetBinError(bin, 0.)
			hist[trigger].SetLineColor(seaborn.GetColorRoot("default", style_counter))
			hist[trigger].SetMarkerColor(seaborn.GetColorRoot("default", style_counter))
			hist[trigger].SetMarkerStyle(21)
			if "mjj" in var or "pt" in var:
				hist[trigger].GetYaxis().SetTitle("Events / " + str(int(hist[trigger].GetXaxis().GetBinWidth(1))) + " GeV")
			l.AddEntry(hist[trigger], trigger, "l")
			if signal_file:
				hist_signal[trigger].SetLineColor(seaborn.GetColorRoot("dark", style_counter))

			if hist[trigger].GetMaximum() > ymax:
				ymax = hist[trigger].GetMaximum()

			style_counter += 1

		first = True
		for trigger in test_triggers:
			if first:
				first = False
				opt = "pe1"
				if plot_log:
					hist[trigger].SetMaximum(ymax * 10.)
				else:
					if "eta" in var:
						hist[trigger].SetMaximum(ymax * 1.5)
					else:
						hist[trigger].SetMaximum(ymax * 1.2)
				# Y axis label
			else:
				opt = "pe1 same"
			hist[trigger].Draw(opt)
			if signal_file:
				hist_signal[trigger].Draw("hist same")
		l.Draw()
		if plot_log:
			c.SaveAs("~/Dijets/data/EightTeeEeVeeBee/TriggerEfficiency/figures/" + c.GetName() + "_log.pdf")
		else:
			c.SaveAs("~/Dijets/data/EightTeeEeVeeBee/TriggerEfficiency/figures/" + c.GetName() + ".pdf")



if __name__ == "__main__":
	f_data = TFile("/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/Results/InclusiveBHistograms_2012.root", "READ")
	signal_mass_points = [500., 750., 1000.]
	f_signal = TFile("/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/Results/InclusiveBHistograms_RSGravitonToBBbar_M_750_TuneZ2star_8TeV_pythia6_FASTSIM.root", "READ")

	for jet_type in ["fatjet", "pfjet"]:
		data_hist = f_data.Get("inclusive/h_" + jet_type + "_mjj")
		data_hist.SetName(data_hist.GetName() + "_data")

		signal_histograms = []
		signal_names = []
		for signal_mass_point in signal_mass_points:
			signal_histograms.append(f_signal.Get("inclusive/h_" + jet_type + "_mjj"))
			signal_histograms[-1].SetName(signal_histograms[-1].GetName() + "_signal" + str(signal_mass_point))
			signal_histograms[-1].Scale(19700 / signal_cross_sections["RSG"][signal_mass_point])
			signal_names.append("RSG to bb, m=" + str(signal_mass_point) + " GeV")

		MakeMjjPlot(data_hist, signal_histograms=signal_histograms, signal_names=signal_names, x_min=0., x_max=1500., save_tag="c_" + jet_type + "_mjj", log=False, fit_min=500., fit_max=1500.)
		MakeMjjPlot(data_hist, signal_histograms=signal_histograms, signal_names=signal_names, x_min=0., x_max=1500., save_tag="c_" + jet_type + "_mjj_log", log=True, fit_min=500., fit_max=1500.)
		MakeMjjPlot(data_hist, signal_histograms=signal_histograms, signal_names=signal_names, x_min=500., x_max=1000., save_tag="c_" + jet_type + "_mjj_zoom", log=False, fit_min=500., fit_max=1500.)
		MakeMjjPlot(data_hist, signal_histograms=signal_histograms, signal_names=signal_names, x_min=500., x_max=1000., save_tag="c_" + jet_type + "_mjj_log_zoom", log=True, fit_min=500., fit_max=1500.)
