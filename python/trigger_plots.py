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

reference_triggers = [
	"HLT_L1DoubleJet36Central", 
	"HLT_Jet60Eta1p7_Jet53Eta1p7_DiBTagIP3DFastPV", 
	"HLT_DiJet40Eta2p6_BTagIP3DFastPV", 
	"HLT_DiJet80Eta2p6_BTagIP3DFastPVLoose"
]
test_triggers = [
	'HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose', 
	#'HLT_Jet80Eta1p7_Jet70Eta1p7_DiBTagIP3DFastPV'
]

online_pt_thresholds = {}
online_pt_thresholds['HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose'] = [160., 120.]
online_pt_thresholds['HLT_Jet80Eta1p7_Jet70Eta1p7_DiBTagIP3DFastPV'] = [80., 70.]


all_triggers = reference_triggers[:]
all_triggers.extend(test_triggers)
print all_triggers

def PrescaleTable(input_file, output_tag):
	f_in = TFile(input_file, "READ")
	tdf = f_in.Get("inclusive")
	patterns_trigger = {}
	for trigger_name in all_triggers:
		patterns_trigger[trigger_name] = re.compile(trigger_name + "_(?P<version>v\d)")

	h_trigger_counts = tdf.Get("h_trigger_counts").Clone()
	h_trigger_counts.SetDirectory(0)
	h_trigger_counts_prescale = tdf.Get("h_trigger_counts_prescale").Clone()
	h_trigger_counts_prescale.SetDirectory(0)
	h_trigger_counts_L1prescale = tdf.Get("h_trigger_counts_L1prescale").Clone()
	h_trigger_counts_L1prescale.SetDirectory(0)
	h_trigger_counts_HLTprescale = tdf.Get("h_trigger_counts_HLTprescale").Clone()
	h_trigger_counts_HLTprescale.SetDirectory(0)

	# Collapse bins with different versions
	trigger_counts = {}
	trigger_counts_prescale = {}
	trigger_counts_L1prescale = {}
	trigger_counts_HLTprescale = {}
	triggers_to_print = []
	for bin in xrange(1, h_trigger_counts.GetNbinsX() + 1):
		if h_trigger_counts.GetBinContent(bin) == 0:
			continue
		trigger_name = h_trigger_counts.GetXaxis().GetBinLabel(bin)
		if trigger_counts.has_key(trigger_name):
			trigger_counts[trigger_name] += h_trigger_counts.GetBinContent(bin)
			trigger_counts_prescale[trigger_name] += h_trigger_counts_prescale.GetBinContent(bin)
			trigger_counts_L1prescale[trigger_name] += h_trigger_counts_L1prescale.GetBinContent(bin)
			trigger_counts_HLTprescale[trigger_name] += h_trigger_counts_HLTprescale.GetBinContent(bin)
		else:
			triggers_to_print.append(trigger_name)
			trigger_counts[trigger_name] = h_trigger_counts.GetBinContent(bin)
			trigger_counts_prescale[trigger_name] = h_trigger_counts_prescale.GetBinContent(bin)
			trigger_counts_L1prescale[trigger_name] = h_trigger_counts_L1prescale.GetBinContent(bin)
			trigger_counts_HLTprescale[trigger_name] = h_trigger_counts_HLTprescale.GetBinContent(bin)

	prescale = {}
	L1prescale = {}
	HLTprescale = {}
	for trigger_name in triggers_to_print:
		prescale[trigger_name] = trigger_counts_prescale[trigger_name] / trigger_counts[trigger_name]
		L1prescale[trigger_name] = trigger_counts_L1prescale[trigger_name] / trigger_counts[trigger_name]
		HLTprescale[trigger_name] = trigger_counts_HLTprescale[trigger_name] / trigger_counts[trigger_name]


	# Latex table
	prescales_table = open(output_tag + "_prescales.tex", 'w')
	prescales_table.write("\\begin{table}\n")
	prescales_table.write("\t\\centering\n")
	prescales_table.write("\t\\begin{tabular}{|l|c|c|c|}\n")
	prescales_table.write("\t\t\\hline\n")
	prescales_table.write("\t\tName\t&\tL1\t&\tHLT\t&\tTotal\t\n")
	prescales_table.write("\t\t\\hline\n")
	for trigger_name in triggers_to_print:
		prescales_table.write("\t\t" + trigger_name + "\t&\t" + str(L1prescale[trigger_name]) + "\t&\t" + str(HLTprescale[trigger_name]) + "\t&\t" + str(prescale[trigger_name]) + "\t\n\t\t\\hline\n")
	prescales_table.write("\t\\end{tabular}\n")
	prescales_table.write("\\end{table}\n")

	prescales_table.close()

def SumVersions(p_tdf, p_pattern):
	first = True
	h_return = 0
	pattern_regex = re.compile(p_pattern)
	for key in p_tdf.GetListOfKeys():
		obj = key.ReadObj()
		name = obj.GetName()
		matches = pattern_regex.search(name)
		if matches:
			if first:
				h_return = obj.Clone()
				h_return.SetDirectory(0)
				first = False
			else:
				h_return.Add(obj)
	if first:
		print "[SumVersions] WARNING : Didn't find any histograms matching pattern" + p_pattern

	return h_return


def VarPlots(input_file, output_tag, plot_log=False, signal_file=None, signal_xs=None):
	f_in = TFile(input_file, "READ")
	tdf = f_in.Get("inclusive")
	variables = ["nevents", "pf_mjj", "pf_deltaeta", "pf_eta1", "pf_eta2", "pf_pt1", "pf_pt2", "pf_btag_csv1", "pf_btag_csv2"]
	rebin = {"pf_mjj":20, "pf_mjj_160_120":20, "pf_mjj_80_70":20, "pf_deltaeta":1, "pf_eta1":2, "pf_eta2":2, "pf_pt1":20, "pf_pt2":20, "pf_btag_csv1":1, "pf_btag_csv2":1}

	if signal_file:
		f_signal = TFile(signal_file, "READ")
		tdf_signal = f_signal.Get("inclusive")

	for var in variables:
		if "mjj" in var or "pt" in var:
			c = ROOT.TCanvas("c_" + var, "c_" + var, 800, 600)
			l = ROOT.TLegend(0.4, 0.7, 0.9, 0.9)
		elif "btag" in var:
			c = ROOT.TCanvas("c_" + var, "c_" + var, 800, 600)
			l = ROOT.TLegend(0.21, 0.5, 0.7, 0.8)
		elif "eta" in var:
			c = ROOT.TCanvas("c_" + var, "c_" + var, 800, 600)
			l = ROOT.TLegend(0.2, 0.75, 0.85, 0.9)
		else:
			c = ROOT.TCanvas("c_" + var, "c_" + var, 1200, 600)
			c.SetRightMargin(0.25)
			l = ROOT.TLegend(0.76, 0.4, 0.99, 0.7)
		if plot_log:
			c.SetLogy()
		l.SetFillColor(0)
		l.SetBorderSize(0)
		style_counter = 0
		hist = {}
		hist_signal = {}
		ymax = -1.
		for trigger in test_triggers:
			hist[trigger] = tdf.Get("h_ref" + trigger + "_" + var)
			hist[trigger].SetDirectory(0)
			if signal_file:
				hist_signal[trigger] = tdf.Get("h_ref" + trigger + "_" + var)
				hist_signal[trigger].SetDirectory(0)
				# Normalize
				hist_signal[trigger].Scale(1. / tdf_signal.Get("h_ref" + trigger + "_nevents").Integral() * 19700. * signal_xs)

			if var in rebin.keys():
				hist[trigger].Rebin(rebin[var])
				if signal_file:
					hist_signal[trigger].Rebin(rebin[var])
			blind = False
			if blind:
				if "mjj" in var:
					for bin in xrange(1, hist[trigger].GetNbinsX() + 1):
						if TMath.Abs(hist[trigger].GetBinCenter(bin) - 750.) < 75.:
							hist[trigger].SetBinContent(bin, 0.)
							hist[trigger].SetBinError(bin, 0.)
			hist[trigger].SetLineColor(seaborn.GetColorRoot("default", style_counter))
			hist[trigger].SetMarkerColor(seaborn.GetColorRoot("default", style_counter))
			hist[trigger].SetMarkerStyle(21)
			if "mjj" in var or "pt" in var:
				hist[trigger].GetYaxis().SetTitle("Events / " + str(int(hist[trigger].GetXaxis().GetBinWidth(1))) + " GeV")
			l.AddEntry(hist[trigger], trigger, "l")
			if signal_file:
				hist_signal[trigger].SetLineColor(seaborn.GetColorRoot("dark", style_counter))

			if hist[trigger].GetMaximum() > ymax:
				ymax = hist[trigger].GetMaximum()

			style_counter += 1

		first = True
		for trigger in test_triggers:
			if first:
				first = False
				opt = "pe1"
				if plot_log:
					hist[trigger].SetMaximum(ymax * 10.)
				else:
					if "eta" in var:
						hist[trigger].SetMaximum(ymax * 1.5)
					else:
						hist[trigger].SetMaximum(ymax * 1.2)
				# Y axis label
			else:
				opt = "pe1 same"
			hist[trigger].Draw(opt)
			if signal_file:
				hist_signal[trigger].Draw("hist same")
		l.Draw()
		if plot_log:
			c.SaveAs("~/Dijets/data/EightTeeEeVeeBee/TriggerEfficiency/figures/" + c.GetName() + "_log.pdf")
		else:
			c.SaveAs("~/Dijets/data/EightTeeEeVeeBee/TriggerEfficiency/figures/" + c.GetName() + ".pdf")


def NormVarPlots(input_file, output_tag):
	f_in = TFile(input_file, "READ")
	tdf = f_in.Get("inclusive")
	efficiency_variables = ["nevents", "pf_mjj", "pf_mjj_160_120", "pf_mjj_80_70", "pf_deltaeta", "pf_eta1", "pf_eta2", "pf_pt1", "pf_pt2", "pf_btag_csv1", "pf_btag_csv2"]
	rebin = {"pf_mjj":20, "pf_mjj_160_120":20, "pf_mjj_80_70":20, "pf_deltaeta":4, "pf_eta1":4, "pf_eta2":4, "pf_pt1":20, "pf_pt2":20, "pf_btag_csv1":1, "pf_btag_csv2":1}

	for var in efficiency_variables:
		c = ROOT.TCanvas("c_norm_" + var, "c_norm_" + var, 1000, 600)
		c.SetRightMargin(0.25)
		l = ROOT.TLegend(0.77, 0.3, 0.99, 0.7)
		l.SetFillColor(0)
		l.SetBorderSize(0)
		style_counter = 0
		hist = {}
		ymax = -1.
		for trigger in all_triggers:
			hist[trigger] = tdf.Get("h_ref" + trigger + "_" + var)
			hist[trigger].SetDirectory(0)
			if hist[trigger].Integral() > 0:
				hist[trigger].Scale(1. / hist[trigger].Integral())
			if "mjj" in var:
				for bin in xrange(1, hist[trigger].GetNbinsX() + 1):
					if TMath.Abs(hist[trigger].GetBinCenter(bin) - 750.) < 75.:
						hist[trigger].SetBinContent(bin, 0.)
			if var in rebin.keys():
				hist[trigger].Rebin(rebin[var])
			hist[trigger].SetLineColor(seaborn.GetColorRoot("default", style_counter))
			hist[trigger].SetMarkerColor(seaborn.GetColorRoot("default", style_counter))
			hist[trigger].SetMarkerStyle(25)
			l.AddEntry(hist[trigger], trigger, "l")
			if hist[trigger].GetMaximum() > ymax:
				ymax = hist[trigger].GetMaximum()
			style_counter += 1

		first = True
		for trigger in all_triggers:
			if first:
				first = False
				opt = "hist"
				hist[trigger].SetMaximum(ymax * 1.2)
			else:
				opt = "hist same"
			hist[trigger].Draw(opt)
		l.Draw()
		c.SaveAs("~/Dijets/data/EightTeeEeVeeBee/TriggerEfficiency/figures/" + c.GetName() + ".pdf")

	for var2D in ["pf_pt1_pt2"]:
		for trigger in all_triggers:
			c = ROOT.TCanvas("c_" + var2D + "_" + trigger, "c_" + var2D + "_" + trigger, 800, 600)
			c.SetRightMargin(0.25)
			hist = tdf.Get("h_ref" + trigger + "_" + var2D)
			hist.SetDirectory(0)
			hist.Draw("colz")
			c.SaveAs("~/Dijets/data/EightTeeEeVeeBee/TriggerEfficiency/figures/" + c.GetName() + ".pdf")

def DivideBinomial(h_num, h_den):
	h_ratio = h_num.Clone()
	h_ratio.SetName(h_num.GetName() + "_over_" + h_den.GetName())
	for bin in xrange(1, h_ratio.GetNbinsX() + 1):
		if h_den.GetBinContent(bin) > 0. and h_num.GetBinContent(bin) > 0. and h_num.GetBinContent(bin) <= h_den.GetBinContent(bin):
			N = h_den.GetBinContent(bin)
			p = h_num.GetBinContent(bin) / N
			h_ratio.SetBinContent(bin, p)
			h_ratio.SetBinError(bin, TMath.Max(1. / N, TMath.Sqrt(p * (1. - p) / N)))
		else:
			h_ratio.SetBinContent(bin, 0.)
			h_ratio.SetBinError(bin, 0.)
	return h_ratio


def EfficiencyPlots(input_file, output_tag):
	f_in = TFile(input_file, "READ")
	tdf = f_in.Get("inclusive")

	# Efficiency plots
	#efficiency_variables = ["nevents", "pfjet_mjj", "pfjet_mjj_160_120", "pfjet_mjj_80_70", "pfjet_deltaeta", "fatjet_deltaeta", "pfjet_eta1", "pfjet_eta2", "pfjet_pt1", "pfjet_pt2", "pfjet_btag_csv1", "pfjet_btag_csv2", "fatjet_mjj", "fatjet_eta1", "fatjet_eta2", "fatjet_pt1", "fatjet_pt2"]
	efficiency_variables = ["fatjet_mjj_160_120", "pfjet_mjj_160_120"]
	rebin = {"pfjet_mjj":20, "pfjet_mjj_160_120":20, "pfjet_mjj_80_70":20, "pfjet_deltaeta":4, "pfjet_eta1":4, "pfjet_eta2":4, "pfjet_pt1":20, "pfjet_pt2":20, "pfjet_btag_csv1":1, "pfjet_btag_csv2":1, "fatjet_mjj":20, "fatjet_mjj_160_120":20, "fatjet_mjj_80_70":20, "fatjet_deltaeta":4, "fatjet_eta1":4, "fatjet_eta2":4, "fatjet_pt1":20, "fatjet_pt2":20, "fatjet_btag_csv1":1, "fatjet_btag_csv2":1}
	for reference_trigger in reference_triggers:
		print "[debug] reference_trigger = " + reference_trigger
		for var in efficiency_variables:
			print "[debug] var = " + var
			if "mjj" in var or "pt" in var:
				c = ROOT.TCanvas("c_trigeff_" + var + "_ref" + reference_trigger, "c_trigeff_" + var + "_ref" + reference_trigger, 800, 600)
				l = ROOT.TLegend(0.38, 0.25, 0.92, 0.4)
			elif "btag" in var:
				c = ROOT.TCanvas("c_trigeff_" + var + "_ref" + reference_trigger, "c_trigeff_" + var + "_ref" + reference_trigger, 800, 600)
				l = ROOT.TLegend(0.2, 0.6, 0.5, 0.9)
			else:
				c = ROOT.TCanvas("c_trigeff_" + var + "_ref" + reference_trigger, "c_trigeff_" + var + "_ref" + reference_trigger, 800, 1000)
				c.SetBottomMargin(0.4)
				l = ROOT.TLegend(0.05, 0., 0.99, 0.3)
			l.SetFillColor(0)
			l.SetBorderSize(0)
			style_counter = 0
			h_eff = {}
			fit_eff = {}
			ymax = -1.
			#h_ref = SumVersions(tdf, "h_ref" + reference_trigger + "_(?P<version>v\d)_" + var)
			h_ref = tdf.Get("h_ref" + reference_trigger + "_" + var)
			if not h_ref:
				print "[EfficiencyPlots] ERROR : Unable to find histogram " + "h_ref" + reference_trigger + "_" + var
				tdf.ls()
				sys.exit(1)
			h_ref.SetDirectory(0)
			if var in rebin.keys():
				h_ref.Rebin(rebin[var])
			for test_trigger in test_triggers:
				print "Trying to get " + "h_test" + test_trigger + "_ref" + reference_trigger + "_" + var
				#h_test = SumVersions(tdf, "h_test" + test_trigger + "_(?P<version>v\d)_ref" + reference_trigger + "_(?P<version2>v\d)_" + var)
				h_test = tdf.Get("h_test" + test_trigger + "_ref" + reference_trigger + "_" + var)
				h_test.SetDirectory(0)
				if var in rebin.keys():
					h_test.Rebin(rebin[var])
				h_eff[test_trigger] = DivideBinomial(h_test, h_ref)
				h_eff[test_trigger].SetLineColor(seaborn.GetColorRoot("default", style_counter))
				h_eff[test_trigger].SetMarkerColor(seaborn.GetColorRoot("default", style_counter))
				h_eff[test_trigger].SetMarkerStyle(25)
				#matches = pattern_trigger_path.search(test_trigger)
				l.AddEntry(h_eff[test_trigger], test_trigger, "pl")
				if h_eff[test_trigger].GetMaximum() > ymax:
					ymax = h_eff[test_trigger].GetMaximum()

				# Fit
				if "mjj" in var or "pt" in var:
					# Start fit at 10%-ish point
					if "mjj" in var:
						start_guess = (online_pt_thresholds[test_trigger][0] + online_pt_thresholds[test_trigger][1]) * 1.2
					elif "pt1" in var:
						start_guess = online_pt_thresholds[test_trigger][0]
					elif "pt2" in var:
						start_guess = online_pt_thresholds[test_trigger][1]
					fit_eff[test_trigger] = ROOT.TF1("fit_"  + test_trigger + "_" + var, "(TMath::Erf((x-[0])/[1]) + 1.) / 2.", start_guess, 600.)

					#  Find 50%-ish point
					turnon_guess = 250.
					for bin in xrange(1, h_eff[test_trigger].GetNbinsX()):
						if h_eff[test_trigger].GetBinContent(bin) <= 0.5 and h_eff[test_trigger].GetBinContent(bin + 1) > 0.5:
							turnon_guess = h_eff[test_trigger].GetBinCenter(bin)
					fit_eff[test_trigger].SetParameter(0, turnon_guess)
					fit_eff[test_trigger].SetParameter(1, 50.)
					fit_eff[test_trigger].SetParLimits(0, 50., 500.)
					fit_eff[test_trigger].SetParLimits(1, 10., 500.)					
					h_eff[test_trigger].Fit(fit_eff[test_trigger], "0")
					fit_eff[test_trigger].SetLineColor(seaborn.GetColorRoot("pastel", style_counter))

				style_counter += 1

			first = True
			for test_trigger in test_triggers:
				if first:
					first = False
					if "mjj" in var:
						frame = ROOT.TH1D("frame", "frame", 100, 150., 1000.)
					elif "pt" in var:
						frame = ROOT.TH1D("frame", "frame", 100, 50., 600.)
					else:
						frame = h_eff[test_trigger].Clone()
					if "mjj" in var or "pt" in var:
						frame.SetMinimum(0.8)
						frame.SetMaximum(1.03)
					else:
						frame.SetMinimum(0.)
						frame.SetMaximum(1.1)
					frame.GetXaxis().SetTitle(h_eff[test_trigger].GetXaxis().GetTitle())
					frame.GetYaxis().SetTitle(h_eff[test_trigger].GetYaxis().GetTitle())
					frame.Draw("axis")
					ninetyfive = ROOT.TLine(frame.GetXaxis().GetXmin(), 0.95, frame.GetXaxis().GetXmax(), 0.95)
					ninetyfive.SetLineStyle(2)
					ninetyfive.SetLineColor(ROOT.kGray)
					ninetyfive.Draw("same")
					ninetynine = ROOT.TLine(frame.GetXaxis().GetXmin(), 0.99, frame.GetXaxis().GetXmax(), 0.99)
					ninetynine.SetLineStyle(2)
					ninetynine.SetLineColor(ROOT.kGray)
					ninetynine.Draw()
				h_eff[test_trigger].Draw("pe1 hist same")
				#if "mjj" in var or "pt" in var:
					#fit_eff[test_trigger].Draw("same")
					#chi2ndf_text = ROOT.TLatex(0.5, 0.25, "#chi^{2}/NDF  =  " + str(fit_eff[test_trigger].GetChisquare()) + " / " + str(fit_eff[test_trigger].GetNDF()))
					#chi2ndf_text.Draw()
			l.Draw()
			c.SaveAs("~/Dijets/data/EightTeeEeVeeBee/TriggerEfficiency/figures/" + c.GetName() + ".pdf")

	for reference_trigger in reference_triggers:
		for test_trigger in test_triggers:
			for var2D in ["pfjet_pt1_pt2"]:
				c = ROOT.TCanvas("c_trigeff_" + var2D + "_ref" + reference_trigger + "_test" + test_trigger, "c_trigeff_" + var2D + "_ref" + reference_trigger + "_test" + test_trigger, 800, 600)
				c.SetRightMargin(0.25)
				h_ref = tdf.Get("h_ref" + reference_trigger + "_" + var2D)
				h_test = tdf.Get("h_test" + test_trigger + "_ref" + reference_trigger + "_" + var2D)
				h_eff = h_test.Clone()
				h_eff.SetName(h_test.GetName() + "_eff")
				h_eff.Divide(h_test, h_ref, 1, 1, "B")
				h_eff.Draw("colz")
				c.SaveAs("~/Dijets/data/EightTeeEeVeeBee/TriggerEfficiency/figures/" + c.GetName() + ".pdf")


	f_in.Close()

#def JetLegEfficiencyPlots(h_ref_pt1_vs_pt2, h_test_pt1_vs_pt2, pt_threshold_1, pt_threshold_2):



if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description = 'Trigger efficiency histograms')
	parser.add_argument('input', type=str, help='Input file')
	parser.add_argument('--signal', type=str, help='Signal file')
	parser.add_argument('--signal_xs', type=float, help='Signal xsec')
	args = parser.parse_args()

	output_tag = args.input
	output_tag.replace(".root", "")

	#PrescaleTable(args.input, output_tag)
	EfficiencyPlots(args.input, output_tag)
	#NormVarPlots(args.input, output_tag)
	#
	#if args.signal:
	#	VarPlots(args.input, output_tag, signal_file=args.signal, signal_xs=args.signal_xs)
	#	VarPlots(args.input, output_tag, plot_log=True, signal_file=args.signal, signal_xs=args.signal_xs)
	#else:
	#	VarPlots(args.input, output_tag)
	#	VarPlots(args.input, output_tag, plot_log=True)
	#MjjPlot(args.input, output_tag, plot_log=True)