import os
import CMSDIJET.QCDAnalysis.simulation_config
from CMSDIJET.QCDAnalysis.simulation_config import *
import CMSDIJET.QCDAnalysis.analysis_configuration_8TeV as analysis_config

# Script to submit BHistogram jobs
# - Two functions, RunData and RunSignal, setup the condor submission of 'cmsRun analysis_cfg.py inputFiles=<> outputFile=<>'. 
# - The functions have to be separate because the data skim files reside on EOS and have to be chopped up into subjobs, while the signal skims are in single files.

dijet_directory = "/home/dryu/Dijets"

# RunData
# - Input files are on EOS, so you can't do the normal files-per-job mechanism (this cp's the files to the worker node, which is bad for EOS). 
# - Instead, do the subjobbing manually. 
def RunBHistogramsEOS(analysis, sample, files_per_job=200, retar=False, data_source=None):
	if not data_source:
		print "[RunBHistogramsEOS] ERROR : Please specify data_source = collision_data or simulation"
		sys.exit(1)

	# Create working directory and cd
	start_directory = os.getcwd()
	working_directory = dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/submit_" + analysis + "_" + sample
	os.system("mkdir -pv " + working_directory)
	os.chdir(working_directory)

	# Build file list 
	file_list_handle = file(analysis_config.files_QCDBEventTree[sample], 'r')
	file_list = file_list_handle.readlines()
	file_list_handle.close()
	file_index = 0
	subjob_index = 0
	subjob_output_filenames = []
	while file_index < len(file_list):
		this_job_files = []
		while file_index < len(file_list) and len(this_job_files) < files_per_job:
			this_job_files.append(file_list[file_index].rstrip())
			file_index += 1
		if len(this_job_files) < 1:
			continue
		command = "condor_cmsRun"
		if retar:
			command += " --retar "
		command += " --submit-file=submit_" + analysis + "_" + sample + ".subjob" + str(subjob_index) + ".jdl "
		command += " --output-tag=BHistograms_" + sample + ".subjob" + str(subjob_index) + " "
		command += " --run " + dijet_directory + "/CMSSW_5_3_32_patch3/src/MyTools/RootUtils/scripts/cmsRun_wrapper.sh " + analysis_config.analysis_cfgs[analysis]
		command += " dataSource=" + data_source
		command += " dataType=data inputFiles="
		for input_file in this_job_files:
			command += input_file + ","
		command = command.rstrip(",")
		subjob_output_filename = os.path.basename(analysis_config.get_b_histogram_filename(analysis, sample) + ".subjob" + str(subjob_index))
		command += " outputFile=" + subjob_output_filename
		subjob_output_filenames.append(subjob_output_filename)

		#print command
		os.system(command)
		subjob_index += 1

	# Postprocessing script
	merge_command = "hadd " + analysis_config.get_b_histogram_filename(analysis, sample) + " " + working_directory + "/" + os.path.basename(analysis_config.get_b_histogram_filename(analysis, sample)) + ".subjob*"
	postprocessing_file = open('postprocessing_' + analysis + "_" + sample + ".py", 'w')
	postprocessing_file.write("import os\n")
	postprocessing_file.write("import sys\n")
	postprocessing_file.write("import glob\n")
	postprocessing_file.write("log_files = glob.glob(" + working_directory + "/*stderr)\n")
	postprocessing_file.write("failed_logs = []\n")
	postprocessing_file.write("for log_file in log_files:\n")
	postprocessing_file.write("\tlog_file_handle = open(log_file, 'r')\n")
	postprocessing_file.write("\tfor line in log_file_handle:\n")
	postprocessing_file.write("\t\tif \"FAILURE\" in line:\n")
	postprocessing_file.write("\t\t\tfailed_logs.append(log_file)\n")
	postprocessing_file.write("if len(failed_logs) == 0:\n")
	postprocessing_file.write("\tos.system(\"" + merge_command + "\")\n")
	postprocessing_file.write("else:\n")
	postprocessing_file.write("\tprint(\"Some jobs failed. You need to retry them.\")")
	postprocessing_file.write("\tfor failed_log in failed_logs:\n")
	postprocessing_file.write("\t\tprint failed_log\n")
	postprocessing_file.close()

	# cd back
	os.chdir(start_directory)

def RunBHistogramsSignal(analysis, sample, files_per_job=1, retar=False, data_source=None):
	# Create working directory and cd
	start_directory = os.getcwd()
	working_directory = dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/submit_" + analysis + "_" + sample
	os.system("mkdir -pv " + working_directory)
	os.chdir(working_directory)

	command = "condor_cmsRun"
	if retar:
		command += " --retar "
	#input_txt = open("tmp.txt", 'w')
	#input_txt.write(analysis_config.files_QCDBEventTree[sample] + "\n")
	#input_txt.close()
	command += " --file-list=" + analysis_config.files_QCDBEventTree[sample] + " "
	command += " --files-per-job=" + str(files_per_job)
	command += " --submit-file=submit_" + analysis + "_" + sample + ".jdl "
	#command += " --output-file=" + output_prefix + "_" + sample + ".root "
	command += " --output-tag=BHistograms_" + sample + " "
	command += " --run "
	command += "  " + dijet_directory + "/CMSSW_5_3_32_patch3/src/MyTools/RootUtils/scripts/cmsRun_wrapper.sh " + analysis_config.analysis_cfgs[analysis] 
	command += " dataSource=simulation "
	command += " dataType=signal "
	command += " signalMass=" + str(analysis_config.simulation.signal_sample_masses[sample]) + " "
	#command += "inputFiles=" + os.path.basename(input_files[sample])
	output_filename = os.path.basename(analysis_config.get_b_histogram_filename(analysis, sample)).replace(".root", "_\$\(Cluster\)_\$\(Process\).root")
	command += " outputFile=" + os.path.basename(analysis_config.get_b_histogram_filename(analysis, sample)).replace(".root", "_\$\(Cluster\)_\$\(Process\).root")
	print command
	os.system(command)
	os.system("rm -f tmp.txt")
	postprocessing_file = open('postprocessing_' + analysis + "_" + sample + ".sh", 'w')
	postprocessing_file.write("#!/bin/bash\n")
	postprocessing_file.write("hadd " + working_directory + "/" + os.path.basename(analysis_config.get_b_histogram_filename(analysis, sample)) + " " + output_filename.replace("_\$\(Cluster\)_\$\(Process\)", "*") + "\n")
	postprocessing_file.close()

	# cd back
	os.chdir(start_directory)

def RunBHistogramsBackground(analysis, sample, files_per_job=1, retar=False, data_source=None):
	# Create working directory and cd
	start_directory = os.getcwd()
	working_directory = dijet_directory + "/data/EightTeeEeVeeBee/BHistograms/condor/submit_" + analysis + "_" + sample
	os.system("mkdir -pv " + working_directory)
	os.chdir(working_directory)

	command = "condor_cmsRun"
	if retar:
		command += " --retar "
	#input_txt = open("tmp.txt", 'w')
	#input_txt.write(analysis_config.files_QCDBEventTree[sample] + "\n")
	#input_txt.close()
	command += " --file-list=" + analysis_config.files_QCDBEventTree[sample] + " "
	command += " --files-per-job=" + str(files_per_job)
	command += " --submit-file=submit_" + analysis + "_" + sample + ".jdl "
	#command += " --output-file=" + output_prefix + "_" + sample + ".root "
	command += " --output-tag=BHistograms_" + sample + " "
	command += " --run "
	command += "  " + dijet_directory + "/CMSSW_5_3_32_patch3/src/MyTools/RootUtils/scripts/cmsRun_wrapper.sh " + analysis_config.analysis_cfgs[analysis] 
	command += " dataSource=simulation "
	command += " dataType=background "
	#command += "inputFiles=" + os.path.basename(input_files[sample])
	output_filename = os.path.basename(analysis_config.get_b_histogram_filename(analysis, sample)).replace(".root", "_\$\(Cluster\)_\$\(Process\).root")
	command += " outputFile=" + os.path.basename(analysis_config.get_b_histogram_filename(analysis, sample)).replace(".root", "_\$\(Cluster\)_\$\(Process\).root")
	print command
	os.system(command)
	os.system("rm -f tmp.txt")
	postprocessing_file = open('postprocessing_' + analysis + "_" + sample + ".sh", 'w')
	postprocessing_file.write("#!/bin/bash\n")
	postprocessing_file.write("hadd " + working_directory + "/" + os.path.basename(analysis_config.get_b_histogram_filename(analysis, sample)) + " " + output_filename.replace("_\$\(Cluster\)_\$\(Process\)", "*") + "\n")
	postprocessing_file.close()

	# cd back
	os.chdir(start_directory)


if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description = 'Run BHistograms')
	parser.add_argument('analysis', type=str, help='Name of analysis chain (see analysis_configuration_8TeV.py)')
	parser.add_argument('--data', type=str, help='Run data sample. Specify the sample name, e.g. BJetsPlusX_2012')
	parser.add_argument('--signal', type=str, help='Run signal MC jobs. Specify the model (Hbb, Zprime, RSG) or specific sample')
	parser.add_argument('--background', type=str, help='Run background MC jobs. Specify the background (QCD, QCDB) or specific sample')
	parser.add_argument('--noretar', action='store_true', help='Force no retar')
	args = parser.parse_args()

	if args.data:
		if analysis_config.data_supersamples.has_key(args.data):
			samples = analysis_config.data_supersamples[args.data]
		elif args.data in analysis_config.data_samples:
			samples = [args.data]
		first = True
		for sample in samples:
			RunBHistogramsEOS(args.analysis, sample, retar=(first and not args.noretar), data_source="collision_data")
			if first:
				first=False

	elif args.signal:
		if args.signal in analysis_config.simulation.signal_models:
			samples = analysis_config.simulation.signal_samples[args.signal]
		else:
			samples = [args.signal]
		first = True
		for sample in samples:
			RunBHistogramsSignal(args.analysis, sample, retar=(first and not args.noretar))
			if first:
				first = False
	elif args.background:
		if args.background in analysis_config.simulation.backgrounds:
			samples = analysis_config.simulation.background_samples[args.background]
		else:
			samples = [args.background]
		first = True
		for sample in samples:
			RunBHistogramsEOS(args.analysis, sample, retar = (first and not args.noretar), data_source="simulation")
			if first:
				first = True
