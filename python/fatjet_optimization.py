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

def mass_peak_plot(names, histograms, save_tag, x_range=None, log=False):
	c = TCanvas("c_mass_peaks_" + save_tag, "c_mass_peaks_" + save_tag, 800, 600)
	l = TLegend(0.6, 0.65, 0.88, 0.88)
	l.SetFillColor(0)
	l.SetBorderSize(0)

	if x_range:
		x_min = x_range[0]
		x_max = x_range[1]
	else:
		x_min = histograms[names[0]].GetXaxis().GetXmin()
		x_max = histograms[names[0]].GetXaxis().GetXmax()


	frame = TH1F("frame", "frame", 100, x_min, x_max)
	y_max = -1.
	for name in names:
		if histograms[name].GetMaximum() > y_max:
			y_max = histograms[name].GetMaximum()
	if log:
		y_min = 0.01
		y_max = y_max * 10
	else:
		y_min = 0.
		y_max = y_max * 1.3
	frame.SetMinimum(y_min)
	frame.SetMaximum(y_max)
	frame.GetXaxis().SetTitle("m_{jj} [GeV]")
	frame.Draw("axis")

	# First loop: draw error bars as filled areas
	style_counter = 0
	for name in names:
		#histograms[name].SetMarkerStyle(20 + style_counter)
		#histograms[name].SetMarkerColor(seaborn.GetColorRoot("dark", style_counter))

		# Draw errors as a filled area
		histograms[name + "_err"] = histograms[name].Clone()
		histograms[name + "_err"].SetMarkerSize(0)
		histograms[name + "_err"].SetFillColor(seaborn.GetColorRoot("pastel", style_counter))
		histograms[name + "_err"].SetFillStyle(3001)
		histograms[name + "_err"].Draw("e2 same")
		style_counter += 1

	# Second loop: draw central values as thick line
	style_counter = 0
	for name in names:
		histograms[name].SetLineWidth(2)
		histograms[name].SetLineColor(seaborn.GetColorRoot("dark", style_counter))
		histograms[name].Draw("hist same")

		#histograms[name].Draw("hist same")
		l.AddEntry(histograms[name], name, "pl")
		style_counter += 1
	l.Draw()
	c.SaveAs(analysis_config.figure_directory + "/" + c.GetName() + ".pdf")

if __name__ == "__main__":
	for model in ["Hbb", "RSG"]:
		for mass_point in [600, 750, 900, 1200]:
			f1 = TFile(analysis_config.get_b_histogram_filename("trigbbh_CSVTM", analysis_config.simulation.get_signal_tag(model, mass_point, "FULLSIM")), "READ")
			f2 = TFile(analysis_config.get_b_histogram_filename("trigbbh_CSVTM_bfat", analysis_config.simulation.get_signal_tag(model, mass_point, "FULLSIM")))
			
			histograms = {}
			histograms["ak5"] = f1.Get("BHistograms/h_pfjet_mjj")
			histograms["ak5"].SetName("h_ak5_" + model + "_" + str(mass_point))
			histograms["ak5"].SetDirectory(0)

			histograms["Fat, #DeltaR=1.1, p_{T}=30 GeV"] = f1.Get("BHistograms/h_fatjet_mjj")
			histograms["Fat, #DeltaR=1.1, p_{T}=30 GeV"].SetName("h_fat1p1_" + model + "_" + str(mass_point))
			histograms["Fat, #DeltaR=1.1, p_{T}=30 GeV"].SetDirectory(0)
			
			histograms["Fat, #DeltaR=0.8, p_{T}=15 GeV"] = f2.Get("BHistograms/h_fatjet_mjj")
			histograms["Fat, #DeltaR=0.8, p_{T}=15 GeV"].SetName("h_fat0p8_" + model + "_" + str(mass_point))
			histograms["Fat, #DeltaR=0.8, p_{T}=15 GeV"].SetDirectory(0)

			#f_ptordered = TFile(analysis_config.get_b_histogram_filename("trigbbh_CSVTM", analysis_config.simulation.get_signal_tag(model, mass_point, "FULLSIM")).replace("BHistograms/", "BHistograms/PtOrdered/"), "READ")
			#histograms["ak5, p_{T} order"] = f_ptordered.Get("BHistograms/h_pfjet_mjj")
			#histograms["ak5, p_{T} order"].SetName("h_ptordered")
			#histograms["ak5, p_{T} order"].SetDirectory(0)
			#for bin in xrange(1, histograms["ak5"].GetNbinsX() + 1):
			#	histograms["ak5, p_{T} order"].SetBinContent(bin, histograms["ak5, p_{T} order"].GetBinContent(bin) / 2)
			#	histograms["ak5, p_{T} order"].SetBinError(bin, histograms["ak5, p_{T} order"].GetBinError(bin) / 2)

			# Rebin and normalize
			for name, hist in histograms.iteritems():
				hist.Rebin(20)
				#hist.Scale(1. / hist.Integral())

			#mass_peak_plot(["ak5", "Fat, #DeltaR=1.1, p_{T}=30 GeV"], histograms, model + "_" + str(mass_point), x_range=[mass_point - 400., mass_point + 300.], log=False)
			mass_peak_plot(["ak5", "Fat, #DeltaR=1.1, p_{T}=30 GeV", "Fat, #DeltaR=0.8, p_{T}=15 GeV"], histograms, model + "_" + str(mass_point), x_range=[mass_point - 600., mass_point + 400.], log=False)
			#mass_peak_plot(["ak5", "ak5, p_{T} order"], histograms, "btag_vs_pt_order_" + model + "_" + str(mass_point), x_range=[mass_point - 300., mass_point + 300.], log=False)
			f1.Close()
			f2.Close()