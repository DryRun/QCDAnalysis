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

triggers = [
	'HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose', 
	'HLT_Jet80Eta1p7_Jet70Eta1p7_DiBTagIP3DFastPV'
]

def BackgroundFit(x, par):
  	return par[0] * (1. - (x[0] / 8.e3))**par[1] / ((x[0] / 8.e3)**(par[2] + par[3] * TMath.Log((x[0] / 8.e3))))

def CrystalBallFit(x, par):
	#Crystal ball function for signal, parameters are 0:alpha,1:n,2:mean,3:sigma,4:normalization;
	t = (x[0]-par[2])/par[3]
	if par[0] < 0:
		t = -t
	absAlpha = TMath.Abs(par[0])
	if (t >= -1. * absAlpha):
		return par[4]*TMath.Exp(-0.5*t*t)
	else:
		a =  TMath.Power(par[1]/absAlpha,par[1])*TMath.Exp(-0.5*absAlpha*absAlpha);
		b= par[1]/absAlpha - absAlpha; 
		return par[4]*(a/TMath.Power(b - t, par[1]))

def MakeFitPullHistogram(hist, fit):
	#print "Fit xmin = " + str(fit.GetXmin())
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
	fit.SetParLimits(0, 0., 20.)
	fit.SetParameter(1, 2.)
	fit.SetParLimits(1, 1., 20.)
	fit.SetParameter(2, hist.GetMean())
	fit.SetParLimits(2, hist.GetMean() - 200., hist.GetMean() + 100.)
	fit.SetParameter(3, hist.GetRMS())
	fit.SetParLimits(3, 1., 1000.)
	fit.SetParameter(4, hist.GetMaximum())

	hist.Fit(fit, "QRI0")
	#if fit.GetNDF() > 0:
	#	print "fit chi2/ndf = " + str(fit.GetChisquare()) + " / " + str(fit.GetNDF()) + " = " + str(fit.GetChisquare() / fit.GetNDF())
	#else:
	#	print "fit chi2/ndf = " + str(fit.GetChisquare()) + " / " + str(fit.GetNDF()) + " = NAN"
	return {"fit":fit, "fit_ratio":MakeFitPullHistogram(hist, fit)}

def DoMjjBackgroundFit(hist, blind=True, fit_min=500., fit_max=2000., rebin=20):
	# Clone the histogram to avoid modifying the original
	hist = hist.Clone()
	hist.SetName(hist.GetName() + "_copy")

	if blind:
		for bin in xrange(1, hist.GetNbinsX() + 1):
			if TMath.Abs(hist.GetBinCenter(bin) - 750.) < 75.:
				hist.SetBinContent(bin, 0.)
				hist.SetBinError(bin, 0.)
	fit = TF1("fit_mjj", BackgroundFit, fit_min, fit_max, 4)
	fit.SetParameter(0, 2.e-4)
	fit.SetParameter(1, 3)
	fit.SetParameter(2, 10)
	fit.SetParameter(3, 1)
	fit.SetParLimits(0, 1.e-6, 1.e2)
	fit.SetParLimits(1, -25., 25.)
	fit.SetParLimits(2, -25., 25.)
	fit.SetParLimits(3, -5., 5.)
	hist.Fit(fit, "QRI0")
	fit_ratio = MakeFitPullHistogram(hist, fit)
	#print "fit chi2/ndf = " + str(fit.GetChisquare()) + " / " + str(fit.GetNDF()) + " = " + str(fit.GetChisquare() / fit.GetNDF())

	return {"fit":fit, "fit_ratio":fit_ratio}


def MjjPlot(input_file, output_tag, plot_log=False, signal_file=None, signal_xs=None, blind=False, fit_min=500., fit_max=2000.):
	f_in = TFile(input_file, "READ")
	tdf = f_in.Get("inclusive")
	rebin = 20

	hist = f_in.Get("h_fatjet_mjj")
	hist.SetDirectory(0)
	hist.Rebin(rebin)

	if blind:
		for bin in xrange(1, hist.GetNbinsX() + 1):
			if TMath.Abs(hist.GetBinCenter(bin) - 750.) < 75.:
				hist.SetBinContent(bin, 0.)
				hist.SetBinError(bin, 0.)

	fit = TF1("fit_mjj", BackgroundFit, fit_min, fit_max, 4)
	fit.SetParameter(0, 2.e-4)
	fit.SetParameter(1, 3)
	fit.SetParameter(2, 10)
	fit.SetParameter(3, 1)
	#fit[trigger].SetParLimits(0, 1.e-6, 1.e2)
	#fit[trigger].SetParLimits(1, -25., 25.)
	#fit[trigger].SetParLimits(2, -25., 25.)
	#fit[trigger].SetParLimits(3, -1., 1.)
	hist.Fit(fit, "ER0I")
	fit_ratio = MakeFitPullHistogram(hist, fit)
	print "fit chi2/ndf = " + str(fit.GetChisquare()) + " / " + str(fit.GetNDF()) + " = " + str(fit.GetChisquare() / fit.GetNDF())

	# Styling
	hist.SetLineColor(ROOT.kBlack)
	hist.SetMarkerColor(ROOT.kBlack)
	hist.SetMarkerStyle(20)
	hist.GetYaxis().SetTitle("Events / " + str(int(hist.GetXaxis().GetBinWidth(1))) + " GeV")
	hist.GetXaxis().SetTitleSize(0)
	hist.GetXaxis().SetLabelSize(0)
	fit.SetLineColor(seaborn.GetColorRoot("dark", 2))
	fit_ratio.SetLineColor(ROOT.kBlack)
	fit_ratio.SetFillColor(seaborn.GetColorRoot("dark", 2))
	fit_ratio.SetFillStyle(1001)
	fit_ratio.GetYaxis().SetTitle("#frac{Data - Fit}{#sigma(Data)}")

	# Drawing
	c = ROOT.TCanvas("c_mjj", "c_mjj", 800, 1000)
	top = ROOT.TPad("top", "top", 0., 0.5, 1., 1.)
	if plot_log:
		top.SetLogy()
	top.SetBottomMargin(0.03)
	top.Draw()
	c.cd()
	bottom = ROOT.TPad("bottom", "bottom", 0., 0., 1., 0.5)
	bottom.SetTopMargin(0.03)
	bottom.SetBottomMargin(0.2)
	bottom.Draw()
	ROOT.SetOwnership(c, False)
	ROOT.SetOwnership(top, False)
	ROOT.SetOwnership(bottom, False)
	top.cd()
	hist.Draw("p e1")
	fit.Draw("same")
	c.cd()
	bottom.cd()
	fit_ratio.Draw("fhist")
	c.cd()

	if signal_file:
		hist_signal.Draw("hist same")
	if plot_log:
		c.SaveAs("~/Dijets/data/EightTeeEeVeeBee/Results/figures/" + c.GetName() + "_log.pdf")
	else:
		c.SaveAs("~/Dijets/data/EightTeeEeVeeBee/Results/figures/" + c.GetName() + ".pdf")

	c_zoom = ROOT.TCanvas("c_mjj_zoom750", "c_mjj_zoom750", 800, 1000)
	zoom_bin_min = hist.GetXaxis().FindBin(500.)
	zoom_bin_max = hist.GetXaxis().FindBin(1000.)
	hist.GetXaxis().SetRange(zoom_bin_min, zoom_bin_max)
	fit_ratio.GetXaxis().SetRange(zoom_bin_min, zoom_bin_max)
	top_zoom = ROOT.TPad("top_zoom", "top_zoom", 0., 0.5, 1., 1.)
	if plot_log:
		top_zoom.SetLogy()
	top_zoom.SetBottomMargin(0.03)
	top_zoom.Draw()
	c_zoom.cd()
	bottom_zoom = ROOT.TPad("bottom_zoom", "bottom_zoom", 0., 0., 1., 0.5)
	bottom_zoom.SetTopMargin(0.03)
	bottom_zoom.SetBottomMargin(0.2)
	bottom_zoom.Draw()
	ROOT.SetOwnership(c, False)
	ROOT.SetOwnership(top_zoom, False)
	ROOT.SetOwnership(bottom_zoom, False)
	top_zoom.cd()
	hist.Draw("p e1")
	fit.Draw("same")
	c_zoom.cd()
	bottom_zoom.cd()
	fit_ratio.Draw("fhist")
	c_zoom.cd()

	if signal_file:
		hist_signal.Draw("hist same")
	if plot_log:
		c_zoom.SaveAs("~/Dijets/data/EightTeeEeVeeBee/Results/figures/" + c_zoom.GetName() + "_log.pdf")
	else:
		c_zoom.SaveAs("~/Dijets/data/EightTeeEeVeeBee/Results/figures/" + c_zoom.GetName() + ".pdf")



if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description = 'Dijet mass spectrum fits')
	parser.add_argument('input', type=str, help='Input file')
	parser.add_argument('hist_name', type=str, help='Histogram name')
	args = parser.parse_args()

	output_tag = args.input
	output_tag.replace(".root", "")

	Fit(args.input, output_tag)
