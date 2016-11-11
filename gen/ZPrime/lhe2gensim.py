import os
import sys

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

input_lhe_files = {}
top_directory = "/home/dryu/Dijets/data/EightTeeEeVeeBee/ZPrime/Reconstruction/"
version = "vTEST"
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
		print "[GetLHEPath] WARNING : LHE file not found at path + " lhe_path + "."
		# Check for zipped file, and unzip
		if os.path.isfile(lhe_path + ".gz"):
			print "[GetLHEPath] WARNING : LHE zipped file found. Attempting to unzip."
			os.system("gunzip " + lhe_path + ".gz")
			if not os.path.isfile(lhe_path):
				print "[GetLHEPath] ERROR : Failed to unzip."
				sys.exit(1)
	return lhe_path

def GetCrabPath(mass, coupling, stage):
	return top_directory + "/crab/crab_" + stage + "_" + GetSample(mass, coupling) + ".py"  

def MakeGenSimCfg(mass, coupling):
	driver_command = "cmsDriver.py Configuration/Generator/python/Hadronizer_TuneCUETP8M1_8TeV_generic_LHE_pythia8_cff.py --mc --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --conditions START53_V7C::All --beamspot Realistic8TeVCollision --step GEN,SIM --filein file:" + GetLHEPath(str(mass)) + " --fileout file:GENSIM.root --python_filename " + GetCfgPath(mass, coupling, "GENSIM") + " -n -1 --no_exec"

def MakeGenSimCrab(mass, coupling, version):
	crab_file = open(GetCrabPath(mass, coupling, stage), "w")
	crab_template = open(top_directory + "/GENSIM/crab/crab_template_GENSIM.py", "r")
	for line in crab_template:
		if "@REQUESTNAME@" in line:
			line = line.replace("@REQUESTNAME@", GetSample(mass, coupling) + "_" + version)
		if "@PSETNAME@" in line:
			line = line.replace("@PSETNAME@", GetCfgPath(mass, coupling, "GENSIM"))
		if "@INPUTFILES@" in line:
			line = line.replace("@INPUTFILES@", "[" + GetLHEPath(mass, coupling) + "]")
		if "@UNITSPERJOB@" in line:
			line = line.replace("@UNITSPERJOB@", 500)
		if "@TOTALUNITS@" in line:
			line = line.replace("@TOTALUNITS@", 50000)
		if "@OUTPUTDATASET@" in line:
			line = line.replace("@OUTPUTPRIMARYDATASET@", GetDatasetFromSample(mass, coupling))

RunGenSimCrab(mass, coupling, submit=False):
	submission_command = "crab submit -c " + GetCrabPath(mass, coupling, "GENSIM")
	if submit:
		os.system(submission_command)
	else:
		print submission_command

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description = 'Make and submit CRAB generation jobs')
    parser.add_argument('version', type=str, help='Version')
    parser.add_argument('--submit', action='store_true', default=False, help='Submit jobs after creation')
    parser.add_argument('--GENSIM', action='store_true', help='')
    parser.add_argument('--DR1', action='store_true', help='')
    parser.add_argument('--DR2', action='store_true', help='')
    parser.add_argument('--masses', type=str, default="400,500,600,750,900,1200", help='Signal masses')
   	parser.add_argument('--coupling', type=float, default=0.25, help='Coupling (0.25 or 0.5)')
   	parser.add_argument('--version', type=str, default="vTEST", help='Coupling (0.25 or 0.5)')
    args = parser.parse_args()
    masses = [int(x) for x in args.masses.split(",")]
    coupling = args.coupling

    if args.GENSIM:
    	for mass in masses:
    		MakeGenSimCfg(mass, coupling)
    		MakeGenSimCrab(mass, coupling, version=args.version)
   			RunGenSim(mass, coupling, submit=args.submit, version=args.version)
