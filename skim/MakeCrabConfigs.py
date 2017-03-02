import os
import sys

background_MC_sample_file = open('background_MC_samples.txt', 'r')
for line in background_MC_sample_file:
	if line[0] == "#":
		continue
	contents = line.split()
	sample_name = contents[0]
	sample_dataset = contents[1]
	os.system("cp crab/crab_ProcessedTreeProducer_mc_template.py crab/crab_ProcessedTreeProducer_mc_" + sample_name + ".py")
	os.system("sed -i -e 's@__DATASET__@" + sample_dataset + "@' crab/crab_ProcessedTreeProducer_mc_" + sample_name  + ".py")
	os.system("sed -i -e 's@__NAME__@" + sample_name + "@' crab/crab_ProcessedTreeProducer_mc_" + sample_name  + ".py")
	print "crab submit -c crab_ProcessedTreeProducer_mc_" + sample_name + ".py"
background_MC_sample_file.close()

#signal_MC_sample_file = open('signal_MC_samples.txt', 'r')
#for line in signal_MC_sample_file:
#	contents = line.split()
#	sample_name = contents[0]
#	sample_dataset = contents[1]
#	os.system("cp crab/crab_ProcessedTreeProducer_mc_template.py crab/crab_ProcessedTreeProducer_mc_" + sample_name + ".py")
#	os.system("sed -i -e 's@__DATASET__@" + sample_dataset + "@' crab/crab_ProcessedTreeProducer_mc_" + sample_name  + ".py")
#	os.system("sed -i -e 's@__NAME__@" + sample_name + "@' crab/crab_ProcessedTreeProducer_mc_" + sample_name  + ".py")
#	print "crab submit -c crab_ProcessedTreeProducer_mc_" + sample_name + ".py"
#signal_MC_sample_file.close()

#data_sample_file = open('data_samples.txt', 'r')
#for line in data_sample_file:
#	contents = line.split()
#	sample_name = contents[0]
#	sample_dataset = contents[1]
#	os.system("cp crab/crab_ProcessedTreeProducer_data_template.py crab/crab_ProcessedTreeProducer_data_" + sample_name + ".py")
#	os.system("sed -i -e 's@__DATASET__@" + sample_dataset + "@' crab/crab_ProcessedTreeProducer_data_" + sample_name  + ".py")
#	os.system("sed -i -e 's@__NAME__@" + sample_name + "@' crab/crab_ProcessedTreeProducer_data_" + sample_name  + ".py")
#	print "crab submit -c crab_ProcessedTreeProducer_data_" + sample_name + ".py"
#data_sample_file.close()
