# Signal samples
signal_models = ["RSG", "Zprime", "Hbb"]
signal_masses = xrange(300, 1250, 50)
signal_samples = {}
signal_sample_masses = {}
signal_sample_namestrings = {
	"RSG":"RSGravitonToBBbar_M_@MASS@_TuneZ2star_8TeV_pythia6_FASTSIM",
	"Zprime":"ZprimeToBB_M_@MASS@_TuneD6T_8TeV_pythia6_FASTSIM",
	"Hbb":"GluGluSpin0ToBBbar_M_@MASS@_TuneCUEP8M1_8TeV_pythia8_FASTSIM"
}
for signal_model in signal_models:
	signal_samples[signal_model] = []
	for signal_mass in signal_masses:
		signal_samples[signal_model].append(signal_sample_namestrings[signal_model].replace("@MASS@", str(signal_mass)))
		signal_sample_masses[signal_sample_namestrings[signal_model].replace("@MASS@", str(signal_mass))] = signal_mass

# Skimmed trees
# - Data files are stored in .txt files (they have thousands of files)
files_QCDBEventTree = {}
file_lists_QCDBEventTree = {
	"2012A":"/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/Results/condor/QCDBEventTree_MultiJet_Run2012A_v1_4.txt",
	"2012B":"/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/Results/condor/QCDBEventTree_BJetPlusX_Run2012B_v1_4.txt",
	"2012C":"/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/Results/condor/QCDBEventTree_BJetPlusX_Run2012C_v1_4.txt",
	"2012D":"/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/Results/condor/QCDBEventTree_BJetPlusX_Run2012D_v1_4.txt",
	"2012B_JetHT":"/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/Results/condor/QCDBEventTree_JetHT_Run2012B_v1_4_1.txt",
	"2012C_JetHT":"/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/Results/condor/QCDBEventTree_JetHT_Run2012C_v1_4_1.txt",
	"2012D_JetHT":"/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/Results/condor/QCDBEventTree_JetHT_Run2012D_v1_4_1.txt"
}
for sample_name, sample_file_list in file_lists_QCDBEventTree.iteritems():
	f = open(sample_file_list, 'r')
	files_QCDBEventTree[sample_name] = []
	for line in f:
		files_QCDBEventTree[sample_name].append(line.rstrip())

# - Skimmed MC trees
files_QCDBEventTree["RSGravitonToBBbar_M_200_TuneZ2star_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_200_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
files_QCDBEventTree["RSGravitonToBBbar_M_250_TuneZ2star_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_250_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
files_QCDBEventTree["RSGravitonToBBbar_M_300_TuneZ2star_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_300_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
files_QCDBEventTree["RSGravitonToBBbar_M_350_TuneZ2star_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_350_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
files_QCDBEventTree["RSGravitonToBBbar_M_400_TuneZ2star_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_400_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
files_QCDBEventTree["RSGravitonToBBbar_M_450_TuneZ2star_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_450_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
files_QCDBEventTree["RSGravitonToBBbar_M_500_TuneZ2star_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_500_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
files_QCDBEventTree["RSGravitonToBBbar_M_550_TuneZ2star_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_550_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
files_QCDBEventTree["RSGravitonToBBbar_M_600_TuneZ2star_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_600_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
files_QCDBEventTree["RSGravitonToBBbar_M_650_TuneZ2star_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_650_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
files_QCDBEventTree["RSGravitonToBBbar_M_700_TuneZ2star_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_700_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
files_QCDBEventTree["RSGravitonToBBbar_M_750_TuneZ2star_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_750_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
files_QCDBEventTree["RSGravitonToBBbar_M_800_TuneZ2star_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_800_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
files_QCDBEventTree["RSGravitonToBBbar_M_850_TuneZ2star_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_850_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
files_QCDBEventTree["RSGravitonToBBbar_M_900_TuneZ2star_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_900_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
files_QCDBEventTree["RSGravitonToBBbar_M_950_TuneZ2star_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_950_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
files_QCDBEventTree["RSGravitonToBBbar_M_1000_TuneZ2star_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_1000_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
files_QCDBEventTree["RSGravitonToBBbar_M_1050_TuneZ2star_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_1050_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
files_QCDBEventTree["RSGravitonToBBbar_M_1100_TuneZ2star_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_1100_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
files_QCDBEventTree["RSGravitonToBBbar_M_1150_TuneZ2star_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_1150_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
files_QCDBEventTree["RSGravitonToBBbar_M_1200_TuneZ2star_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/RSGravitonToBBbar_M_1200_TuneZ2star_8TeV_pythia6_FASTSIM_AODSIM_QCDBEventTree.root"
files_QCDBEventTree["ZprimeToBB_M_200_TuneD6T_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_200_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
files_QCDBEventTree["ZprimeToBB_M_250_TuneD6T_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_250_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
files_QCDBEventTree["ZprimeToBB_M_300_TuneD6T_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_300_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
files_QCDBEventTree["ZprimeToBB_M_350_TuneD6T_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_350_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
files_QCDBEventTree["ZprimeToBB_M_400_TuneD6T_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_400_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
files_QCDBEventTree["ZprimeToBB_M_450_TuneD6T_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_450_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
files_QCDBEventTree["ZprimeToBB_M_500_TuneD6T_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_500_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
files_QCDBEventTree["ZprimeToBB_M_550_TuneD6T_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_550_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
files_QCDBEventTree["ZprimeToBB_M_600_TuneD6T_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_600_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
files_QCDBEventTree["ZprimeToBB_M_650_TuneD6T_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_650_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
files_QCDBEventTree["ZprimeToBB_M_700_TuneD6T_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_700_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
files_QCDBEventTree["ZprimeToBB_M_750_TuneD6T_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_750_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
files_QCDBEventTree["ZprimeToBB_M_800_TuneD6T_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_800_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
files_QCDBEventTree["ZprimeToBB_M_850_TuneD6T_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_850_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
files_QCDBEventTree["ZprimeToBB_M_900_TuneD6T_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_900_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
files_QCDBEventTree["ZprimeToBB_M_950_TuneD6T_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_950_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
files_QCDBEventTree["ZprimeToBB_M_1000_TuneD6T_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_1000_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
files_QCDBEventTree["ZprimeToBB_M_1050_TuneD6T_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_1050_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
files_QCDBEventTree["ZprimeToBB_M_1100_TuneD6T_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_1100_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
files_QCDBEventTree["ZprimeToBB_M_1150_TuneD6T_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_1150_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"
files_QCDBEventTree["ZprimeToBB_M_1200_TuneD6T_8TeV_pythia6_FASTSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/ZprimeToBB_M_1200_TuneD6T_8TeV_pythia6_FASTSIM_QCDBEventTree.root"

# Results files (from InclusiveBHistograms)
files_InclusiveBHistograms = {}
files_InclusiveBHistograms["BJetPlusX_2012"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/Results/InclusiveBHistograms_2012.root"
files_InclusiveBHistograms["BJetPlusX_2012BCD"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/Results/InclusiveBHistograms_BJetPlusX_2012BCD.root"
files_InclusiveBHistograms["JetHT_2012BCD"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/Results/InclusiveBHistograms_JetHT_2012BCD.root"
files_InclusiveBHistograms["BJetPlusX_tight_2012BCD"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/Results/InclusiveBHistograms_BJetPlusX_tight_2012BCD.root"
files_InclusiveBHistograms["JetHT_tight_2012BCD"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/Results/InclusiveBHistograms_JetHT_tight_2012BCD.root"

# Figures
figure_directory = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/Results/figures/"