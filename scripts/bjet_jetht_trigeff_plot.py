import os
import sys
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


print "Loading histograms"
analyses = ["trigmu_highmass_CSVTM", "trigmu_lowmass_CSVTM", "trigmubbh_highmass_CSVTM", "trigmubbl_lowmass_CSVTM", "trigmubbll_lowmass_CSVTM"]
files = {}
for analysis in analyses:
    files[analysis] = ROOT.TFile(analysis_config.get_b_histogram_filename(analysis, "SingleMu_2012"), "READ")

from array import array
mass_bins = array("d", [1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325, 354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 4509, 4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808, 7060, 7320, 7589, 7866, 8000])

variables = ["mjj", "pt1", "pt2", "pt_btag1", "pt_btag2"]
histograms = {}
for analysis in analyses:
    histograms[analysis] = {}
    for variable in variables:
        histograms[analysis][variable] = files[analysis].Get("BHistograms/h_pfjet_" + variable)
        histograms[analysis][variable].SetName("h_" + analysis + "_" + variable)
        histograms[analysis][variable].SetDirectory(0)
        if analysis == "trigmubbll_lowmass":
            histograms[analysis][variable].Scale(1.7) # Prescale
        if variable == "mjj":
            print "(rebinning)...",
            histograms[analysis][variable] = histogram_tools.rebin_histogram(histograms[analysis][variable], mass_bins, normalization_bin_width=1)
            print "(done)"
        elif "pt" in variable:
            histograms[analysis][variable].Rebin(25)

print "Making efficiency histograms"
efficiency_pairs = {
    "highmass":["trigmubbh_highmass_CSVTM", "trigmu_highmass_CSVTM"],
    "lowmass":["trigmubbl_lowmass_CSVTM", "trigmu_lowmass_CSVTM"],
    "llowmass":["trigmubbll_lowmass_CSVTM", "trigmu_lowmass_CSVTM"]
}
efficiency_titles = {"highmass":"160/120", "lowmass":"80/70", "llowmass":"60/53"}
efficiency_colors = {"highmass":"red", "lowmass":"green", "llowmass":"blue"}

efficiency_histograms = {}
for efficiency_name, efficiency_analyses in efficiency_pairs.iteritems():
    efficiency_histograms[efficiency_name] = {}
    for variable in variables:
        efficiency_histograms[efficiency_name][variable] = histograms[efficiency_analyses[0]][variable].Clone()
        efficiency_histograms[efficiency_name][variable].SetName("h_eff_" + efficiency_name + "_" + variable)
        efficiency_histograms[efficiency_name][variable].SetDirectory(0)
        efficiency_histograms[efficiency_name][variable].Divide(histograms[efficiency_analyses[0]][variable], histograms[efficiency_analyses[1]][variable], 1, 1, "B")
        efficiency_histograms[efficiency_name][variable].SetTitle(efficiency_titles[efficiency_name])
        efficiency_histograms[efficiency_name][variable].linecolor = efficiency_colors[efficiency_name]

# Fit mjj efficiency
print "Fitting mjj efficiencies"
guesses = {"highmass":0.5, "lowmass":0.4, "llowmass":0.2}
mjj_ranges = {"highmass":[453, 1455], "lowmass":[419, 1246], "llowmass":[296, 1246]}
efficiency_fits = {}
efficiency_fitratio_histograms = {}
for efficiency_name in efficiency_pairs:
    print "Fitting " + efficiency_name
    efficiency_fits[efficiency_name] = TF1("fit_" + efficiency_name, "[0]", mjj_ranges[efficiency_name][0], mjj_ranges[efficiency_name][1])
    efficiency_fits[efficiency_name].SetParameter(0, guesses[efficiency_name])
    efficiency_fits[efficiency_name].SetParameter(1, 0)
    efficiency_histograms[efficiency_name]["mjj"].Fit(efficiency_fits[efficiency_name], "SR0")
    efficiency_fitratio_histograms[efficiency_name] = efficiency_histograms[efficiency_name]["mjj"].Clone()
    print "[debug] efficiency_fitratio_histograms[efficiency_name] integral = " + str(efficiency_fitratio_histograms[efficiency_name].Integral())
    efficiency_fitratio_histograms[efficiency_name].SetName("efficiency_fitratio_histograms_" + efficiency_name)
    for bin in xrange(1, efficiency_histograms[efficiency_name]["mjj"].GetNbinsX() + 1):
        fit_value = efficiency_fits[efficiency_name].Eval(efficiency_histograms[efficiency_name]["mjj"].GetXaxis().GetBinCenter(bin))
        if efficiency_histograms[efficiency_name]["mjj"].GetBinError(bin) != 0 and efficiency_histograms[efficiency_name]["mjj"].GetXaxis().GetBinCenter(bin) >= 296 and efficiency_histograms[efficiency_name]["mjj"].GetXaxis().GetBinCenter(bin) <= 1058:
            efficiency_fitratio_histograms[efficiency_name].SetBinContent(bin, (efficiency_histograms[efficiency_name]["mjj"].GetBinContent(bin) - fit_value) / efficiency_histograms[efficiency_name]["mjj"].GetBinError(bin))
            efficiency_fitratio_histograms[efficiency_name].SetBinError(bin, 0)
        else:
            efficiency_fitratio_histograms[efficiency_name].SetBinContent(bin, 0)
            efficiency_fitratio_histograms[efficiency_name].SetBinError(bin, 0)

# Load JetHT histograms
print "Loading JetHT histograms from " + analysis_config.dijet_directory + "/data/EightTeeEeVeeBee/TriggerEfficiency/trigeff_jetht_data.root"
f_jetht = TFile(analysis_config.dijet_directory + "/data/EightTeeEeVeeBee/TriggerEfficiency/trigeff_jetht_data.root", "READ")
efficiency_histograms["jetht_lowmass"] = {"mjj":f_jetht.Get("h_trigeff_jetht_lowmass").Clone()}
efficiency_histograms["jetht_lowmass"]["mjj"].SetDirectory(0)
efficiency_fits["jetht_lowmass"] = TF1("fit_jetht_lowmass", "[0]", 296, 1246)
efficiency_histograms["jetht_lowmass"]["mjj"].Fit(efficiency_fits["jetht_lowmass"], "SR0")
efficiency_histograms["jetht_highmass"] = {"mjj":f_jetht.Get("h_trigeff_jetht_highmass").Clone()}
efficiency_histograms["jetht_highmass"]["mjj"].SetDirectory(0)
efficiency_fits["jetht_highmass"] = TF1("fit_jetht_highmass", "[0]", 526, 1455)
efficiency_histograms["jetht_highmass"]["mjj"].Fit(efficiency_fits["jetht_highmass"], "SR0")
f_jetht.Close()

# Scale efficiency histograms using the linear fits
normalized_efficiency_histograms = {}
for efficiency_name, efficiency_histogram_var in efficiency_histograms.iteritems():
	normalized_efficiency_histograms[efficiency_name] = efficiency_histogram_var["mjj"].Clone()
	normalized_efficiency_histograms[efficiency_name].Scale(1. / efficiency_fits[efficiency_name].GetParameter(0))

# mjj trigger efficiency plots
print "Making c_trigeff_singlemu_vs_jetht_lowmass_data"
c_lowmass = TCanvas("c_trigeff_singlemu_vs_jetht_lowmass_data", "c_trigeff_singlemu_vs_jetht_lowmass_data", 800, 600)
l = TLegend(0.2, 0.7, 0.4, 0.88)
l.SetFillColor(0)
l.SetBorderSize(0)
frame_lowmass = TH1F("frame_lowmass", "frame_lowmass", 100, 0., 1400.)
frame_lowmass.GetXaxis().SetTitle("m_{jj} [GeV]")
frame_lowmass.GetYaxis().SetTitle("Relative #epsilon_{b tag}^{online} / #LT #epsilon_{b tag}^{online} #GT")
frame_lowmass.SetMinimum(0.)
frame_lowmass.SetMaximum(3.)
frame_lowmass.Draw("axis")
normalized_efficiency_histograms["llowmass"].SetMarkerSize(1)
normalized_efficiency_histograms["llowmass"].SetMarkerColor(seaborn.GetColorRoot("default", 1))
normalized_efficiency_histograms["llowmass"].SetMarkerStyle(20)
normalized_efficiency_histograms["llowmass"].SetLineColor(seaborn.GetColorRoot("default", 1))
normalized_efficiency_histograms["llowmass"].SetLineWidth(2)
normalized_efficiency_histograms["llowmass"].Draw("same")
l.AddEntry(normalized_efficiency_histograms["llowmass"], "SingleMu", "lp")
normalized_efficiency_histograms["jetht_lowmass"].SetMarkerSize(1)
normalized_efficiency_histograms["jetht_lowmass"].SetMarkerColor(seaborn.GetColorRoot("default", 2))
normalized_efficiency_histograms["jetht_lowmass"].SetMarkerStyle(21)
normalized_efficiency_histograms["jetht_lowmass"].SetLineColor(seaborn.GetColorRoot("default", 2))
normalized_efficiency_histograms["jetht_lowmass"].SetLineWidth(2)
normalized_efficiency_histograms["jetht_lowmass"].Draw("same")
l.AddEntry(normalized_efficiency_histograms["jetht_lowmass"], "JetHT", "lp")
l.Draw()
c_lowmass.SaveAs(analysis_config.figure_directory + "/" + c_lowmass.GetName() + ".pdf")

print "Making c_trigeff_singlemu_vs_jetht_highmass_data"
c_highmass = TCanvas("c_trigeff_singlemu_vs_jetht_highmass_data", "c_trigeff_singlemu_vs_jetht_highmass_data", 800, 600)
frame_highmass = TH1F("frame_highmass", "frame_highmass", 100, 0., 1800.)
frame_highmass.GetXaxis().SetTitle("m_{jj} [GeV]")
frame_highmass.GetYaxis().SetTitle("Relative #epsilon_{b tag}^{online} / #langle #epsilon_{b tag}^{online} #rangle")
frame_highmass.SetMinimum(0.)
frame_highmass.SetMaximum(3.)
frame_highmass.Draw("axis")
normalized_efficiency_histograms["highmass"].SetMarkerSize(1)
normalized_efficiency_histograms["highmass"].SetMarkerColor(seaborn.GetColorRoot("default", 1))
normalized_efficiency_histograms["highmass"].SetMarkerStyle(20)
normalized_efficiency_histograms["highmass"].SetLineColor(seaborn.GetColorRoot("default", 1))
normalized_efficiency_histograms["highmass"].SetLineWidth(2)
normalized_efficiency_histograms["highmass"].Draw("same")
normalized_efficiency_histograms["jetht_highmass"].SetMarkerSize(1)
normalized_efficiency_histograms["jetht_highmass"].SetMarkerColor(seaborn.GetColorRoot("default", 2))
normalized_efficiency_histograms["jetht_highmass"].SetMarkerStyle(21)
normalized_efficiency_histograms["jetht_highmass"].SetLineColor(seaborn.GetColorRoot("default", 2))
normalized_efficiency_histograms["jetht_highmass"].SetLineWidth(2)
normalized_efficiency_histograms["jetht_highmass"].Draw("same")
l.Draw()
c_highmass.SaveAs(analysis_config.figure_directory + "/" + c_highmass.GetName() + ".pdf")

# SingleMu efficiencies only, vs all variables
for var in ["mjj", "pt1", "pt2", "pt_btag1", "pt_btag2"]:
	for sr in ["llowmass", "lowmass", "highmass"]:
		print "Making " + "c_trigeff_singlemu_" + sr + "_" + var
		c = TCanvas("c_trigeff_singlemu_" + sr + "_" + var, "c_trigeff_singlemu_" + sr + "_" + var, 800, 600)
		l = TLegend(0.2, 0.75, 0.4, 0.9)
		l.SetFillColor(0)
		l.SetBorderSize(0)
		if var == "mjj":
			frame = TH1F("frame_" + var + "_" + sr, "frame_" + var + "_" + sr, 100, 0., 2000.)
		else:
			frame = TH1F("frame_" + var + "_" + sr, "frame_" + var + "_" + sr, 100, 0., 1000.)
		frame.SetMinimum(0.)
		if sr == "llowmass":
			frame.SetMaximum(0.15)
		elif sr == "lowmass":
			frame.SetMaximum(0.5)
		elif sr == "highmass":
			frame.SetMaximum(0.8)
		frame.Draw("axis")
		if var == "mjj":
			frame.GetXaxis().SetTitle("m_{jj} [GeV]")
		elif var == "pt1":
			frame.GetXaxis().SetTitle("p_{T} (leading) [GeV]")
		elif var == "pt2":
			frame.GetXaxis().SetTitle("p_{T} (subleading) [GeV]")
		elif var == "pt_btag1":
			frame.GetXaxis().SetTitle("p_{T} (leading CSV) [GeV]")
		elif var == "pt_btag2":
			frame.GetXaxis().SetTitle("p_{T} (subleading CSV) [GeV]")
		frame.GetYaxis().SetTitle("Relative #epsilon_{b tag}^{online}")
		frame.Draw("axis")
		efficiency_histograms[sr][var].SetMarkerSize(1)
		efficiency_histograms[sr][var].SetMarkerColor(seaborn.GetColorRoot("default", 1))
		efficiency_histograms[sr][var].SetMarkerStyle(20)
		efficiency_histograms[sr][var].SetLineColor(seaborn.GetColorRoot("default", 1))
		efficiency_histograms[sr][var].SetLineWidth(2)
		efficiency_histograms[sr][var].Draw("same")
		l.AddEntry(efficiency_histograms[sr][var], "SingleMu", "lp")
		l.Draw()
		c.SaveAs(analysis_config.figure_directory + "/" + c.GetName() + ".pdf")
