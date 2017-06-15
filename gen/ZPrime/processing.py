import os
import sys

nevents = {0.25:{}}
nevents[0.25][300] = 64533
nevents[0.25][325] = 64063
nevents[0.25][350] = 65517
nevents[0.25][400] = 67291
nevents[0.25][500] = 65287
nevents[0.25][600] = 76252
nevents[0.25][750] = 65844
nevents[0.25][900] = 68725
nevents[0.25][1200] = 66924

datasets = {
		"GENSIM":{
			350:"/ZPrimeToCCBB_M_350_g0p25_TuneCUEP8M1_8TeV_MadgraphPythia8/dryu-GEN-SIM_1_0_4-09aa5bb01c248493e60679fcd1b56ec8/USER",
			400:"/ZPrimeToCCBB_M_400_g0p25_TuneCUEP8M1_8TeV_MadgraphPythia8/dryu-GEN-SIM_1_0_4-09aa5bb01c248493e60679fcd1b56ec8/USER",
			500:"/ZPrimeToCCBB_M_500_g0p25_TuneCUEP8M1_8TeV_MadgraphPythia8/dryu-GEN-SIM_1_0_4-09aa5bb01c248493e60679fcd1b56ec8/USER",
			600:"/ZPrimeToCCBB_M_600_g0p25_TuneCUEP8M1_8TeV_MadgraphPythia8/dryu-GEN-SIM_1_0_4-09aa5bb01c248493e60679fcd1b56ec8/USER",
			750:"/ZPrimeToCCBB_M_750_g0p25_TuneCUEP8M1_8TeV_MadgraphPythia8/dryu-GEN-SIM_1_0_4-09aa5bb01c248493e60679fcd1b56ec8/USER",
			900:"/ZPrimeToCCBB_M_900_g0p25_TuneCUEP8M1_8TeV_MadgraphPythia8/dryu-GEN-SIM_1_0_4-09aa5bb01c248493e60679fcd1b56ec8/USER",
			1200:"/ZPrimeToCCBB_M_1200_g0p25_TuneCUEP8M1_8TeV_MadgraphPythia8/dryu-GEN-SIM_1_0_4-09aa5bb01c248493e60679fcd1b56ec8/USER",
		},
		"DR1":{
			350:"/ZPrimeToCCBB_M_1200_g0p25_TuneCUEP8M1_8TeV_MadgraphPythia8/dryu-DR1_1_0_5-25f662c8c8577d562263f1e0c47637d7/USER",
			400:"/ZPrimeToCCBB_M_350_g0p25_TuneCUEP8M1_8TeV_MadgraphPythia8/dryu-DR1_1_0_5-25f662c8c8577d562263f1e0c47637d7/USER",
			500:"/ZPrimeToCCBB_M_400_g0p25_TuneCUEP8M1_8TeV_MadgraphPythia8/dryu-DR1_1_0_5-25f662c8c8577d562263f1e0c47637d7/USER",
			600:"/ZPrimeToCCBB_M_500_g0p25_TuneCUEP8M1_8TeV_MadgraphPythia8/dryu-DR1_1_0_5-25f662c8c8577d562263f1e0c47637d7/USER",
			750:"/ZPrimeToCCBB_M_600_g0p25_TuneCUEP8M1_8TeV_MadgraphPythia8/dryu-DR1_1_0_5-25f662c8c8577d562263f1e0c47637d7/USER",
			900:"/ZPrimeToCCBB_M_750_g0p25_TuneCUEP8M1_8TeV_MadgraphPythia8/dryu-DR1_1_0_5-25f662c8c8577d562263f1e0c47637d7/USER",
			1200:"/ZPrimeToCCBB_M_900_g0p25_TuneCUEP8M1_8TeV_MadgraphPythia8/dryu-DR1_1_0_5-25f662c8c8577d562263f1e0c47637d7/USER"
		},
}

def SplitLHE(input_lhe, output_lhe_base=None, events_per_file=1000):
	print "Welcome to SplitLHE. Input file = " + input_lhe
	if not output_lhe_base:
		output_lhe_base = ('.').join(os.path.basename(input_lhe).split('.')[:-1]) + "_split"

	output_lhe_files = []

	with open(input_lhe,"r") as infile:
		event_counter = 0    # Count number of events
		file_counter = -1     # Index for output files. Numbered so baseout_0.lhe has all the init stuff in it (we'll get rid of it at the end)

		outFile = open(output_lhe_base+"_"+str(file_counter)+".lhe","w")    # Open first output file to stick all init stuff in
		output_lhe_files.append(output_lhe_base+"_"+str(file_counter)+".lhe")
		commonBlock = '' # Store init info etc

		# Loop over each line
		while 1:
			line = infile.readline()
			if not line:
				break
			else :
				# Get common block
				if ( ( event_counter == 0 ) and not( "<event>" in line ) ):
					commonBlock += line
				else: pass
					
				# Decide if this line represents start of a new event        
				if( "<event>" in line ):
					if ( (event_counter) % int(events_per_file) == 0 ):                                                    # If we've gone through nEvt events, time for a new file. 
						outFile.write("</LesHouchesEvents>")                                         # End file correctly 
						outFile.close()                                                                                    # Close old output lhe file
						file_counter += 1
						outFile = open(output_lhe_base+"_"+str(file_counter)+".lhe","w")            # Open new output lhe file with increased index. Should prob catch exceptions...
						output_lhe_files.append(output_lhe_base+"_"+str(file_counter)+".lhe")
						outFile.write(commonBlock)                                                            # Add common block to start of each file
						print "File #:", file_counter
					event_counter += 1

				outFile.write(line)                                        
		
		print event_counter, " events in the original LHE file"
		#os.remove(output_lhe_base+"_-1.lhe") # Leftover with baseout_0.lhe with just init information. Delete this! 
		
		infile.close()
		outFile.write("</LesHouchesEvents>")
		outFile.close()
	print "New output LHE files:"
	print output_lhe_files
	print "Done with SplitLHE."

def GetNEventsInLHE(lhe_path):
	events = 0
	lhe_file = open(lhe_path, 'r')
	for line in lhe_file:
		events += line.count("<event>")
	return events

top_directory = "/home/dryu/Dijets/data/EightTeeEeVeeBee/ZPrime/Reconstruction/"
# Sample = "ZPrime_M#_g#"
# Dataset primary name = "ZPrime_M_#_g0p25_TuneX_8TeV_MadgraphPythia8"

def GetSample(mass, coupling):
	return "ZPrimeToCCBB_M_" + str(mass) + "_g" + str(coupling).replace(".", "p")

def GetDatasetFromSample(mass, coupling):
	return GetSample(mass, coupling) + "_TuneCUEP8M1_8TeV_MadgraphPythia8"

def GetCfgPath(mass, coupling, stage):
	return top_directory + "/" + stage + "/" + GetSample(mass, coupling) + "_cfg.py"

def GetLHEPath(mass, coupling):
	lhe_path = "/home/dryu/Dijets/data/EightTeeEeVeeBee/ZPrime/Zprime_8TeV_ccbar_bbar_only/Events/mZ_" + str(mass) + "_" + str(coupling) + "/events.lhe"
	if not os.path.isfile(lhe_path):
		print "[GetLHEPath] WARNING : LHE file not found at path + " + lhe_path + "."
		# Check for zipped file, and unzip
		if os.path.isfile(lhe_path + ".gz"):
			print "[GetLHEPath] WARNING : LHE zipped file found. Attempting to unzip."
			os.system("gunzip " + lhe_path + ".gz")
			if not os.path.isfile(lhe_path):
				print "[GetLHEPath] ERROR : Failed to unzip."
				sys.exit(1)
	return lhe_path

def GetCrabPath(mass, coupling, stage):
	return top_directory + "/" + stage + "/crab_" + stage + "_" + GetSample(mass, coupling) + ".py"  

def MakeGenSimCfg(mass, coupling):
	driver_command = "cmsDriver.py Configuration/Generator/python/Hadronizer_TuneCUETP8M1_8TeV_generic_LHE_pythia8_cff.py --mc --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --conditions START53_V7C::All --beamspot Realistic8TeVCollision --step GEN,SIM --filein file:" + os.path.basename(GetLHEPath(mass, coupling)) + " --fileout file:GENSIM.root --python_filename " + GetCfgPath(mass, coupling, "GENSIM") + " -n -1 --no_exec"
	os.system(driver_command)

def MakeGenSimCrab(mass, coupling, version):
	crab_file = open(GetCrabPath(mass, coupling, "GENSIM"), "w")
	crab_template = open("/home/dryu/Dijets/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/gen/ZPrime/crab_template_GENSIM.py", "r")
	for line in crab_template:
		if "@REQUESTNAME@" in line:
			line = line.replace("@REQUESTNAME@", GetSample(mass, coupling) + "_" + version)
		if "@PSETNAME@" in line:
			line = line.replace("@PSETNAME@", GetCfgPath(mass, coupling, "GENSIM"))
		if "@INPUTFILES@" in line:
			line = line.replace("@INPUTFILES@", "['" + GetLHEPath(mass, coupling) + "']")
		if "@UNITSPERJOB@" in line:
			line = line.replace("@UNITSPERJOB@", "500")
		if "@TOTALUNITS@" in line:
			line = line.replace("@TOTALUNITS@", str(nevents[coupling][mass]))
		if "@OUTPUTPRIMARYDATASET@" in line:
			line = line.replace("@OUTPUTPRIMARYDATASET@", GetDatasetFromSample(mass, coupling))
		if "OUTPUTDATASETTAG" in line:
			line = line.replace("@OUTPUTDATASETTAG@", "GEN-SIM_" + version)
		crab_file.write(line)

def RunGenSim(mass, coupling, submit=False):
	submission_command = "crab submit -c " + os.path.basename(GetCrabPath(mass, coupling, "GENSIM"))
	submission_directory = "/home/dryu/Dijets/data/EightTeeEeVeeBee/ZPrime/Reconstruction//GENSIM/"
	if submit:
		print "Submitting from " + submission_directory
		start_directory = os.getcwd()
		os.chdir(submission_directory)
		print "Submission command: " + submission_command
		os.system(submission_command)
		os.chdir(start_directory)
	else:
		print "cd " + submission_directory
		print submission_command

		
def MakeDR1Cfg(mass, coupling):
	driver_command = "cmsDriver.py step1 --filein \"dbs:" + datasets["GENSIM"][mass] + "\" --fileout file:DIGI-RECO-step1.root --pileup_input \"dbs:/MinBias_TuneZ2star_8TeV-pythia6/Summer12-START50_V13-v3/GEN-SIM\" --mc --eventcontent RAWSIM --pileup 2012_Summer_50ns_PoissonOOTPU --datatier GEN-SIM-RAW --conditions START53_V19::All --step DIGI,L1,DIGI2RAW,HLT:7E33v2 --python_filename " + GetCfgPath(mass, coupling, "DR1") + " --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring"
	os.system(driver_command)

def MakeDR1Crab(mass, coupling, version):
	crab_file = open(GetCrabPath(mass, coupling, "DR1"), "w")
	crab_template = open("/home/dryu/Dijets/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/gen/ZPrime/crab_template_DR1.py", "r")
	for line in crab_template:
		if '@REQUESTNAME@' in line:
			line = line.replace("@REQUESTNAME@", GetSample(mass, coupling) + "_DR1_" + version)
		if '@PSETNAME@' in line:
			line = line.replace("@PSETNAME@", GetCfgPath(mass, coupling, "DR1"))
		if '@INPUTDATASET@' in line:
			line = line.replace("@INPUTDATASET@", datasets["GENSIM"][mass])
		if "OUTPUTDATASETTAG" in line:
			line = line.replace("@OUTPUTDATASETTAG@", "DR1_" + version)
		crab_file.write(line)
	if "TEST" in version:
		crab_file.write("config.Data.totalUnits = 1")
	crab_file.close()

def RunDR1(mass, coupling, submit=False):
	submission_command = "crab submit -c " + os.path.basename(GetCrabPath(mass, coupling, "DR1"))
	submission_directory = "/home/dryu/Dijets/data/EightTeeEeVeeBee/ZPrime/Reconstruction/DR1/"
	if submit:
		print "Submitting from " + submission_directory
		start_directory = os.getcwd()
		os.chdir(submission_directory)
		print "Submission command: " + submission_command
		os.system(submission_command)
		os.chdir(start_directory)
	else:
		print "cd " + submission_directory
		print submission_command

def MakeDR2Cfg(mass, coupling):
	driver_command = "cmsDriver.py step2 --filein \"dbs:" + datasets["DR1"][mass] + "\" --fileout file:DIGI-RECO-step2.root --mc --eventcontent AODSIM,DQM --datatier AODSIM,DQM --conditions START53_V19::All --step RAW2DIGI,L1Reco,RECO,VALIDATION:validation_prod,DQM:DQMOfflinePOGMC --python_filename " + GetCfgPath(mass, coupling, "DR2") + " --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 164"
	os.system(driver_command)

def MakeDR2Crab(mass, coupling, version):
	crab_file = open(GetCrabPath(mass, coupling, "DR2"), "w")
	crab_template = open("/home/dryu/Dijets/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/gen/ZPrime/crab_template_DR2.py", "r")
	for line in crab_template:
		if '@REQUESTNAME@' in line:
			line = line.replace("@REQUESTNAME@", GetSample(mass, coupling) + "_DR2_" + version)
		if '@PSETNAME@' in line:
			line = line.replace("@PSETNAME@", GetCfgPath(mass, coupling, "DR2"))
		if '@INPUTDATASET@' in line:
			line = line.replace("@INPUTDATASET@", datasets["DR1"][mass])
		if "OUTPUTDATASETTAG" in line:
			line = line.replace("@OUTPUTDATASETTAG@", "DR2_" + version)
		crab_file.write(line)
	if "TEST" in version:
		crab_file.write("config.Data.totalUnits = 1")
	crab_file.close()

def RunDR2(mass, coupling, submit=False):
	submission_command = "crab submit -c " + os.path.basename(GetCrabPath(mass, coupling, "DR2"))
	submission_directory = "/home/dryu/Dijets/data/EightTeeEeVeeBee/ZPrime/Reconstruction/DR2/"
	if submit:
		print "Submitting from " + submission_directory
		start_directory = os.getcwd()
		os.chdir(submission_directory)
		print "Submission command: " + submission_command
		os.system(submission_command)
		os.chdir(start_directory)
	else:
		print "cd " + submission_directory
		print submission_command


if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description = 'Make and submit CRAB generation jobs')
	parser.add_argument('--submit', action='store_true', default=False, help='Submit jobs after creation')
	parser.add_argument('--count_events', action='store_true', help='Count events in LHE files')
	parser.add_argument('--GENSIM', action='store_true', help='')
	parser.add_argument('--DR1', action='store_true', help='')
	parser.add_argument('--DR2', action='store_true', help='')
	parser.add_argument('--masses', type=str, default="350,400,500,600,750,900,1200", help='Signal masses')
	parser.add_argument('--coupling', type=float, default=0.25, help='Coupling (0.25 or 0.5)')
	parser.add_argument('--version', type=str, default="vTEST", help='Version (default vTEST)')
	args = parser.parse_args()
	masses = [int(x) for x in args.masses.split(",")]
	coupling = args.coupling

	if args.count_events:
		for mass in masses:
			print GetLHEPath(mass, coupling) + " : " + str(GetNEventsInLHE(GetLHEPath(mass, coupling)))

	if args.GENSIM:
		for mass in masses:
			MakeGenSimCfg(mass, coupling)
		for mass in masses:
			MakeGenSimCrab(mass, coupling, version=args.version)
		for mass in masses:
			RunGenSim(mass, coupling, submit=args.submit)
	if args.DR1:
		for mass in masses:
			MakeDR1Cfg(mass, coupling)
		for mass in masses:
			MakeDR1Crab(mass, coupling, version=args.version)
		for mass in masses:
			RunDR1(mass, coupling, submit=args.submit)
	if args.DR2:
		for mass in masses:
			MakeDR2Cfg(mass, coupling)
		for mass in masses:
			MakeDR2Crab(mass, coupling, version=args.version)
		for mass in masses:
			RunDR2(mass, coupling, submit=args.submit)
