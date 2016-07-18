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


def make_efficiency_histogram(test_hist, ref_hist, output_file):
	efficiency_hist = test_hist.Clone()
	efficiency_hist.SetName("h_trigger_efficiency")
	for bin in xrange(1, test_hist.GetNbinsX() + 1):
		num = test_hist.GetBinContent(bin)
		den = ref_hist.GetBinContent(bin)
		if den > 0:
			eff = num / den
			d_eff = (eff * (1. - eff) / den)**0.5
		else:
			eff = 0.
			d_eff = 0.
		efficiency_hist.SetBinContent(bin, eff)
		efficiency_hist.SetBinError(bin, d_eff)
	output_file.cd()
	efficiency_hist.Write()

if __name__ == "__main__":
	analyses = ["trigbbh_CSVTM", "trigbbl_CSVTM"]
	trigeff_files = {
		"trigbbh_CSVTM":"/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/TriggerEfficiency/BHistograms_trigeff_trigbbh_CSVTM_BJetPlusX_2012.root",
		"trigbbl_CSVTM":"/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/TriggerEfficiency/BHistograms_trigeff_trigbbl_CSVTM_BJetPlusX_2012.root",
	}
	test_triggers = {
		"trigbbh_CSVTM":"HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose",
		"trigbbl_CSVTM":"HLT_Jet80Eta1p7_Jet70Eta1p7_DiBTagIP3DFastPV",
	}
	for analysis in analyses:
		f = TFile(trigeff_files[analysis], "READ")
		reference_trigger = "HLT_Jet60Eta1p7_Jet53Eta1p7_DiBTagIP3DFastPV"
		ref_hist = f.Get("BHistograms/h_ref" + reference_trigger + "_pfjet_mjj")
		test_hist = f.Get("BHistograms/h_test" + test_triggers[analysis] + "_ref" + reference_trigger + "_pfjet_mjj")
		make_efficiency_histogram(test_hist, ref_hist, TFile(analysis_config.trigger_efficiency_file[analysis], "RECREATE"))
