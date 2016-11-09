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
def SetupGENSIM(sample):
	subjob = 0
	for input_lhe in input_lhe_files[sample]:
		crab_file = open(top_directory + "/GENSIM/crab/crab_GENSIM_" + str(subjob) + ".py", "w")


		driver_command = "cmsDriver.py Configuration/Generator/python/Hadronizer_TuneCUETP8M1_8TeV_generic_LHE_pythia8_cff.py --mc --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --conditions START53_V7C::All --beamspot Realistic8TeVCollision --step GEN,SIM --filein file:/home/dryu/Dijets/data/EightTeeEeVeeBee/ZPrime/Zprime_8TeV_ccbar_bbar_only/Events/mZ_400_0.25/events.lhe --fileout file:test.GEN.root -n -1 --no_exec"

		subjob += 1

