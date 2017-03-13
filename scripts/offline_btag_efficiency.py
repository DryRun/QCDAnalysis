import os
import sys
from array import array
import ROOT
from ROOT import *
gROOT.SetBatch(True)
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
gSystem.Load("~/Dijets/CMSSW_5_3_32_patch3/lib/slc6_amd64_gcc472/libMyToolsRootUtils.so")
import CMSDIJET.QCDAnalysis.analysis_configuration_8TeV as analysis_config
sys.path.append("/uscms/home/dryu/Dijets/CMSSW_5_3_32_patch3/python/MyTools/RootUtils")
import histogram_tools
seaborn = Root.SeabornInterface()
seaborn.Initialize()
import time

class OfflineBTagPlots():
	def __init__(self, numerator_analysis, denominator_analysis, samples):
		print "[OfflineBTagPlots::__init__] Initializing with sr = " + sr + ", samples = ",
		print samples
		self._samples = samples
		self._numerator_analysis = numerator_analysis
		self._denominator_analysis = denominator_analysis
		self._input_files = {"numerator":{}, "denominator":{}}
		for sample in self._samples:
			self._input_files["numerator"][sample] = TFile(analysis_config.get_b_histogram_filename(self._numerator_analysis, sample))
			self._input_files["denominator"][sample] = TFile(analysis_config.get_b_histogram_filename(self._denominator_analysis, sample))

	def EfficiencyPlot(self, var="mjj", logy=True, binning=None, simple_rebin=None, save_tag="", sample_xsecs=None, x_range=None, ratio_range=None, legend_position="topright", numerator_legend=None, denominator_legend=None, ratio_title=None):
		numerator_histogram = None
		denominator_histogram = None
		for sample in self._samples:
			print "[EfficiencyPlot] DEBUG : Sample " + sample
			if sample_xsecs:
				xsec = sample_xsecs[sample]
				print "[EfficiencyPlot] DEBUG : Getting histogram from " + self._input_files["numerator"][sample].GetPath()
				numerator_normalization = 19710. * xsec / self._input_files["numerator"][sample].Get("BHistograms/h_sample_nevents").Integral()
				print "[EfficiencyPlot] DEBUG : Getting histogram from " + self._input_files["denominator"][sample].GetPath()
				denominator_normalization = 19710. * xsec / self._input_files["denominator"][sample].Get("BHistograms/h_sample_nevents").Integral()
				if numerator_normalization != denominator_normalization:
					print "[EfficiencyPlot] WARNING : Numerator and denominator normalizations do not match! Continuing, but investigate this. Numerator nevents = " + str(self._input_files["numerator"][sample].Get("BHistograms/h_sample_nevents").Integral()) + ", denominator nevents = " + str(self._input_files["denominator"][sample].Get("BHistograms/h_sample_nevents").Integral())
			else:
				# Check input nevents
				num_nevents = self._input_files["numerator"][sample].Get("BHistograms/h_sample_nevents").Integral()
				den_nevents = self._input_files["denominator"][sample].Get("BHistograms/h_sample_nevents").Integral()
				if num_nevents != den_nevents:
					# Allow tiny differences...?
					if abs((num_nevents - den_nevents) / den_nevents) < 0.001:
						print "[EfficiencyPlot] ERROR : Small inconsistency between number of events between numerator and denominator. I'm going to rescale away the difference, but you may want to fix this."
						numerator_normalization = den_nevents / num_nevents
						denominator_normalization = 1.
					else:
						print "[EfficiencyPlot] ERROR : Inconsistent number of events between numerator and denominator. Results would be wrong, so I'm aborting."
						print "[EfficiencyPlot] ERROR : \tNumerator = " + str(self._input_files["numerator"][sample].Get("BHistograms/h_sample_nevents").Integral())
						print "[EfficiencyPlot] ERROR : \tDenominator = " + str(self._input_files["denominator"][sample].Get("BHistograms/h_sample_nevents").Integral())
						sys.exit(1)
				else:
					numerator_normalization = 1.
					denominator_normalization = 1.
			if numerator_histogram:
				numerator_histogram.Add(self._input_files["numerator"][sample].Get("BHistograms/h_pfjet_" + var), numerator_normalization)
			else:
				numerator_histogram = self._input_files["numerator"][sample].Get("BHistograms/h_pfjet_" + var).Clone()
				numerator_histogram.Scale(numerator_normalization)
				numerator_histogram.SetDirectory(0)
				numerator_histogram.SetName(numerator_histogram.GetName() + save_tag + "_num" + str(time.time()))
			if denominator_histogram:
				denominator_histogram.Add(self._input_files["denominator"][sample].Get("BHistograms/h_pfjet_" + var), denominator_normalization)
			else:
				denominator_histogram = self._input_files["denominator"][sample].Get("BHistograms/h_pfjet_" + var).Clone()
				denominator_histogram.Scale(denominator_normalization)
				denominator_histogram.SetDirectory(0)
				denominator_histogram.SetName(denominator_histogram.GetName() + save_tag + "_den" + str(time.time()))

		# Rebin
		if binning:
			numerator_histogram = histogram_tools.rebin_histogram(numerator_histogram, binning)
			denominator_histogram = histogram_tools.rebin_histogram(denominator_histogram, binning)
		elif simple_rebin:
			numerator_histogram.Rebin(simple_rebin)
			denominator_histogram.Rebin(simple_rebin)


		cname = "c_offline_btag_eff_" + var
		if logy:
			cname += "_log"
		c = TCanvas(cname, "Offline b-tag #epsilon", 800, 1000)
		top = TPad("top", "top", 0., 0.5, 1., 1.)
		top.SetBottomMargin(0.02)
		if logy:
			top.SetLogy()
		top.Draw()
		top.cd()

		frame_top = numerator_histogram.Clone()
		frame_top.Reset()
		if x_range:
			frame_top.GetXaxis().SetRangeUser(x_range[0], x_range[1])
		if logy:
			y_min = 0.1
			y_max = max(numerator_histogram.GetMaximum(), denominator_histogram.GetMaximum()) * 10.
		else:
			y_min = 0.
			y_max = max(numerator_histogram.GetMaximum(), denominator_histogram.GetMaximum()) * 1.5
		frame_top.SetMinimum(y_min)
		frame_top.SetMaximum(y_max)
		frame_top.GetXaxis().SetLabelSize(0)
		frame_top.GetXaxis().SetTitleSize(0)
		if binning:
			#frame_top.GetYaxis().SetTitle("Events / 1 GeV")
			frame_top.GetYaxis().SetTitle("Events")
		else:
			frame_top.GetYaxis().SetTitle("Events")
		frame_top.Draw("axis")
		print "numerator integral = " + str(numerator_histogram.Integral())
		print "denominator integral = " + str(denominator_histogram.Integral())
		numerator_histogram.SetMarkerStyle(20)
		numerator_histogram.SetMarkerColor(seaborn.GetColorRoot("default", 0))
		numerator_histogram.SetLineColor(seaborn.GetColorRoot("default", 0))
		numerator_histogram.Draw("same")
		denominator_histogram.SetMarkerStyle(24)
		denominator_histogram.SetMarkerColor(seaborn.GetColorRoot("default", 2))
		denominator_histogram.SetLineColor(seaborn.GetColorRoot("default", 2))
		denominator_histogram.Draw("same")
		if legend_position == "topright":
			l = TLegend(0.6, 0.6, 0.85, 0.8)
		elif legend_position == "bottomright":
			l = TLegend(0.6, 0.2, 0.85, 0.4)

		l.SetFillColor(0)
		l.SetBorderSize(0)
		if numerator_legend:
			l.AddEntry(numerator_histogram, numerator_legend)
		else:
			l.AddEntry(numerator_histogram, "CSVT+CSVM")
		if denominator_legend:
			l.AddEntry(denominator_histogram, denominator_legend)

		else:
			l.AddEntry(denominator_histogram, "No CSV")
		l.Draw()

		c.cd()
		bottom = TPad("bottom", "bottom", 0., 0., 1., 0.5)
		bottom.SetTopMargin(0.01)
		bottom.SetBottomMargin(0.2)
		bottom.Draw()
		bottom.cd()
		ratio_histogram = numerator_histogram.Clone()
		ratio_histogram.Reset()
		if x_range:
			ratio_histogram.GetXaxis().SetRangeUser(x_range[0], x_range[1])
		ratio_histogram.SetName(numerator_histogram.GetName() + "_ratio_" + save_tag + str(time.time()))
		ratio_histogram.SetDirectory(0)
		for bin in xrange(1, numerator_histogram.GetNbinsX() + 1):
			# Undo bin normalization
			if numerator_histogram.GetBinError(bin) > 0 and denominator_histogram.GetBinError(bin) > 0:
				#num_unnormalized = (numerator_histogram.GetBinContent(bin))**2 / (numerator_histogram.GetBinError(bin))**2
				#den_unnormalized = (denominator_histogram.GetBinContent(bin))**2 / (denominator_histogram.GetBinError(bin))**2
				num = numerator_histogram.GetBinContent(bin)
				den = denominator_histogram.GetBinContent(bin)
				ratio = 1. * num / den 
				ratio_err = sqrt(ratio * (1. - ratio) / den)
				#ratio_err = max(sqrt(ratio * (1. - ratio) / den), 1./den)
			else:
				ratio = 0.
				ratio_err = 0.
			ratio_histogram.SetBinContent(bin, ratio)
			ratio_histogram.SetBinError(bin, ratio_err)
		ratio_histogram.SetMarkerSize(1)
		ratio_histogram.SetMarkerColor(kBlack)
		ratio_histogram.SetLineColor(kBlack)
		ratio_histogram.SetLineWidth(2)
		if "mjj" in var:
			ratio_histogram.GetXaxis().SetTitle("m_{jj} [GeV]")
		elif "pt" in var:
			ratio_histogram.GetXaxis().SetTitle("p_{T} [GeV]")
		if ratio_title:
			ratio_histogram.GetYaxis().SetTitle(ratio_title)
		else:
			ratio_histogram.GetYaxis().SetTitle("Offline 2#timesb-tag efficiency")
		if ratio_range:
			ratio_histogram.SetMinimum(ratio_range[0])
			ratio_histogram.SetMaximum(ratio_range[1])
		else:
			ratio_histogram.SetMinimum(0.)
			ratio_histogram.SetMaximum(1.)
		ratio_histogram.Draw()

		c.cd()
		c.SaveAs(analysis_config.figure_directory + "/OfflineBTag/" + c.GetName() + save_tag + ".pdf")
		ROOT.SetOwnership(c, False)
		ROOT.SetOwnership(top, False)
		ROOT.SetOwnership(bottom, False)

if __name__ == "__main__":
	do_signal = True
	do_qcd = True
	do_singlemu = False
	dijet_binning = array("d", [1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325, 354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 4509, 4686, 4869, 5000])

	wp = "CSVTM"

	if do_signal:
		signal_masses = [400, 500, 600, 750, 900, 1200]
		samples = []
		for model in ["Hbb", "RSG"]:
			for mass in signal_masses:
				samples.append(analysis_config.simulation.get_signal_tag(model, mass, "FULLSIM"))
		for sr in ["lowmass", "highmass"]:
			if sr == "lowmass":
				numerator_analysis = "NoTrigger_eta1p7_" + wp
				denominator_analysis = "NoTrigger_eta1p7"
			elif sr == "highmass":
				numerator_analysis = "NoTrigger_eta2p2_" + wp
				denominator_analysis = "NoTrigger_eta2p2"
			plotter = OfflineBTagPlots(numerator_analysis, denominator_analysis, samples)
			plotter.EfficiencyPlot(logy=False, binning=dijet_binning, save_tag="_" + wp + "_" + sr + "_signal")

			for sample in samples:
				plotter = OfflineBTagPlots(numerator_analysis, denominator_analysis, [sample])
				plotter.EfficiencyPlot(logy=False, binning=dijet_binning, save_tag="_" + wp + "_" + sr + "_signal_" + sample)

	if do_qcd:
		QCD_samples = ["QCD_Pt-80to120_TuneZ2star_8TeV_pythia6","QCD_Pt-120to170_TuneZ2star_8TeV_pythia6","QCD_Pt-170to300_TuneZ2star_8TeV_pythia6","QCD_Pt-300to470_TuneZ2star_8TeV_pythia6","QCD_Pt-470to600_TuneZ2star_8TeV_pythia6","QCD_Pt-600to800_TuneZ2star_8TeV_pythia6","QCD_Pt-800to1000_TuneZ2star_8TeV_pythia6","QCD_Pt-1000to1400_TuneZ2star_8TeV_pythia6","QCD_Pt-1400to1800_TuneZ2star_8TeV_pythia6","QCD_Pt-1800_TuneZ2star_8TeV_pythia6"]
		for sr in ["lowmass", "highmass"]:
			if sr == "lowmass":
				numerator_analysis = "NoTrigger_eta1p7_" + wp
				denominator_analysis = "NoTrigger_eta1p7"
			elif sr == "highmass":
				numerator_analysis = "NoTrigger_eta2p2_" + wp
				denominator_analysis = "NoTrigger_eta2p2"
			plotter = OfflineBTagPlots(numerator_analysis, denominator_analysis, QCD_samples)
			plotter.EfficiencyPlot(var="mjj", logy=True, binning=dijet_binning, save_tag="_" + wp + "_" + sr + "_qcd", ratio_range=[0.,5.e-3], x_range=[0., 2000.], legend_position="bottomright")
			plotter.EfficiencyPlot(var="pt_btag1", logy=True, simple_rebin=5, save_tag="_" + wp + "_" + sr + "_qcd", ratio_range=[0.,5.e-3], x_range=[0., 1000.], legend_position="bottomright")
			plotter.EfficiencyPlot(var="pt_btag2", logy=True, simple_rebin=5, save_tag="_" + wp + "_" + sr + "_qcd", ratio_range=[0.,5.e-3], x_range=[0., 1000.], legend_position="bottomright")

			plotter.EfficiencyPlot(var="mjj", logy=True, binning=dijet_binning, save_tag="_" + wp + "_" + sr + "_qcd_norm", ratio_range=[0.,5.e-3], x_range=[0., 2000.], legend_position="bottomright", sample_xsecs=analysis_config.simulation.background_cross_sections)

	if do_singlemu:
		for sr in ["lowmass", "highmass"]:
			# Total b-tagging efficiency
			if sr == "lowmass":
				numerator_analysis = "trigmu24ibbl_" + sr + "_" + wp
			elif sr == "highmass":
				numerator_analysis = "trigmu24ibbh_" + sr + "_" + wp
			denominator_analysis = "trigmu24i_" + sr
			plotter = OfflineBTagPlots(numerator_analysis, denominator_analysis, ["SingleMu_2012"])
			plotter.EfficiencyPlot(var="mjj", logy=True, binning=dijet_binning, save_tag="_" + wp + "_" + sr + "_totalbtag_singlemu", ratio_range=[0.,0.02], x_range=[0., 2000.], legend_position="topright", numerator_legend="With on+off b-tagging", denominator_legend="No b-tagging", ratio_title="Total online*offline b-tag efficiency")

			# Offline b-tagging efficiency
			if sr == "lowmass":
				numerator_analysis = "trigmu24i_" + sr + "_" + wp
			elif sr == "highmass":
				numerator_analysis = "trigmu24i_" + sr + "_" + wp
			denominator_analysis = "trigmu24i_" + sr
			plotter = OfflineBTagPlots(numerator_analysis, denominator_analysis, ["SingleMu_2012"])
			plotter.EfficiencyPlot(var="mjj", logy=True, binning=dijet_binning, save_tag="_" + wp + "_" + sr + "_offbtag_singlemu", ratio_range=[0.,0.06], x_range=[0., 2000.], legend_position="topright")

			# Online b-tagging efficiency
			if sr == "lowmass":
				numerator_analysis = "trigmu24ibbl_" + sr
			elif sr == "highmass":
				numerator_analysis = "trigmu24ibbh_" + sr
			denominator_analysis = "trigmu24i_" + sr
			plotter = OfflineBTagPlots(numerator_analysis, denominator_analysis, ["SingleMu_2012"])
			plotter.EfficiencyPlot(var="mjj", logy=True, binning=dijet_binning, save_tag="_" + wp + "_" + sr + "_onbtag_singlemu", ratio_range=[0.,0.1], x_range=[0., 2000.], legend_position="topright", numerator_legend="With online b-tag", denominator_legend="Without online b-tag", ratio_title="Online b-tag efficiency (no offline CSV)")

