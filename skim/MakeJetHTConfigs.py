import os
import sys

data_sample_file = open('data_samples_JetHT.txt', 'r')
for line in data_sample_file:
	contents = line.split()
	sample_name = contents[0]
	sample_dataset = contents[1]
	os.system("cp crab/crab_ProcessedTreeProducer_data_JetHT_template.py crab/crab_ProcessedTreeProducer_data_" + sample_name + ".py")
	os.system("sed -i -e 's@__DATASET__@" + sample_dataset + "@' crab/crab_ProcessedTreeProducer_data_" + sample_name  + ".py")
	os.system("sed -i -e 's@__NAME__@" + sample_name + "@' crab/crab_ProcessedTreeProducer_data_" + sample_name  + ".py")
	print "crab submit -c crab_ProcessedTreeProducer_data_" + sample_name + ".py"
data_sample_file.close()
