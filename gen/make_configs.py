import os
import sys
import CMSDIJET.QCDAnalysis.simulation_config
from CMSDIJET.QCDAnalysis.simulation_config import *
## Naming schemes
#fastsim_mass_points = range(200, 1250, 50)
#fullsim_mass_points = [300, 750, 1000]
#
#models = ["Hbb", "RSG"]
#cff_templates = {}
#cff_templates["Hbb"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/python/PYTHIA6_Tauola_gg_bbHX_bb_8TeV_cff.py.template"
#cff_templates["RSG"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/python/RSGravitonToBBbar_M_X_TuneZ2star_8TeV_pythia6_cff.py.template"
#
#cff_files = {}
#cff_files["Hbb"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/python/PYTHIA6_Tauola_gg_bbH@MASS@_bb_8TeV_cff.py"
#cff_files["RSG"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/python/RSGravitonToBBbar_M_@MASS@_TuneZ2star_8TeV_pythia6_cff.py"
#
#cfg_files = {}
#cfg_files["Hbb"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/gen/PYTHIA6_Tauola_gg_bbH@MASS@_bb_8TeV_cfg.py"
#cfg_files["RSG"] = "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/gen/RSGravitonToBBbar_M_@MASS@_TuneZ2star_8TeV_pythia6_cfg.py"
#
#output_tags = {}
#output_tags["Hbb"] = "PYTHIA6_Tauola_gg_bbH@MASS@_bb_8TeV"
#output_tags["RSG"] = "RSGravitonToBBbar_M_@MASS@_TuneZ2star_8TeV_pythia6"

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

def MakeFullSimCfgs(p_model, p_mass_point):
	stages = ["GENSIM", "REDIGI", "RECOSIM"]

	commands = {}
	commands["GENSIM"] = "cmsDriver.py " + GetSimulationCFF(p_model, p_mass_point).replace("$CMSSW_BASE/src/", "") + " --python_filename " + GetConfigPath(p_model, p_mass_point, "GENSIM", "FULLSIM") + " --step GEN,SIM --fileout file:" + GetOutputTag(p_model, p_mass_point, "GENSIM", "FULLSIM") + ".root --mc --pileup NoPileUp --datamix NODATAMIXER --conditions auto:mc --beamspot Realistic8TeVCollision --eventcontent RAWSIM --datatier GEN-SIM -n 100 --no_exec"
	commands["REDIGI"] = "cmsDriver.py REDIGI --python_filename " + GetConfigPath(p_model, p_mass_point, "REDIGI", "FULLSIM") + " --step DIGI,L1,DIGI2RAW,HLT:7E33v2 --filein file:" + GetOutputTag(p_model, p_mass_point, "GENSIM", "FULLSIM") + ".root --fileout file:" + GetOutputTag(p_model, p_mass_point, "REDIGI", "FULLSIM") + ".root --mc --pileup 2012_Summer_50ns_PoissonOOTPU --datamix NODATAMIXER --conditions auto:mc --beamspot Realistic8TeVCollision --eventcontent RAWSIM --datatier GEN-SIM-RAW -n 100 --no_exec"
	commands["RECOSIM"] = "cmsDriver.py RECO --python_filename " + GetConfigPath(p_model, p_mass_point, "RECOSIM", "FULLSIM") + " --step RAW2DIGI,L1Reco,RECO,VALIDATION:validation_prod,DQM:DQMOfflinePOGMC --filein file:" + GetOutputTag(p_model, p_mass_point, "REDIGI", "FULLSIM") + ".root --fileout file:" + GetOutputTag(p_model, p_mass_point, "RECOSIM", "FULLSIM") + ".root --mc --pileup 2012_Summer_50ns_PoissonOOTPU --datamix NODATAMIXER --conditions auto:mc --beamspot Realistic8TeVCollision --eventcontent AODSIM,DQM --datatier AODSIM,DQM -n 100 --no_exec"

	for stage in stages:
		os.system(commands[stage])
		do_add_input_files = (stage != "GENSIM")
		AddSubjobOption(GetConfigPath(p_model, p_mass_point, stage, "FULLSIM"), GetOutputTag(p_model, p_mass_point, stage, "FULLSIM"), add_subjob=True, add_input_files=do_add_input_files)

#def MakeFullSimCfg(p_cff, p_cfg, p_output_tag):
#	cfg_GENSIM = p_cfg.replace("@STAGE@", "GENSIM")
#	cfg_REDIGI = p_cfg.replace("@STAGE@", "REDIGI")
#	cfg_RECO = p_cfg.replace("@STAGE@", "RECO")
#	command1 = "cmsDriver.py " + p_cff.replace("$CMSSW_BASE/src/", "") + " --python_filename " + cfg_GENSIM + " --step GEN,SIM --fileout file:" + p_output_tag + "_FullSim_GENSIM.root --mc --pileup NoPileUp --datamix NODATAMIXER --conditions auto:mc --beamspot Realistic8TeVCollision --eventcontent RAWSIM --datatier GEN-SIM -n 1000 --no_exec"
#	command2 = "cmsDriver.py REDIGI --python_filename " + cfg_REDIGI + " --step DIGI,L1,DIGI2RAW,HLT:7E33v2 --filein file:" + p_output_tag + "_FullSim_GENSIM.root --fileout file:" + p_output_tag + "_FullSim_RAW.root --mc --pileup 2012_Summer_50ns_PoissonOOTPU --datamix NODATAMIXER --conditions auto:mc --beamspot Realistic8TeVCollision --eventcontent RAWSIM --datatier GEN-SIM-RAW -n 1000 --no_exec"
#	command3 = "cmsDriver.py RECO --python_filename " + cfg_RECO + " --step RAW2DIGI,L1Reco,RECO,VALIDATION:validation_prod,DQM:DQMOfflinePOGMC --filein file:" + p_output_tag + "_FullSim_RAW.root --fileout file:" + p_output_tag + "_FullSim_RECOSIM.root --mc --pileup 2012_Summer_50ns_PoissonOOTPU --datamix NODATAMIXER --conditions auto:mc --beamspot Realistic8TeVCollision --eventcontent AODSIM,DQM --datatier AODSIM,DQM -n 1000 --no_exec"
#	#command = "cmsDriver.py " + p_cff.replace("$CMSSW_BASE/src/", "") + " --fileout file:" + p_output_tag + "_FullSim_AODSIM.root --mc --eventcontent AODSIM --conditions auto:mc --beamspot Realistic8TeVCollision --step GEN,SIM,DIGI,L1,DIGI2RAW,HLT:7E33v2,RAW2DIGI,L1Reco,RECO --python_filename " + p_cfg + " --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 5"
#	#print command1
#	#print command2
#	#print command3
#	os.system(command1)
#	os.system(command2)
#	os.system(command3)
#
#	AddSubjobOption(cfg_GENSIM)
#	AddSubjobOption(cfg_REDIGI)
#	AddSubjobOption(cfg_RECO)

def MakeFastSimCfg(p_model, p_mass_point):
	stages = ["AODSIM"] # RECOSIM?
	n_events = 5000
	for stage in stages:
		# RECOSIM output is large (~2 MB per event). Not reasonable for storage, well, anywhere.
		#command = "cmsDriver.py " + GetSimulationCFF(p_model, p_mass_point).replace("$CMSSW_BASE/src/", "") + " --python_filename " + GetConfigPath(p_model, p_mass_point, "RECOSIM", "FASTSIM") + " --fileout file:" + GetOutputTag(p_model, p_mass_point, "RECOSIM", "FASTSIM") + ".root --step GEN,FASTSIM,HLT:7E33v2 --mc --eventcontent RECOSIM --datatier GEN-SIM-DIGI-RECO --pileup 2012_Startup_inTimeOnly --geometry DB --conditions auto:mc --beamspot Realistic8TeVCollision --no_exec -n 5000"
		command = "cmsDriver.py " + GetSimulationCFF(p_model, p_mass_point).replace("$CMSSW_BASE/src/", "") + " --python_filename " + GetConfigPath(p_model, p_mass_point, stage, "FASTSIM") + " --fileout file:" + GetOutputTag(p_model, p_mass_point, stage, "FASTSIM") + ".root --step GEN,FASTSIM,HLT:7E33v2 --mc --eventcontent " + stage + " --datatier GEN-SIM-DIGI-RECO --pileup 2012_Startup_inTimeOnly --geometry DB --conditions auto:mc --beamspot Realistic8TeVCollision --no_exec -n " + str(n_events)
		print command
		os.system(command)
		AddSubjobOption(GetConfigPath(p_model, p_mass_point, stage, "FASTSIM"), GetOutputTag(p_model, p_mass_point, "RECOSIM", "FASTSIM"))

#def MakeFastSimCfg(p_cff, p_cfg, p_output_tag):
#	cfg_FASTSIM = p_cfg.replace("@STAGE@", "FASTSIM")
#	command = "cmsDriver.py " + p_cff.replace("$CMSSW_BASE/src/", "") + " --python_filename " + cfg_FASTSIM + " --fileout file:" + p_output_tag + "_FastSim_RECOSIM.root --step GEN,FASTSIM,HLT:7E33v2 --mc --eventcontent RECOSIM --datatier GEN-SIM-DIGI-RECO --pileup 2012_Startup_inTimeOnly --geometry DB --conditions auto:mc --beamspot Realistic8TeVCollision --no_exec -n 1000"
#	#print command
#	os.system(command)
#	AddSubjobOption(cfg_FASTSIM)

#cmsDriver.py PYTHIA6_Bd2Psi2SKpi_TuneZ2star_8TeV_cff_py_GEN_SIM_DIGI_L1_DIGI2RAW_HLT.py --step GEN,SIM,DIGI,L1,DIGI2RAW,HLT:7E33v2 --beamspot [[Realistic8TeVCollision][Realistic8TeVCollision]] --conditions START53_V7C::All --pileup [[NoPileUp][NoPileUp]] --datamix NODATAMIXER --eventcontent RAWSIM --datatier GEN-SIM 

#cmsDriver.py PYTHIA6_Bd2Psi2SKpi_TuneZ2star_8TeV_cff_py_RAW2DIGI_L1Reco_RECO.py --step [[RAW2DIGI][RAW2DIGI]],L1Reco,RECO --conditions START53_V19F::All --datamix NODATAMIXER --eventcontent RECOSIM --datatier GEN-SIM-RECO
def AddSubjobOption(p_cfg, p_output_tag, add_subjob = False, add_input_files = False):
	os.system("mv " + p_cfg + " " + p_cfg + ".bak")
	old = open(os.path.expandvars(p_cfg + ".bak"), 'r')
	new = open(os.path.expandvars(p_cfg), 'w')
	for line in old:
		
		if "import FWCore.ParameterSet.Config as cms" in line: # Add options
			# Add VarParsing
			new.write(line)
			new.write("import FWCore.ParameterSet.VarParsing as VarParsing\n")
			new.write("#------------------------------------------------------------------------------------\n")
			new.write("# Options\n")
			new.write("#------------------------------------------------------------------------------------\n")
			new.write("options = VarParsing.VarParsing()\n")
			if add_subjob:
				new.write("options.register('subjob',\n")
				new.write("\t0, #default value\n")
				new.write("\tVarParsing.VarParsing.multiplicity.singleton,\n")
				new.write("\tVarParsing.VarParsing.varType.int,\n")
				new.write("\t\"Subjob index, also used for random seed\"\n")
				new.write(")\n")
			if add_input_files:
				new.write("options.register('inputFiles',\n")
				new.write("\t[], #default value\n")
				new.write("\tVarParsing.VarParsing.multiplicity.list,\n")
				new.write("\tVarParsing.VarParsing.varType.string,\n")
				new.write("\t\"Input files\"\n")
				new.write(")\n")
			new.write("options.parseArguments()\n")
		elif "# Path and EndPath definitions" in line and add_subjob:
			# Add random number seed
			new.write("\n")
			new.write("RandomNumberGeneratorService = cms.Service(\"RandomNumberGeneratorService\",\n")
			new.write("    generator = cms.PSet(\n")
			new.write("        initialSeed = cms.untracked.uint32(123456789 + options.subjob),\n")
			new.write("        engineName = cms.untracked.string('HepJamesRandom')\n")
			new.write("    )\n")
			new.write(")\n\n")
			new.write(line)
		elif p_output_tag in line and "fileName = cms.untracked.string" in line and add_subjob:
			# Add subjob index to output filenames
			new.write(line.replace(".root'", ".root.' + str(options.subjob)"))
		elif "fileNames = cms.untracked.vstring" in line and add_input_files:
			# Replace input files with option
			new.write("\tfileNames = cms.untracked.vstring(options.inputFiles)\n")
		else:
			new.write(line)
	old.close()
	new.close()

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
			) for model in ["Hbb", "RSG"] for mass_point in mass_points["FASTSIM"]
		)
	if args.cfg:
		#Parallel(n_jobs=4)(
		#	delayed(MakeFullSimCfgs)(model, mass_point) for model in ["Hbb", "RSG"] for mass_point in mass_points["FULLSIM"]
		#)

		Parallel(n_jobs=4)(
			delayed(MakeFastSimCfg)(model, mass_point) for model in ["Hbb", "RSG"] for mass_point in mass_points["FASTSIM"]
		)

