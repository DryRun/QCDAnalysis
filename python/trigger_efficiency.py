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
Root.SetCanvasStyle()
gStyle.SetPalette(1)

import CMSDIJET.QCDAnalysis.analysis_configuration_8TeV as analysis_config


def make_efficiency_histogram(test_hist, ref_hist, output_file=None):
	efficiency_hist = test_hist.Clone()
	efficiency_hist.SetName("h_trigger_efficiency")
	for bin in xrange(1, test_hist.GetNbinsX() + 1):
		num = test_hist.GetBinContent(bin)
		den = ref_hist.GetBinContent(bin)
		if den > 0 and num <= den:
			eff = num / den
			d_eff = (eff * (1. - eff) / den)**0.5
		else:
			eff = 0.
			d_eff = 0.
		efficiency_hist.SetBinContent(bin, eff)
		efficiency_hist.SetBinError(bin, d_eff)
	if output_file:
		output_file.cd()
		efficiency_hist.Write()
	return efficiency_hist

def fit_efficiency(histogram, fit_range, save_tag):
	fits = {}
	fits["erf"] = ROOT.TF1("erf", "(0.5 * (1 + TMath::Erf((x-[0])/[1])))**[2]", fit_range[0], fit_range[1])
	fits["erf"].SetParameter(0, 250)
	fits["erf"].SetParameter(1, 100)
	fits["erf"].SetParameter(2, 1)

	fits["sigmoid"] = ROOT.TF1("sigmoid", "(1. / (1. + TMath::Exp(-1. * (x - [0]) / [1])))**[2]", fit_range[0], fit_range[1])
	fits["sigmoid"].SetParameter(0, 250)
	fits["sigmoid"].SetParameter(1, 100)
	fits["sigmoid"].SetParameter(2, 1)

	#fits["arctan"] = TF1("arctan", "(0.5 * (1 + TMath::ArcTan((x-[0])/[1])))**[2]", fit_ranges[0], fit_ranges[1])
	#fits["arctan"].SetParameter(0, 250)
	#fits["arctan"].SetParameter(1, 100)
	#fits["arctan"].SetParameter(2, 1)

	for function_name, function in fits.iteritems():
		print "Starting fit " + function_name
		histogram.Fit(function, "R0")
		print "chi2/ndf = " + str(function.GetChisquare()) + " / " + str(function.GetNDF()) + " = " + str(function.GetChisquare() / function.GetNDF())

		print "Making canvas"
		c = TCanvas("c_" + function_name + "_" + save_tag, "c_" + function_name + "_" + save_tag, 800, 1000)
		top = TPad("top", "top", 0., 0.5, 1., 1.)
		top.SetBottomMargin(0.03)
		top.Draw()
		top.cd()
		frame_top = ROOT.TH1D("frame_top", "frame_top", 100, 0., 800.)
		frame_top.SetMinimum(-0.1)
		frame_top.SetMaximum(1.1)
		frame_top.GetXaxis().SetLabelSize(0)
		frame_top.GetXaxis().SetTitleSize(0)
		frame_top.Draw("axis")
		histogram.Draw("same")
		function.SetLineColor(seaborn.GetColorRoot("default", 2))
		function.Draw("same")

		c.cd()
		bottom = TPad("bottom", "bottom", 0., 0., 1., 0.5)
		bottom.SetTopMargin(0.02)
		bottom.SetBottomMargin(0.25)
		bottom.Draw()
		bottom.cd()
		frame_bottom = ROOT.TH1D("frame_bottom", "frame_bottom", 100, 0., 800.)
		frame_bottom.SetMinimum(-3.)
		frame_bottom.SetMaximum(3.)
		frame_bottom.Draw("axis")

		pulls = histogram.Clone()
		pulls.Reset()
		for bin in xrange(1, histogram.GetNbinsX()):
			bin_center = histogram.GetXaxis().GetBinCenter(bin)
			if histogram.GetBinError(bin) > 0:
				pulls.SetBinContent(bin, (histogram.GetBinContent(bin) - fits[function_name].Eval(bin_center)) / (histogram.GetBinError(bin)))
			else:
				pulls.SetBinContent(bin, 0)
		pulls.Draw("same")

		c.cd()
		c.SaveAs(analysis_config.figure_directory + "/trigger_efficiency_fit_" + function_name + "_" + save_tag + ".pdf")
	
		ROOT.SetOwnership(c, False)
		ROOT.SetOwnership(top, False)
		ROOT.SetOwnership(bottom, False)

def trigger_efficiency_plot(ref_hist, test_hist, save_tag):
	c = TCanvas("c_" + save_tag, "c_" + save_tag, 800, 1000)
	l = TLegend(0.68, 0.66, 0.9, 0.88)
	l.SetFillColor(0)
	l.SetBorderSize(0)
	top = TPad("top_" + save_tag, "top_" + save_tag, 0., 0.5, 1., 1.)
	top.SetBottomMargin(0.03)
	top.Draw()
	top.SetLogy()
	top.cd()

	frame = TH1D("frame", "frame", 100, 0., 750.)
	frame.SetMinimum(1.)
	frame.SetMaximum(1.e6)
	frame.GetXaxis().SetLabelSize(0)
	frame.GetXaxis().SetTitleSize(0)
	frame.Draw("axis")

	ref_hist.SetMarkerStyle(25)
	ref_hist.SetMarkerColor(seaborn.GetColorRoot("dark", 0))
	ref_hist.SetLineColor(seaborn.GetColorRoot("dark", 0))
	ref_hist.Draw("p same")

	test_hist.SetMarkerStyle(20)
	test_hist.SetMarkerColor(seaborn.GetColorRoot("dark", 2))
	test_hist.SetLineColor(seaborn.GetColorRoot("dark", 2))
	test_hist.Draw("p same")

	l.AddEntry(ref_hist, "Reference", "lp")
	l.AddEntry(test_hist, "Test", "lp")
	l.Draw()

	c.cd()
	bottom = TPad("bottom_" + save_tag, "bottom_" + save_tag, 0., 0, 1., 0.5)
	bottom.SetTopMargin(0.02)
	bottom.SetBottomMargin(0.2)
	bottom.Draw()
	bottom.cd()
	efficiency_hist = make_efficiency_histogram(test_hist, ref_hist, output_file=None)
	frame_bottom = TH1D("frame_bottom", "frame_bottom", 100, 0., 750.)
	frame_bottom.SetMinimum(0.25)
	frame_bottom.SetMaximum(1.1)
	frame_bottom.GetXaxis().SetTitle("m_{jj} [GeV]")
	frame_bottom.GetYaxis().SetTitle("Efficiency")
	frame_bottom.Draw("axis")
	lines = {}
	for eff in [0.9, 0.95, 0.99, 1.]:
		lines[eff] = TLine(0., eff, 750., eff)
		lines[eff].SetLineColor(kGray)
		lines[eff].SetLineStyle(2)
		lines[eff].SetLineWidth(1)
		lines[eff].Draw("same")
	efficiency_hist.SetMarkerStyle(20)
	efficiency_hist.SetMarkerSize(0)
	efficiency_hist.SetMarkerColor(1)
	efficiency_hist.SetLineColor(1)
	efficiency_hist.SetLineStyle(0)
	efficiency_hist.SetLineWidth(2)
	efficiency_hist.Draw("hist same")

	c.cd()
	c.SaveAs(analysis_config.figure_directory + "/" + c.GetName() + ".pdf")

	ROOT.SetOwnership(top, False)
	ROOT.SetOwnership(bottom, False)
	ROOT.SetOwnership(c, False)


if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Run and plot fits")
	parser.add_argument("--plot", action='store_true', help='Make basic trigger efficiency plot')
	parser.add_argument("--efficiency", action='store_true', help='Make efficiency histograms')
	parser.add_argument("--fit", action='store_true', help='Fit and plot efficiency histograms')
	args = parser.parse_args()

	analyses = ["trigbbh_CSVTM", "trigbbl_CSVTM"]
	fit_ranges = {
		"trigbbl_CSVTM":[175, 400],
		"trigbbh_CSVTM":[300, 600]
	}
	trigeff_files = {
		"trigbbh_CSVTM":"/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/TriggerEfficiency/BHistograms_trigeff_trigbbh_CSVTM_BJetPlusX_2012.root",
		"trigbbl_CSVTM":"/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/TriggerEfficiency/BHistograms_trigeff_trigbbl_CSVTM_BJetPlusX_2012.root",
	}
	test_triggers = {
		"trigbbh_CSVTM":"HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose",
		"trigbbl_CSVTM":"HLT_Jet80Eta1p7_Jet70Eta1p7_DiBTagIP3DFastPV",
	}

	if args.plot:
		for analysis in analyses:
			f = TFile(trigeff_files[analysis], "READ")
			if analysis == "trigbbh_CSVTM":
				reference_trigger = "HLT_Jet60Eta1p7_Jet53Eta1p7_DiBTagIP3DFastPV"
			elif analysis == "trigbbl_CSVTM":
				reference_trigger = "HLT_Jet60Eta1p7_Jet53Eta1p7_DiBTagIP3DFastPV"
			ref_hist = f.Get("BHistograms/h_ref" + reference_trigger + "_pfjet_mjj")
			test_hist = f.Get("BHistograms/h_test" + test_triggers[analysis] + "_ref" + reference_trigger + "_pfjet_mjj")
			ref_hist.Rebin(10)
			test_hist.Rebin(10)
			trigger_efficiency_plot(ref_hist, test_hist, "trigger_efficiency_" + analysis)
			f.Close()

	if args.efficiency:
		for analysis in analyses:
			f = TFile(trigeff_files[analysis], "READ")
			reference_trigger = "HLT_Jet60Eta1p7_Jet53Eta1p7_DiBTagIP3DFastPV"
			ref_hist = f.Get("BHistograms/h_ref" + reference_trigger + "_pfjet_mjj")
			test_hist = f.Get("BHistograms/h_test" + test_triggers[analysis] + "_ref" + reference_trigger + "_pfjet_mjj")
			make_efficiency_histogram(test_hist, ref_hist, TFile(analysis_config.trigger_efficiency_file[analysis], "RECREATE"))
			f.Close()

	if args.fit:
		for analysis in analyses:
			f = TFile(analysis_config.trigger_efficiency_file[analysis], "READ")
			h = f.Get("h_trigger_efficiency")
			fit_efficiency(h, fit_ranges[analysis], analysis)