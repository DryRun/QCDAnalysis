import os
import CMSDIJET.QCDAnalysis.simulation_config
from CMSDIJET.QCDAnalysis.simulation_config import *
import CMSDIJET.QCDAnalysis.analysis_configuration_8TeV as analysis_config

# Script to submit BHistogram jobs
# - Two functions, RunData and RunSignal, setup the condor submission of 'cmsRun analysis_cfg.py inputFiles=<> outputFile=<>'. 
# - The functions have to be separate because the data skim files reside on EOS and have to be chopped up into subjobs, while the signal skims are in single files.

# RunData
# - Input files are on EOS, so you can't do the normal files-per-job mechanism (this cp's the files to the worker node, which is bad for EOS). 
# - Instead, do the subjobbing manually. 
def RunData(analysis, sample, files_per_job=200):
	# Create working directory and cd
	start_directory = os.getcwd()
	working_directory = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/BHistograms/condor/submit_" + analysis + "_" + sample
	os.system("mkdir -pv " + working_directory)
	os.chdir(working_directory)

	first = True
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
		if first:
			first = False
			command += " --retar "
		command += " --submit-file=submit_" + analysis + "_" + sample + ".subjob" + str(subjob_index) + ".jdl "
		command += " --output-tag=BHistograms_" + sample + ".subjob" + str(subjob_index) + " "
		command += " --run /uscms/home/dryu/Dijets/CMSSW_5_3_32_patch3/src/MyTools/RootUtils/scripts/cmsRun_wrapper.sh " + analysis_config.analysis_cfgs[analysis] + " dataSource=collision_data dataType=data inputFiles="
		for input_file in this_job_files:
			command += input_file + ","
		command = command.rstrip(",")
		subjob_output_filename = os.path.basename(analysis_config.get_b_histogram_filename(analysis, sample) + ".subjob" + str(subjob_index))
		command += " outputFile=" + subjob_output_filename
		subjob_output_filenames.append(subjob_output_filename)

		#print command
		os.system(command)
		subjob_index += 1

	# Print merge command
	merge_command = "hadd " + analysis_config.get_b_histogram_filename(analysis, sample) + " " + working_directory + "/" + os.path.basename(analysis_config.get_b_histogram_filename(analysis, sample)) + ".subjob*"
	postprocessing_file = open('postprocessing_' + analysis + "_" + sample + ".sh", 'w')
	postprocessing_file.write("#!/bin/bash\n")
	postprocessing_file.write(merge_command + "\n")
	postprocessing_file.close()

	# cd back
	os.chdir(start_directory)

def RunSignal(analysis, samples):

	#samples, input_files, sample_masses, cfg_file="~/Dijets/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/analyze/BHistograms_cfg.py", output_prefix="BHistograms"):
	first = True
	for sample in samples:
		# Create working directory and cd
		start_directory = os.getcwd()
		working_directory = "/uscms/home/dryu/Dijets/data/EightTeeEeVeeBee/BHistograms/condor/submit_" + analysis + "_" + sample
		os.system("mkdir -pv " + working_directory)
		os.chdir(working_directory)

		command = "condor_cmsRun"
		if first:
			first = False
			command += " --retar "
		input_txt = open("tmp.txt", 'w')
		input_txt.write(analysis_config.files_QCDBEventTree[sample] + "\n")
		input_txt.close()
		command += " --file-list=tmp.txt "
		command += " --submit-file=submit_" + analysis + "_" + sample + ".jdl "
		#command += " --output-file=" + output_prefix + "_" + sample + ".root "
		command += " --output-tag=BHistograms_" + sample + " "
		command += " --run /uscms/home/dryu/Dijets/CMSSW_5_3_32_patch3/src/MyTools/RootUtils/scripts/cmsRun_wrapper.sh " + analysis_config.analysis_cfgs[analysis] 
		command += " dataSource=simulation "
		command += " dataType=signal "
		command += " signalMass=" + str(sample_masses[sample]) + " "
		#command += "inputFiles=" + os.path.basename(input_files[sample])
		command += " outputFile=" + os.path.basename(analysis_config.get_b_histogram_filename(analysis, sample))
		#print command
		os.system(command)
		os.system("rm -f tmp.txt")
		postprocessing_file = open('postprocessing_' + analysis + "_" + sample + ".sh", 'w')
		postprocessing_file.write("#!/bin/bash\n")
		postprocessing_file.write("mv " + working_directory + "/" + os.path.basename(analysis_config.get_b_histogram_filename(analysis, sample)) + " " + analysis_config.get_b_histogram_filename(analysis, sample) + "\n")
		postprocessing_file.close()

		# cd back
		os.chdir(start_directory)


if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description = 'Run BHistograms')
	parser.add_argument('analysis', type=str, help='Name of analysis chain (see analysis_configuration_8TeV.py)')
	parser.add_argument('sample', type=str, help='Name of sample (see analysis_configuration_8TeV.py; can also be a data supersample (e.g. BJetPlusX_2012) or a general signal model (Hbb, Zprime, RSG))')
	#parser.add_argument('--data', action='store_true', help='Run data jobs')
	#parser.add_argument('--signal', type=str, help='Run signal MC jobs. Specify the model: Hbb, Zprime, RSG')
	args = parser.parse_args()

	if analysis_config.data_supersamples.has_key(args.sample):
		for sample in analysis_config.data_supersamples[args.sample]:
			RunData(args.analysis, sample)
	elif args.sample in analysis_config.data_samples:
		RunData(args.analysis, sample)
	else:
		# Signal job
		if args.sample in analysis_config.signal_models:
			# All signal samples corresponding to the specified model
			signal_samples = analysis_config.signal_samples[args.sample]
		else:
			# Single signal sample
			signal_samples = [args.sample]
		RunSignal(args.analysis, signal_samples)

