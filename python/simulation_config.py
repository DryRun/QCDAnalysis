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

