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
import CMSDIJET.QCDAnalysis.analysis_configuration_8TeV as analysis_config
import CMSDIJET.QCDAnalysis.mjj_common as mjj_common
from CMSDIJET.QCDAnalysis.plots import AnalysisComparisonPlot

def f8(seq): # Dave Kirby
    # Order preserving
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]

if __name__ == "__main__":

	for analysis in ["lowmass", "highmass"]:
		if analysis == "highmass":
			f_bjetplusx = TFile(analysis_config.get_b_histogram_filename("trigbbh_CSVTM", "BJetPlusX_2012"), "READ")
			f_singlemu = TFile(analysis_config.get_b_histogram_filename("mu_highmass_CSVTM", "SingleMu_2012"), "READ")
		else:
			f_bjetplusx = TFile(analysis_config.get_b_histogram_filename("trigbbl_CSVTM", "BJetPlusX_2012BCD"), "READ")
			f_singlemu = TFile(analysis_config.get_b_histogram_filename("mu_lowmass_CSVTM", "SingleMu_2012"), "READ")
		print "[debug] For BJetsPlusX_2012, input events = " + str(f_bjetplusx.Get("BHistograms/h_input_nevents").GetEntries())
		print "[debug] For SingleMu_2012, input events = " + str(f_singlemu.Get("BHistograms/h_input_nevents").GetEntries())
		bjetplusx_histogram = f_bjetplusx.Get("BHistograms/h_pfjet_mjj").Rebin(25)
		bjetplusx_histogram.SetDirectory(0)
		f_bjetplusx.Close()
		singlemu_histogram = f_singlemu.Get("BHistograms/h_pfjet_mjj").Rebin(25)
		singlemu_histogram.SetDirectory(0)
		f_singlemu.Close()

		# Normalize the histograms above 450 GeV
		norm_low_bin = bjetplusx_histogram.GetXaxis().FindBin(450)
		norm_high_bin = bjetplusx_histogram.GetXaxis().GetNbins()
		singlemu_histogram.Scale(bjetplusx_histogram.Integral(norm_low_bin, norm_high_bin) / singlemu_histogram.Integral(norm_low_bin, norm_high_bin))

		plot = AnalysisComparisonPlot(bjetplusx_histogram, singlemu_histogram, "BJetPlusX", "SingleMu", "online_btag_efficiency_mu_" + analysis, x_range=[0., 1200.], log=True)
		plot.draw()
		plot.top.cd()

		# Fit constant to ratio
		ratio_fit = TF1("ratio_fit", "[0]", 400, 1000)
		plot.hist_ratio.Fit(ratio_fit, "QR0")
		plot.canvas.cd()
		plot.bottom.cd()
		ratio_fit.Draw("same")
		plot.canvas.cd()
		print "Ratio chi2/ndf = " + str(ratio_fit.GetChisquare()) + " / " + str(ratio_fit.GetNDF()) + " = " + str(ratio_fit.GetChisquare() / ratio_fit.GetNDF())
		plot.save()
		print ratio_fit

		print plot.top
