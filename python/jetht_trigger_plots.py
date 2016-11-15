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

def ht_threshold_plot(names, histograms, save_tag, x_range=None, logy=False):
	c = TCanvas(save_tag, save_tag, 800, 1200)
	top = TPad("top", "top", 0., 0.5, 1., 1.)
	top.SetBottomMargin(0.03)
	top.Draw()
	if logy:
		top.SetLogy()

	c.cd()
	bottom = TPad("bottom", "bottom", 0, 0., 1., 0.5)
	bottom.SetTopMargin(0.02)
	bottom.SetBottomMargin(0.15)
	bottom.Draw()

	c.cd()
	top.cd()

	if x_range:
		x_min = x_range[0]
		x_max = x_range[1]
	else:
		x_min = histograms[names[0]].GetXaxis().GetXmin()
		x_max = histograms[names[0]].GetXaxis().GetXmax()
	y_max = -1.
	for name in names:
		if histograms[name].GetMaximum() > y_max:
			y_max = histograms[name].GetMaximum()
	if logy:
		y_min = 100.
		y_max = y_max * 10
	else:
		y_min = 0.
		y_max = y_max * 1.4
	frame_top = TH1F("frame_top", "frame_top", 10, x_min, x_max)
	frame_top.SetMinimum(y_min)
	frame_top.SetMaximum(y_max)
	frame_top.GetXaxis().SetLabelSize(0)
	frame_top.GetXaxis().SetTitleSize(0)
	frame_top.Draw("axis")
	legend_top = TLegend(0.7, 0.55, 0.88, 0.88)
	legend_top.SetFillColor(0)
	legend_top.SetBorderSize(0)

	style_counter = 0
	for name in names:
		histograms[name].SetMarkerStyle(20 + style_counter)
		histograms[name].SetMarkerColor(seaborn.GetColorRoot("dark", style_counter))
		histograms[name].SetLineColor(seaborn.GetColorRoot("dark", style_counter))
		histograms[name].Draw("p same")
		legend_top.AddEntry(histograms[name], name, "p")
		style_counter += 1
	legend_top.Draw()

	c.cd()
	bottom.cd()
	frame_bottom = TH1F("frame_bottom", "frame_bottom", 10, x_min, x_max)
	frame_bottom.SetMinimum(-0.2)
	frame_bottom.SetMaximum(1.3)
	frame_bottom.GetXaxis().SetTitle("m_{jj} [GeV]")
	frame_bottom.Draw("axis")
	legend_bottom = TLegend(0.6, 0.25, 0.9, 0.65)
	legend_bottom.SetFillColor(0)
	legend_bottom.SetBorderSize(0)

	ratio_histograms = {}
	for i in xrange(1, len(names)):
		ratio_histograms[names[i]] = histograms[names[i]].Clone()
		ratio_histograms[names[i]].Divide(histograms[names[i-1]])
		ratio_histograms[names[i]].SetMarkerStyle(20 + i)
		ratio_histograms[names[i]].SetMarkerColor(seaborn.GetColorRoot("dark", i))
		ratio_histograms[names[i]].SetLineColor(seaborn.GetColorRoot("dark", i))
		ratio_histograms[names[i]].Draw("hist same")
		ratio_histograms[names[i]].Draw("p same")
		legend_bottom.AddEntry(ratio_histograms[names[i]], names[i] + " / " + names[i-1], "lp")
	legend_bottom.Draw()

	c.SaveAs(analysis_config.figure_directory + "/" + save_tag + ".pdf")

	# Stop ROOT from being a dick
	ROOT.SetOwnership(c, False)
	ROOT.SetOwnership(top, False)
	ROOT.SetOwnership(bottom, False)

# Cobble together m(jj) histogram from several JetHT triggers. 
def jetht_frankenhist(names, histograms, ranges):
	frankenhist = histograms[names[0]].Clone()
	frankenhist.Reset()
	for bin in xrange(1, frankenhist.GetNbinsX() + 1):
		x = frankenhist.GetXaxis().GetBinCenter(bin)
		# Find range
		for name in names:
			if x > ranges[name][0] and x < ranges[name][1]:
				frankenhist.SetBinContent(bin, histograms[name].GetBinContent(bin))
				frankenhist.SetBinError(bin, histograms[name].GetBinError(bin))
				break
	return frankenhist


if __name__ == "__main__":
	print "Welcome to jetht_trigger_plot.py"
	import argparse
	parser = argparse.ArgumentParser(description = 'Dijet mass spectrum fits')
	parser.add_argument('--ht', action='store_true', help='Make JetHT threshold plot')
	parser.add_argument('--btag', action='store_true', help='Make online B tag efficiency plot')
	parser.add_argument('--btag_mc_jetht', action='store_true', help='Make online B tag efficiency plot from MC')
	parser.add_argument('--btag_mc_notrig', action='store_true', help='Make online B tag efficiency plot from MC')
	args = parser.parse_args()
	print args

	if args.ht:
		analyses = {}
		names = []
		for mass in xrange(200, 700, 50):
			if mass == 600:
				continue
			names.append("HT" + str(mass))
			analyses["HT" + str(mass)] = "trigjetht" + str(mass)
		sample = "JetHT_2012BCD"
		histograms = {}
		for name in names:
			f = TFile(analysis_config.get_b_histogram_filename(analyses[name], sample), "READ")
			#histograms[name] = mjj_common.apply_dijet_binning_normalized(f.Get("BHistograms/h_pfjet_mjj"))
			print "[debug] For name " + name + ", input events = " + str(f.Get("BHistograms/h_input_nevents").GetEntries())
			print "[debug] \tPrescale = " + str(f.Get("BHistograms/h_pass_nevents_weighted").GetBinContent(1) / f.Get("BHistograms/h_pass_nevents").GetBinContent(1))
			histograms[name] = f.Get("BHistograms/h_pfjet_mjj").Rebin(20)
			histograms[name].SetName(histograms[name].GetName() + "_" + name)
			histograms[name].SetDirectory(0)
			f.Close()
		ht_threshold_plot(names, histograms, save_tag="jetht_thresholds", x_range=[0., 1200.], logy=True)

	if args.btag:
		for sr in ["lowmass", "highmass"]:
			ht_analyses = {}
			names = []
			for mass in xrange(200, 700, 50):
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
				"HT200":[200, 400],
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
			print "[debug] names = ",
			print names
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

	if args.btag_mc_jetht:
		print "Making btag MC plot (vs HT triggers)"
		for sr in ["lowmass", "highmass"]:
			print "On SR " + sr
			for model in ["Hbb", "RSG"]:
				print "On model " + model
				ht_analyses = {}
				analyses = []
				for ht_threhold in xrange(200, 700, 50):
					if ht_threhold == 600:
						continue
					if ht_threhold == 650:
						continue
					analyses.append("HT" + str(ht_threhold))
					if sr == "highht_threhold":
						ht_analyses["HT" + str(ht_threhold)] = "trigjetht" + str(ht_threhold) + "_CSVTM"
					else:
						ht_analyses["HT" + str(ht_threhold)] = "trigjetht" + str(ht_threhold) + "_eta1p7_CSVTM"
		
				# For now, only the high mass SR has the unprescaled JetHT triggers
				if sr == "highmass":
					analyses.append("HTUnprescaled")
					ht_analyses["HTUnprescaled"] = "trigjetht_CSVTM"
				ranges = {
					"HT200":[200, 400],
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

				#mc_sample = analysis_config.simulation.get_signal_tag(model, "All", "FULLSIM")
				bjetplusx_histogram_total = None
				jetht_histograms_total = {}
				for signal_mass in [400, 600, 750, 900, 1200]:
					jetht_histograms = {}
					bjetplusx_histogram = None
					bjetplusx_nevents = 0
					bjetplusx_sample = analysis_config.simulation.get_signal_tag(model, signal_mass, "FULLSIM")
					if sr == "highmass":
						f = TFile(analysis_config.get_b_histogram_filename("trigbbh_CSVTM", bjetplusx_sample), "READ")
					else:
						f = TFile(analysis_config.get_b_histogram_filename("trigbbl_CSVTM", bjetplusx_sample), "READ")
					print "[debug] \th_pfjet_mjj integral = " + str(f.Get("BHistograms/h_pfjet_mjj").Integral())
					bjetplusx_histogram = f.Get("BHistograms/h_pfjet_mjj")
					bjetplusx_histogram.SetName(bjetplusx_histogram.GetName() + "_BJetPlusX")
					bjetplusx_histogram.SetDirectory(0)
					if not bjetplusx_histogram_total:
						bjetplusx_histogram_total = f.Get("BHistograms/h_pfjet_mjj")
						bjetplusx_histogram_total.SetName(bjetplusx_histogram_total.GetName() + "_BJetPlusX")
						bjetplusx_histogram_total.SetDirectory(0)
					else:
						bjetplusx_histogram_total.Add(f.Get("BHistograms/h_pfjet_mjj"))
					this_bjetplusx_nevents = f.Get("BHistograms/h_input_nevents").Integral()
					print bjetplusx_sample + " this_bjetplusx_nevents = " + str(this_bjetplusx_nevents) + " events"
					bjetplusx_nevents += this_bjetplusx_nevents
					f.Close()

					jetht_sample = analysis_config.simulation.get_signal_tag(model, signal_mass, "FULLSIM")
					for analysis in analyses:
						#print "[debug] Opening " + analysis_config.get_b_histogram_filename(ht_analyses[analysis], jetht_sample)
						f = TFile(analysis_config.get_b_histogram_filename(ht_analyses[analysis], jetht_sample), "READ")
						this_jetht_nevents = f.Get("BHistograms/h_input_nevents").Integral()
						print analysis + " this_jetht_nevents = " + str(this_jetht_nevents)
						if not f.Get("BHistograms/h_pfjet_mjj"):
							print "ERROR : h_pfjet_mjj not found in file " + analysis_config.get_b_histogram_filename(ht_analyses[analysis], jetht_sample)
							sys.exit(1)
						jetht_histograms[analysis] = f.Get("BHistograms/h_pfjet_mjj")
						jetht_histograms[analysis].Scale(bjetplusx_nevents/this_jetht_nevents)
						jetht_histograms[analysis].SetName(jetht_histograms[analysis].GetName() + "_" + analysis)
						jetht_histograms[analysis].SetDirectory(0)
						if not analysis in jetht_histograms_total:
							jetht_histograms_total[analysis] = f.Get("BHistograms/h_pfjet_mjj")
							jetht_histograms_total[analysis].Scale(bjetplusx_nevents/this_jetht_nevents)
							jetht_histograms_total[analysis].SetName(jetht_histograms_total[analysis].GetName() + "_" + analysis)
							jetht_histograms_total[analysis].SetDirectory(0)
						else:
							h_tmp = f.Get("BHistograms/h_pfjet_mjj")
							h_tmp.Scale(bjetplusx_nevents/this_jetht_nevents)
							jetht_histograms_total[analysis].Add(h_tmp)
						f.Close()

					jetht_histogram = jetht_frankenhist(analyses, jetht_histograms, ranges)
					jetht_histogram.Rebin(25)
					bjetplusx_histogram.Rebin(25)
					print "jetht_histogram integral = " + str(jetht_histogram.Integral())
					print "bjetplus_histogram integral = " + str(bjetplusx_histogram.Integral())

					plot = AnalysisComparisonPlot(bjetplusx_histogram, jetht_histogram, "BJetPlusX", "JetHT", "online_btag_efficiency_MC_" + sr + "_" + model + "_" + str(signal_mass), x_range=[0., 1200.], log=True)
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
					if ratio_fit.GetNDF() > 0:
						print "Ratio chi2/ndf = " + str(ratio_fit.GetChisquare()) + " / " + str(ratio_fit.GetNDF()) + " = " + str(ratio_fit.GetChisquare() / ratio_fit.GetNDF())
					else:
						print "ndf = 0! Something went wrong."
					plot.save()
					print ratio_fit

					print plot.top
				jetht_histogram_total = jetht_frankenhist(analyses, jetht_histograms_total, ranges)
				jetht_histogram_total.Rebin(25)
				bjetplusx_histogram_total.Rebin(25)
				plot = AnalysisComparisonPlot(bjetplusx_histogram_total, jetht_histogram_total, "BJetPlusX", "JetHT", "online_btag_efficiency_MC_" + sr + "_" + model + "_total", x_range=[0., 1200.], log=True)
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
				if ratio_fit.GetNDF() > 0:
					print "Ratio chi2/ndf = " + str(ratio_fit.GetChisquare()) + " / " + str(ratio_fit.GetNDF()) + " = " + str(ratio_fit.GetChisquare() / ratio_fit.GetNDF())
				else:
					print "ndf = 0! Something went wrong."
				plot.save()


	if args.btag_mc_notrig:
		print "Making btag MC plot (vs HT triggers)"
		for var in ["mjj", "pt_btag1", "pt_btag2"]:
			for sr in ["lowmass", "highmass"]:
				print "On SR " + sr
				if sr == "lowmass":
					notrig_analysis = "NoTrigger_eta1p7_CSVTM"
				else:
					notrig_analysis = "NoTrigger_eta2p2_CSVTM"
				for model in ["Hbb", "RSG"]:
					print "On model " + model

					bjetplusx_histogram_total = None
					notrig_histogram_total = None
					bjetplusx_nevents = 0
					notrig_nevents = 0
					for signal_mass in [400, 600, 750, 900, 1200]:
						mc_sample = analysis_config.simulation.get_signal_tag(model, signal_mass, "FULLSIM")
						if sr == "highmass":
							f = TFile(analysis_config.get_b_histogram_filename("trigbbh_CSVTM", mc_sample), "READ")
						else:
							f = TFile(analysis_config.get_b_histogram_filename("trigbbl_CSVTM", mc_sample), "READ")
						print "[debug] \th_pfjet_" + var + " integral = " + str(f.Get("BHistograms/h_pfjet_" + var).Integral())
						bjetplusx_histogram = f.Get("BHistograms/h_pfjet_" + var)
						bjetplusx_histogram.SetName(bjetplusx_histogram.GetName() + "_BJetPlusX")
						bjetplusx_histogram.SetDirectory(0)
						if not bjetplusx_histogram_total:
							bjetplusx_histogram_total = f.Get("BHistograms/h_pfjet_" + var)
							bjetplusx_histogram_total.SetName(bjetplusx_histogram_total.GetName() + "_BJetPlusX")
							bjetplusx_histogram_total.SetDirectory(0)
						else:
							bjetplusx_histogram_total.Add(f.Get("BHistograms/h_pfjet_" + var))
						this_bjetplusx_nevents = f.Get("BHistograms/h_input_nevents").Integral()
						print mc_sample + " this_bjetplusx_nevents = " + str(this_bjetplusx_nevents) + " events"
						bjetplusx_nevents += this_bjetplusx_nevents
						f.Close()

						f = TFile(analysis_config.get_b_histogram_filename(notrig_analysis, mc_sample), "READ")
						this_notrig_nevents = f.Get("BHistograms/h_input_nevents").Integral()
						notrig_nevents += this_notrig_nevents
						print "this_notrig_nevents = " + str(this_notrig_nevents)
						if not f.Get("BHistograms/h_pfjet_" + var):
							print "ERROR : h_pfjet_" + var + " not found in file " + analysis_config.get_b_histogram_filename(notrig_analysis, mc_sample)
							sys.exit(1)
						notrig_histogram = f.Get("BHistograms/h_pfjet_" + var)
						print "Ensuring that the numerator and denominator have the same input normalization. Scale factor = " + str(this_bjetplusx_nevents/this_notrig_nevents)
						notrig_histogram.Scale(this_bjetplusx_nevents/this_notrig_nevents)
						notrig_histogram.SetName(notrig_histogram.GetName() + "_" + notrig_analysis)
						notrig_histogram.SetDirectory(0)
						if not notrig_histogram_total:
							notrig_histogram_total = f.Get("BHistograms/h_pfjet_" + var)
							notrig_histogram_total.Scale(this_bjetplusx_nevents/this_notrig_nevents)
							notrig_histogram_total.SetName(notrig_histogram_total.GetName() + "_notrig_total")
							notrig_histogram_total.SetDirectory(0)
						else:
							h_tmp = f.Get("BHistograms/h_pfjet_" + var)
							h_tmp.Scale(this_bjetplusx_nevents/this_notrig_nevents)
							notrig_histogram_total.Add(h_tmp)
						f.Close()

						notrig_histogram.Rebin(25)
						bjetplusx_histogram.Rebin(25)
						print "notrig_histogram integral = " + str(notrig_histogram.Integral())
						print "bjetplus_histogram integral = " + str(bjetplusx_histogram.Integral())

						plot = AnalysisComparisonPlot(bjetplusx_histogram, notrig_histogram, "BJetPlusX", "No Trigger", "online_btag_efficiency_MC_NoTrigger_" + sr + "_" + model + "_" + str(signal_mass), x_range=[0., 1200.], log=True)
						if sr == "lowmass":
							plot.ratio_min = -0.2
							plot.ratio_max = 0.5
						else:
							plot.ratio_min = -0.2
							plot.ratio_max = 1.0
						plot.draw()
						plot.top.cd()
						ymin = plot.frame_top.GetMinimum()
						ymax = plot.frame_top.GetMaximum()
						# Fit constant to ratio
						ratio_fit = TF1("ratio_fit", "[0]", 400, 1000)
						plot.hist_ratio.Fit(ratio_fit, "QR0")
						plot.canvas.cd()
						plot.bottom.cd()
						ratio_fit.Draw("same")
						plot.canvas.cd()
						if ratio_fit.GetNDF() > 0:
							print "Ratio chi2/ndf = " + str(ratio_fit.GetChisquare()) + " / " + str(ratio_fit.GetNDF()) + " = " + str(ratio_fit.GetChisquare() / ratio_fit.GetNDF())
						else:
							print "ndf = 0! Something went wrong."
						plot.save()
						print ratio_fit

						print plot.top
					notrig_histogram_total.Rebin(25)
					bjetplusx_histogram_total.Rebin(25)
					plot = AnalysisComparisonPlot(bjetplusx_histogram_total, notrig_histogram_total, "BJetPlusX", "No Trigger", "online_btag_efficiency_MC_NoTrigger_" + sr + "_" + model + "_total_" + var, x_range=[0., 1200.], log=True)
					if sr == "lowmass":
						plot.ratio_min = -0.2
						plot.ratio_max = 0.5
					else:
						plot.ratio_min = -0.2
						plot.ratio_max = 1.0
					plot.draw()
					plot.top.cd()
					ymin = plot.frame_top.GetMinimum()
					ymax = plot.frame_top.GetMaximum()
					# Fit constant to ratio
					ratio_fit = TF1("ratio_fit", "[0]", 400, 1000)
					plot.hist_ratio.Fit(ratio_fit, "QR0")
					plot.canvas.cd()
					plot.bottom.cd()
					ratio_fit.Draw("same")
					plot.canvas.cd()
					if ratio_fit.GetNDF() > 0:
						print "Ratio chi2/ndf = " + str(ratio_fit.GetChisquare()) + " / " + str(ratio_fit.GetNDF()) + " = " + str(ratio_fit.GetChisquare() / ratio_fit.GetNDF())
					else:
						print "ndf = 0! Something went wrong."
					plot.save()
