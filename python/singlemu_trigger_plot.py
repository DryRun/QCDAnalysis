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
		ht_analyses = {}
		names = []
		for mass in xrange(250, 700, 50):
			if mass == 600:
				continue
			if mass == 650:
				continue
			names.append("HT" + str(mass))
			if sr == "highmass":
				ht_analyses["HT" + str(mass)] = "trigjetht" + str(mass) + "_CSVTM"
			else:
				ht_analyses["HT" + str(mass)] = "trigjetht" + str(mass) + "_eta1p7_CSVTM"

		# For now, only the high mass SR has the unprescaled JetHT triggers
		if sr == "highmass":
			names.append("HTUnprescaled")
			ht_analyses["HTUnprescaled"] = "trigjetht_CSVTM"
		ranges = {
			"HT250":[400, 475],
			"HT300":[475, 525],
			"HT350":[525, 575],
			"HT400":[575, 625],
			"HT450":[625, 700],
			"HT500":[700, 750],
			"HT550":[750, 900],
			#"HT650":[800, 900],
			"HTUnprescaled":[900, 2000]
		}
		boundaries = []
		for name, interval in ranges.iteritems():
			boundaries.append(interval[0])
			boundaries.append(interval[1])
		boundaries = f8(boundaries)
		boundaries.sort()

		jetht_sample = "JetHT_2012BCD"
		histograms = {}
		for name in names:
			f = TFile(analysis_config.get_b_histogram_filename(ht_analyses[name], jetht_sample), "READ")
			#histograms[name] = mjj_common.apply_dijet_binning_normalized(f.Get("BHistograms/h_pfjet_mjj"))
			print "[debug] For name " + name + ", input events = " + str(f.Get("BHistograms/h_input_nevents").GetEntries())
			print "[debug] \tPrescale = " + str(f.Get("BHistograms/h_pass_nevents_weighted").GetBinContent(1) / f.Get("BHistograms/h_pass_nevents").GetBinContent(1))
			histograms[name] = f.Get("BHistograms/h_pfjet_mjj")
			histograms[name].SetName(histograms[name].GetName() + "_" + name)
			histograms[name].SetDirectory(0)
			f.Close()
		jetht_histogram = jetht_frankenhist(names, histograms, ranges)
		jetht_histogram.Rebin(25)

		if sr == "highmass":
			f_bjetplusx = TFile(analysis_config.get_b_histogram_filename("trigbbh_CSVTM", "BJetPlusX_2012BCD"), "READ")
		else:
			f_bjetplusx = TFile(analysis_config.get_b_histogram_filename("trigbbl_CSVTM", "BJetPlusX_2012BCD"), "READ")
		print "[debug] For BJetsPlusX_2012BCD, input events = " + str(f_bjetplusx.Get("BHistograms/h_input_nevents").GetEntries())
		bjetplusx_histogram = f_bjetplusx.Get("BHistograms/h_pfjet_mjj").Rebin(25)
		bjetplusx_histogram.SetDirectory(0)
		f_bjetplusx.Close()

		plot = AnalysisComparisonPlot(bjetplusx_histogram, jetht_histogram, "BJetPlusX", "JetHT", "online_btag_efficiency_" + sr, x_range=[0., 1200.], log=True)
		plot.draw()
		plot.top.cd()
		ymin = plot.frame_top.GetMinimum()
		ymax = plot.frame_top.GetMaximum()
		for boundary in boundaries:
			plot.draw_line("top", boundary, ymin, boundary, ymax)
			plot.draw_line("bottom", boundary, -0.2, boundary, 1.2)
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
