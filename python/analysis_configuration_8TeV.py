import os
import sys
sys.path.append(os.path.expandvars("$CMSSW_BASE/python/CMSDIJET/QCDAnalysis"))
import simulation_configuration_8TeV as simulation

dijet_directory = os.path.expandvars("$DIJETHOME")

# Data samples
data_samples = ["MultiJet_2012A", "BJetPlusX_2012B", "BJetPlusX_2012C", "BJetPlusX_2012D", "JetHT_2012B", "JetHT_2012C", "JetHT_2012D", "SingleMu_2012A", "SingleMu_2012B", "SingleMu_2012C", "SingleMu_2012D"]
data_supersamples = {}
data_supersamples["BJetPlusX_2012"] = ["MultiJet_2012A", "BJetPlusX_2012B", "BJetPlusX_2012C", "BJetPlusX_2012D"]
data_supersamples["BJetPlusXJEC13_2012"] = ["MultiJetJEC13_2012A", "BJetPlusXJEC13_2012B", "BJetPlusXJEC13_2012C", "BJetPlusXJEC13_2012D"]
data_supersamples["BJetPlusX_2012BCD"] = ["BJetPlusX_2012B", "BJetPlusX_2012C", "BJetPlusX_2012D"]
data_supersamples["JetHT_2012BCD"] = ["JetHT_2012B", "JetHT_2012C", "JetHT_2012D"]
data_supersamples["SingleMu_2012"] = ["SingleMu_2012A", "SingleMu_2012B", "SingleMu_2012C", "SingleMu_2012D"]

# Skimmed trees
# - Data files are stored in .txt files (they have thousands of files, and reside on EOS)
files_QCDBEventTree = {
	"MultiJet_2012A":dijet_directory + "/data/EightTeeEeVeeBee/Results/condor/QCDBEventTree_MultiJet_Run2012A_v1_4.txt",
	"BJetPlusX_2012B":dijet_directory + "/data/EightTeeEeVeeBee/Results/condor/QCDBEventTree_BJetPlusX_Run2012B_v1_4.txt",
	"BJetPlusX_2012C":dijet_directory + "/data/EightTeeEeVeeBee/Results/condor/QCDBEventTree_BJetPlusX_Run2012C_v1_4.txt",
	"BJetPlusX_2012D":dijet_directory + "/data/EightTeeEeVeeBee/Results/condor/QCDBEventTree_BJetPlusX_Run2012D_v1_4.txt",
	"MultiJetJEC13_2012A":dijet_directory + "/data/EightTeeEeVeeBee/Results/condor/QCDBEventTree_MultiJet_Run2012A_v2_0.txt",
	"BJetPlusXJEC13_2012B":dijet_directory + "/data/EightTeeEeVeeBee/Results/condor/QCDBEventTree_BJetPlusX_Run2012B_v2_0.txt",
	"BJetPlusXJEC13_2012C":dijet_directory + "/data/EightTeeEeVeeBee/Results/condor/QCDBEventTree_BJetPlusX_Run2012C_v2_0.txt",
	"BJetPlusXJEC13_2012D":dijet_directory + "/data/EightTeeEeVeeBee/Results/condor/QCDBEventTree_BJetPlusX_Run2012D_v2_0.txt",
	"JetHT_2012B":dijet_directory + "/data/EightTeeEeVeeBee/Results/condor/QCDBEventTree_JetHT_Run2012B_v1_4_1.txt",
	"JetHT_2012C":dijet_directory + "/data/EightTeeEeVeeBee/Results/condor/QCDBEventTree_JetHT_Run2012C_v1_4_1.txt",
	"JetHT_2012D":dijet_directory + "/data/EightTeeEeVeeBee/Results/condor/QCDBEventTree_JetHT_Run2012D_v1_4_1.txt",
	"SingleMu_2012A":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_SingleMu_Run2012A_v2_1_2.txt",
	"SingleMu_2012B":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_SingleMu_Run2012B_v2_1_2.txt",
	"SingleMu_2012C":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_SingleMu_Run2012C_v2_1_2.txt",
	"SingleMu_2012D":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_SingleMu_Run2012D_v2_1_2.txt",

	# Signal MCRSGravitonToBBbar_M_300_TuneZ2star_8TeV_pythia8_FULLSIM
	# Private production, on CMS LPC
	#"RSGravitonToBBbar_M_250_TuneZ2star_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_RSGravitonToBBbar_M_250_TuneZ2star_8TeV_pythia8_FULLSIM.txt",
	#"RSGravitonToBBbar_M_300_TuneZ2star_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_RSGravitonToBBbar_M_300_TuneZ2star_8TeV_pythia8_FULLSIM.txt",
	#"RSGravitonToBBbar_M_400_TuneZ2star_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_RSGravitonToBBbar_M_400_TuneZ2star_8TeV_pythia8_FULLSIM.txt",
	#"RSGravitonToBBbar_M_500_TuneZ2star_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_RSGravitonToBBbar_M_500_TuneZ2star_8TeV_pythia8_FULLSIM.txt",
	#"RSGravitonToBBbar_M_600_TuneZ2star_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_RSGravitonToBBbar_M_600_TuneZ2star_8TeV_pythia8_FULLSIM.txt",
	#"RSGravitonToBBbar_M_750_TuneZ2star_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_RSGravitonToBBbar_M_750_TuneZ2star_8TeV_pythia8_FULLSIM.txt",
	#"RSGravitonToBBbar_M_900_TuneZ2star_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_RSGravitonToBBbar_M_900_TuneZ2star_8TeV_pythia8_FULLSIM.txt",
	#"RSGravitonToBBbar_M_1200_TuneZ2star_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_RSGravitonToBBbar_M_1200_TuneZ2star_8TeV_pythia8_FULLSIM.txt",
	#"GluGluSpin0ToBBbar_M_250_TuneCUEP8M1_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_GluGluSpin0ToBBbar_M_250_TuneCUEP8M1_8TeV_pythia8_FULLSIM.txt",
	#"GluGluSpin0ToBBbar_M_300_TuneCUEP8M1_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_GluGluSpin0ToBBbar_M_300_TuneCUEP8M1_8TeV_pythia8_FULLSIM.txt",
	#"GluGluSpin0ToBBbar_M_400_TuneCUEP8M1_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_GluGluSpin0ToBBbar_M_400_TuneCUEP8M1_8TeV_pythia8_FULLSIM.txt",
	#"GluGluSpin0ToBBbar_M_500_TuneCUEP8M1_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_GluGluSpin0ToBBbar_M_500_TuneCUEP8M1_8TeV_pythia8_FULLSIM.txt",
	#"GluGluSpin0ToBBbar_M_600_TuneCUEP8M1_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_GluGluSpin0ToBBbar_M_600_TuneCUEP8M1_8TeV_pythia8_FULLSIM.txt",
	#"GluGluSpin0ToBBbar_M_750_TuneCUEP8M1_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_GluGluSpin0ToBBbar_M_750_TuneCUEP8M1_8TeV_pythia8_FULLSIM.txt",
	#"GluGluSpin0ToBBbar_M_900_TuneCUEP8M1_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_GluGluSpin0ToBBbar_M_900_TuneCUEP8M1_8TeV_pythia8_FULLSIM.txt",
	#"GluGluSpin0ToBBbar_M_1200_TuneCUEP8M1_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_GluGluSpin0ToBBbar_M_1200_TuneCUEP8M1_8TeV_pythia8_FULLSIM.txt",
	"RSGravitonToBBbar_kMpl01_M_350_TuneCUEP8M1_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_RSG_350.txt",
	"RSGravitonToBBbar_kMpl01_M_400_TuneCUEP8M1_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_RSGravToBBbar_M-400_JEC13.txt",
	"RSGravitonToBBbar_kMpl01_M_500_TuneCUEP8M1_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_RSGravToBBbar_M-500_JEC13.txt",
	"RSGravitonToBBbar_kMpl01_M_600_TuneCUEP8M1_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_RSGravToBBbar_M-600_JEC13.txt",
	"RSGravitonToBBbar_kMpl01_M_750_TuneCUEP8M1_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_RSGravToBBbar_M-750_JEC13.txt",
	"RSGravitonToBBbar_kMpl01_M_900_TuneCUEP8M1_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_RSGravToBBbar_M-900_JEC13.txt",
	"RSGravitonToBBbar_kMpl01_M_1200_TuneCUEP8M1_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_RSGravToBBbar_M-1200_JEC13.txt",
	"GluGluSpin0ToBBbar_M_350_TuneCUEP8M1_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_Hbb_350.txt",
	"GluGluSpin0ToBBbar_M_400_TuneCUEP8M1_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_GluGluSpin0ToBBbar_M-400_JEC13.txt",
	"GluGluSpin0ToBBbar_M_500_TuneCUEP8M1_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_GluGluSpin0ToBBbar_M-500_JEC13.txt",
	"GluGluSpin0ToBBbar_M_600_TuneCUEP8M1_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_GluGluSpin0ToBBbar_M-600_JEC13.txt",
	"GluGluSpin0ToBBbar_M_750_TuneCUEP8M1_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_GluGluSpin0ToBBbar_M-750_JEC13.txt",
	"GluGluSpin0ToBBbar_M_900_TuneCUEP8M1_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_GluGluSpin0ToBBbar_M-900_JEC13.txt",
	"GluGluSpin0ToBBbar_M_1200_TuneCUEP8M1_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_GluGluSpin0ToBBbar_M-1200_JEC13.txt",
	"ZPrimeToCCBB_M_350_g0p25_TuneCUEP8M1_8TeV_MadgraphPythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_ZPrime_350.txt",
	"ZPrimeToCCBB_M_400_g0p25_TuneCUEP8M1_8TeV_MadgraphPythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_ZPrime_400.txt",
	"ZPrimeToCCBB_M_500_g0p25_TuneCUEP8M1_8TeV_MadgraphPythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_ZPrime_500.txt",
	"ZPrimeToCCBB_M_600_g0p25_TuneCUEP8M1_8TeV_MadgraphPythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_ZPrime_600.txt",
	"ZPrimeToCCBB_M_750_g0p25_TuneCUEP8M1_8TeV_MadgraphPythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_ZPrime_750.txt",
	"ZPrimeToCCBB_M_900_g0p25_TuneCUEP8M1_8TeV_MadgraphPythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_ZPrime_900.txt",
	"ZPrimeToCCBB_M_1200_g0p25_TuneCUEP8M1_8TeV_MadgraphPythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_ZPrime_1200.txt",


	# Old RSG with incorrect PDF in name. 
	"RSGravitonToBBbar_M_400_TuneZ2star_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_RSGravToBBbar_M-400_TuneCUETP8M1_8TeV-pythia8_FULLSIM.txt",
	"RSGravitonToBBbar_M_500_TuneZ2star_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_RSGravToBBbar_M-500_TuneCUETP8M1_8TeV-pythia8_FULLSIM.txt",
	"RSGravitonToBBbar_M_600_TuneZ2star_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_RSGravToBBbar_M-600_TuneCUETP8M1_8TeV-pythia8_FULLSIM.txt",
	"RSGravitonToBBbar_M_750_TuneZ2star_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_RSGravToBBbar_M-750_TuneCUETP8M1_8TeV-pythia8_FULLSIM.txt",
	"RSGravitonToBBbar_M_900_TuneZ2star_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_RSGravToBBbar_M-900_TuneCUETP8M1_8TeV-pythia8_FULLSIM.txt",
	"RSGravitonToBBbar_M_1200_TuneZ2star_8TeV_pythia8_FULLSIM":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_RSGravToBBbar_M-1200_TuneCUETP8M1_8TeV-pythia8_FULLSIM.txt",

	 
	# Background
	"QCD_Pt-50To150_bEnriched_TuneZ2star_8TeV-pythia6-evtgen":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_QCD_Pt-50To150_bEnriched_TuneZ2star_8TeV-pythia6-evtgen.txt",
	"QCD_Pt-15To30_bEnriched_TuneZ2star_8TeV-pythia6-evtgen":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_QCD_Pt-15To30_bEnriched_TuneZ2star_8TeV-pythia6-evtgen.txt",
	"QCD_Pt-30To50_bEnriched_TuneZ2star_8TeV-pythia6-evtgen":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_QCD_Pt-30To50_bEnriched_TuneZ2star_8TeV-pythia6-evtgen.txt",
	"QCD_Pt-1000to1400_TuneZ2star_8TeV_pythia6":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_QCD_Pt-1000to1400_TuneZ2star_8TeV_pythia6.txt",
	"QCD_Pt-120to170_TuneZ2star_8TeV_pythia6":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_QCD_Pt-120to170_TuneZ2star_8TeV_pythia6.txt",
	"QCD_Pt-1400to1800_TuneZ2star_8TeV_pythia6":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_QCD_Pt-1400to1800_TuneZ2star_8TeV_pythia6.txt",
	"QCD_Pt-170to300_TuneZ2star_8TeV_pythia6":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_QCD_Pt-170to300_TuneZ2star_8TeV_pythia6.txt",
	"QCD_Pt-1800_TuneZ2star_8TeV_pythia6":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_QCD_Pt-1800_TuneZ2star_8TeV_pythia6.txt",
	"QCD_Pt-300to470_TuneZ2star_8TeV_pythia6":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_QCD_Pt-300to470_TuneZ2star_8TeV_pythia6.txt",
	"QCD_Pt-470to600_TuneZ2star_8TeV_pythia6":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_QCD_Pt-470to600_TuneZ2star_8TeV_pythia6.txt",
	"QCD_Pt-600to800_TuneZ2star_8TeV_pythia6":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_QCD_Pt-600to800_TuneZ2star_8TeV_pythia6.txt",
	"QCD_Pt-800to1000_TuneZ2star_8TeV_pythia6":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_QCD_Pt-800to1000_TuneZ2star_8TeV_pythia6.txt",
	"QCD_Pt-80to120_TuneZ2star_8TeV_pythia6":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/QCDBEventTree_QCD_Pt-80to120_TuneZ2star_8TeV_pythia6.txt",

	"TTJets_Hadronic":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/TTJets_Had.txt",
	"TTJets_SemiLept":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/TTJets_SemiLep.txt",
	"TTJets_Leptonic":dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/TTJets_Lep.txt",
}
#for sample_name, sample_file_list in file_lists_QCDBEventTree.iteritems():
#	f = open(sample_file_list, 'r')
#	files_QCDBEventTree[sample_name] = []
#	for line in f:
#		files_QCDBEventTree[sample_name].append(line.rstrip())
# - MC files: only 1 per sample, so no need for .txt files
#files_QCDBEventTree["RSGravitonToBBbar_M_200_TuneZ2star_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_200_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
#files_QCDBEventTree["RSGravitonToBBbar_M_250_TuneZ2star_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_250_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
#files_QCDBEventTree["RSGravitonToBBbar_M_300_TuneZ2star_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_300_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
#files_QCDBEventTree["RSGravitonToBBbar_M_350_TuneZ2star_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_350_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
#files_QCDBEventTree["RSGravitonToBBbar_M_400_TuneZ2star_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_400_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
#files_QCDBEventTree["RSGravitonToBBbar_M_450_TuneZ2star_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_450_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
#files_QCDBEventTree["RSGravitonToBBbar_M_500_TuneZ2star_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_500_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
#files_QCDBEventTree["RSGravitonToBBbar_M_550_TuneZ2star_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_550_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
#files_QCDBEventTree["RSGravitonToBBbar_M_600_TuneZ2star_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_600_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
#files_QCDBEventTree["RSGravitonToBBbar_M_650_TuneZ2star_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_650_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
#files_QCDBEventTree["RSGravitonToBBbar_M_700_TuneZ2star_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_700_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
#files_QCDBEventTree["RSGravitonToBBbar_M_750_TuneZ2star_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_750_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
#files_QCDBEventTree["RSGravitonToBBbar_M_800_TuneZ2star_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_800_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
#files_QCDBEventTree["RSGravitonToBBbar_M_850_TuneZ2star_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_850_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
#files_QCDBEventTree["RSGravitonToBBbar_M_900_TuneZ2star_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_900_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
#files_QCDBEventTree["RSGravitonToBBbar_M_950_TuneZ2star_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_950_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
#files_QCDBEventTree["RSGravitonToBBbar_M_1000_TuneZ2star_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_1000_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
#files_QCDBEventTree["RSGravitonToBBbar_M_1050_TuneZ2star_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_1050_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
#files_QCDBEventTree["RSGravitonToBBbar_M_1100_TuneZ2star_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_1100_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
#files_QCDBEventTree["RSGravitonToBBbar_M_1150_TuneZ2star_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_1150_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
#files_QCDBEventTree["RSGravitonToBBbar_M_1200_TuneZ2star_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_1200_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
#files_QCDBEventTree["ZprimeToBB_M_200_TuneD6T_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_200_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
#files_QCDBEventTree["ZprimeToBB_M_250_TuneD6T_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_250_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
#files_QCDBEventTree["ZprimeToBB_M_300_TuneD6T_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_300_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
#files_QCDBEventTree["ZprimeToBB_M_350_TuneD6T_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_350_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
#files_QCDBEventTree["ZprimeToBB_M_400_TuneD6T_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_400_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
#files_QCDBEventTree["ZprimeToBB_M_450_TuneD6T_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_450_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
#files_QCDBEventTree["ZprimeToBB_M_500_TuneD6T_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_500_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
#files_QCDBEventTree["ZprimeToBB_M_550_TuneD6T_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_550_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
#files_QCDBEventTree["ZprimeToBB_M_600_TuneD6T_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_600_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
#files_QCDBEventTree["ZprimeToBB_M_650_TuneD6T_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_650_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
#files_QCDBEventTree["ZprimeToBB_M_700_TuneD6T_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_700_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
#files_QCDBEventTree["ZprimeToBB_M_750_TuneD6T_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_750_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
#files_QCDBEventTree["ZprimeToBB_M_800_TuneD6T_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_800_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
#files_QCDBEventTree["ZprimeToBB_M_850_TuneD6T_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_850_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
#files_QCDBEventTree["ZprimeToBB_M_900_TuneD6T_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_900_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
#files_QCDBEventTree["ZprimeToBB_M_950_TuneD6T_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_950_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
#files_QCDBEventTree["ZprimeToBB_M_1000_TuneD6T_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_1000_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
#files_QCDBEventTree["ZprimeToBB_M_1050_TuneD6T_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_1050_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
#files_QCDBEventTree["ZprimeToBB_M_1100_TuneD6T_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_1100_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
#files_QCDBEventTree["ZprimeToBB_M_1150_TuneD6T_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_1150_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
#files_QCDBEventTree["ZprimeToBB_M_1200_TuneD6T_8TeV_pythia6_FASTSIM"] = dijet_directory + "/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_1200_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"

# Histogram files
b_histogram_directory = dijet_directory + "/data/EightTeeEeVeeBee/BHistograms"
def get_b_histogram_filename(analysis, sample):
	return b_histogram_directory + "/BHistograms_" + analysis + "_" + sample + ".root"
#files_BHistograms = {}
#files_BHistograms["BJetPlusX_2012"] = dijet_directory + "/data/EightTeeEeVeeBee/Results/InclusiveBHistograms_2012.root"
#files_BHistograms["BJetPlusX_2012BCD"] = dijet_directory + "/data/EightTeeEeVeeBee/Results/InclusiveBHistograms_BJetPlusX_2012BCD.root"
#files_BHistograms["JetHT_2012BCD"] = dijet_directory + "/data/EightTeeEeVeeBee/Results/InclusiveBHistograms_JetHT_2012BCD.root"
#files_BHistograms["InclusiveBHistograms_BJetPlusX_tight_2012BCDCD"] = dijet_directory + "/data/EightTeeEeVeeBee/Results/InclusiveBHistograms_BJetPlusX_tight_2012BCD.root"
#files_BHistograms["JetHT_tight_2012BCD"] = dijet_directory + "/data/EightTeeEeVeeBee/Results/InclusiveBHistograms_JetHT_tight_2012BCD.root"

# Figures
figure_directory = dijet_directory + "/data/EightTeeEeVeeBee/Results/figures/"


# Analyses
analysis_cfgs = {}
analysis_cfgs["trigbbh_CSVL"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigbbh_CSVL_cfg.py"
analysis_cfgs["trigbbh_CSVM"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigbbh_CSVM_cfg.py"
analysis_cfgs["trigbbh_CSVT"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigbbh_CSVT_cfg.py"
analysis_cfgs["trigbbh_CSVTM"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigbbh_CSVTM_cfg.py"
analysis_cfgs["trigbbh_CSVTL"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigbbh_CSVTL_cfg.py"
analysis_cfgs["trigbbh_CSVML"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigbbh_CSVML_cfg.py"
analysis_cfgs["trigbbhl_CSVTM"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigbbhl_CSVTM_cfg.py"
analysis_cfgs["trigbbl_CSVL"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigbbl_CSVL_cfg.py"
analysis_cfgs["trigbbl_CSVM"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigbbl_CSVM_cfg.py"
analysis_cfgs["trigbbl_CSVT"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigbbl_CSVT_cfg.py"
analysis_cfgs["trigbbl_CSVTM"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigbbl_CSVTM_cfg.py"
analysis_cfgs["trigbbl_CSVTL"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigbbl_CSVTL_cfg.py"
analysis_cfgs["trigbbl_CSVML"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigbbl_CSVML_cfg.py"
analysis_cfgs["trigbbll_CSVTM"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigbbll_CSVTM_cfg.py"
analysis_cfgs["trigbbll_CSVM"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigbbll_CSVM_cfg.py"
analysis_cfgs["trigbbl_raw"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigbbl_raw_cfg.py"
analysis_cfgs["trigbbh_trigbbl_CSVTM"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigbbh_trigbbl_CSVTM_cfg.py"
analysis_cfgs["trigbbh_trigbbl_CSVM"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigbbh_trigbbl_CSVM_cfg.py"

analysis_cfgs["trigeff_trigbbh_CSVL"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BTriggerEfficiency_trigbbh_CSVL_cfg.py"
analysis_cfgs["trigeff_trigbbl_CSVL"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BTriggerEfficiency_trigbbl_CSVL_cfg.py"
analysis_cfgs["trigeff_trigbbh_CSVM"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BTriggerEfficiency_trigbbh_CSVM_cfg.py"
analysis_cfgs["trigeff_trigbbl_CSVM"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BTriggerEfficiency_trigbbl_CSVM_cfg.py"
analysis_cfgs["trigeff_trigbbh_CSVT"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BTriggerEfficiency_trigbbh_CSVT_cfg.py"
analysis_cfgs["trigeff_trigbbl_CSVT"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BTriggerEfficiency_trigbbl_CSVT_cfg.py"
analysis_cfgs["trigeff_trigbbh_CSVTM"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BTriggerEfficiency_trigbbh_CSVTM_cfg.py"
analysis_cfgs["trigeff_trigbbl_CSVTM"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BTriggerEfficiency_trigbbl_CSVTM_cfg.py"
analysis_cfgs["trigjetht_CSVL"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht_CSVL_cfg.py"
analysis_cfgs["trigjetht_CSVM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht_CSVM_cfg.py"
analysis_cfgs["trigjetht_CSVT"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht_CSVT_cfg.py"
analysis_cfgs["trigjetht_CSVML"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht_CSVML_cfg.py"
analysis_cfgs["trigjetht_CSVTL"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht_CSVTL_cfg.py"
analysis_cfgs["trigjetht_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht_CSVTM_cfg.py"
analysis_cfgs["trigjetht_eta1p7_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht_eta1p7_CSVTM_cfg.py"
analysis_cfgs["trigjetht_eta1p7_CSVM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht_eta1p7_CSVM_cfg.py"

analysis_cfgs["trigjetht200_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht200_CSVTM_cfg.py"
analysis_cfgs["trigjetht250_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht250_CSVTM_cfg.py"
analysis_cfgs["trigjetht300_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht300_CSVTM_cfg.py"
analysis_cfgs["trigjetht350_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht350_CSVTM_cfg.py"
analysis_cfgs["trigjetht400_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht400_CSVTM_cfg.py"
analysis_cfgs["trigjetht450_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht450_CSVTM_cfg.py"
analysis_cfgs["trigjetht500_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht500_CSVTM_cfg.py"
analysis_cfgs["trigjetht550_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht550_CSVTM_cfg.py"
analysis_cfgs["trigjetht650_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht650_CSVTM_cfg.py"

analysis_cfgs["trigjetht200_CSVM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht200_CSVM_cfg.py"
analysis_cfgs["trigjetht250_CSVM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht250_CSVM_cfg.py"
analysis_cfgs["trigjetht300_CSVM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht300_CSVM_cfg.py"
analysis_cfgs["trigjetht350_CSVM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht350_CSVM_cfg.py"
analysis_cfgs["trigjetht400_CSVM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht400_CSVM_cfg.py"
analysis_cfgs["trigjetht450_CSVM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht450_CSVM_cfg.py"
analysis_cfgs["trigjetht500_CSVM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht500_CSVM_cfg.py"
analysis_cfgs["trigjetht550_CSVM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht550_CSVM_cfg.py"
analysis_cfgs["trigjetht650_CSVM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht650_CSVM_cfg.py"

analysis_cfgs["trigjetht200"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht200_cfg.py"
analysis_cfgs["trigjetht250"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht250_cfg.py"
analysis_cfgs["trigjetht300"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht300_cfg.py"
analysis_cfgs["trigjetht350"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht350_cfg.py"
analysis_cfgs["trigjetht400"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht400_cfg.py"
analysis_cfgs["trigjetht450"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht450_cfg.py"
analysis_cfgs["trigjetht500"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht500_cfg.py"
analysis_cfgs["trigjetht550"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht550_cfg.py"
analysis_cfgs["trigjetht650"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht650_cfg.py"
analysis_cfgs["trigjetht"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht_cfg.py"

analysis_cfgs["trigjetht200_eta1p7_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht200_eta1p7_CSVTM_cfg.py"
analysis_cfgs["trigjetht250_eta1p7_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht250_eta1p7_CSVTM_cfg.py"
analysis_cfgs["trigjetht300_eta1p7_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht300_eta1p7_CSVTM_cfg.py"
analysis_cfgs["trigjetht350_eta1p7_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht350_eta1p7_CSVTM_cfg.py"
analysis_cfgs["trigjetht400_eta1p7_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht400_eta1p7_CSVTM_cfg.py"
analysis_cfgs["trigjetht450_eta1p7_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht450_eta1p7_CSVTM_cfg.py"
analysis_cfgs["trigjetht500_eta1p7_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht500_eta1p7_CSVTM_cfg.py"
analysis_cfgs["trigjetht550_eta1p7_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht550_eta1p7_CSVTM_cfg.py"
analysis_cfgs["trigjetht650_eta1p7_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht650_eta1p7_CSVTM_cfg.py"

analysis_cfgs["trigjetht200_eta1p7_CSVM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht200_eta1p7_CSVM_cfg.py"
analysis_cfgs["trigjetht250_eta1p7_CSVM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht250_eta1p7_CSVM_cfg.py"
analysis_cfgs["trigjetht300_eta1p7_CSVM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht300_eta1p7_CSVM_cfg.py"
analysis_cfgs["trigjetht350_eta1p7_CSVM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht350_eta1p7_CSVM_cfg.py"
analysis_cfgs["trigjetht400_eta1p7_CSVM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht400_eta1p7_CSVM_cfg.py"
analysis_cfgs["trigjetht450_eta1p7_CSVM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht450_eta1p7_CSVM_cfg.py"
analysis_cfgs["trigjetht500_eta1p7_CSVM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht500_eta1p7_CSVM_cfg.py"
analysis_cfgs["trigjetht550_eta1p7_CSVM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht550_eta1p7_CSVM_cfg.py"
analysis_cfgs["trigjetht650_eta1p7_CSVM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht650_eta1p7_CSVM_cfg.py"

analysis_cfgs["trigjetht200_eta1p7"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht200_eta1p7_cfg.py"
analysis_cfgs["trigjetht250_eta1p7"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht250_eta1p7_cfg.py"
analysis_cfgs["trigjetht300_eta1p7"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht300_eta1p7_cfg.py"
analysis_cfgs["trigjetht350_eta1p7"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht350_eta1p7_cfg.py"
analysis_cfgs["trigjetht400_eta1p7"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht400_eta1p7_cfg.py"
analysis_cfgs["trigjetht450_eta1p7"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht450_eta1p7_cfg.py"
analysis_cfgs["trigjetht500_eta1p7"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht500_eta1p7_cfg.py"
analysis_cfgs["trigjetht550_eta1p7"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht550_eta1p7_cfg.py"
analysis_cfgs["trigjetht650_eta1p7"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht650_eta1p7_cfg.py"
analysis_cfgs["trigjetht_eta1p7"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigjetht_eta1p7_cfg.py"

analysis_cfgs["trigbbh_CSVTM_bfat"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigbbh_CSVTM_bfat_cfg.py"
analysis_cfgs["trigeff_trigbbh_CSVTM_bfat"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BTriggerEfficiency_trigbbh_CSVTM_bfat_cfg.py"

analysis_cfgs["trigmu_lowmass_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigmu_lowmass_CSVTM_cfg.py"
analysis_cfgs["trigmu_highmass_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigmu_highmass_CSVTM_cfg.py"
analysis_cfgs["trigmubbll_lowmass_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigmubbll_lowmass_CSVTM_cfg.py"
analysis_cfgs["trigmubbl_lowmass_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigmubbl_lowmass_CSVTM_cfg.py"
analysis_cfgs["trigmubbh_highmass_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigmubbh_highmass_CSVTM_cfg.py"

analysis_cfgs["trigmu24i_lowmass_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigmu24i_lowmass_CSVTM_cfg.py"
analysis_cfgs["trigmu24i_highmass_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigmu24i_highmass_CSVTM_cfg.py"
analysis_cfgs["trigmu24ibbll_lowmass_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigmu24ibbll_lowmass_CSVTM_cfg.py"
analysis_cfgs["trigmu24ibbl_lowmass_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigmu24ibbl_lowmass_CSVTM_cfg.py"
analysis_cfgs["trigmu24ibbh_highmass_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigmu24ibbh_highmass_CSVTM_cfg.py"

analysis_cfgs["trigmu24i_lowmass_CSVM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigmu24i_lowmass_CSVM_cfg.py"
analysis_cfgs["trigmu24i_highmass_CSVM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigmu24i_highmass_CSVM_cfg.py"
analysis_cfgs["trigmu24ibbll_lowmass_CSVM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigmu24ibbll_lowmass_CSVM_cfg.py"
analysis_cfgs["trigmu24ibbl_lowmass_CSVM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigmu24ibbl_lowmass_CSVM_cfg.py"
analysis_cfgs["trigmu24ibbh_highmass_CSVM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigmu24ibbh_highmass_CSVM_cfg.py"

analysis_cfgs["trigmu24i_lowmass"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigmu24i_lowmass_cfg.py"
analysis_cfgs["trigmu24i_highmass"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigmu24i_highmass_cfg.py"
analysis_cfgs["trigmu24ibbl_lowmass"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigmu24ibbl_lowmass_cfg.py"
analysis_cfgs["trigmu24ibbh_highmass"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigmu24ibbh_highmass_cfg.py"

analysis_cfgs["trigmu40_lowmass_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigmu40_lowmass_CSVTM_cfg.py"
analysis_cfgs["trigmu40_highmass_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigmu40_highmass_CSVTM_cfg.py"
analysis_cfgs["trigmu40bbll_lowmass_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigmu40bbll_lowmass_CSVTM_cfg.py"
analysis_cfgs["trigmu40bbl_lowmass_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigmu40bbl_lowmass_CSVTM_cfg.py"
analysis_cfgs["trigmu40bbh_highmass_CSVTM"] = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_trigmu40bbh_highmass_CSVTM_cfg.py"

analysis_cfgs["NoTrigger_eta2p2_CSVTM"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_NoTrigger_eta2p2_CSVTM_cfg.py"
analysis_cfgs["NoTrigger_eta1p7_CSVTM"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_NoTrigger_eta1p7_CSVTM_cfg.py"
analysis_cfgs["NoTrigger_eta2p2_CSVTL"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_NoTrigger_eta2p2_CSVTL_cfg.py"
analysis_cfgs["NoTrigger_eta1p7_CSVTL"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_NoTrigger_eta1p7_CSVTL_cfg.py"
analysis_cfgs["NoTrigger_eta2p2_CSVML"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_NoTrigger_eta2p2_CSVML_cfg.py"
analysis_cfgs["NoTrigger_eta1p7_CSVML"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_NoTrigger_eta1p7_CSVML_cfg.py"
analysis_cfgs["NoTrigger_eta2p2_CSVT"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_NoTrigger_eta2p2_CSVT_cfg.py"
analysis_cfgs["NoTrigger_eta1p7_CSVT"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_NoTrigger_eta1p7_CSVT_cfg.py"
analysis_cfgs["NoTrigger_eta2p2_CSVM"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_NoTrigger_eta2p2_CSVM_cfg.py"
analysis_cfgs["NoTrigger_eta1p7_CSVM"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_NoTrigger_eta1p7_CSVM_cfg.py"
analysis_cfgs["NoTrigger_eta2p2_CSVL"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_NoTrigger_eta2p2_CSVL_cfg.py"
analysis_cfgs["NoTrigger_eta1p7_CSVL"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_NoTrigger_eta1p7_CSVL_cfg.py"
analysis_cfgs["NoTrigger_eta2p2"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_NoTrigger_eta2p2_cfg.py"
analysis_cfgs["NoTrigger_eta1p7"]   = dijet_directory + "/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_NoTrigger_eta1p7_cfg.py"

# Limit setting paths
limit_paths = {}
limit_paths["limits"] = "/uscms_data/d1/dryu/Dijets/EightTeeEeVeeBee/Results/Limits/"
limit_paths["datacards"] = limit_paths["limits"] + "/datacards/"
limit_paths["workspaces"] = limit_paths["limits"] + "/workspaces/"
limit_paths["condor"] = limit_paths["limits"] + "/condor/"
limit_paths["resonance_shapes"] = "/uscms_data/d1/dryu/Dijets/EightTeeEeVeeBee/Results/ResonanceShapes/"

# Trigger efficiency histograms
trigger_efficiency_file = {}
trigger_efficiency_file["trigbbh_CSVTM"] = dijet_directory + "/data/EightTeeEeVeeBee/TriggerEfficiency/efficiency_trigbbh.root"
trigger_efficiency_file["trigbbl_CSVTM"] = dijet_directory + "/data/EightTeeEeVeeBee/TriggerEfficiency/efficiency_trigbbl.root"

# Get the path to a workspace. 
def get_workspace_filename(analysis_name, model):
	return limit_paths["workspaces"] + "/workspace_" + analysis_name + "_" + model + ".root"


# Bias studies
bias_study_directory = dijet_directory + "/data/EightTeeEeVeeBee/Fits/BiasStudies/"
def get_bias_study_directory(model, analysis, mass, mu):
	return bias_study_directory + "/" + model + "_" + analysis + "/m" + str(mass) + "_mu" + str(mu) + "/"

def get_bias_study_results(model, analysis, mass, mu, f_gen, f_test):
	return get_bias_study_directory(model, analysis, mass, mu) + "/mlfit" + model + "_" + analysis + "_m" + str(mass) + "_gen_" + f_gen + "_fit_" + f_test + "_mu" + str(mu) + ".root"

def get_signal_fit_file(analysis, model, mass, fit_function, interpolated=False):
	path = dijet_directory + "/data/EightTeeEeVeeBee/Fits/Signal/" + fit_function + "/fit_" + analysis + "_" + model + "_m" + str(mass)
	if interpolated:
		path += "_interpolated"
	#if correctTrigger:
	#	path += "_correctTrigger"
	#if fitTrigger:
	#	path += "_fitTrigger"
	path += ".root"
	return path

external_limits = dijet_directory + "/data/EightTeeEeVeeBee/Fits/Limits/External/"

# wp = CSVTM etc
# eta = eta1p7, eta2p2
def get_offline_btag_file(wp, eta):
	return os.path.expandvars("$CMSSW_BASE/src/CMSDIJET/StatisticalTools/data/offline_btag_eff_{}_{}.root".format(wp, eta))
