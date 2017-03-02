from ROOT import *
gSystem.Load("~/Dijets/CMSSW_5_3_32_patch3/lib/slc6_amd64_gcc472/libMyToolsRootUtils.so")
import CMSDIJET.QCDAnalysis.analysis_configuration_8TeV as analysis_config

# Combine the QCD MC samples with appropriate weights
qcd_samples = ["QCD_Pt-80to120_TuneZ2star_8TeV_pythia6","QCD_Pt-120to170_TuneZ2star_8TeV_pythia6","QCD_Pt-170to300_TuneZ2star_8TeV_pythia6","QCD_Pt-300to470_TuneZ2star_8TeV_pythia6","QCD_Pt-470to600_TuneZ2star_8TeV_pythia6","QCD_Pt-600to800_TuneZ2star_8TeV_pythia6","QCD_Pt-800to1000_TuneZ2star_8TeV_pythia6","QCD_Pt-1000to1400_TuneZ2star_8TeV_pythia6","QCD_Pt-1400to1800_TuneZ2star_8TeV_pythia6","QCD_Pt-1800_TuneZ2star_8TeV_pythia6"]
analyses = ["NoTrigger_eta2p2", "NoTrigger_eta2p2_CSVTM", "NoTrigger_eta1p7", "NoTrigger_eta1p7_CSVTM", "trigbbl_CSVTM", "trigbbh_CSVTM"]

lumi = 19710.

for analysis in analyses:
	first = True
	output_file = TFile(analysis_config.get_b_histogram_filename(analysis, "QCD_TuneZ2star_8TeV_pythia6"), "RECREATE")
	output_directory = output_file.mkdir("BHistograms")
	histograms = {}
	for sample in qcd_samples:
		input_file = TFile(analysis_config.get_b_histogram_filename(analysis, sample), "READ")
		input_directory = input_file.Get("BHistograms")
		input_directory.cd()
		xsec = analysis_config.simulation.background_cross_sections[sample]
		normalization = xsec * lumi / input_file.Get("BHistograms/h_sample_nevents").Integral()
		for key in gDirectory.GetListOfKeys():
			key.Print()
			if "TH1" in key.GetClassName() or "TH2" in key.GetClassName():
				hist = key.ReadObj()
				hist.Scale(normalization)
				if first:
					histograms[hist.GetName()] = hist
					histograms[hist.GetName()].SetDirectory(output_directory)
				else:
					histograms[hist.GetName()].Add(hist)
		first = False
	output_directory.cd()
	for hist in histograms.values():
		hist.Write()
