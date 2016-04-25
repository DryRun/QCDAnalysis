import os
import sys
import math
from math import ceil
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/MyTools/RootUtils/python"))
import CondorJDLFile
from CondorJDLFile import CondorJDLFile
from CondorJDLFile import CondorQueue
import re
pattern_pfn = re.compile("root://cmsxrootd.fnal.gov///store") # Is this correct? Double check!

###
# This python script setup up a Queue'd submission of cmsRun to condor.
# Requirements:
# 	- The cfg.py file must have an option inputFilesTxt, which accepts a text file of input files.

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description = 'Setup and run cmsRun via condor')
	parser.add_argument('cfg', type=str, help='Configuration .py')
	parser.add_argument('--output_name', type=str, help='Output name')
	parser.add_argument('--local_input_files', type=str, help='.txt file containing list of local input files')
	parser.add_argument('--remote_input_files', type=str, help='.txt file containing list of remote input files')
	parser.add_argument('--files_per_job', type=int, default=-1, help='Files per subjob')
	args = parser.parse_args()

	if args.local_input_files and args.remote_input_files:
		print "[cmsRun_condor] ERROR : Cannot accept lists of local and remote files at the same time!"
		sys.exit(1)

	# Get input files
	input_files = []
	if args.local_input_files:
		input_files_txt = open(args.local_input_files, 'r')
		input_files = [line.rstrip() for line in input_files_txt]
	elif args.remote_input_files:
		input_files_txt = open(args.remote_input_files, 'r')
		input_files = [line.rstrip() for line in input_files_txt]

 	import datetime
 	current_timestamp = datetime.datetime.now().strftime("_%Y%m%d_%H%M%S")

	job_name = "cmsRun_" + os.path.basename(args.cfg).replace(".py", "").replace("_cfg", "") + "_" + current_timestamp

	# Make working directory
	working_directory = "/uscms/home/dryu/nobackup/condor_submissions/" + job_name
	os.system("mkdir -pv " + working_directory)

	# Make JDL file
	jdl = CondorJDLFile(working_directory)
	jdl.set_executable(os.path.expandvars("$CMSSW_BASE/python/MyTools/RootUtils/cmsRunWrapper.sh"))
	jdl.set_job_name(job_name)

	# Make lists of input files
	subjob_input_files = {}
	if args.files_per_job == -1:
		n_subjobs = 1
	else:
		n_subjobs = int(math.ceil(len(input_files) / args.files_per_job))
	for i_subjob in xrange(n_subjobs):
		subjob_input_files[i_subjob] = [input_files[i_file] for i_file in xrange(i_subjob * args.files_per_job, min(len(input_files), (i_subjob + 1) * args.files_per_job))]

	# Setup each subjob
	for i_subjob in xrange(n_subjobs):
		# If the input files are local, copy them to the worker nodes
		input_files_to_transfer = []
		if args.local_input_files:
			input_files_to_transfer = subjob_input_files[i_subjob]

		# Arguments
		arguments_string = args.cfg
		if args.local_input_files or args.remote_input_files:
			arguments_string += " inputFiles="
			if args.local_input_files:
				for input_file in subjob_input_files[i_subjob]:
					arguments_string += os.path.basename(input_file) + ","
				arguments_string.rstrip(",")
			elif args.remote_input_files:
				for input_file in subjob_input_files[i_subjob]:
					arguments_string += input_file + ","
		if args.output_name:
			arguments_string += " outputFile=" + args.output_name + ".$(Process)"
		else:
			arguments_string += "outputFile=output.root.$(Process)"

		jdl.add_queue(transfer_input_files = input_files_to_transfer, arguments = arguments_string, n_jobs = 1)

	jdl.submit(test=False)
