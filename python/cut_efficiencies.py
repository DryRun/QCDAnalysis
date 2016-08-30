import os
import sys
import ROOT
from ROOT import *

gROOT.SetBatch(True)

import CMSDIJET.QCDAnalysis.analysis_configuration_8TeV as analysis_config

def histogram_to_table(headers, cutflow_histograms, normalize=False, txt_file=None):
	# Get cut names
	cuts = []
	for bin in xrange(1, cutflow_histograms[headers[0]].GetNbinsX()):
		cut_name = cutflow_histograms[headers[0]].GetXaxis().GetBinLabel(bin)
		if cut_name == "":
			continue
		cuts.append(cut_name)

	# Get yields
	yields = {}
	d_yields = {}
	for header in headers:
		yields[header] = {}
		d_yields[header] = {}
		for bin in xrange(1, cutflow_histograms[header].GetNbinsX()):
			cut_name = cutflow_histograms[header].GetXaxis().GetBinLabel(bin)
			yields[header][cut_name] = cutflow_histograms[header].GetBinContent(bin)
			d_yields[header][cut_name] = cutflow_histograms[header].GetBinError(bin)
	if txt_file:
		sys.stdout = open(txt_file, 'w')
	print "\\begin{table}\n",
	print "\t\\centering\n",
	print "\t\\begin{tabular}{|",
	for i in xrange(len(cuts)):
		print "c|",
	print "}\n",
	print "\t\t\\hline\n",
	print "\t\tSample",
	for cut_name in cuts:
		print "\t&\t" + cut_name,
	print "\\\\\n",
	for header in headers:
		print "\t\t" + header,
		for cut_name in cuts:
			if normalize:
				if yields[header][cuts[0]] <= 0:
					print "Cannot normalize because first yield = " + str(yields[header][cuts[0]]),
				eff = yields[header][cut_name] / yields[header][cuts[0]]
				d_eff = (eff * (1. - eff) / yields[header][cuts[0]])**0.5
				print "\t&\t$" + str(round(eff, 4)) + " \\pm " + str(round(d_eff, 4)) + "$",
			else:
				print "\t&\t$" + str(round(yields[header][cut_name], 1)) + " \\pm " + str(round(d_yields[header][cut_name], 1)) + "$",
		print "\t\t\\hline\n",
	print "\t\\end{tabular}\n",
	print "\t\\caption{Event yields after successive cuts.}\n",
	print "\t\\label{table:X}\n",
	print "\\end{tabular}\n",
	print "\\end{table}\n",

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description = 'Make tables from cutflow histograms')
	#parser.add_argument('analysis', type=str, help='Analysis name')
	#parser.add_argument('sample', type=str, help='Sample name')
	args = parser.parse_args()

	analyses = ["trigbbl_CSVTM", "trigbbh_CSVTM"]
	samples = ["BJetPlusX_2012"]
	for model in ["Hbb", "RSG"]:
		for mass in [300, 400, 500, 600, 750, 900, 1200]:
			samples.append(analysis_config.simulation.get_signal_tag(model, mass, "FULLSIM"))

	for analysis in analyses:
		headers = []
		cutflow_histograms = {}
		for sample in samples:
			headers.append(sample)
			f = TFile(analysis_config.get_b_histogram_filename(analysis, sample), "READ")
			cutflow_histograms[sample] = f.Get("BHistograms/CutFlowCounter_QCDEventSelector").Clone()
			cutflow_histograms[sample].SetDirectory(0)
			f.Close()
		histogram_to_table(headers, cutflow_histograms, normalize=False, txt_file=analysis_config.figure_directory + "/cutflow_" + analysis + ".tex")
		histogram_to_table(headers, cutflow_histograms, normalize=True, txt_file=analysis_config.figure_directory + "/cuteff_" + analysis + ".tex")


