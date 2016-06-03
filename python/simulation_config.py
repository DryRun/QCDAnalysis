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
signal_cross_sections["RSG"] = {}
signal_cross_sections["RSG"][200.] = 9.287e-07 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG"][250.] = 3.519e-07 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG"][300.] = 1.556e-07 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG"][350.] = 7.611e-08 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG"][400.] = 4.014e-08 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG"][450.] = 2.205e-08 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG"][500.] = 1.309e-08 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG"][550.] = 8.126e-09 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG"][600.] = 5.188e-09 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG"][650.] = 3.328e-09 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG"][700.] = 2.253e-09 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG"][750.] = 1.551e-09 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG"][800.] = 1.078e-09 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG"][850.] = 7.717e-10 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG"][900.] = 5.48e-10 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG"][950.] = 3.991e-10 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG"][1000.] = 2.97e-10 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG"][1050.] = 2.247e-10 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG"][1100.] = 1.719e-10 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG"][1150.] = 1.305e-10 * 10**9 # Taken from FASTSIM generation logs, 5000 events
signal_cross_sections["RSG"][1200.] = 9.891e-11 * 10**9 # Taken from FASTSIM generation logs, 5000 events

signal_cross_sections["Zprime"] = {}
signal_cross_sections["Zprime"][200.] = 3.161e-07 * 10**9
signal_cross_sections["Zprime"][250.] = 1.418e-07 * 10**9
signal_cross_sections["Zprime"][300.] = 7.633e-08 * 10**9
signal_cross_sections["Zprime"][350.] = 4.432e-08 * 10**9
signal_cross_sections["Zprime"][400.] = 2.682e-08 * 10**9
signal_cross_sections["Zprime"][450.] = 1.684e-08 * 10**9
signal_cross_sections["Zprime"][500.] = 1.118e-08 * 10**9
signal_cross_sections["Zprime"][550.] = 7.707e-09 * 10**9
signal_cross_sections["Zprime"][600.] = 5.335e-09 * 10**9
signal_cross_sections["Zprime"][650.] = 3.852e-09 * 10**9
signal_cross_sections["Zprime"][700.] = 2.814e-09 * 10**9
signal_cross_sections["Zprime"][750.] = 2.129e-09 * 10**9
signal_cross_sections["Zprime"][800.] = 1.579e-09 * 10**9
signal_cross_sections["Zprime"][850.] = 1.236e-09 * 10**9
signal_cross_sections["Zprime"][900.] = 9.322e-10 * 10**9
signal_cross_sections["Zprime"][950.] = 7.256e-10 * 10**9
signal_cross_sections["Zprime"][1000.] = 5.793e-10 * 10**9
signal_cross_sections["Zprime"][1050.] = 4.534e-10 * 10**9
signal_cross_sections["Zprime"][1100.] = 3.633e-10 * 10**9
signal_cross_sections["Zprime"][1150.] = 2.96e-10 * 10**9
signal_cross_sections["Zprime"][1200.] = 2.392e-10 * 10**9

fullsim_datasets = {"GENSIM":{}, "DR1":{}, "DR2":{}}
fullsim_datasets["GENSIM"] = {
	"GluGluSpin0ToBBbar_M_750_TuneCUEP8M1_8TeV_pythia8_FASTSIM":"/GluGluSpin0ToBBbar/dryu-GEN-SIM_v1_1-76ca9f00fbd35571059515ca22287825/USER"
}
