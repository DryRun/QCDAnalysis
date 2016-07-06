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

def signal_acc_eff():
	for analysis in ["trigbbh_CSVTM", "trigbbl_CSVTM"]:
		for model in ["Hbb", "RSG"]:
			for mass in [300, 600, 750, 900, 1200]:
				f = TFile(analysis_config.get_b_histogram_filename(analysis, analysis_config.simulation.get_signal_tag(model, mass, "FULLSIM"), ), "READ")
				nevents = (f.Get("BHistograms/h_input_nevents")).Integral()
				h_mjj = f.Get("BHistograms/h_pfjet_mjj")
				nsignal = h_mjj.Integral(1, h_mjj.GetNbinsX() + 1)
				if nevents > 0:
					acceff = 1. * nsignal / nevents
				else:
					acceff = 0.
				print analysis + "\t&\t" + model + "\t&\t" + str(mass) + "\t&\t" + str(nsignal) + "\t&\t" + str(nevents) + "\t&\t" + str(acceff) + "\t\\\\\n"

if __name__ == "__main__":
	signal_acc_eff()