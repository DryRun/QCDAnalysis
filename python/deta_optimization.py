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
import CMSDIJET.QCDAnalysis.analysis_configuration_8TeV as analysis_config

def deta_optimization(signal_hist, background_hist, save_tag):
	# Get delta eta boundaries
	delta_eta_cuts = []

	for bin in xrange(1, signal_hist.GetNbinsX() + 1):
		bin_up_edge = signal_hist.GetXaxis().GetBinUpEdge(bin)
		if bin_up_edge > 0:
			delta_eta_cuts.append(bin_up_edge)

	tgraph = {}
	tgraph["s"] = TGraphErrors(len(delta_eta_cuts))
	tgraph["b"] = TGraphErrors(len(delta_eta_cuts))
	tgraph["sig"] = TGraphErrors(len(delta_eta_cuts))

	counter = 0
	for delta_eta_cut in delta_eta_cuts:
		low_bin = signal_hist.GetXaxis().FindBin(-1. * delta_eta_cut + 0.0001)
		high_bin = signal_hist.GetXaxis().FindBin(delta_eta_cut - 0.0001)
		s = signal_hist.Integral(low_bin, high_bin)
		ds2 = 0.
		for bin in xrange(low_bin, high_bin + 1):
			ds2 += signal_hist.GetBinError(bin)
		ds = ds2**0.5
		b = background_hist.Integral(low_bin, high_bin)
		if b > 0:
			sig = s / (b**0.5)
			dsig = sig * ((ds / b**0.5)**2 + (b**0.5 * s/b**1.5 * 0.5)**2)**0.5
		else:
			sig = 0
			dsig = 0
		tgraph["s"].SetPoint(counter, delta_eta_cut, s)
		tgraph["s"].SetPointError(counter, 0., ds)
		tgraph["b"].SetPoint(counter, delta_eta_cut, b)
		tgraph["b"].SetPointError(counter, 0., b**0.5)
		tgraph["sig"].SetPoint(counter, delta_eta_cut, sig)
		tgraph["sig"].SetPointError(counter, 0., dsig)
		print "\t\t\t$" + str(round(delta_eta_cut, 2)) + "$\t&\t$" + str(round(s, 2)) + "\\pm" + str(round(s**0.5, 2)) + "$\t&\t$" + str(round(b, 2)) + "\\pm" + str(round(b**0.5, 2)) + "$\t&\t$" + str(round(sig, 2)) + "\\pm" + str(round(dsig, 2)) + "$\t\\\\"
		counter += 1

	c = TCanvas("c_deta_optimization" + save_tag, "c_deta_optimization" + save_tag, 800, 1200)
	top = TPad("top", "top", 0., 0.5, 1., 1.)
	top.SetBottomMargin(0.03)
	top.SetLogy()
	top.Draw()
	top.cd()

	frame_top = TH1F("frame_top", "frame_top", 100, 0., 2.)
	frame_top.SetMinimum(0.1)
	frame_top.SetMaximum(tgraph["b"].GetHistogram().GetMaximum() * 10.)
	frame_top.GetXaxis().SetLabelSize(0)
	frame_top.GetXaxis().SetTitleSize(0)
	frame_top.GetYaxis().SetTitle("Yield")
	frame_top.Draw("axis")
	tgraph["b"].SetMarkerStyle(20)
	tgraph["b"].SetMarkerColor(seaborn.GetColorRoot("dark", 2))
	tgraph["b"].SetLineColor(seaborn.GetColorRoot("dark", 2))
	tgraph["b"].Draw("pl")
	tgraph["s"].SetMarkerStyle(21)
	tgraph["s"].SetMarkerColor(seaborn.GetColorRoot("dark", 3))
	tgraph["s"].SetLineColor(seaborn.GetColorRoot("dark", 3))
	tgraph["s"].Draw("pl")
	l = TLegend(0.6, 0.25, 0.9, 0.45)
	l.SetFillColor(0)
	l.SetBorderSize(0)
	l.AddEntry(tgraph["b"], "Background", "pl")
	l.AddEntry(tgraph["s"], "Signal", "pl")
	l.Draw()

	c.cd()
	frame_bottom = TH1F("frame_bottom", "frame_bottom", 100, 0., 2.)
	frame_bottom.SetMinimum(0.)
	frame_bottom.SetMaximum(tgraph["sig"].GetHistogram().GetMaximum() * 1.2)
	bottom = TPad("bottom", "bottom", 0., 0., 1., 0.5)
	bottom.SetTopMargin(0.02)
	bottom.SetBottomMargin(0.2)
	bottom.Draw()
	bottom.cd()
	frame_bottom.GetXaxis().SetTitle("|#Delta#eta| cut")
	frame_bottom.GetYaxis().SetTitle("s/#sqrt{b}")
	frame_bottom.Draw("axis")
	tgraph["sig"].SetMarkerStyle(21)
	tgraph["sig"].SetMarkerColor(1)
	tgraph["sig"].SetLineColor(1)
	tgraph["sig"].Draw("pl")

	c.cd()
	c.SaveAs(analysis_config.figure_directory + "/" + c.GetName() + ".pdf")

	ROOT.SetOwnership(c, False)
	ROOT.SetOwnership(top, False)
	ROOT.SetOwnership(bottom, False)


if __name__ == "__main__":
	analysis = "trigbbh_CSVTM"
	for model in ["Hbb", "RSG"]:
		for mass in [600, 750, 900, 1200]:
			print "On " + model + " / " + str(mass)

			signal_file = TFile(analysis_config.get_b_histogram_filename(analysis, analysis_config.simulation.get_signal_tag(model, mass, "FULLSIM")), "READ")
			signal_histogram = signal_file.Get("BHistograms/h_nminusone_PFDijetMaxDeltaEta_vs_PFMjj")
			xsec = 1. # 1 pb placeholder
			ngenevt = signal_file.Get("BHistograms/h_input_nevents").Integral()
			signal_histogram.Scale(19700. * xsec / ngenevt)

			print "Background file " + analysis_config.get_b_histogram_filename(analysis, "BJetPlusX_2012")
			background_file = TFile(analysis_config.get_b_histogram_filename(analysis, "BJetPlusX_2012"), "READ")
			background_histogram = background_file.Get("BHistograms/h_nminusone_PFDijetMaxDeltaEta_vs_PFMjj")

			signal_histogram_mjj = signal_histogram.ProjectionY()
			signal_fit_results = DoSignalFit(signal_histogram_mjj, fit_range=[mass-150., mass+150.])
			signal_x0 = signal_fit_results["fit"].GetParameter(2)
			signal_sigma = signal_fit_results["fit"].GetParameter(3)
			print "\tWindow = [" + str(signal_x0 - signal_sigma) + ", " + str(signal_x0 + signal_sigma) + "]"

			low_bin = signal_histogram.GetYaxis().FindBin(signal_x0 - signal_sigma)
			high_bin = signal_histogram.GetYaxis().FindBin(signal_x0 + signal_sigma)

			deta_optimization(signal_histogram.ProjectionX("signal_deta", low_bin, high_bin), background_histogram.ProjectionX("background_deta", low_bin, high_bin), model + "_" + str(mass))
