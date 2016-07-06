import os
import sys
import ROOT
from ROOT import *

gROOT.SetBatch(True)

import CMSDIJET.QCDAnalysis.analysis_configuration_8TeV as analysis_config

def histogram_to_table(hist, normalize=False, txt_file=None):
	yields = {}
	d_yields = {}
	cuts = []
	for bin in xrange(1, hist.GetNbinsX()):
		cut_name = hist.GetXaxis().GetBinLabel(bin)
		if cut_name == "":
			continue
		cuts.append(cut_name)
		yields[cut_name] = hist.GetBinContent(bin)
		d_yields[cut_name] = hist.GetBinError(bin)
	if txt_file:
		sys.stdout = open(txt_file, 'w')
	print "\\begin{table}\n",
	print "\t\\centering\n",
	print "\t\\begin{tabular}{|",
	for i in xrange(len(cuts)):
		print "c|",
	print "}\n",
	print "\t\t\\hline\n",
	print "\t\t",
	for cut_name in cuts:
		print "\t&\t" + cut_name,
	print "\\\\\n",
	print "\t\tSR name",
	for cut_name in cuts:
		print "\t&\t",
		if normalize:
			if yields[cuts[0]] <= 0:
				print "Cannot normalize because first yield = " + str(yields[cuts[0]]),
			eff = yields[cut_name] / yields[cuts[0]]
			d_eff = (eff * (1. - eff) / yields[cuts[0]])**0.5
			print "\t&\t$" + str(round(eff, 3)) + " \\pm " + str(round(d_eff, 3)) + "$",
		else:
			print "\t&\t$" + str(round(yields[cut_name], 1)) + " \\pm " + str(round(d_yields[cut_name], 1)) + "$",
	print "\t\t\\hline",
	print "\t\\end{tabular}\n",
	print "\t\\caption{Event yields after successive cuts.}\n",
	print "\t\\label{table:X}\n",
	print "\\end{tabular}\n",
	print "\\end{table}\n",

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description = 'Make tables from cutflow histograms')
	parser.add_argument('analysis', type=str, help='Analysis name')
	parser.add_argument('sample', type=str, help='Sample name')
	args = parser.parse_args()

	f = TFile(analysis_config.get_b_histogram_filename(args.analysis, args.sample), "READ")
	h = f.Get("BHistograms/CutFlowCounter_QCDEventSelector")
	histogram_to_table(h, normalize=False, txt_file=analysis_config.figure_directory + "/cutflow_" + args.analysis + "_" + args.sample + ".tex")
	histogram_to_table(h, normalize=True, txt_file=analysis_config.figure_directory + "/cuteff_" + args.analysis + "_" + args.sample + ".tex")


