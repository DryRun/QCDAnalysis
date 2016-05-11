import os
import sys

# Naming schemes
fastsim_mass_points = range(200, 1250, 50)
fullsim_mass_points = [300, 750, 1000]

models = ["Hbb", "RSG"]
cff_templates = {}
cff_templates["Hbb"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/python/PYTHIA6_Tauola_gg_bbHX_bb_8TeV_cff.py.template"
cff_templates["RSG"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/python/RSGravitonToBBbar_M_X_TuneZ2star_8TeV_pythia6_cff.py.template"

cff_files = {}
cff_files["Hbb"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/python/PYTHIA6_Tauola_gg_bbH@MASS@_bb_8TeV_cff.py"
cff_files["RSG"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/python/RSGravitonToBBbar_M_@MASS@_TuneZ2star_8TeV_pythia6_cff.py"

cfg_files = {}
cfg_files["Hbb"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/gen/PYTHIA6_Tauola_gg_bbH@MASS@_bb_8TeV_cfg.py"
cfg_files["RSG"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/gen/RSGravitonToBBbar_M_@MASS@_TuneZ2star_8TeV_pythia6_cfg.py"

output_tags = {}
output_tags["Hbb"] = "PYTHIA6_Tauola_gg_bbH@MASS@_bb_8TeV"
output_tags["RSG"] = "RSGravitonToBBbar_M_@MASS@_TuneZ2star_8TeV_pythia6"

def MakeCff(p_template, p_mass, p_output):
	template = open(os.path.expandvars(p_template), 'r')
	cff = open(os.path.expandvars(p_output), 'w')
	for in_line in template:
		out_line = in_line.rstrip()
		if "@MASS@" in in_line:
			out_line = out_line.replace("@MASS@", str(p_mass))
		cff.write(out_line + "\n")
	template.close()
	cff.close()

def MakeFullSimCfg(p_cff, p_cfg, p_output_tag):
	command1 = "cmsDriver.py " + p_cff.replace("$CMSSW_BASE/src/", "") + " --python_filename " + p_cfg.replace(".py", "_GENSIM.py") + " --step GEN,SIM --fileout file:" + p_output_tag + "_FullSim_GENSIM.root --mc --pileup NoPileUp --datamix NODATAMIXER --conditions auto:mc --beamspot Realistic8TeVCollision --eventcontent RAWSIM --datatier GEN-SIM -n 10 --no_exec"
	command2 = "cmsDriver.py REDIGI --python_filename " + p_cfg.replace(".py", "_REDIGI.py") + " --step DIGI,L1,DIGI2RAW,HLT:7E33v2 --filein file:" + p_output_tag + "_FullSim_GENSIM.root --fileout file:" + p_output_tag + "_FullSim_RAW.root --mc --pileup 2012_Summer_50ns_PoissonOOTPU --datamix NODATAMIXER --conditions auto:mc --beamspot Realistic8TeVCollision --eventcontent RAWSIM --datatier GEN-SIM-RAW -n 10 --no_exec"
	command3 = "cmsDriver.py RECO --python_filename " + p_cfg.replace(".py", "_RECO.py") + " --step RAW2DIGI,L1Reco,RECO,VALIDATION:validation_prod,DQM:DQMOfflinePOGMC --filein file:" + p_output_tag + "_FullSim_RAW.root --fileout file:" + p_output_tag + "_FullSim_RECOSIM.root --mc --pileup 2012_Summer_50ns_PoissonOOTPU --datamix NODATAMIXER --conditions auto:mc --beamspot Realistic8TeVCollision --eventcontent AODSIM,DQM --datatier AODSIM,DQM -n 10 --no_exec"
	#command = "cmsDriver.py " + p_cff.replace("$CMSSW_BASE/src/", "") + " --fileout file:" + p_output_tag + "_FullSim_AODSIM.root --mc --eventcontent AODSIM --conditions auto:mc --beamspot Realistic8TeVCollision --step GEN,SIM,DIGI,L1,DIGI2RAW,HLT:7E33v2,RAW2DIGI,L1Reco,RECO --python_filename " + p_cfg + " --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 5"
	print command1
	print command2
	print command3
	#os.system(command1)
	#os.system(command2)
	#os.system(command3)

def MakeFastSimCfg(p_cff, p_cfg, p_output_tag):
	command = "cmsDriver.py " + p_cff.replace("$CMSSW_BASE/src/", "") + " --python_filename " + p_cfg + " --fileout file:" + p_output_tag + "_FastSim_RECOSIM.root --step GEN,FASTSIM,HLT:7E33v2 --mc --eventcontent RECOSIM --datatier GEN-SIM-DIGI-RECO --pileup 2012_Startup_inTimeOnly --geometry DB --conditions auto:mc --beamspot Realistic8TeVCollision --no_exec -n 5"
	#print command
	os.system(command)

#cmsDriver.py PYTHIA6_Bd2Psi2SKpi_TuneZ2star_8TeV_cff_py_GEN_SIM_DIGI_L1_DIGI2RAW_HLT.py --step GEN,SIM,DIGI,L1,DIGI2RAW,HLT:7E33v2 --beamspot [[Realistic8TeVCollision][Realistic8TeVCollision]] --conditions START53_V7C::All --pileup [[NoPileUp][NoPileUp]] --datamix NODATAMIXER --eventcontent RAWSIM --datatier GEN-SIM 

#cmsDriver.py PYTHIA6_Bd2Psi2SKpi_TuneZ2star_8TeV_cff_py_RAW2DIGI_L1Reco_RECO.py --step [[RAW2DIGI][RAW2DIGI]],L1Reco,RECO --conditions START53_V19F::All --datamix NODATAMIXER --eventcontent RECOSIM --datatier GEN-SIM-RECO


def MakeCrabCfg(p_cfg):
	pass


if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description = 'Make config files for simulation')
	parser.add_argument('--cff', action='store_true', help='Make _cff files')
	parser.add_argument('--cfg', action='store_true', help='Make _cfg files')
	args = parser.parse_args()

	from joblib import Parallel
	from joblib import delayed

	if args.cff:
		Parallel(n_jobs=4)(
			delayed(MakeCff)(
				cff_templates[model], 
				mass_point,
				cff_files[model].replace("@MASS@", str(mass_point))
			) for model in ["Hbb", "RSG"] for mass_point in mass_points
		)
	if args.cfg:
		Parallel(n_jobs=4)(
			delayed(MakeFullSimCfg)(
				cff_files[model].replace("@MASS@", str(mass_point)),
				cfg_files[model].replace("@MASS@", str(mass_point)), 
				output_tags[model].replace("@MASS@", str(mass_point))
			) for model in ["Hbb", "RSG"] for mass_point in fullsim_mass_points
		)

		#Parallel(n_jobs=4)(
		#	delayed(MakeFastSimCfg)(
		#		cff_files[model].replace("@MASS@", str(mass_point)),
		#		cfg_files[model].replace("@MASS@", str(mass_point)), 
		#		output_tags[model].replace("@MASS@", str(mass_point))
		#	) for model in ["Hbb", "RSG"] for mass_point in fastsim_mass_points
		#)

