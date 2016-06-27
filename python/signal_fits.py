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

def CrystalBallFit(x, par):
	#Crystal ball function for signal, parameters are 0:alpha,1:n,2:mean,3:sigma,4:normalization;
	t = (x[0]-par[2])/par[3]
	if par[0] < 0:
		t = -t
	absAlpha = TMath.Abs(par[0])
	if (t >= -absAlpha):
		return par[4]*TMath.Exp(-0.5*t*t)
	else:
		a =  TMath.Power(par[1]/absAlpha,par[1])*TMath.Exp(-0.5*absAlpha*absAlpha);
		b= par[1]/absAlpha - absAlpha; 
		return par[4]*(a/TMath.Power(b - t, par[1]))

def MakeFitPullHistogram(hist, fit):
	print "Fit xmin = " + str(fit.GetXmin())
	hist_ratio = hist.Clone()
	hist_ratio.SetName(hist.GetName() + "_fit_ratio")
	for bin in xrange(1, hist_ratio.GetNbinsX() + 1):
		xmin = hist_ratio.GetXaxis().GetBinLowEdge(bin)
		xmax = hist_ratio.GetXaxis().GetBinUpEdge(bin)
		if xmax < fit.GetXmin() or xmin > fit.GetXmax():
			hist_ratio.SetBinContent(bin, 0.)
			hist_ratio.SetBinError(bin, 0.)
			continue
		fit_integral = fit.Integral(xmin, xmax)
		if hist.GetBinError(bin) > 0:
			hist_ratio.SetBinContent(bin, (hist.GetBinContent(bin) * hist.GetBinWidth(bin) - fit_integral) / (hist.GetBinError(bin) * hist.GetBinWidth(bin)))
			hist_ratio.SetBinError(bin, 0.)
		else:
			hist_ratio.SetBinContent(bin, 0.)
			hist_ratio.SetBinError(bin, 0.)
	return hist_ratio

def DoSignalFit(hist, fit_range=None):
	fit = ROOT.TF1(hist.GetName() + "_fit", CrystalBallFit, fit_range[0], fit_range[1], 5)
	fit.SetParameter(0, 3.)
	fit.SetParameter(1, 2.)
	fit.SetParameter(2, hist.GetMean())
	fit.SetParameter(3, hist.GetRMS())
	fit.SetParameter(4, hist.Integral())
	hist.Fit(fit, "QRI0")
	return {"fit":fit, "fit_ratio":MakeFitPullHistogram(hist, fit)}


# Make signal peak plot
def SignalPlot(input_file, output_tag, x_range=None, plot_log=False, fit_range=None):
	h_fatjet_mjj = input_file.Get("inclusive/h_fatjet_mjj")
	h_pfjet_mjj = input_file.Get("inclusive/h_pfjet_mjj")

	fit_results_fatjet = DoSignalFit(h_fatjet_mjj, fit_range=fit_range)
	fit_results_pfjet = DoSignalFit(h_pfjet_mjj, fit_range=fit_range)



if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description = 'Signal peak fits')
	parser.add_argument('input', type=str, help='Input file')
	parser.add_argument('hist_name', type=str, help='Histogram name')
	args = parser.parse_args()

	output_tag = args.input
	output_tag.replace(".root", "")

	Fit(args.input, output_tag)
