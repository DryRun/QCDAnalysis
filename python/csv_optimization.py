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

# Roughly determine significance of a signal histogram with respect to a data histogram
# - Fit signal and data with rough shapes
# - Define "signal region" as half-maximum of signal
# - S = s/sqrt(b) within that window
def significance(analyses, signal_histograms, data_histograms, signal_mass, fit_analysis):
	signal_fit_results = DoSignalFit(signal_histograms[fit_analysis], fit_range=[signal_mass-150., signal_mass+150.])
	signal_x0 = signal_fit_results["fit"].GetParameter(2)
	signal_sigma = signal_fit_results["fit"].GetParameter(3)
	#print "Signal x0, sigma = " + str(signal_x0) + ", " + str(signal_sigma) + " [taken from " + fit_analysis + "]"
	window = [signal_x0 - signal_sigma, signal_x0 + signal_sigma]

	# Make sure window is inside fit range
	for analysis in analyses:
		if "trigbbl" in analysis:
			if window[0] < 354.:
				window[0] = 354.
		elif "trigbbh" in analysis:
			if window[0] < 526.:
				window[0] = 526.

	print "Window = [" + str(window[0]) + ", " + str(window[1]) + "]"
	first = True
	print "\t\t\t\\hline"
	for analysis in analyses:
		low_bin = signal_histograms[analysis].GetXaxis().FindBin(window[0])
		high_bin = signal_histograms[analysis].GetXaxis().FindBin(window[1])
		low_edge = signal_histograms[analysis].GetXaxis().GetBinLowEdge(low_bin)
		up_edge = signal_histograms[analysis].GetXaxis().GetBinUpEdge(high_bin)

		s = signal_histograms[analysis].Integral(low_bin, high_bin)
		#b = data_histograms[analysis].Integral(low_bin, high_bin)
		if "bbl" in analysis:
			fit_min = 354.
			fit_max = 1607.
		elif "bbh" in analysis:
			fit_min = 526.
			fit_max = 1607.
		background_fit_results = DoMjjBackgroundFit(data_histograms[analysis], fit_min=fit_min, fit_max=fit_max)
		b = background_fit_results["fit"].Integral(low_edge, up_edge)
		if first:
			mass_string = "\\multirow{" + str(len(analyses)) + "}{*}{$" + str(signal_mass) + "\ (" + str(round(low_edge, 2)) + "-" + str(round(up_edge, 2)) + ")$ GeV"
			first = False
		else:
			mass_string = "\t\t\t\t\t\t\t\t\t\t"
		if b > 0:
			print "\t\t\t" + mass_string + "\t&\t" + analysis + "\t&\t$" + str(round(s, 2)) + "$\t&\t$" + str(round(b, 2)) + "$\t&\t$" + str(round(s/b**0.5, 2)) + "$\t\\\\"
		else:
			print "\t\t\t" + mass_string + "\t&\t" + analysis + "\t&\t$" + str(round(s, 2)) + "$\t&\t$" + str(round(b, 2)) + "$\t&\tNAN\t\\\\"
	print "\t\t\t\\hline"

if __name__ == "__main__":
	for model in ["Hbb", "RSG"]:
		#for analysis_base in ["trigbbh", "trigbbl"]:
		for analysis_base in ["trigbbl", "trigbbh"]:
			if analysis_base == "trigbbh":
				masses = [600, 750, 900, 1200]
			elif analysis_base == "trigbbl":
				masses = [400, 600, 750, 900]
			analyses = [analysis_base + "_" + x for x in ["CSVL", "CSVM", "CSVT", "CSVTL", "CSVTM", "CSVML"]]
			for mass in masses:
				signal_histograms = {}
				data_histograms = {}
				for analysis in analyses:
					signal_sample = analysis_config.simulation.get_signal_tag(model, mass, "FULLSIM")
					#print "Signal file: " + analysis_config.get_b_histogram_filename(analysis, signal_sample)
					signal_histogram_file = TFile(analysis_config.get_b_histogram_filename(analysis, signal_sample), "READ")
					#print "Data file: " + analysis_config.get_b_histogram_filename(analysis, "BJetPlusX_2012")
					data_histogram_file = TFile(analysis_config.get_b_histogram_filename(analysis, "BJetPlusX_2012"), "READ")
					signal_histograms[analysis] = signal_histogram_file.Get("BHistograms/h_pfjet_mjj")
					if not signal_histograms[analysis]:
						print "ERROR : Couldn't find signal histogram BHistograms/h_pfjet_mjj in file " + analysis_config.get_b_histogram_filename(analysis, signal_sample)
						continue
					signal_histograms[analysis].SetDirectory(0)
					ngenevt = signal_histogram_file.Get("BHistograms/h_input_nevents").Integral()
					xsec = 1. # 1 pb placeholder
					signal_histograms[analysis].Scale(19700. * xsec / ngenevt)
					print "[debug] Data file " + analysis_config.get_b_histogram_filename(analysis, "BJetPlusX_2012")
					data_histograms[analysis] = data_histogram_file.Get("BHistograms/h_pfjet_mjj")
					data_histograms[analysis].SetDirectory(0)
					if not data_histograms[analysis]:
						print "ERROR : Couldn't find data histogram"
						sys.exit(1)
					data_input_nevt = data_histogram_file.Get("BHistograms/h_input_nevents").Integral()
					print "DEBUG : Analysis " + analysis + ", mass " + str(mass) + " input_nevents = " + str(data_input_nevt)
				significance(analyses, signal_histograms, data_histograms, mass, analyses[0])

