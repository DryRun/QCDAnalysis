# Signal samples
signal_models = ["RSG", "Hbb"] # Zprime
#signal_masses = [250, 300, 400, 500, 600, 750, 900, 1200]
signal_masses = [400, 500, 600, 750, 900, 1200]

limit_signal_masses = {
	"trigbbl_CSVTM":range(400, 950, 50),
	"trigbbh_CSVTM":range(550, 1250, 50)
}

simulated_masses = [250, 300, 400, 500, 600, 750, 900, 1200]

output_tags = {}
#output_tags["Hbb"] = "HERWIGPP_POWHEG_GluonFusion_H@MASS@_bbbar_8TeV_@SIMTYPE@"
output_tags["Hbb"] = "GluGluSpin0ToBBbar_M_@MASS@_TuneCUEP8M1_8TeV_pythia8_@SIMTYPE@"
output_tags["RSG"] = "RSGravitonToBBbar_M_@MASS@_TuneZ2star_8TeV_pythia8_@SIMTYPE@"
output_tags["Zprime"] = "ZprimeToBB_M_@MASS@_TuneD6T_8TeV_pythia6_@SIMTYPE@"
def GetOutputTag(p_model, p_mass_point, p_simtype):
	return output_tags[p_model].replace("@MASS@", str(p_mass_point)).replace("@SIMTYPE@", p_simtype)

def get_signal_tag(p_model, p_mass_point, p_simtype):
	return output_tags[p_model].replace("@MASS@", str(p_mass_point)).replace("@SIMTYPE@", p_simtype)

signal_samples = {}
signal_sample_masses = {}

signal_sample_namestrings = {
	"RSG":"RSGravitonToBBbar_M_@MASS@_TuneZ2star_8TeV_pythia8_FULLSIM",
	"RSG_FASTSIM":"RSGravitonToBBbar_M_@MASS@_TuneZ2star_8TeV_pythia6_FASTSIM",
	"Zprime_FASTSIM":"ZprimeToBB_M_@MASS@_TuneD6T_8TeV_pythia6_FULLSIM",
	"Hbb":"GluGluSpin0ToBBbar_M_@MASS@_TuneCUEP8M1_8TeV_pythia8_FULLSIM"
}
for signal_model in signal_models:
	signal_samples[signal_model] = []
	for signal_mass in signal_masses:
		if signal_model == "Zprime":
			simtype = "FASTSIM"
		else:
			simtype = "FULLSIM"
		signal_samples[signal_model].append(GetOutputTag(signal_model, signal_mass, simtype))
		signal_sample_masses[GetOutputTag(signal_model, signal_mass, simtype)] = signal_mass

backgrounds = ["QCD", "QCDB", "TTJets"]
background_supersamples = {
	"QCD":["QCD_Pt-1000to1400_TuneZ2star_8TeV_pythia6","QCD_Pt-120to170_TuneZ2star_8TeV_pythia6","QCD_Pt-1400to1800_TuneZ2star_8TeV_pythia6","QCD_Pt-170to300_TuneZ2star_8TeV_pythia6","QCD_Pt-1800_TuneZ2star_8TeV_pythia6","QCD_Pt-300to470_TuneZ2star_8TeV_pythia6","QCD_Pt-470to600_TuneZ2star_8TeV_pythia6","QCD_Pt-600to800_TuneZ2star_8TeV_pythia6","QCD_Pt-800to1000_TuneZ2star_8TeV_pythia6","QCD_Pt-80to120_TuneZ2star_8TeV_pythia6"],
	"QCDB":["QCD_Pt-50To150_bEnriched_TuneZ2star_8TeV-pythia6-evtgen","QCD_Pt-15To30_bEnriched_TuneZ2star_8TeV-pythia6-evtgen","QCD_Pt-30To50_bEnriched_TuneZ2star_8TeV-pythia6-evtgen",],
	"TTJets":["TTJets_Hadronic", "TTJets_SemiLept", "TTJets_Leptonic"],
}

# Text files listing the bulk private MC production
private_mc_file_lists = {}
private_mc_file_lists["RSGravitonToBBbar_M_250_TuneZ2star_8TeV_pythia8_FULLSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/condor/RSGravitonToBBbar_250_v1_3.txt"
private_mc_file_lists["RSGravitonToBBbar_M_400_TuneZ2star_8TeV_pythia8_FULLSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/condor/RSGravitonToBBbar_400_v1_3.txt"
private_mc_file_lists["RSGravitonToBBbar_M_500_TuneZ2star_8TeV_pythia8_FULLSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/condor/RSGravitonToBBbar_500_v1_3.txt"
private_mc_file_lists["RSGravitonToBBbar_M_300_TuneZ2star_8TeV_pythia8_FULLSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/condor/RSGravitonToBBbar_300_v1_3.txt"
private_mc_file_lists["RSGravitonToBBbar_M_600_TuneZ2star_8TeV_pythia8_FULLSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/condor/RSGravitonToBBbar_600_v1_3.txt"
private_mc_file_lists["RSGravitonToBBbar_M_750_TuneZ2star_8TeV_pythia8_FULLSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/condor/RSGravitonToBBbar_750_v1_3.txt"
private_mc_file_lists["RSGravitonToBBbar_M_900_TuneZ2star_8TeV_pythia8_FULLSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/condor/RSGravitonToBBbar_900_v1_3.txt"
private_mc_file_lists["RSGravitonToBBbar_M_1200_TuneZ2star_8TeV_pythia8_FULLSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/condor/RSGravitonToBBbar_1200_v1_3.txt"
private_mc_file_lists["GluGluSpin0ToBBbar_M_250_TuneCUEP8M1_8TeV_pythia8_FULLSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/condor/GluGluSpin0ToBBbar_250_v1_3.txt"
private_mc_file_lists["GluGluSpin0ToBBbar_M_400_TuneCUEP8M1_8TeV_pythia8_FULLSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/condor/GluGluSpin0ToBBbar_400_v1_3.txt"
private_mc_file_lists["GluGluSpin0ToBBbar_M_500_TuneCUEP8M1_8TeV_pythia8_FULLSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/condor/GluGluSpin0ToBBbar_500_v1_3.txt"
private_mc_file_lists["GluGluSpin0ToBBbar_M_300_TuneCUEP8M1_8TeV_pythia8_FULLSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/condor/GluGluSpin0ToBBbar_300_v1_3.txt"
private_mc_file_lists["GluGluSpin0ToBBbar_M_600_TuneCUEP8M1_8TeV_pythia8_FULLSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/condor/GluGluSpin0ToBBbar_600_v1_3.txt"
private_mc_file_lists["GluGluSpin0ToBBbar_M_750_TuneCUEP8M1_8TeV_pythia8_FULLSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/condor/GluGluSpin0ToBBbar_750_v1_3.txt"
private_mc_file_lists["GluGluSpin0ToBBbar_M_900_TuneCUEP8M1_8TeV_pythia8_FULLSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/condor/GluGluSpin0ToBBbar_900_v1_3.txt"
private_mc_file_lists["GluGluSpin0ToBBbar_M_1200_TuneCUEP8M1_8TeV_pythia8_FULLSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/QCDBEventTree/condor/GluGluSpin0ToBBbar_1200_v1_3.txt"


# Fast sim configuration
fastsim_models = ["RSG", "Zprime"]
cff_templates = {}
cff_templates["RSG"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/python/RSGravitonToBBbar_M_X_TuneZ2star_8TeV_pythia6_cff.py.template"
cff_templates["Zprime"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/python/ZprimeToBB_M_X_TuneD6T_8TeV_pythia6_cff.py.template"

cff_files = {}
cff_files["RSG"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/python/RSGravitonToBBbar_M_@MASS@_TuneZ2star_8TeV_pythia6_cff.py"
cff_files["Zprime"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/python/ZprimeToBB_M_@MASS@_TuneD6T_8TeV_pythia6_cff.py"
def GetSimulationCFF(p_model, p_mass_point):
	return cff_files[p_model].replace("@MASS@", str(p_mass_point))

cfg_files = {}
cfg_files["RSG"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/gen/RSGravitonToBBbar_M_@MASS@_TuneZ2star_8TeV_pythia6_@SIMTYPE@_@STAGE@_cfg.py"
cfg_files["Zprime"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/gen/ZprimeToBB_M_@MASS@_TuneD6T_8TeV_pythia6_@SIMTYPE@_@STAGE@_cfg.py"
def GetConfigPath(p_model, p_mass_point, p_stage, p_simtype):
	return cfg_files[p_model].replace("@MASS@", str(p_mass_point)).replace("@STAGE@", p_stage).replace("@SIMTYPE@", p_simtype)


submission_jdl_files = {}
submission_jdl_files["Hbb"] = "HERWIGPP_POWHEG_GluonFusion_H@MASS@_bbbar_8TeV_@SIMTYPE@_@STAGE@.jdl" # @STAGE@ = FASTSIM, GENSIM, REDIGI, RECO
submission_jdl_files["RSG"] = "RSGravitonToBBbar_M_@MASS@_TuneZ2star_8TeV_pythia6_@SIMTYPE@_@STAGE@.jdl" # @STAGE@ = FASTSIM, GENSIM, REDIGI, RECO
submission_jdl_files["Zprime"] = "ZprimeToBB_M_@MASS@_TuneD6T_8TeV_pythia6_@SIMTYPE@_@STAGE@.jdl" # @STAGE@ = FASTSIM, GENSIM, REDIGI, RECO
def GetSubmissionJDLFile(p_model, p_mass_point, p_stage, p_simtype):
	return submission_jdl_files[p_model].replace("@MASS@", str(p_mass_point)).replace("@STAGE@", p_stage).replace("@SIMTYPE@", p_simtype)

# Location of locally generated stuff on EOS
eos_folder = "root://cmseos.fnal.gov//store/user/dryu/"
eos_aods = {}
eos_aods["Hbb"] = eos_folder + "EightTeeEeVeeBee/Simulation/@SIMTYPE@/HERWIGPP_POWHEG_GluonFusion_H@MASS@_bbbar_8TeV_@SIMTYPE@_@STAGE@.root" # @STAGE@ = FASTSIM, GENSIM, REDIGI, RECO
eos_aods["RSG"] = eos_folder + "EightTeeEeVeeBee/Simulation/@SIMTYPE@/RSGravitonToBBbar_M_@MASS@_TuneZ2star_8TeV_pythia6_@SIMTYPE@_@STAGE@.root" # @STAGE@ = FASTSIM, GENSIM, REDIGI, RECO
eos_aods["Zprime"] = eos_folder + "EightTeeEeVeeBee/Simulation/@SIMTYPE@/ZprimeToBB_M_@MASS@_TuneD6T_8TeV_pythia6_@SIMTYPE@_@STAGE@.root" # @STAGE@ = FASTSIM, GENSIM, REDIGI, RECO
def GetEOSLocation(p_model, p_mass_point, p_stage, p_simtype):
	return eos_aods[p_model].replace("@MASS@", str(p_mass_point)).replace("@STAGE@", p_stage).replace("@SIMTYPE@", p_simtype)

signal_cross_sections = {}
signal_cross_sections["RSGravitonToBBbar_M_300_TuneZ2star_8TeV_pythia8_FULLSIM"]    = 1.556e-07 * 10**9
signal_cross_sections["RSGravitonToBBbar_M_600_TuneZ2star_8TeV_pythia8_FULLSIM"]    = 5.188e-09 * 10**9
signal_cross_sections["RSGravitonToBBbar_M_750_TuneZ2star_8TeV_pythia8_FULLSIM"]    = 1.551e-09 * 10**9
signal_cross_sections["RSGravitonToBBbar_M_900_TuneZ2star_8TeV_pythia8_FULLSIM"]    = 5.48e-10 * 10**9
signal_cross_sections["RSGravitonToBBbar_M_1200_TuneZ2star_8TeV_pythia8_FULLSIM"]   = 9.891e-11 * 10**9
signal_cross_sections["GluGluSpin0ToBBbar_M_300_TuneCUEP8M1_8TeV_pythia8_FULLSIM"]  = 1.556e-07 * 10**9
signal_cross_sections["GluGluSpin0ToBBbar_M_600_TuneCUEP8M1_8TeV_pythia8_FULLSIM"]  = 5.188e-09 * 10**9
signal_cross_sections["GluGluSpin0ToBBbar_M_750_TuneCUEP8M1_8TeV_pythia8_FULLSIM"]  = 1.551e-09 * 10**9
signal_cross_sections["GluGluSpin0ToBBbar_M_900_TuneCUEP8M1_8TeV_pythia8_FULLSIM"]  = 5.48e-10 * 10**9
signal_cross_sections["GluGluSpin0ToBBbar_M_1200_TuneCUEP8M1_8TeV_pythia8_FULLSIM"] = 9.891e-11 * 10**9

signal_cross_sections["RSG200_TuneZ2star_8TeV_pythia6"] = 9.287e-07 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG250_TuneZ2star_8TeV_pythia6"] = 3.519e-07 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG300_TuneZ2star_8TeV_pythia6"] = 1.556e-07 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG350_TuneZ2star_8TeV_pythia6"] = 7.611e-08 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG400_TuneZ2star_8TeV_pythia6"] = 4.014e-08 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG450_TuneZ2star_8TeV_pythia6"] = 2.205e-08 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG500_TuneZ2star_8TeV_pythia6"] = 1.309e-08 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG550_TuneZ2star_8TeV_pythia6"] = 8.126e-09 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG600_TuneZ2star_8TeV_pythia6"] = 5.188e-09 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG650_TuneZ2star_8TeV_pythia6"] = 3.328e-09 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG700_TuneZ2star_8TeV_pythia6"] = 2.253e-09 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG750_TuneZ2star_8TeV_pythia6"] = 1.551e-09 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG800_TuneZ2star_8TeV_pythia6"] = 1.078e-09 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG850_TuneZ2star_8TeV_pythia6"] = 7.717e-10 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG900_TuneZ2star_8TeV_pythia6"] = 5.48e-10 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG950_TuneZ2star_8TeV_pythia6"] = 3.991e-10 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG1000_TuneZ2star_8TeV_pythia6"] = 2.97e-10 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG1050_TuneZ2star_8TeV_pythia6"] = 2.247e-10 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG1100_TuneZ2star_8TeV_pythia6"] = 1.719e-10 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG1150_TuneZ2star_8TeV_pythia6"] = 1.305e-10 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG1200_TuneZ2star_8TeV_pythia6"] = 9.891e-11 * 10**9 # Taken from FASTSIM generation logs, 5000 events

signal_cross_sections["ZprimeToBB_M_200_TuneD6T_8TeV_pythia6"] = 3.161e-07 * 10**9
signal_cross_sections["ZprimeToBB_M_250_TuneD6T_8TeV_pythia6"] = 1.418e-07 * 10**9
signal_cross_sections["ZprimeToBB_M_300_TuneD6T_8TeV_pythia6"] = 7.633e-08 * 10**9
signal_cross_sections["ZprimeToBB_M_350_TuneD6T_8TeV_pythia6"] = 4.432e-08 * 10**9
signal_cross_sections["ZprimeToBB_M_400_TuneD6T_8TeV_pythia6"] = 2.682e-08 * 10**9
signal_cross_sections["ZprimeToBB_M_450_TuneD6T_8TeV_pythia6"] = 1.684e-08 * 10**9
signal_cross_sections["ZprimeToBB_M_500_TuneD6T_8TeV_pythia6"] = 1.118e-08 * 10**9
signal_cross_sections["ZprimeToBB_M_550_TuneD6T_8TeV_pythia6"] = 7.707e-09 * 10**9
signal_cross_sections["ZprimeToBB_M_600_TuneD6T_8TeV_pythia6"] = 5.335e-09 * 10**9
signal_cross_sections["ZprimeToBB_M_650_TuneD6T_8TeV_pythia6"] = 3.852e-09 * 10**9
signal_cross_sections["ZprimeToBB_M_700_TuneD6T_8TeV_pythia6"] = 2.814e-09 * 10**9
signal_cross_sections["ZprimeToBB_M_750_TuneD6T_8TeV_pythia6"] = 2.129e-09 * 10**9
signal_cross_sections["ZprimeToBB_M_800_TuneD6T_8TeV_pythia6"] = 1.579e-09 * 10**9
signal_cross_sections["ZprimeToBB_M_850_TuneD6T_8TeV_pythia6"] = 1.236e-09 * 10**9
signal_cross_sections["ZprimeToBB_M_900_TuneD6T_8TeV_pythia6"] = 9.322e-10 * 10**9
signal_cross_sections["ZprimeToBB_M_950_TuneD6T_8TeV_pythia6"] = 7.256e-10 * 10**9
signal_cross_sections["ZprimeToBB_M_1000_TuneD6T_8TeV_pythia6"] = 5.793e-10 * 10**9
signal_cross_sections["ZprimeToBB_M_1050_TuneD6T_8TeV_pythia6"] = 4.534e-10 * 10**9
signal_cross_sections["ZprimeToBB_M_1100_TuneD6T_8TeV_pythia6"] = 3.633e-10 * 10**9
signal_cross_sections["ZprimeToBB_M_1150_TuneD6T_8TeV_pythia6"] = 2.96e-10 * 10**9
signal_cross_sections["ZprimeToBB_M_1200_TuneD6T_8TeV_pythia6"] = 2.392e-10 * 10**9

background_cross_sections = {}
background_cross_sections["TTJets_Hadronic"] = 252.89 * 0.68 * 0.68
background_cross_sections["TTJets_SemiLept"] = 252.89 * 2 * 0.32 * 0.68
background_cross_sections["TTJets_Leptonic"] = 252.89 * 0.32 * 0.32

background_cross_section_uncertainties = {}
background_cross_section_uncertainties["TTJets"] = 0.1
background_cross_section_uncertainties["TTJets_Hadronic"] = 0.1
background_cross_section_uncertainties["TTJets_SemiLept"] = 0.1
background_cross_section_uncertainties["TTJets_Leptonic"] = 0.1


fullsim_datasets = {"GENSIM":{}, "DR1":{}, "DR2":{}}
fullsim_datasets["GENSIM"] = {
	"GluGluSpin0ToBBbar_M_750_TuneCUEP8M1_8TeV_pythia8_FASTSIM":"/GluGluSpin0ToBBbar/dryu-GEN-SIM_v1_1-76ca9f00fbd35571059515ca22287825/USER"
}

n_gen_events = {}
n_gen_events["RSGravitonToBBbar_M_200_TuneZ2star_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["RSGravitonToBBbar_M_250_TuneZ2star_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["RSGravitonToBBbar_M_300_TuneZ2star_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["RSGravitonToBBbar_M_350_TuneZ2star_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["RSGravitonToBBbar_M_400_TuneZ2star_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["RSGravitonToBBbar_M_450_TuneZ2star_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["RSGravitonToBBbar_M_500_TuneZ2star_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["RSGravitonToBBbar_M_550_TuneZ2star_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["RSGravitonToBBbar_M_600_TuneZ2star_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["RSGravitonToBBbar_M_650_TuneZ2star_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["RSGravitonToBBbar_M_700_TuneZ2star_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["RSGravitonToBBbar_M_750_TuneZ2star_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["RSGravitonToBBbar_M_800_TuneZ2star_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["RSGravitonToBBbar_M_850_TuneZ2star_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["RSGravitonToBBbar_M_900_TuneZ2star_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["RSGravitonToBBbar_M_950_TuneZ2star_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["RSGravitonToBBbar_M_1000_TuneZ2star_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["RSGravitonToBBbar_M_1050_TuneZ2star_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["RSGravitonToBBbar_M_1100_TuneZ2star_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["RSGravitonToBBbar_M_1150_TuneZ2star_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["RSGravitonToBBbar_M_1200_TuneZ2star_8TeV_pythia6_FASTSIM"] = 5000

n_gen_events["ZprimeToBB_M_200_TuneD6T_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["ZprimeToBB_M_250_TuneD6T_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["ZprimeToBB_M_300_TuneD6T_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["ZprimeToBB_M_350_TuneD6T_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["ZprimeToBB_M_400_TuneD6T_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["ZprimeToBB_M_450_TuneD6T_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["ZprimeToBB_M_500_TuneD6T_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["ZprimeToBB_M_550_TuneD6T_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["ZprimeToBB_M_600_TuneD6T_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["ZprimeToBB_M_650_TuneD6T_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["ZprimeToBB_M_700_TuneD6T_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["ZprimeToBB_M_750_TuneD6T_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["ZprimeToBB_M_800_TuneD6T_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["ZprimeToBB_M_850_TuneD6T_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["ZprimeToBB_M_900_TuneD6T_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["ZprimeToBB_M_950_TuneD6T_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["ZprimeToBB_M_1000_TuneD6T_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["ZprimeToBB_M_1050_TuneD6T_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["ZprimeToBB_M_1100_TuneD6T_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["ZprimeToBB_M_1150_TuneD6T_8TeV_pythia6_FASTSIM"] = 5000
n_gen_events["ZprimeToBB_M_1200_TuneD6T_8TeV_pythia6_FASTSIM"] = 5000

pat_file_lists = {}
pat_file_lists["RSGravitonToBBbar_M_600_TuneZ2star_8TeV_pythia8_FULLSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/PAT/PAT_RSG_600.txt"
pat_file_lists["RSGravitonToBBbar_M_750_TuneZ2star_8TeV_pythia8_FULLSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/PAT/PAT_RSG_750.txt"
pat_file_lists["RSGravitonToBBbar_M_900_TuneZ2star_8TeV_pythia8_FULLSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/PAT/PAT_RSG_900.txt"
pat_file_lists["RSGravitonToBBbar_M_1200_TuneZ2star_8TeV_pythia8_FULLSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/PAT/PAT_RSG_1200.txt"
pat_file_lists["GluGluSpin0ToBBbar_M_600_TuneCUEP8M1_8TeV_pythia8_FULLSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/PAT/PAT_Hbb_600.txt"
pat_file_lists["GluGluSpin0ToBBbar_M_750_TuneCUEP8M1_8TeV_pythia8_FULLSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/PAT/PAT_Hbb_750.txt"
pat_file_lists["GluGluSpin0ToBBbar_M_900_TuneCUEP8M1_8TeV_pythia8_FULLSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/PAT/PAT_Hbb_900.txt"
pat_file_lists["GluGluSpin0ToBBbar_M_1200_TuneCUEP8M1_8TeV_pythia8_FULLSIM"] = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/PAT/PAT_Hbb_1200.txt"

def get_signal_AE_filename():
	return "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/Simulation/signal_acc_times_eff.pkl"

def get_signal_AE(analysis, model, mass):
	import pickle
	signal_acc_times_eff = pickle.load(open(get_signal_AE_filename(), "rb"))
	print signal_acc_times_eff
	return signal_acc_times_eff[model][analysis][mass]

if __name__ == "__main__":
	import ROOT
	from ROOT import *
	# Get n gen events
	for model in ["Zprime", "RSG"]:
		for mass in xrange(300, 1250, 50):
			f = TFile.Open(GetEOSLocation(model, mass, "AODSIM", "FASTSIM"))
			print model + " / " + str(mass) + " = " + str(f.Get("Events").GetEntriesFast())
