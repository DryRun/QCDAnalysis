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

def signal_peak_mjj_plot(names, histograms, save_tag, x_range=None, logy=False, colors=None, styles=None):
	c = TCanvas("c_" + save_tag, "c_" + save_tag, 800, 600)
	if logy:
		c.SetLogy()
	l = TLegend(0.7, 0.6, 0.88, 0.88)
	l.SetBorderSize(0)
	l.SetFillColor(0)

	if x_range:
		x_min = x_range[0]
		x_max = x_range[1]
	else:
		x_min = histograms[names[0]].GetXaxis().GetXmin()
		x_max = histograms[names[0]].GetXaxis().GetXmax()

	y_max = -1
	for name in names:
		if histograms[name].GetMaximum() > y_max:
			y_max = histograms[name].GetMaximum()
	if logy:
		y_min = 0.001
		y_max = y_max * 10
	else:
		y_min = 0
		y_max = y_max * 1.5

	frame = TH1D("frame", "frame", 100, x_min, x_max)
	frame.SetMinimum(y_min)
	frame.SetMaximum(y_max)
	frame.GetXaxis().SetTitle("m_{jj} [GeV]")
	frame.Draw("axis")

	style_counter = 0
	for name in names:
		if colors:
			histograms[name].SetLineColor(colors[name])
		else:
			histograms[name].SetLineColor(seaborn.GetColorRoot("dark", style_counter))
		if styles:
			histograms[name].SetLineStyle(styles[name])
		else:
			histograms[name].SetLineStyle(1)

		histograms[name].SetLineWidth(2)
		histograms[name].Draw("hist same")
		l.AddEntry(histograms[name], name, "l")
		style_counter += 1
	l.Draw()
	c.SaveAs(analysis_config.figure_directory + "/" + c.GetName() + ".pdf")


if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description = 'Signal peak plots')
	parser.add_argument('--mjj', action='store_true', help='mjj plot')
	parser.add_argument('--mjjM', action='store_true', help='mjj/M plot')
	args = parser.parse_args()

	models = ["Hbb", "RSG"]
	analyses = ["trigbbl_CSVTM", "trigbbh_CSVTM"]
	masses = {
		"trigbbl_CSVTM":[400, 500, 600, 750],
		"trigbbh_CSVTM":[600, 750, 900, 1200]
	}

	if args.mjj:
		for analysis in analyses:
			names = []
			histograms = {}
			colors = {}
			styles = {}
			for model in models:
				color_counter = 0
				for mass in masses[analysis]:
					f = TFile(analysis_config.get_b_histogram_filename(analysis, analysis_config.simulation.get_signal_tag(model, mass, "FULLSIM")))
					if model == "Hbb":
						name = "H, m=" + str(mass) + " GeV"
					elif model == "RSG":
						name = "G, m=" + str(mass) + " GeV"
					names.append(name)
					histograms[name] = f.Get("BHistograms/h_pfjet_mjj")
					histograms[name].SetDirectory(0)
					histograms[name].Rebin(25)
					histograms[name].Scale(1. / histograms[name].Integral())
					f.Close()
					if model == "Hbb":
						styles[name] = 2
					elif model == "RSG":
						styles[name] = 3
					colors[name] = seaborn.GetColorRoot("dark", color_counter)
					color_counter += 1
			save_tag = "signal_peaks_mjj_" + analysis

			signal_peak_mjj_plot(names=names, histograms=histograms, save_tag=save_tag, x_range=[masses[analysis][0] - 400, masses[analysis][-1] + 200], logy=False, colors=colors, styles=styles)
			signal_peak_mjj_plot(names=names, histograms=histograms, save_tag=save_tag + "_log", x_range=[masses[analysis][0] - 400, masses[analysis][-1] + 200], logy=True, colors=colors, styles=styles)

	if args.mjjM:
		for analysis in analyses:
			for model in models:
				names = []
				histograms = {}
				colors = {}
				color_counter = 0
				for mass in masses[analysis]:
					f = TFile(analysis_config.get_b_histogram_filename(analysis, analysis_config.simulation.get_signal_tag(model, mass, "FULLSIM")))
					name = "m=" + str(mass) + " GeV"
					names.append(name)
					histograms[name] = f.Get("BHistograms/h_pfjet_mjj_over_M")
					histograms[name].SetDirectory(0)
					histograms[name].Scale(1. / histograms[name].Integral())
					f.Close()
					colors[name] = seaborn.GetColorRoot("dark", color_counter)
					color_counter += 1
				save_tag = "signal_peaks_mjj_over_M_" + analysis + "_" + model

				signal_peak_mjj_plot(names=names, histograms=histograms, save_tag=save_tag, x_range=[0., 2.], logy=False, colors=colors)
				signal_peak_mjj_plot(names=names, histograms=histograms, save_tag=save_tag + "_log", x_range=[0., 2.], logy=True, colors=colors)
