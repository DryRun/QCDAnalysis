# Naming schemes
simulation_types = ["FASTSIM", "FULLSIM"]

mass_points = {}
mass_points["FASTSIM"] = range(200, 1250, 50)
mass_points["FULLSIM"] = [300, 750, 1000]

models = ["Hbb", "RSG", "Zprime"]
cff_templates = {}
cff_templates["Hbb"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/python/HERWIGPP_POWHEG_GluonFusion_HX_bbbar_8TeV_cff.py.template"
cff_templates["RSG"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/python/RSGravitonToBBbar_M_X_TuneZ2star_8TeV_pythia6_cff.py.template"
cff_templates["Zprime"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/python/ZprimeToBB_M_X_TuneD6T_8TeV_pythia6_cff.py.template"

cff_files = {}
cff_files["Hbb"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/python/HERWIGPP_POWHEG_GluonFusion_H@MASS@_bbbar_8TeV_cff.py"
cff_files["RSG"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/python/RSGravitonToBBbar_M_@MASS@_TuneZ2star_8TeV_pythia6_cff.py"
cff_files["Zprime"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/python/ZprimeToBB_M_@MASS@_TuneD6T_8TeV_pythia6_cff.py"
def GetSimulationCFF(p_model, p_mass_point):
	return cff_files[p_model].replace("@MASS@", str(p_mass_point))

cfg_files = {}
cfg_files["Hbb"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/gen/HERWIGPP_POWHEG_GluonFusion_H@MASS@_bbbar_8TeV_@SIMTYPE@_@STAGE@_cfg.py"
cfg_files["RSG"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/gen/RSGravitonToBBbar_M_@MASS@_TuneZ2star_8TeV_pythia6_@SIMTYPE@_@STAGE@_cfg.py"
cfg_files["Zprime"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/gen/ZprimeToBB_M_@MASS@_TuneD6T_8TeV_pythia6_@SIMTYPE@_@STAGE@_cfg.py"
def GetConfigPath(p_model, p_mass_point, p_stage, p_simtype):
	return cfg_files[p_model].replace("@MASS@", str(p_mass_point)).replace("@STAGE@", p_stage).replace("@SIMTYPE@", p_simtype)

output_tags = {}
output_tags["Hbb"] = "HERWIGPP_POWHEG_GluonFusion_H@MASS@_bbbar_8TeV_@SIMTYPE@"
output_tags["RSG"] = "RSGravitonToBBbar_M_@MASS@_TuneZ2star_8TeV_pythia6_@SIMTYPE@"
output_tags["Zprime"] = "ZprimeToBB_M_@MASS@_TuneD6T_8TeV_pythia6_@SIMTYPE@"
def GetOutputTag(p_model, p_mass_point, p_simtype):
	return output_tags[p_model].replace("@MASS@", str(p_mass_point)).replace("@SIMTYPE@", p_simtype)


submission_jdl_files = {}
submission_jdl_files["Hbb"] = "HERWIGPP_POWHEG_GluonFusion_H@MASS@_bbbar_8TeV_@SIMTYPE@_@STAGE@.jdl" # @STAGE@ = FASTSIM, GENSIM, REDIGI, RECO
submission_jdl_files["RSG"] = "RSGravitonToBBbar_M_@MASS@_TuneZ2star_8TeV_pythia6_@SIMTYPE@_@STAGE@.jdl" # @STAGE@ = FASTSIM, GENSIM, REDIGI, RECO
submission_jdl_files["Zprime"] = "ZprimeToBB_M_@MASS@_TuneD6T_8TeV_pythia6_@SIMTYPE@_@STAGE@.jdl" # @STAGE@ = FASTSIM, GENSIM, REDIGI, RECO
def GetSubmissionJDLFile(p_model, p_mass_point, p_stage, p_simtype):
	return submission_jdl_files[p_model].replace("@MASS@", str(p_mass_point)).replace("@STAGE@", p_stage).replace("@SIMTYPE@", p_simtype)

eos_folder = "root://cmseos.fnal.gov//store/user/dryu/"
eos_aods = {}
eos_aods["Hbb"] = eos_folder + "EightTeeEeVeeBee/Simulation/@SIMTYPE@/HERWIGPP_POWHEG_GluonFusion_H@MASS@_bbbar_8TeV_@SIMTYPE@_@STAGE@.root" # @STAGE@ = FASTSIM, GENSIM, REDIGI, RECO
eos_aods["RSG"] = eos_folder + "EightTeeEeVeeBee/Simulation/@SIMTYPE@/RSGravitonToBBbar_M_@MASS@_TuneZ2star_8TeV_pythia6_@SIMTYPE@_@STAGE@.root" # @STAGE@ = FASTSIM, GENSIM, REDIGI, RECO
eos_aods["Zprime"] = eos_folder + "EightTeeEeVeeBee/Simulation/@SIMTYPE@/ZprimeToBB_M_@MASS@_TuneD6T_8TeV_pythia6_@SIMTYPE@_@STAGE@.root" # @STAGE@ = FASTSIM, GENSIM, REDIGI, RECO
def GetEOSLocation(p_model, p_mass_point, p_stage, p_simtype):
	return eos_aods[p_model].replace("@MASS@", str(p_mass_point)).replace("@STAGE@", p_stage).replace("@SIMTYPE@", p_simtype)

signal_cross_sections = {}
signal_cross_sections["RSGravitonToBBbar_M_200_TuneZ2star_8TeV_pythia6"] = 9.287e-07 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSGravitonToBBbar_M_250_TuneZ2star_8TeV_pythia6"] = 3.519e-07 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSGravitonToBBbar_M_300_TuneZ2star_8TeV_pythia6"] = 1.556e-07 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSGravitonToBBbar_M_350_TuneZ2star_8TeV_pythia6"] = 7.611e-08 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSGravitonToBBbar_M_400_TuneZ2star_8TeV_pythia6"] = 4.014e-08 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSGravitonToBBbar_M_450_TuneZ2star_8TeV_pythia6"] = 2.205e-08 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSGravitonToBBbar_M_500_TuneZ2star_8TeV_pythia6"] = 1.309e-08 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSGravitonToBBbar_M_550_TuneZ2star_8TeV_pythia6"] = 8.126e-09 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSGravitonToBBbar_M_600_TuneZ2star_8TeV_pythia6"] = 5.188e-09 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSGravitonToBBbar_M_650_TuneZ2star_8TeV_pythia6"] = 3.328e-09 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSGravitonToBBbar_M_700_TuneZ2star_8TeV_pythia6"] = 2.253e-09 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSGravitonToBBbar_M_750_TuneZ2star_8TeV_pythia6"] = 1.551e-09 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSGravitonToBBbar_M_800_TuneZ2star_8TeV_pythia6"] = 1.078e-09 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSGravitonToBBbar_M_850_TuneZ2star_8TeV_pythia6"] = 7.717e-10 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSGravitonToBBbar_M_900_TuneZ2star_8TeV_pythia6"] = 5.48e-10 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSGravitonToBBbar_M_950_TuneZ2star_8TeV_pythia6"] = 3.991e-10 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSGravitonToBBbar_M_1000_TuneZ2star_8TeV_pythia6"] = 2.97e-10 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSGravitonToBBbar_M_1050_TuneZ2star_8TeV_pythia6"] = 2.247e-10 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSGravitonToBBbar_M_1100_TuneZ2star_8TeV_pythia6"] = 1.719e-10 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSGravitonToBBbar_M_1150_TuneZ2star_8TeV_pythia6"] = 1.305e-10 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSGravitonToBBbar_M_1200_TuneZ2star_8TeV_pythia6"] = 9.891e-11 * 10**9 # Taken from FASTSIM generation logs, 5000 events

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

fullsim_datasets = {"GENSIM":{}, "DR1":{}, "DR2":{}}
fullsim_datasets["GENSIM"] = {
	"GluGluSpin0ToBBbar_M_750_TuneCUEP8M1_8TeV_pythia8_FASTSIM":"/GluGluSpin0ToBBbar/dryu-GEN-SIM_v1_1-76ca9f00fbd35571059515ca22287825/USER"
}

n_gen_events = {}
n_gen_events["RSGravitonToBBbar_M_200_TuneZ2star_8TeV_pythia6"] = 5000
n_gen_events["RSGravitonToBBbar_M_250_TuneZ2star_8TeV_pythia6"] = 5000
n_gen_events["RSGravitonToBBbar_M_300_TuneZ2star_8TeV_pythia6"] = 5000
n_gen_events["RSGravitonToBBbar_M_350_TuneZ2star_8TeV_pythia6"] = 5000
n_gen_events["RSGravitonToBBbar_M_400_TuneZ2star_8TeV_pythia6"] = 5000
n_gen_events["RSGravitonToBBbar_M_450_TuneZ2star_8TeV_pythia6"] = 5000
n_gen_events["RSGravitonToBBbar_M_500_TuneZ2star_8TeV_pythia6"] = 5000
n_gen_events["RSGravitonToBBbar_M_550_TuneZ2star_8TeV_pythia6"] = 5000
n_gen_events["RSGravitonToBBbar_M_600_TuneZ2star_8TeV_pythia6"] = 5000
n_gen_events["RSGravitonToBBbar_M_650_TuneZ2star_8TeV_pythia6"] = 5000
n_gen_events["RSGravitonToBBbar_M_700_TuneZ2star_8TeV_pythia6"] = 5000
n_gen_events["RSGravitonToBBbar_M_750_TuneZ2star_8TeV_pythia6"] = 5000
n_gen_events["RSGravitonToBBbar_M_800_TuneZ2star_8TeV_pythia6"] = 5000
n_gen_events["RSGravitonToBBbar_M_850_TuneZ2star_8TeV_pythia6"] = 5000
n_gen_events["RSGravitonToBBbar_M_900_TuneZ2star_8TeV_pythia6"] = 5000
n_gen_events["RSGravitonToBBbar_M_950_TuneZ2star_8TeV_pythia6"] = 5000
n_gen_events["RSGravitonToBBbar_M_1000_TuneZ2star_8TeV_pythia6"] = 5000
n_gen_events["RSGravitonToBBbar_M_1050_TuneZ2star_8TeV_pythia6"] = 5000
n_gen_events["RSGravitonToBBbar_M_1100_TuneZ2star_8TeV_pythia6"] = 5000
n_gen_events["RSGravitonToBBbar_M_1150_TuneZ2star_8TeV_pythia6"] = 5000
n_gen_events["RSGravitonToBBbar_M_1200_TuneZ2star_8TeV_pythia6"] = 5000

n_gen_events["ZprimeToBB_M_200_TuneD6T_8TeV_pythia6"] = 5000
n_gen_events["ZprimeToBB_M_250_TuneD6T_8TeV_pythia6"] = 5000
n_gen_events["ZprimeToBB_M_300_TuneD6T_8TeV_pythia6"] = 5000
n_gen_events["ZprimeToBB_M_350_TuneD6T_8TeV_pythia6"] = 5000
n_gen_events["ZprimeToBB_M_400_TuneD6T_8TeV_pythia6"] = 5000
n_gen_events["ZprimeToBB_M_450_TuneD6T_8TeV_pythia6"] = 5000
n_gen_events["ZprimeToBB_M_500_TuneD6T_8TeV_pythia6"] = 5000
n_gen_events["ZprimeToBB_M_550_TuneD6T_8TeV_pythia6"] = 5000
n_gen_events["ZprimeToBB_M_600_TuneD6T_8TeV_pythia6"] = 5000
n_gen_events["ZprimeToBB_M_650_TuneD6T_8TeV_pythia6"] = 5000
n_gen_events["ZprimeToBB_M_700_TuneD6T_8TeV_pythia6"] = 5000
n_gen_events["ZprimeToBB_M_750_TuneD6T_8TeV_pythia6"] = 5000
n_gen_events["ZprimeToBB_M_800_TuneD6T_8TeV_pythia6"] = 5000
n_gen_events["ZprimeToBB_M_850_TuneD6T_8TeV_pythia6"] = 5000
n_gen_events["ZprimeToBB_M_900_TuneD6T_8TeV_pythia6"] = 5000
n_gen_events["ZprimeToBB_M_950_TuneD6T_8TeV_pythia6"] = 5000
n_gen_events["ZprimeToBB_M_1000_TuneD6T_8TeV_pythia6"] = 5000
n_gen_events["ZprimeToBB_M_1050_TuneD6T_8TeV_pythia6"] = 5000
n_gen_events["ZprimeToBB_M_1100_TuneD6T_8TeV_pythia6"] = 5000
n_gen_events["ZprimeToBB_M_1150_TuneD6T_8TeV_pythia6"] = 5000
n_gen_events["ZprimeToBB_M_1200_TuneD6T_8TeV_pythia6"] = 5000

if __name__ == "__main__":
	import ROOT
	from ROOT import *
	# Get n gen events
	for model in ["Zprime", "RSG"]:
		for mass in xrange(300, 1250, 50):
			f = TFile.Open(GetEOSLocation(model, mass, "AODSIM", "FASTSIM"))
			print model + " / " + str(mass) + " = " + str(f.Get("Events").GetEntriesFast())
