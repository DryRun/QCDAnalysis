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
from root_plots import EfficiencyPlot
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
			# For trigjetht, have to cobble together the frankenhist later.
			if not (numerator_analysis == "trigjetht_eta1p7_CSVTM" or numerator_analysis == "trigjetht_eta2p2_CSVTM"):
				print "Numerator input file = " + analysis_config.get_b_histogram_filename(self._numerator_analysis, sample)
				self._input_files["numerator"][sample] = TFile(analysis_config.get_b_histogram_filename(self._numerator_analysis, sample))
			if not (denominator_analysis == "trigjetht_eta1p7" or denominator_analysis == "trigjetht_eta2p2"):
				print "Denominator input file = " + analysis_config.get_b_histogram_filename(self._denominator_analysis, sample)
				self._input_files["denominator"][sample] = TFile(analysis_config.get_b_histogram_filename(self._denominator_analysis, sample))

	# Separate plotting function for JetHT frankenhist
	def FrankenEfficiencyPlot(self, logy=True, binning=None, simple_rebin=None, save_tag="", x_range=None, ratio_range=None, legend_position="topright", numerator_legend=None, denominator_legend=None, ratio_title=None):
		ht_slices = ["HT200","HT250","HT300","HT350","HT400","HT450","HT500","HT550","HTUnprescaled"] # HT650
		if self._numerator_analysis == "trigjetht_eta1p7_CSVTM":
			numerator_analyses = {
				"HT200":"trigjetht200_eta1p7_CSVTM",
				"HT250":"trigjetht250_eta1p7_CSVTM",
				"HT300":"trigjetht300_eta1p7_CSVTM",
				"HT350":"trigjetht350_eta1p7_CSVTM",
				"HT400":"trigjetht400_eta1p7_CSVTM",
				"HT450":"trigjetht450_eta1p7_CSVTM",
				"HT500":"trigjetht500_eta1p7_CSVTM",
				"HT550":"trigjetht550_eta1p7_CSVTM",
				#"HT650":"trigjetht650_eta1p7_CSVTM",
				"HTUnprescaled":"trigjetht_eta1p7_CSVTM"
			}
		elif self._numerator_analysis == "trigjetht_eta2p2_CSVTM":
			numerator_analyses = {
				"HT200":"trigjetht200_CSVTM",
				"HT250":"trigjetht250_CSVTM",
				"HT300":"trigjetht300_CSVTM",
				"HT350":"trigjetht350_CSVTM",
				"HT400":"trigjetht400_CSVTM",
				"HT450":"trigjetht450_CSVTM",
				"HT500":"trigjetht500_CSVTM",
				"HT550":"trigjetht550_CSVTM",
				#"HT650":"trigjetht650_CSVTM",
				"HTUnprescaled":"trigjetht_CSVTM"
			}
		else:
			print "[OfflineBTagPlots::FrankenEfficiencyPlot] ERROR : numerator analysis must be trigjetht_eta1p7_CSVTM or trigjetht_eta2p2_CSVTM"
			sys.exit(1)
		if self._denominator_analysis == "trigjetht_eta1p7":
			denominator_analyses = {
				"HT200":"trigjetht200_eta1p7",
				"HT250":"trigjetht250_eta1p7",
				"HT300":"trigjetht300_eta1p7",
				"HT350":"trigjetht350_eta1p7",
				"HT400":"trigjetht400_eta1p7",
				"HT450":"trigjetht450_eta1p7",
				"HT500":"trigjetht500_eta1p7",
				"HT550":"trigjetht550_eta1p7",
				#"HT650":"trigjetht650_eta1p7",
				"HTUnprescaled":"trigjetht_eta1p7"
			}
		elif self._denominator_analysis == "trigjetht_eta2p2":
			denominator_analyses = {
				"HT200":"trigjetht200",
				"HT250":"trigjetht250",
				"HT300":"trigjetht300",
				"HT350":"trigjetht350",
				"HT400":"trigjetht400",
				"HT450":"trigjetht450",
				"HT500":"trigjetht500",
				"HT550":"trigjetht550",
				#"HT650":"trigjetht650",
				"HTUnprescaled":"trigjetht"
			}
		else:
			print "[OfflineBTagPlots::FrankenEfficiencyPlot] ERROR : denominator analysis must be trigjetht_eta1p7 or trigjetht_eta2p2"
			sys.exit(1)
		ht_ranges = {
			"HT200":[220, 386],
			"HT250":[386, 489],
			"HT300":[489, 526],
			"HT350":[526, 606],
			"HT400":[606, 649],
			"HT450":[649, 740],
			"HT500":[740, 788],
			"HT550":[788, 890],
			#"HT650":[890, 2000],
			"HTUnprescaled":[890, 2000]
		}
		numerator_histogram = None
		denominator_histogram = None
		for sample in self._samples:
			print "[EfficiencyPlot] DEBUG : Sample " + sample
			numerator_slice_histograms = {}
			denominator_slice_histograms = {}
			for slice_name in ht_slices:
				print slice_name
				print analysis_config.get_b_histogram_filename(numerator_analyses[slice_name], sample)
				numerator_file = TFile(analysis_config.get_b_histogram_filename(numerator_analyses[slice_name], sample), "READ")
				print analysis_config.get_b_histogram_filename(denominator_analyses[slice_name], sample)
				denominator_file = TFile(analysis_config.get_b_histogram_filename(denominator_analyses[slice_name], sample), "READ")

				# Check input nevents
				num_nevents = numerator_file.Get("BHistograms/h_input_nevents").Integral()
				den_nevents = denominator_file.Get("BHistograms/h_input_nevents").Integral()
				if num_nevents != den_nevents:
					# Allow tiny differences...?
					if abs((num_nevents - den_nevents) / den_nevents) < 0.001:
						print "[EfficiencyPlot] ERROR : Small inconsistency between number of events between numerator and denominator. I'm going to rescale away the difference, but you may want to fix this."
						numerator_normalization = den_nevents / num_nevents
						denominator_normalization = 1.
					else:
						print "[EfficiencyPlot] ERROR : Inconsistent number of events between numerator and denominator. Results would be wrong, so I'm aborting."
						print "[EfficiencyPlot] ERROR : \tNumerator = " + str(numerator_file.Get("BHistograms/h_input_nevents").Integral())
						print "[EfficiencyPlot] ERROR : \tDenominator = " + str(denominator_file.Get("BHistograms/h_input_nevents").Integral())
						sys.exit(1)
				else:
					numerator_normalization = 1.
					denominator_normalization = 1.
				numerator_slice_histograms[slice_name] = numerator_file.Get("BHistograms/h_pfjet_mjj")
				numerator_slice_histograms[slice_name].SetName("h_pfjet_mjj_num_" + slice_name + "_" + sample)
				numerator_slice_histograms[slice_name].SetDirectory(0)
				numerator_slice_histograms[slice_name].Scale(numerator_normalization)
				denominator_slice_histograms[slice_name] = denominator_file.Get("BHistograms/h_pfjet_mjj")
				denominator_slice_histograms[slice_name].SetName("h_pfjet_mjj_den_" + slice_name + "_" + sample)
				denominator_slice_histograms[slice_name].SetDirectory(0)
				denominator_slice_histograms[slice_name].Scale(denominator_normalization)
				numerator_file.Close()
				denominator_file.Close()
			# Make frankenhist
			this_numerator_histogram = self.FrankenHist(ht_slices, numerator_slice_histograms, ht_ranges)
			this_denominator_histogram = self.FrankenHist(ht_slices, denominator_slice_histograms, ht_ranges)
			if not numerator_histogram:
				numerator_histogram = this_numerator_histogram.Clone()
				numerator_histogram.SetName(numerator_histogram.GetName() + save_tag + "_num_" + str(time.time()))
				denominator_histogram = this_denominator_histogram.Clone()
				denominator_histogram.SetName(denominator_histogram.GetName() + save_tag + "_num_" + str(time.time()))
			else:
				numerator_histogram.Add(this_numerator_histogram)
				denominator_histogram.Add(this_denominator_histogram)

		# Rebin
		if binning:
			numerator_histogram = histogram_tools.rebin_histogram(numerator_histogram, binning)
			denominator_histogram = histogram_tools.rebin_histogram(denominator_histogram, binning)
		elif simple_rebin:
			numerator_histogram.Rebin(simple_rebin)
			denominator_histogram.Rebin(simple_rebin)


		cname = "c_offline_btag_eff_mjj"
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
				num_unnormalized = (numerator_histogram.GetBinContent(bin))**2 / (numerator_histogram.GetBinError(bin))**2
				den_unnormalized = (denominator_histogram.GetBinContent(bin))**2 / (denominator_histogram.GetBinError(bin))**2
				num = numerator_histogram.GetBinContent(bin)
				den = denominator_histogram.GetBinContent(bin)
				ratio = 1. * num_unnormalized / den_unnormalized 
				ratio_err = sqrt(ratio * (1. - ratio) / den_unnormalized)
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
		ratio_histogram.GetXaxis().SetTitle("m_{jj} [GeV]")
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

	def EfficiencyPlot(self, var="mjj", logy=True, binning=None, simple_rebin=None, save_tag="", sample_xsecs=None, x_range=None, ratio_range=None, legend_position="topright", numerator_legend=None, denominator_legend=None, ratio_title=None, prescaled=False, fit=False, fit_range=None):
		numerator_histogram = None
		denominator_histogram = None
		for sample in self._samples:
			if sample_xsecs:
				xsec = sample_xsecs[sample]
				numerator_normalization = 19710. * xsec / self._input_files["numerator"][sample].Get("BHistograms/h_sample_nevents").Integral()
				denominator_normalization = 19710. * xsec / self._input_files["denominator"][sample].Get("BHistograms/h_sample_nevents").Integral()
				if numerator_normalization != denominator_normalization:
					print "[EfficiencyPlot] WARNING : Numerator and denominator normalizations do not match! Continuing, but investigate this. Numerator nevents = " + str(self._input_files["numerator"][sample].Get("BHistograms/h_sample_nevents").Integral()) + ", denominator nevents = " + str(self._input_files["denominator"][sample].Get("BHistograms/h_sample_nevents").Integral())
			else:
				# Check input nevents
				if self._input_files["numerator"][sample].Get("BHistograms/h_sample_nevents"):
					num_nevents = self._input_files["numerator"][sample].Get("BHistograms/h_sample_nevents").Integral()
					den_nevents = self._input_files["denominator"][sample].Get("BHistograms/h_sample_nevents").Integral()
				else:
					num_nevents = self._input_files["numerator"][sample].Get("BHistograms/h_input_nevents").Integral()
					den_nevents = self._input_files["denominator"][sample].Get("BHistograms/h_input_nevents").Integral()
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
		numerator_histogram_fine = numerator_histogram.Clone()
		denominator_histogram_fine = denominator_histogram.Clone()
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
				if prescaled:
					num = (numerator_histogram.GetBinContent(bin))**2 / (numerator_histogram.GetBinError(bin))**2
					den = (denominator_histogram.GetBinContent(bin))**2 / (denominator_histogram.GetBinError(bin))**2
				else:
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


		# Fit the ratio
		if fit:
			# Make finely binned ratio
			#ratio_histogram_fine = numerator_histogram_fine.Clone()
			#ratio_histogram_fine.Reset()
			#if x_range:
			#	ratio_histogram_fine.GetXaxis().SetRangeUser(x_range[0], x_range[1])
			#ratio_histogram_fine.SetName(numerator_histogram_fine.GetName() + "_ratio_fine_" + save_tag + str(time.time()))
			#ratio_histogram_fine.SetDirectory(0)
			#for bin in xrange(1, numerator_histogram_fine.GetNbinsX() + 1):
			#	# Undo bin normalization
			#	if numerator_histogram_fine.GetBinError(bin) > 0 and denominator_histogram_fine.GetBinError(bin) > 0:
			#		if prescaled:
			#			num = (numerator_histogram_fine.GetBinContent(bin))**2 / (numerator_histogram_fine.GetBinError(bin))**2
			#			den = (denominator_histogram_fine.GetBinContent(bin))**2 / (denominator_histogram_fine.GetBinError(bin))**2
			#		else:
			#			num = numerator_histogram_fine.GetBinContent(bin)
			#			den = denominator_histogram_fine.GetBinContent(bin)
			#		ratio = 1. * num / den 
			#		ratio_err = sqrt(ratio * (1. - ratio) / den)
			#		#ratio_err = max(sqrt(ratio * (1. - ratio) / den), 1./den)
			#	else:
			#		ratio = 0.
			#		ratio_err = 0.
			#	ratio_histogram_fine.SetBinContent(bin, ratio)
			#	ratio_histogram_fine.SetBinError(bin, ratio_err)

			print "Fitting " + save_tag + " with some functions"
			fitter = TBinomialEfficiencyFitter(numerator_histogram, denominator_histogram)
			fits = {}
			print "\nFitting quadratic"
			fits["quadratic"] = TF1("quadratic", "[0]+[1]*x+[2]*x*x", fit_range[0], fit_range[1])
			fits["quadratic"].SetParameter(0, 0.01)
			fits["quadratic"].SetParameter(1, -1.e-5)
			fits["quadratic"].SetParLimits(1, -1.e5, 1.e5)
			fits["quadratic"].SetParameter(2, 1.e-11)
			fits["quadratic"].SetParLimits(2, -1.e5, 1.e5)
			ratio_histogram.Fit(fits["quadratic"], "R0")

			print "\nFitting quadexp"
			fits["quadexp"] = TF1("quadexp", "[0]+[1]*x+[2]*x*x+ [3]*exp([4]*x)", fit_range[0], fit_range[1])
			fits["quadexp"].SetParameter(0, 3.97724e-03)
			fits["quadexp"].SetParameter(1, -3.69019e-06)
			fits["quadexp"].SetParameter(2, 1.37598e-09)
			fits["quadexp"].SetParameter(3, 2.95236e+00)
			fits["quadexp"].SetParameter(4, -1.54774e-02)
			fitter.Fit(fits["quadexp"], "R0")

			print "\nFitting linexp"
			fits["linexp"] = TF1("linexp", "[0]+[1]*x + [2]*exp([3]*x)", fit_range[0], fit_range[1])
			fits["linexp"].SetParameter(0, 3.97724e-03)
			fits["linexp"].SetParameter(1, -3.69019e-06)
			fits["linexp"].SetParameter(2, 2.95236e+00)
			fits["linexp"].SetParameter(3, -1.54774e-02)
			fitter.Fit(fits["linexp"], "R0")

			# Print chi2/ndfs
			for fit_name, fit_function in fits.iteritems():
				print "chi^2/ndf (p) for " + fit_name + " = " + str(fit_function.GetChisquare()) + "/" + str(fit_function.GetNDF()) + " (" + str(TMath.Prob(fit_function.GetChisquare(), fit_function.GetNDF()))

			pull_histograms = {}
			for fit_name, fit_function in fits.iteritems():
				print "[debug] Making pull histogram for " + fit_name
				pull_histograms[fit_name] = ratio_histogram.Clone()
				pull_histograms[fit_name].SetDirectory(0)
				pull_histograms[fit_name].SetName("ratio_fit_pulls_" + fit_name)
				pull_histograms[fit_name].Reset()
				for bin in xrange(1, pull_histograms[fit_name].GetNbinsX() + 1):
					bin_center = pull_histograms[fit_name].GetXaxis().GetBinCenter(bin)
					if (bin_center < fit_range[0]) or (bin_center > fit_range[1]):
						#print "Pull hist : skipping bin with center " + str(bin_center)
						pull_histograms[fit_name].SetBinContent(bin, 0.)
					elif ratio_histogram.GetBinError(bin):
						#print "[debug] Bin " + str(bin) + " / pull = " + str(round(ratio_histogram.GetBinContent(bin), 2)) + "-" + str(round(fit_function.Eval(bin_center), 2)) +  "/" +  str(round(ratio_histogram.GetBinError(bin), 2)) + " = " + str(round((ratio_histogram.GetBinContent(bin) - fit_function.Eval(bin_center)) / ratio_histogram.GetBinError(bin), 2))
						pull_histograms[fit_name].SetBinContent(bin, (ratio_histogram.GetBinContent(bin) - fit_function.Eval(bin_center)) / ratio_histogram.GetBinError(bin))
					else:
						pull_histograms[fit_name].SetBinContent(bin, 0.)
			c_eff_fit = TCanvas("c_offline_btag_fit", "c_offline_btag_fit", 800, 1000)
			top_eff_fit = TPad("top_fit", "top_fit", 0., 0.5, 1., 1.)
			top_eff_fit.SetBottomMargin(0.02)
			top_eff_fit.Draw()
			top_eff_fit.cd()
			ratio_histogram.GetXaxis().SetTitleSize(0)
			ratio_histogram.GetXaxis().SetLabelSize(0)
			ratio_histogram.GetYaxis().SetTitle("Offline b-tag efficiency")
			ratio_histogram.Draw()
			fits["quadratic"].SetLineColor(seaborn.GetColorRoot("dark", 2))
			fits["quadratic"].SetLineWidth(2)
			pull_histograms["quadratic"].SetLineColor(seaborn.GetColorRoot("dark", 2))
			fits["quadratic"].Draw("same")
			fits["linexp"].SetLineColor(seaborn.GetColorRoot("dark", 4))
			pull_histograms["linexp"].SetLineColor(seaborn.GetColorRoot("dark", 4))
			fits["linexp"].SetLineWidth(2)
			fits["linexp"].Draw("same")
			l_eff_fit = TLegend(0.6, 0.6, 0.88, 0.8)
			l_eff_fit.SetBorderSize(0)
			l_eff_fit.SetFillColor(0)
			l_eff_fit.AddEntry(ratio_histogram, "Data", "pl")
			l_eff_fit.AddEntry(fits["quadratic"], "Fit (quadratic)", "l")
			l_eff_fit.AddEntry(fits["linexp"], "Fit (linear+exp)", "l")
			l_eff_fit.Draw()

			c_eff_fit.cd()
			bottom_eff_fit = TPad("bottom_fit", "bottom_fit", 0., 0., 1., 0.5)
			bottom_eff_fit.SetBottomMargin(0.2)
			bottom_eff_fit.SetTopMargin(0.02)
			bottom_eff_fit.Draw()
			bottom_eff_fit.cd()
			if fit_range[0] <= 296:
				default_fit = "quadratic"
			else:
				default_fit = "linexp"
			pull_histograms[default_fit].SetLineWidth(2)
			pull_histograms[default_fit].GetXaxis().SetTitle("m_{jj} [GeV]")
			pull_histograms[default_fit].GetYaxis().SetTitle
			if "mjj" in var:
				pull_histograms[default_fit].GetXaxis().SetTitle("m_{jj} [GeV]")
			elif "pt" in var:
				pull_histograms[default_fit].GetXaxis().SetTitle("p_{T} [GeV]")
			pull_histograms[default_fit].GetYaxis().SetTitle("(fit - data) / (#sigma(data))")
			pull_histograms[default_fit].SetMinimum(-10.)
			pull_histograms[default_fit].SetMaximum(10.)
			pull_histograms[default_fit].Draw("hist")

			#pull_histograms["quadratic"].SetLineWidth(2)
			#pull_histograms["quadratic"].SetLineColor(seaborn.GetColorRoot("dark", 2))
			#pull_histograms["quadratic"].Draw("hist same")

			c_eff_fit.cd()
			c_eff_fit.SaveAs(analysis_config.figure_directory + "/OfflineBTag/" + c_eff_fit.GetName() + save_tag + ".pdf")
			
			ROOT.SetOwnership(c_eff_fit, False)
			ROOT.SetOwnership(top_eff_fit, False)
			ROOT.SetOwnership(bottom_eff_fit, False)



	# Cobble together m(jj) histogram from several JetHT triggers. 
	def FrankenHist(self, HT_slices, histograms, ranges):
		frankenhist = histograms[HT_slices[0]].Clone()
		frankenhist.SetDirectory(0)
		frankenhist.Sumw2()
		frankenhist.Reset()
		for bin in xrange(1, frankenhist.GetNbinsX() + 1):
			x = frankenhist.GetXaxis().GetBinCenter(bin)
			# Find range
			for HT_slice in HT_slices:
				if x > ranges[HT_slice][0] and x < ranges[HT_slice][1]:
					frankenhist.SetBinContent(bin, histograms[HT_slice].GetBinContent(bin))
					frankenhist.SetBinError(bin, histograms[HT_slice].GetBinError(bin))
					break
		return frankenhist

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description = 'Offline b-tag efficiency measurement, plots, etc')
	parser.add_argument('--do_signal', action='store_true', help='Make plot of offline b-tagging efficiency in signal MC')
	parser.add_argument('--do_qcd', action='store_true', help='Make plot of offline b-tagging efficiency in QCD MC')
	parser.add_argument('--do_singlemu', action='store_true', help='Make plot of offline b-tagging efficiency in SingleMu24i data')
	parser.add_argument('--do_singlejet', action='store_true', help='Make efficiency plot from single b-tag efficiencies')
	parser.add_argument('--do_jetht', action='store_true', help='Make plot of offline b-tagging efficiency in JetHT data')
	args = parser.parse_args()
	#do_signal = False
	#do_qcd = False
	#do_singlemu = False
	#do_jetht = True
	dijet_binning = array("d", [1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325, 354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 4509, 4686, 4869, 5000])

	wp = "CSVTM"

	if args.do_signal:
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

	if args.do_qcd:
		QCD_samples = ["QCD_Pt-80to120_TuneZ2star_8TeV_pythia6","QCD_Pt-120to170_TuneZ2star_8TeV_pythia6","QCD_Pt-170to300_TuneZ2star_8TeV_pythia6","QCD_Pt-300to470_TuneZ2star_8TeV_pythia6","QCD_Pt-470to600_TuneZ2star_8TeV_pythia6","QCD_Pt-600to800_TuneZ2star_8TeV_pythia6","QCD_Pt-800to1000_TuneZ2star_8TeV_pythia6","QCD_Pt-1000to1400_TuneZ2star_8TeV_pythia6","QCD_Pt-1400to1800_TuneZ2star_8TeV_pythia6","QCD_Pt-1800_TuneZ2star_8TeV_pythia6"]
		for sr in ["lowmass", "highmass"]:
			if sr == "lowmass":
				numerator_analysis = "NoTrigger_eta1p7_" + wp
				denominator_analysis = "NoTrigger_eta1p7"
				fit_range = [296,1058]
			elif sr == "highmass":
				numerator_analysis = "NoTrigger_eta2p2_" + wp
				denominator_analysis = "NoTrigger_eta2p2"
				fit_range=[419,1607]
			plotter = OfflineBTagPlots(numerator_analysis, denominator_analysis, QCD_samples)
			plotter.EfficiencyPlot(var="mjj", logy=True, binning=dijet_binning, save_tag="_" + wp + "_" + sr + "_qcd", ratio_range=[0.,5.e-3], x_range=[0., 2000.], legend_position="bottomright", fit=True, fit_range=fit_range)
			plotter.EfficiencyPlot(var="pt_btag1", logy=True, simple_rebin=5, save_tag="_" + wp + "_" + sr + "_qcd", ratio_range=[0.,5.e-3], x_range=[0., 1000.], legend_position="bottomright")
			plotter.EfficiencyPlot(var="pt_btag2", logy=True, simple_rebin=5, save_tag="_" + wp + "_" + sr + "_qcd", ratio_range=[0.,5.e-3], x_range=[0., 1000.], legend_position="bottomright")
			#plotter.EfficiencyPlot(var="mjj", logy=True, binning=dijet_binning, save_tag="_" + wp + "_" + sr + "_qcd_norm", ratio_range=[0.,5.e-3], x_range=[0., 2000.], legend_position="bottomright", sample_xsecs=analysis_config.simulation.background_cross_sections, fit=True, fit_range=fit_range, prescaled=True)

	if args.do_singlemu:
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

	if args.do_jetht:
		for sr in ["lowmass", "highmass"]:
			if sr == "lowmass":
				numerator_analysis = "trigjetht_eta1p7_CSVTM"
				denominator_analysis = "trigjetht_eta1p7"
			else:
				numerator_analysis = "trigjetht_eta2p2_CSVTM"
				denominator_analysis = "trigjetht_eta2p2"
			plotter = OfflineBTagPlots(numerator_analysis, denominator_analysis, ["JetHT_2012BCD"])
			plotter.FrankenEfficiencyPlot(logy=True, binning=dijet_binning, save_tag="_JetHT_CSVTM_" + sr, ratio_range=[0.,0.01], x_range=[0., 2000.], legend_position="topright", numerator_legend="With offline b-tag", denominator_legend="Without offline b-tag", ratio_title="Offline b-tag efficiency)")

		#for ht_slice in [200, 250, 300, 350, 400, 450, 500, 550, 650]:
		#	if sr == "lowmass":
		#		numerator_analysis = "trigjetht" + str(ht_slice) + "_eta1p7_CSVTM"
		#		denominator_analysis = "trigjetht" + str(ht_slice) + "_eta1p7"
		#	else:
		#		numerator_analysis = "trigjetht" + str(ht_slice) + "_CSVTM"
		#		denominator_analysis = "trigjetht" + str(ht_slice)

		#	plotter = OfflineBTagPlots(numerator_analysis, denominator_analysis, ["JetHT_2012BCD"])
		#	plotter.EfficiencyPlot(var="mjj", logy=True, binning=dijet_binning, save_tag="_CSVTM_" + sr + "_jetht" + str(ht_slice), ratio_range=[0.,0.01], x_range=[0., 2000.], legend_position="topright", numerator_legend="With offline b-tag", denominator_legend="Without offline b-tag", ratio_title="Offline b-tag efficiency", prescaled=True)

	if args.do_singlejet:
		for analysis in ["trigbbl_CSVTM", "trigbbh_CSVTM"]:
			f = TFile(analysis_config.get_b_histogram_filename(analysis, "BJetPlusX_2012"), "READ")
			h_mjj = histogram_tools.rebin_histogram(f.Get("BHistograms/h_pfjet_mjj"), dijet_binning)
			h_mjj_btagcorr = histogram_tools.rebin_histogram(f.Get("BHistograms/h_pfjet_mjj_btagcorr"), dijet_binning)
			EfficiencyPlot(h_mjj, h_mjj_btagcorr, name_num="No correction", name_den="b tag correction", logy=True, save_directory=analysis_config.figure_directory + "/OfflineBTag", save_tag="from_singlejet_"+analysis)