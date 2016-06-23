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
def significance(signal_hist, data_hist, signal_mass):
	signal_fit_results = DoSignalFit(signal_hist, fit_range=[signal_mass-150., signal_mass+150.])
	background_fit_results = DoMjjBackgroundFit(data_hist, fit_min=signal_mass-150., signal_mass+150.])
	


def DoMjjBackgroundFit(hist, blind=True, fit_min=500., fit_max=2000., rebin=20):


