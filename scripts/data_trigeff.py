import os
import sys
import array
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

class TrigEffPlotter():
	def __init__(self):
		self._analyses = []
		self._efficiency_combinations = {}
		self._mjj_histograms = {}
		self._mjj_histograms_csvorder = {}
		self._mjj_histograms_vetothirdjet = {}
		self._efficiency_histograms = {}
		self._efficiency_histograms_csvorder = {}
		self._efficiency_histograms_vetothirdjet = {}
		self._mjj_histograms_fine = {}
		self._efficiency_histograms_fine = {}
		self._mass_bins = array.array("d", [1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325, 354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 4509, 4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808, 7060, 7320, 7589, 7866, 8000])
		self.GetJetHTHistogram()
		self.GetSingleMuHistograms()
		self.GetBJetPlusXHistograms()
		self.MakeEfficiencyHistograms()
		self.FitEfficiencies()

	def GetJetHTHistogram(self):
		for sr_name in ["highmass", "lowmass"]:
			analyses = {}
			HT_slices = []
			for mass in xrange(200, 600, 50):
				HT_slices.append("HT" + str(mass))
				analyses["HT" + str(mass)] = "trigjetht" + str(mass)
				if sr_name == "lowmass":
					analyses["HT" + str(mass)] += "_eta1p7"
				analyses["HT" + str(mass)] += "_CSVTM"
			sample = "JetHT_2012BCD"
			HT_slice_histograms = {}
			for HT_slice in HT_slices:
				f = TFile(analysis_config.get_b_histogram_filename(analyses[HT_slice], sample), "READ")
				HT_slice_histograms[HT_slice] = f.Get("BHistograms/h_pfjet_mjj")
				HT_slice_histograms[HT_slice].SetName(HT_slice_histograms[HT_slice].GetName() + "_" + analyses[HT_slice])
				HT_slice_histograms[HT_slice].SetDirectory(0)
				f.Close()
			HT_slices.append("HTUnprescaled")
			unprescaled_analysis_name = "trigjetht"
			if sr_name == "lowmass":
				unprescaled_analysis_name += "_eta1p7"
			unprescaled_analysis_name += "_CSVTM"
			analyses["HTUnprescaled"] = unprescaled_analysis_name
			f_unprescaled = TFile(analysis_config.get_b_histogram_filename(unprescaled_analysis_name, sample), "READ")
			HT_slice_histograms["HTUnprescaled"] = f_unprescaled.Get("BHistograms/h_pfjet_mjj")
			HT_slice_histograms["HTUnprescaled"].SetName(HT_slice_histograms["HTUnprescaled"].GetName() + "_" + analyses["HTUnprescaled"])
			HT_slice_histograms["HTUnprescaled"].SetDirectory(0)
			f_unprescaled.Close()
			ranges = {
				"HT200":[220, 386],
				"HT250":[386, 489],
				"HT300":[489, 526],
				"HT350":[526, 606],
				"HT400":[606, 649],
				"HT450":[649, 740],
				"HT500":[740, 788],
				"HT550":[788, 890],
				#"HT650":[800, 890],
				"HTUnprescaled":[890, 2000]
			}

			self._analyses.append("JetHT")
			print "[GetJetHTHistogram] DEBUG : Making frankenhist"
			self._mjj_histograms_fine["JetHT"] = self.FrankenHist(HT_slices, HT_slice_histograms, ranges)
			print "[GetJetHTHistogram] DEBUG : Integral = " + str(self._mjj_histograms_fine["JetHT"].Integral())
			self._mjj_histograms["JetHT"] = histogram_tools.rebin_histogram(self._mjj_histograms_fine["JetHT"], self._mass_bins, normalization_bin_width=1)


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

	def GetSingleMuHistograms(self):
		this_analyses = ["trigmu_highmass_CSVTM", "trigmu_lowmass_CSVTM", "trigmubbh_highmass_CSVTM", "trigmubbl_lowmass_CSVTM", "trigmubbll_lowmass_CSVTM", "trigmu24i_lowmass_CSVTM", "trigmu24ibbl_lowmass_CSVTM", "trigmu24ibbll_lowmass_CSVTM", "trigmu40_lowmass_CSVTM", "trigmu40bbl_lowmass_CSVTM", "trigmu40bbll_lowmass_CSVTM"]
		this_analyses.extend(["trigmu24i_highmass_CSVTM", "trigmu24ibbh_highmass_CSVTM"])
		for analysis in this_analyses:
			print "Opening " + analysis_config.get_b_histogram_filename(analysis, "SingleMu_2012")
			f = ROOT.TFile(analysis_config.get_b_histogram_filename(analysis, "SingleMu_2012"), "READ")
			self._mjj_histograms_fine[analysis] = f.Get("BHistograms/h_pfjet_mjj")
			self._mjj_histograms_fine[analysis].SetName("h_" + analysis + "_mjj_fine")
			self._mjj_histograms_fine[analysis].SetDirectory(0)
			self._mjj_histograms[analysis] = histogram_tools.rebin_histogram(self._mjj_histograms_fine[analysis], self._mass_bins, normalization_bin_width=1)
			self._mjj_histograms[analysis].SetName("h_" + analysis + "_mjj")
			self._mjj_histograms[analysis].SetDirectory(0)

			if not "highmass" in analysis:
				self._mjj_histograms_csvorder[analysis] = f.Get("BHistograms/h_pfjet_mjj_csvorder")
				self._mjj_histograms_csvorder[analysis].SetName("h_" + analysis + "_mjj_csvorder")
				self._mjj_histograms_csvorder[analysis].SetDirectory(0)
				self._mjj_histograms_csvorder[analysis] = histogram_tools.rebin_histogram(self._mjj_histograms_csvorder[analysis], self._mass_bins, normalization_bin_width=1)

				self._mjj_histograms_vetothirdjet[analysis] = f.Get("BHistograms/h_pfjet_mjj_vetothirdjet")
				self._mjj_histograms_vetothirdjet[analysis].SetName("h_" + analysis + "_mjj_vetothirdjet")
				self._mjj_histograms_vetothirdjet[analysis].SetDirectory(0)
				self._mjj_histograms_vetothirdjet[analysis] = histogram_tools.rebin_histogram(self._mjj_histograms_vetothirdjet[analysis], self._mass_bins, normalization_bin_width=1)

			if "bbll" in analysis:
				self._mjj_histograms_fine[analysis].Scale(1.7) # Prescale for singlemu + 60/53. The prescale was not computer for these analyses.
				self._mjj_histograms[analysis].Scale(1.7) # Prescale for singlemu + 60/53. The prescale was not computer for these analyses.
			self._analyses.append(analysis)
			f.Close()


	def GetBJetPlusXHistograms(self):
		this_analyses = ["trigbbh_CSVTM", "trigbbl_CSVTM", "trigbbll_CSVTM"]
		this_samples = ["BJetPlusX_2012", "BJetPlusX_2012BCD"]
		for analysis in this_analyses:
			for sample in this_samples:
				name = analysis + "_" + sample
				f = ROOT.TFile(analysis_config.get_b_histogram_filename(analysis, sample), "READ")
				self._mjj_histograms_fine[name] = f.Get("BHistograms/h_pfjet_mjj")
				self._mjj_histograms_fine[name].SetName("h_" + name + "_mjj_fine")
				self._mjj_histograms_fine[name].SetDirectory(0)
				self._mjj_histograms[name] = histogram_tools.rebin_histogram(self._mjj_histograms_fine[name], self._mass_bins, normalization_bin_width=1)
				self._mjj_histograms[name].SetName("h_" + name + "_mjj")
				self._mjj_histograms[name].SetDirectory(0)
				self._mjj_histograms_csvorder[name] = f.Get("BHistograms/h_pfjet_mjj_csvorder")
				self._mjj_histograms_csvorder[name].SetName("h_" + name + "_mjj_csvorder")
				self._mjj_histograms_csvorder[name].SetDirectory(0)
				self._mjj_histograms_csvorder[name] = histogram_tools.rebin_histogram(self._mjj_histograms_csvorder[name], self._mass_bins, normalization_bin_width=1)
				self._mjj_histograms_vetothirdjet[name] = f.Get("BHistograms/h_pfjet_mjj_vetothirdjet")
				self._mjj_histograms_vetothirdjet[name].SetName("h_" + name + "_mjj_vetothirdjet")
				self._mjj_histograms_vetothirdjet[name].SetDirectory(0)
				self._mjj_histograms_vetothirdjet[name] = histogram_tools.rebin_histogram(self._mjj_histograms_vetothirdjet[name], self._mass_bins, normalization_bin_width=1)
				self._analyses.append(name)
				f.Close()

	def MakeEfficiencyHistograms(self):
		self._efficiency_combinations.update({
			"JetHT_highmass":["trigbbh_CSVTM_BJetPlusX_2012BCD", "JetHT"],
			"JetHT_lowmass":["trigbbl_CSVTM_BJetPlusX_2012BCD", "JetHT"], 
			"JetHT_llowmass":["trigbbll_CSVTM_BJetPlusX_2012BCD", "JetHT"],
			#"SingleMu_highmass":["trigmubbh_highmass_CSVTM", "trigmu_highmass_CSVTM"], 
			#"SingleMu_lowmass":["trigmubbl_lowmass_CSVTM", "trigmu_lowmass_CSVTM"], 
			#"SingleMu_llowmass":["trigmubbll_lowmass_CSVTM", "trigmu_lowmass_CSVTM"], 
			"SingleMu24i_highmass":["trigmu24ibbh_highmass_CSVTM", "trigmu24i_highmass_CSVTM"], 
			"SingleMu24i_lowmass":["trigmu24ibbl_lowmass_CSVTM", "trigmu24i_lowmass_CSVTM"], 
			#"SingleMu24i_llowmass":["trigmu24ibbll_lowmass_CSVTM", "trigmu24i_lowmass_CSVTM"], 
			#"SingleMu40_highmass":["trigmu40bbh_highmass_CSVTM", "trigmu40_highmass_CSVTM"], 
			#"SingleMu40_lowmass":["trigmu40bbl_lowmass_CSVTM", "trigmu40_lowmass_CSVTM"], 
			#"SingleMu40_llowmass":["trigmu40bbll_lowmass_CSVTM", "trigmu40_lowmass_CSVTM"], 
			"BJet60_53_lowmass":["trigbbl_CSVTM_BJetPlusX_2012", "trigbbll_CSVTM_BJetPlusX_2012"], 
			"BJet80_70_highmass":["trigbbh_CSVTM_BJetPlusX_2012", "trigbbl_CSVTM_BJetPlusX_2012"], 
			})
		self._legend_entries = {
			"trigbbh_CSVTM":"160/120 + b-tag",
			"trigbbl_CSVTM":"80/70 + b-tag",
			"trigbbll_CSVTM":"60/53 + b-tag",
			"trigbbh_CSVTM_BJetPlusX_2012":"160/120 + b-tag",
			"trigbbl_CSVTM_BJetPlusX_2012":"80/70 + b-tag",
			"trigbbll_CSVTM_BJetPlusX_2012":"60/53 + b-tag",
			"trigbbh_CSVTM_BJetPlusX_2012BCD":"160/120 + b-tag",
			"trigbbl_CSVTM_BJetPlusX_2012BCD":"80/70 + b-tag",
			"trigbbll_CSVTM_BJetPlusX_2012BCD":"60/53 + b-tag",
			"trigmu_highmass_CSVTM":"mu24i||mu40",
			"trigmu_lowmass_CSVTM":"mu24i||mu40",
			"trigmubbh_highmass_CSVTM":"(mu24i||mu40)&&(160/120+b-tag)",
			"trigmubbl_lowmass_CSVTM":"(mu24i||mu40)&&(80/70+b-tag)",
			"trigmubbll_lowmass_CSVTM":"(mu24i||mu40)&&(60/53+b-tag)", 
			"trigmu24ibbh_highmass_CSVTM":"(mu24i)&&(160/120+b-tag)",
			"trigmu24ibbl_lowmass_CSVTM":"(mu24i)&&(80/70+b-tag)",
			"trigmu24ibbll_lowmass_CSVTM":"(mu24i)&&(60/53+b-tag)", 
			"trigmu40bbh_highmass_CSVTM":"(mu40)&&(160/120+b-tag)",
			"trigmu40bbl_lowmass_CSVTM":"(mu40)&&(80/70+b-tag)",
			"trigmu40bbll_lowmass_CSVTM":"(mu40)&&(60/53+b-tag)", 
			"JetHT":"JetHT"
		}
		self._efficiency_guesses = {
				"JetHT_highmass":0.4,
				"JetHT_lowmass":0.2,
				"JetHT_llowmass":0.1,
				"SingleMu_highmass":0.2,
				"SingleMu_lowmass":0.1,
				"SingleMu_llowmass":0.05,
				"SingleMu24i_highmass":0.2,
				"SingleMu24i_lowmass":0.1,
				"SingleMu24i_llowmass":0.05,
				"SingleMu40_highmass":0.2,
				"SingleMu40_lowmass":0.1,
				"SingleMu40_llowmass":0.05,
				"BJet60_53_lowmass":1,
				"BJet80_70_highmass":1,
		}
		self._colors = {
			"JetHT_highmass":seaborn.GetColorRoot("default", 0),
			"JetHT_lowmass":seaborn.GetColorRoot("default", 1),
			"JetHT_llowmass":seaborn.GetColorRoot("default", 2),
			"SingleMu_highmass":seaborn.GetColorRoot("default", 3),
			"SingleMu_lowmass":seaborn.GetColorRoot("default", 3),
			"SingleMu_llowmass":seaborn.GetColorRoot("default", 5),
			"SingleMu24i_highmass":seaborn.GetColorRoot("pastel", 3),
			"SingleMu24i_lowmass":seaborn.GetColorRoot("pastel", 3),
			"SingleMu24i_llowmass":seaborn.GetColorRoot("pastel", 5),
			"SingleMu40_highmass":seaborn.GetColorRoot("dark", 3),
			"SingleMu40_lowmass":seaborn.GetColorRoot("dark", 3),
			"SingleMu40_llowmass":seaborn.GetColorRoot("dark", 5),
			"BJet60_53_lowmass":seaborn.GetColorRoot("cubehelix", 0, 20),
			"BJet80_70_highmass":seaborn.GetColorRoot("cubehelix", 10, 20),
		}
		self._line_styles = {
			"JetHT_highmass":1,
			"JetHT_lowmass":1,
			"JetHT_llowmass":1,
			"SingleMu_highmass":1,
			"SingleMu_lowmass":1,
			"SingleMu_llowmass":1,
			"SingleMu24i_highmass":2,
			"SingleMu24i_lowmass":2,
			"SingleMu24i_llowmass":2,
			"SingleMu40_highmass":3,
			"SingleMu40_lowmass":3,
			"SingleMu40_llowmass":3,
			"BJet60_53_lowmass":1,
			"BJet80_70_highmass":1,
		}
		for efficiency_name, hist_pair in self._efficiency_combinations.iteritems():
			print "[MakeEfficiencyHistograms] INFO : Making efficiency histogram " + efficiency_name
			print "[MakeEfficiencyHistograms] INFO : \tNumerator (" + hist_pair[0] + ") integral = " + str(self._mjj_histograms[hist_pair[0]].Integral())
			print "[MakeEfficiencyHistograms] INFO : \tDenominator (" + hist_pair[1] + ") integral = " + str(self._mjj_histograms[hist_pair[1]].Integral())
			self._efficiency_histograms[efficiency_name] = self._mjj_histograms[hist_pair[0]].Clone()
			self._efficiency_histograms[efficiency_name].SetName("h_efficiency_" + efficiency_name)
			self._efficiency_histograms[efficiency_name].SetDirectory(0)

			if "JetHT" in efficiency_name:# or efficiency_name == "BJet80_70_highmass": This is inappropriate, I think. 80/70 - 160/120 don't have the same correlations.
				self._efficiency_histograms[efficiency_name].Divide(self._mjj_histograms[hist_pair[1]])
				# Set the histogram errors to N/n * sqrt((N+n(x-2))/(nN)), where x is the prescale
				for bin in xrange(1, self._efficiency_histograms[efficiency_name].GetNbinsX() + 1):
					bin_width = self._efficiency_histograms[efficiency_name].GetXaxis().GetBinWidth(bin)
					n = self._mjj_histograms[hist_pair[0]].GetBinContent(bin) * bin_width
					N = self._mjj_histograms[hist_pair[1]].GetBinContent(bin) * bin_width
					print "n = " + str(n) + " / N = " + str(N) + " / dN = " + str(self._mjj_histograms[hist_pair[1]].GetBinError(bin) * bin_width)
					if N == 0:
						continue
					x = 1. * (self._mjj_histograms[hist_pair[1]].GetBinError(bin) * bin_width)**2 / N
					print "Bin center = " + str(self._efficiency_histograms[efficiency_name].GetXaxis().GetBinCenter(bin)) + " / x=" + str(x)
					if x == 0 or n == 0:
						continue
					err = n / N * sqrt((N + n * (x - 2)) / (n * N))
					self._efficiency_histograms[efficiency_name].SetBinError(bin, err)
			else:
				self._efficiency_histograms[efficiency_name].Divide(self._mjj_histograms[hist_pair[0]], self._mjj_histograms[hist_pair[1]], 1, 1, "B")
			self._efficiency_histograms[efficiency_name].SetMarkerStyle(20)
			self._efficiency_histograms[efficiency_name].SetMarkerSize(1)
			self._efficiency_histograms[efficiency_name].SetMarkerColor(self._colors[efficiency_name])
			self._efficiency_histograms[efficiency_name].SetLineWidth(2)
			self._efficiency_histograms[efficiency_name].SetLineStyle(self._line_styles[efficiency_name])
			self._efficiency_histograms[efficiency_name].SetLineColor(self._colors[efficiency_name])

			self._mjj_histograms[hist_pair[0]].SetMarkerStyle(24)
			self._mjj_histograms[hist_pair[0]].SetMarkerColor(self._colors[efficiency_name])
			self._mjj_histograms[hist_pair[1]].SetMarkerStyle(20)
			self._mjj_histograms[hist_pair[1]].SetMarkerColor(self._colors[efficiency_name])

			# Finely binned
			self._efficiency_histograms_fine[efficiency_name] = self._mjj_histograms_fine[hist_pair[0]].Clone()
			self._efficiency_histograms_fine[efficiency_name].SetName("h_efficiency_" + efficiency_name)
			self._efficiency_histograms_fine[efficiency_name].SetDirectory(0)
			if "JetHT" in efficiency_name or efficiency_name == "BJet80_70_highmass":
				self._efficiency_histograms_fine[efficiency_name].Divide(self._mjj_histograms_fine[hist_pair[1]])
			else:
				self._efficiency_histograms_fine[efficiency_name].Divide(self._mjj_histograms_fine[hist_pair[0]], self._mjj_histograms_fine[hist_pair[1]], 1, 1, "B")
			self._efficiency_histograms_fine[efficiency_name].SetMarkerStyle(20)
			self._efficiency_histograms_fine[efficiency_name].SetMarkerSize(1)
			self._efficiency_histograms_fine[efficiency_name].SetMarkerColor(self._colors[efficiency_name])
			self._efficiency_histograms_fine[efficiency_name].SetLineWidth(2)
			self._efficiency_histograms_fine[efficiency_name].SetLineStyle(self._line_styles[efficiency_name])
			self._efficiency_histograms_fine[efficiency_name].SetLineColor(self._colors[efficiency_name])

			self._mjj_histograms_fine[hist_pair[0]].SetMarkerStyle(24)
			self._mjj_histograms_fine[hist_pair[0]].SetMarkerColor(self._colors[efficiency_name])
			self._mjj_histograms_fine[hist_pair[1]].SetMarkerStyle(20)
			self._mjj_histograms_fine[hist_pair[1]].SetMarkerColor(self._colors[efficiency_name])


			# Variations with no 3rd jet or CSV ordering
			if self._mjj_histograms_csvorder.has_key(hist_pair[0]) and self._mjj_histograms_csvorder.has_key(hist_pair[1]):
				self._efficiency_histograms_csvorder[efficiency_name] = self._mjj_histograms[hist_pair[0]].Clone()
				self._efficiency_histograms_csvorder[efficiency_name].SetName("h_efficiency_" + efficiency_name + "_csvorder")
				self._efficiency_histograms_csvorder[efficiency_name].SetDirectory(0)
				if "JetHT" in efficiency_name:
					self._efficiency_histograms_csvorder[efficiency_name].Divide(self._mjj_histograms[hist_pair[1]])
				else:
					self._efficiency_histograms_csvorder[efficiency_name].Divide(self._mjj_histograms[hist_pair[0]], self._mjj_histograms[hist_pair[1]], 1, 1, "B")
				self._efficiency_histograms_csvorder[efficiency_name].SetMarkerStyle(21)
				self._efficiency_histograms_csvorder[efficiency_name].SetMarkerSize(1)
				self._efficiency_histograms_csvorder[efficiency_name].SetMarkerColor(self._colors[efficiency_name])
				self._efficiency_histograms_csvorder[efficiency_name].SetLineWidth(2)
				self._efficiency_histograms_csvorder[efficiency_name].SetLineStyle(self._line_styles[efficiency_name])
				self._efficiency_histograms_csvorder[efficiency_name].SetLineColor(self._colors[efficiency_name])

				self._mjj_histograms_csvorder[hist_pair[0]].SetMarkerStyle(25)
				self._mjj_histograms_csvorder[hist_pair[0]].SetMarkerColor(self._colors[efficiency_name])
				self._mjj_histograms_csvorder[hist_pair[1]].SetMarkerStyle(20)
				self._mjj_histograms_csvorder[hist_pair[1]].SetMarkerColor(self._colors[efficiency_name])

			if self._mjj_histograms_vetothirdjet.has_key(hist_pair[0]) and self._mjj_histograms_vetothirdjet.has_key(hist_pair[1]):
				self._efficiency_histograms_vetothirdjet[efficiency_name] = self._mjj_histograms_vetothirdjet[hist_pair[0]].Clone()
				self._efficiency_histograms_vetothirdjet[efficiency_name].SetName("h_efficiency_" + efficiency_name + "_vetothirdjet")
				self._efficiency_histograms_vetothirdjet[efficiency_name].SetDirectory(0)
				if "JetHT" in efficiency_name:
					self._efficiency_histograms_vetothirdjet[efficiency_name].Divide(self._mjj_histograms_vetothirdjet[hist_pair[1]])
				else:
					self._efficiency_histograms_vetothirdjet[efficiency_name].Divide(self._mjj_histograms_vetothirdjet[hist_pair[0]], self._mjj_histograms_vetothirdjet[hist_pair[1]], 1, 1, "B")
				self._efficiency_histograms_vetothirdjet[efficiency_name].SetMarkerStyle(22)
				self._efficiency_histograms_vetothirdjet[efficiency_name].SetMarkerSize(1)
				self._efficiency_histograms_vetothirdjet[efficiency_name].SetMarkerColor(self._colors[efficiency_name])
				self._efficiency_histograms_vetothirdjet[efficiency_name].SetLineWidth(2)
				self._efficiency_histograms_vetothirdjet[efficiency_name].SetLineStyle(self._line_styles[efficiency_name])
				self._efficiency_histograms_vetothirdjet[efficiency_name].SetLineColor(self._colors[efficiency_name])

				self._mjj_histograms_vetothirdjet[hist_pair[0]].SetMarkerStyle(26)
				self._mjj_histograms_vetothirdjet[hist_pair[0]].SetMarkerColor(self._colors[efficiency_name])
				self._mjj_histograms_vetothirdjet[hist_pair[1]].SetMarkerStyle(20)
				self._mjj_histograms_vetothirdjet[hist_pair[1]].SetMarkerColor(self._colors[efficiency_name])

	def FitEfficiencies(self):
		self._efficiency_fits = {}
		self._fit_ranges = {}
		self._fit_chi2s = {}
		self._fit_ndfs = {}

		# Fit JetHT with constant first, to get online b-tag efficiencies
		# - Use coarse histograms.
		for name, hist in self._efficiency_histograms.iteritems():
			if "JetHT" in name:
				print "Fitting " + name					
				if "highmass" in name:
					self._fit_ranges[name] = [526, 1607]
				elif "lowmass" in name:
					self._fit_ranges[name] = [386, 1246]
				self._efficiency_fits[name] = ROOT.TF1("linear_" + name, "[0]", self._fit_ranges[name][0], self._fit_ranges[name][1])
				self._efficiency_fits[name].SetLineColor(self._colors[name])
				if "lowmass" in name:
					self._efficiency_fits[name].SetParameter(0, 0.2)
				elif "highmass" in name:
					self._efficiency_fits[name].SetParameter(0, 0.5)
				hist.Fit(self._efficiency_fits[name], "R0")

		# Fit SingleMu and BJetPlusX with sigmoid functions
		for name, hist in self._efficiency_histograms_fine.iteritems():
			if "SingleMu" in name or "BJet" in name:
				print "Fitting " + name
				if "highmass" in name:
					self._fit_ranges[name] = [354, 1607]
				elif "llowmass" in name:
					self._fit_ranges[name] = [197, 526]
				elif "lowmass" in name:
					self._fit_ranges[name] = [197, 526]

				self._efficiency_fits[name] = ROOT.TF1("sigmoid_" + name, "[2] * (1. / (1. + TMath::Exp(-1. * (x - [0]) / [1])))", self._fit_ranges[name][0], self._fit_ranges[name][1])
				self._efficiency_fits[name].SetLineColor(self._colors[name])
				self._efficiency_fits[name].SetParameter(0, 200.)
				if "lowmass" in name:
					self._efficiency_fits[name].SetParLimits(0, 0., 400.)
				elif "highmass" in name:
					self._efficiency_fits[name].SetParLimits(0, 0., 1000.)
				self._efficiency_fits[name].SetParameter(1, 100.)
				if "SingleMu" in name:
					self._efficiency_fits[name].SetParameter(2, 0.2)
				elif name == "BJet60_53_lowmass":
					self._efficiency_fits[name].SetParameter(2, 1.)
				elif name == "BJet80_70_highmass":
					self._efficiency_fits[name].SetParameter(2, 3.)
	
				fit_result = hist.Fit(self._efficiency_fits[name], "R0S")
				self._fit_chi2s[name] = self._efficiency_fits[name].GetChisquare()
				self._fit_ndfs[name] = self._efficiency_fits[name].GetNDF()
				fit_result.Print("V")

	def MakeSingleMuComparisons(self):
		for sr_name in ["lowmass", "llowmass"]:
			c = TCanvas("c_trigeff_SingleMu_comparison_" + sr_name)
			l = TLegend(0.7, 0.7, 0.88, 0.88)
			l.SetFillColor(0)
			l.SetBorderSize(0)
			frame = TH1F("frame_" + sr_name, "frame_" + sr_name, 100, 0., 1800.)
			frame.SetMinimum(0.)
			frame.SetMaximum(self._efficiency_guesses["SingleMu_" + sr_name] * 3.)
			frame.GetXaxis().SetTitle("m_{jj} [GeV]")
			frame.GetYaxis().SetTitle("Efficiency")
			frame.Draw()
			for mu_name in ["SingleMu", "SingleMu24i", "SingleMu40"]:
				self._efficiency_histograms[mu_name + "_" + sr_name].Draw("same")
				l.AddEntry(self._efficiency_histograms[mu_name + "_" + sr_name], mu_name, "lp")
				if self._efficiency_histograms_csvorder.has_key(mu_name + "_" + sr_name):
					self._efficiency_histograms_csvorder[mu_name + "_" + sr_name].Draw("same")
					l.AddEntry(self._efficiency_histograms_csvorder[mu_name + "_" + sr_name], mu_name + "/CSV", "lp")
				if self._efficiency_histograms_vetothirdjet.has_key(mu_name + "_" + sr_name):
					self._efficiency_histograms_vetothirdjet[mu_name + "_" + sr_name].Draw("same")
					l.AddEntry(self._efficiency_histograms_vetothirdjet[mu_name + "_" + sr_name], mu_name + "/<3j", "lp")
			l.Draw()
			c.SaveAs("/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/TriggerEfficiency/figures/" + c.GetName() + ".pdf")

	def MakeSingleEfficiencyPlots(self):
		for efficiency_name, efficiency_histogram in self._efficiency_histograms.iteritems():
			print "[MakeSingleEfficiencyPlots] INFO : Plotting " + efficiency_name
			c = TCanvas("c_trigeff_" + efficiency_name, "c_trigeff_" + efficiency_name, 800, 1000)
			l = TLegend(0.5, 0.6, 0.88, 0.88)
			l.SetFillColor(0)
			l.SetBorderSize(0)
			l.SetHeader(efficiency_name)

			top = TPad("top", "top", 0., 0.5, 1., 1.)
			top.SetBottomMargin(0.02)
			top.Draw()
			top.SetLogy()
			top.cd()
			frame_top = TH1F("frame_top", "frame_top", 100, 0., 1800.)
			frame_top.GetXaxis().SetTitleSize(0)
			frame_top.GetXaxis().SetLabelSize(0)
			frame_top.GetYaxis().SetTitle("Events / 1 GeV")
			frame_top.SetMinimum(1.)
			frame_top.SetMaximum(10. * max(self._mjj_histograms[self._efficiency_combinations[efficiency_name][0]].GetMaximum(), self._mjj_histograms[self._efficiency_combinations[efficiency_name][1]].GetMaximum()))
			frame_top.Draw()
			self._mjj_histograms[self._efficiency_combinations[efficiency_name][0]].Draw("same")
			self._mjj_histograms[self._efficiency_combinations[efficiency_name][1]].Draw("same")
			if self._efficiency_combinations[efficiency_name][0] in self._legend_entries:
				l.AddEntry(self._mjj_histograms[self._efficiency_combinations[efficiency_name][0]], self._legend_entries[self._efficiency_combinations[efficiency_name][0]], "lp")
			else:
				l.AddEntry(self._mjj_histograms[self._efficiency_combinations[efficiency_name][0]], self._efficiency_combinations[efficiency_name][0], "lp")
			if self._efficiency_combinations[efficiency_name][1] in self._legend_entries:
				l.AddEntry(self._mjj_histograms[self._efficiency_combinations[efficiency_name][1]], self._legend_entries[self._efficiency_combinations[efficiency_name][1]], "lp")
			else:
				l.AddEntry(self._mjj_histograms[self._efficiency_combinations[efficiency_name][1]], self._efficiency_combinations[efficiency_name][1], "lp")
			l.Draw()

			c.cd()
			bottom = TPad("bottom", "bottom", 0., 0., 1., 0.5)
			bottom.SetTopMargin(0.02)
			bottom.SetBottomMargin(0.2)
			bottom.Draw()
			bottom.cd()
			frame_bottom = TH1F("frame_bottom", "frame_bottom", 100, 0., 1800.)
			frame_bottom.GetXaxis().SetTitle("m_{jj} [GeV]")
			frame_bottom.GetYaxis().SetTitle("Efficiency")
			frame_bottom.SetMinimum(0.)
			frame_bottom.SetMaximum(self._efficiency_guesses[efficiency_name] * 4.)
			frame_bottom.Draw()
			efficiency_histogram.Draw("same")
			#if "SingleMu" in efficiency_name or "BJet" in efficiency_name:
			self._efficiency_fits[efficiency_name].Draw("same")
			c.cd()
			c.SaveAs("/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/TriggerEfficiency/figures/" + c.GetName() + ".pdf")
			ROOT.SetOwnership(c, False)
			ROOT.SetOwnership(top, False)
			ROOT.SetOwnership(bottom, False)

	def MakeJetHTSingleMuComparisons(self):
		for sr_name in ["lowmass", "llowmass"]:
			c = TCanvas("c_trigeff_jetht_vs_singlemu_" + sr_name, "c_trigeff_jetht_vs_singlemu_" + sr_name, 800, 600)
			l = TLegend(0.7, 0.7, 0.88, 0.88)
			if sr_name == "highmass":
				l.SetHeader("Test b-tagged 160/120")
			elif sr_name == "lowmass":
				l.SetHeader("Test b-tagged 80/70")
			elif sr_name == "llowmass":
				l.SetHeader("Test b-tagged 60/53")
			l.SetFillColor(0)
			l.SetBorderSize(0)
			frame = TH1F("frame_" + sr_name, "frame_" + sr_name, 100, 0., 1800.)
			frame.SetMinimum(0.)
			frame.SetMaximum(self._efficiency_guesses["SingleMu_" + sr_name] * 7.)
			frame.GetXaxis().SetTitle("m_{jj} [GeV]")
			frame.GetYaxis().SetTitle("Efficiency")
			frame.Draw()

			# SingleMu-based efficiency
			self._efficiency_histograms["SingleMu_" + sr_name].Draw("same")
			l.AddEntry(self._efficiency_histograms["SingleMu_" + sr_name], "SingleMu", "lp")

			# JetHT_based efficiency
			self._efficiency_histograms["JetHT_" + sr_name].Draw("same")
			l.AddEntry(self._efficiency_histograms["JetHT_" + sr_name], "JetHT", "lp")
			l.Draw()
			c.SaveAs("/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/TriggerEfficiency/figures/" + c.GetName() + ".pdf")

	def MakeSingleMu6053Comparison(self):
		c = TCanvas("c_trigeff_80_70_over_60_53", "c_trigeff_80_70_over_60_53", 800, 600)
		l = TLegend(0.7, 0.7, 0.88, 0.88)
		l.SetHeader("80/70 vs 60/53")
		l.SetFillColor(0)
		l.SetBorderSize(0)
		frame = TH1F("frame_SingleMu6053Comparison", "frame_SingleMu6053Comparison", 100, 0., 1800.)
		frame.SetMinimum(0.)
		frame.SetMaximum(1.5)
		frame.GetXaxis().SetTitle("m_{jj} [GeV]")
		frame.GetYaxis().SetTitle("Efficiency")
		frame.Draw()

		# SingleMu-based efficiency
		self._efficiency_histograms["BJet60_53_lowmass"].Draw("same")
		l.AddEntry(self._efficiency_histograms["BJet60_53_lowmass"], "60/53 + b-tag", "lp")

		# JetHT_based efficiency
		self._efficiency_histograms["SingleMu_lowmass"].Draw("same")
		l.AddEntry(self._efficiency_histograms["SingleMu_lowmass"], "SingleMu", "lp")
		l.Draw()
		c.SaveAs("/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/TriggerEfficiency/figures/" + c.GetName() + ".pdf")

if __name__ == "__main__":
	trig_eff_plotter = TrigEffPlotter()
	#trig_eff_plotter.MakeSingleMuComparisons()
	trig_eff_plotter.MakeSingleEfficiencyPlots()
	#trig_eff_plotter.MakeJetHTSingleMuComparisons()
	#trig_eff_plotter.MakeSingleMu6053Comparison()
