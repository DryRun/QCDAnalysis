import os
import sys

signal_MC_sample_file = open('signal_MC_samples.txt', 'r')
for line in signal_MC_sample_file:
	contents = line.split()
	sample_name = contents[0]
	sample_dataset = contents[1]
	os.system("cp crab/crab_ProcessedTreeProducer_mc_SingleMu_template.py crab/crab_ProcessedTreeProducer_mc_SingleMu_" + sample_name + ".py")
	os.system("sed -i -e 's@__DATASET__@" + sample_dataset + "@' crab/crab_ProcessedTreeProducer_mc_SingleMu_" + sample_name  + ".py")
	os.system("sed -i -e 's@__NAME__@" + sample_name + "@' crab/crab_ProcessedTreeProducer_mc_SingleMu_" + sample_name  + ".py")
	print "crab submit -c crab_ProcessedTreeProducer_mc_SingleMu_" + sample_name + ".py"
signal_MC_sample_file.close()

