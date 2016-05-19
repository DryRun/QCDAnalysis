# Naming schemes
simulation_types = ["FASTSIM", "FULLSIM"]

mass_points = {}
mass_points["FASTSIM"] = range(200, 1250, 50)
mass_points["FULLSIM"] = [300, 750, 1000]

models = ["Hbb", "RSG", "Z'"]
cff_templates = {}
cff_templates["Hbb"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/python/PYTHIA6_Tauola_gg_bbHX_bb_8TeV_cff.py.template"
cff_templates["RSG"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/python/RSGravitonToBBbar_M_X_TuneZ2star_8TeV_pythia6_cff.py.template"
cff_templates["Z'"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/python/ZprimeToBB_M_X_TuneD6T_8TeV_pythia6_cff.py.template"

cff_files = {}
cff_files["Hbb"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/python/PYTHIA6_Tauola_gg_bbH@MASS@_bb_8TeV_cff.py"
cff_files["RSG"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/python/RSGravitonToBBbar_M_@MASS@_TuneZ2star_8TeV_pythia6_cff.py"
cff_files["Z'"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/python/ZprimeToBB_M_@MASS@_TuneD6T_8TeV_pythia6_cff.py"
def GetSimulationCFF(p_model, p_mass_point):
	return cff_files[p_model].replace("@MASS@", str(p_mass_point))

cfg_files = {}
cfg_files["Hbb"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/gen/PYTHIA6_Tauola_gg_bbH@MASS@_bb_8TeV_@SIMTYPE@_@STAGE@_cfg.py"
cfg_files["RSG"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/gen/RSGravitonToBBbar_M_@MASS@_TuneZ2star_8TeV_pythia6_@SIMTYPE@_@STAGE@_cfg.py"
cfg_files["Z'"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/gen/ZprimeToBB_M_@MASS@_TuneD6T_8TeV_pythia6_@SIMTYPE@_@STAGE@_cfg.py"
def GetConfigPath(p_model, p_mass_point, p_stage, p_simtype):
	return cfg_files[p_model].replace("@MASS@", str(p_mass_point)).replace("@STAGE@", p_stage).replace("@SIMTYPE@", p_simtype)

output_tags = {}
output_tags["Hbb"] = "PYTHIA6_Tauola_gg_bbH@MASS@_bb_8TeV_@SIMTYPE@_@STAGE@"
output_tags["RSG"] = "RSGravitonToBBbar_M_@MASS@_TuneZ2star_8TeV_pythia6_@SIMTYPE@_@STAGE@"
output_tags["Z'"] = "ZprimeToBB_M_@MASS@_TuneD6T_8TeV_pythia6_@SIMTYPE@_@STAGE@"
def GetOutputTag(p_model, p_mass_point, p_stage, p_simtype):
	return output_tags[p_model].replace("@MASS@", str(p_mass_point)).replace("@STAGE@", p_stage).replace("@SIMTYPE@", p_simtype)


submission_jdl_files = {}
submission_jdl_files["Hbb"] = "PYTHIA6_Tauola_gg_bbH@MASS@_bb_8TeV_@SIMTYPE@_@STAGE@.jdl" # @STAGE@ = FASTSIM, GENSIM, REDIGI, RECO
submission_jdl_files["RSG"] = "RSGravitonToBBbar_M_@MASS@_TuneZ2star_8TeV_pythia6_@SIMTYPE@_@STAGE@.jdl" # @STAGE@ = FASTSIM, GENSIM, REDIGI, RECO
submission_jdl_files["Z'"] = "ZprimeToBB_M_@MASS@_TuneD6T_8TeV_pythia6_@SIMTYPE@_@STAGE@.jdl" # @STAGE@ = FASTSIM, GENSIM, REDIGI, RECO
def GetSubmissionJDLFile(p_model, p_mass_point, p_stage, p_simtype):
	return submission_jdl_files[p_model].replace("@MASS@", str(p_mass_point)).replace("@STAGE@", p_stage).replace("@SIMTYPE@", p_simtype)

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