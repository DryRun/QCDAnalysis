from sys import argv
import commands
import time
import re
import os
import string
from os import listdir

import sys
sys.path.append('./')

models = ['GluGluSpin0ToBBbar', 'RSGravitonToBBbar']
masses = [300, 600, 750, 900, 1200]

def get_dataset_name_pieces(model, mass, stage):
    if model == "GluGluSpin0ToBBbar":
        base1 = "GluGluSpin0ToBBbar_M_@MASS@_TuneCUEP8M1_8TeV_pythia8"
    elif model == "RSGravitonToBBbar":
        base1 = "RSGravitonToBBbar_kMpl01_M_@MASS@_TuneCUEP8M1_8TeV_pythia8"
    return [base1.replace("@MASS@", str(int(mass))), "dryu-" + stage, "USER"]

def get_dataset_name(model, mass, stage):
    return "/" + "/".join(get_dataset_name_pieces(model, mass, "DR1")) + "/"

def get_CFI_path(model, mass):
    return "$CMSSW_BASE/src/CMSDIJET/QCDAnalysis/python/" + get_dataset_name_pieces(model, mass, "NULL")[0] + "_cfi.py" 

def make_CFI(model, mass, width=0.01):
    if model == "GluGluSpin0ToBBbar":
        template = open("/uscms/home/dryu/Dijets/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/python/GluGluSpin0ToBBbar_M_X_TuneCUEP8M1_8TeV_pythia8_cfi.py.template")
    elif model == "RSGravitonToBBbar":
        template = open("/uscms/home/dryu/Dijets/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/python/RSGravitonToBBbar_kMpl01_M_X_TuneCUEP8M1_8TeV_pythia8_cfi.py.template")
    cfi = open(os.path.expandvars(get_CFI_path(model, mass)), 'w')
    for line in template:
        if 'm0' in line:
            cfi.write(line.rstrip('\',\n')+("%.0f" % mass)+'\', \n')
        elif 'mWidth' in line:
            cfi.write(line.rstrip('\',\n')+("%.1f" % (mass*width))+'\', \n')
        else:
            cfi.write(line)
    cfi.close()
    template.close()

def create_GENSIM_cfg(model, mass):
    command = 'cmsDriver.py ' + get_CFI_path(model, mass).replace("$CMSSW_BASE/src/", "")+' --fileout file:GEN-SIM.root --mc --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --conditions auto:mc --beamspot Realistic8TeVCollision --step GEN,SIM --python_filename GEN-SIM_'+model+"_"+str(mass)+'_cfg.py --no_exec -n 3'
    print command
    os.system(command)

#################

def create_GENSIM_crab(model, mass, unitsPerJob, totalUnits, version=''):

    fin = open( 'crab_GEN-SIM_cfg.py.template', 'r')
    fout = open( 'crab_GEN-SIM_'+model + "_" + str(mass)+'_cfg.py', 'w')

    for line in fin:
        if 'requestName' in line:
            fout.write(line.rstrip('\n')+' \'gen-sim_'+model+'_'+str(mass)+ "_v" + version+'\'\n')
        elif 'psetName' in line:
            fout.write(line.rstrip('\n')+' \'GEN-SIM_'+model+"_"+str(mass)+'_cfg.py\'\n')
        elif 'unitsPerJob' in line:
            fout.write(line.rstrip('\n')+' '+str(unitsPerJob)+'\n')
        elif 'totalUnits' in line:
            fout.write(line.rstrip('\n')+' '+str(totalUnits)+'\n')
        elif 'outputPrimaryDataset' in line:
            fout.write(line.rstrip('\n')+' \''+(model.replace('_X_', '_'+str(mass)+'_'))+'\'\n')
        elif 'outputDatasetTag' in line:
            fout.write(line.rstrip('\'\n')+"_v" + version+'\'\n')
        else:
            fout.write(line)
    fout.close()
    fin.close()

#################################

def submit_GENSIM_crab(model, mass, submit=False):
    command = 'crab submit -c '+'crab_GEN-SIM_'+model + "_" + str(mass)+'_cfg.py'
    print command
    if submit:
        os.system(command)


#################################

def sequence_GENSIM(model, mass,version='',submit=False):
    make_CFI(model, mass)
    create_GENSIM_cfg(model, mass)
    if version == "test":
        n_total = 1000
    else:
        n_total = 100000
    create_GENSIM_crab(model, mass, 1000, n_total, version)
    submit_GENSIM_crab(model, mass, submit)

#################################

def create_DR1_cfg(model, mass):
    command = 'cmsDriver.py step1 --filein file:GEN-SIM.root --fileout file:DIGI-RECO_step1.root --mc --eventcontent RAWSIM --pileup 2012_Summer_50ns_PoissonOOTPU --datatier GEN-SIM-RAW --conditions auto:mc --step DIGI,L1,DIGI2RAW,HLT:7E33v2 --python_filename DIGI-RECO_1_'+model + "_" + str(mass)+'_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n -1' 
    print command
    os.system(command)

#################################

def create_DR1_crab(model, mass, dataset, version=''):

    fin = open( 'crab_DR1_cfg.py.template', 'r')
    fout = open( 'crab_DR1_'+model + "_" + str(mass)+'_cfg.py', 'w')

    for line in fin:
        if 'requestName' in line:
            fout.write(line.rstrip('\n')+' \'dr1_'+model+'_'+str(mass)+ "_v" + version+'\'\n')
        elif 'psetName' in line:
            fout.write(line.rstrip('\n')+' \'DIGI-RECO_1_'+model + "_" + str(mass)+'_cfg.py\'\n')
        elif 'inputDataset' in line:
            fout.write(line.rstrip('\n')+' \''+dataset+'\'\n')
        elif 'outputDatasetTag' in line:
            fout.write(line.rstrip('\'\n')+ "_v" + version+'\'\n')
        else:
            fout.write(line)
    fout.close()
    fin.close()

#################################

def submit_DR1_crab(model, mass, submit=False):
    command = 'crab submit -c '+'crab_DR1_'+model + "_" + str(mass)+'_cfg.py'
    print command
    if submit:
        os.system(command)

#################################

def sequence_DR1(model, mass,version='',submit=False):
    create_DR1_cfg(model, mass)
    create_DR1_crab(model, mass, get_dataset_name(model, mass, "DR1"), version)
    submit_DR1_crab(model, mass, submit)

#################################

def create_DR2_cfg(model, mass):
    command = 'cmsDriver.py step2 --filein file:DIGI-RECO_step1.root --fileout file:DIGI-RECO.root --mc --eventcontent AODSIM,DQM --datatier AODSIM,DQMIO --conditions auto:mc --step RAW2DIGI,L1Reco,RECO,DQM:DQMOfflinePOGMC  --python_filename DIGI-RECO_2_'+model + "_" + str(mass)+'_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 1'
    print command
    os.system(command)

#################################

def create_DR2_crab(model, mass, dataset,version=''):

    fin = open( 'crab_DR2_cfg.py.template', 'r')
    fout = open( 'crab_DR2_'+model + "_" + str(mass)+'_cfg.py', 'w')

    for line in fin:
        if 'requestName' in line:
            fout.write(line.rstrip('\n')+' \'dr2_'+model+'_'+str(mass)+ "_v" + version+'\'\n')
        elif 'psetName' in line:
            fout.write(line.rstrip('\n')+' \'DIGI-RECO_2_'+model + "_" + str(mass)+'_cfg.py\'\n')
        elif 'inputDataset' in line:
            fout.write(line.rstrip('\n')+' \''+dataset+'\'\n')
        elif 'outputDatasetTag' in line:
            fout.write(line.rstrip('\'\n')+"_v"+version+'\'\n')
        else:
            fout.write(line)
    fout.close()
    fin.close()

#################################

def submit_DR2_crab(model, mass, submit=False):
    command = 'crab submit -c '+'crab_DR2_'+model + "_" + str(mass)+'_cfg.py'
    print command
    if submit:
        os.system(command)

#################################

def sequence_DR2(model, mass,version='', submit=False):
    create_DR2_cfg(model, mass)
    create_DR2_crab(model, mass, get_dataset_name(model, mass, "DR2"), version )
    submit_DR2_crab(model, mass, submit)

#################################


# finally, we run:
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description = 'Make and submit CRAB generation jobs')
    parser.add_argument('version', type=str, help='Version')
    parser.add_argument('--submit', action='store_true', default=False, help='Submit jobs after creation')
    parser.add_argument('--GENSIM', action='store_true', help='')
    parser.add_argument('--DR1', action='store_true', help='')
    parser.add_argument('--DR2', action='store_true', help='')
    args = parser.parse_args()

    for model in models:
        for mass in masses:
            if args.GENSIM:
                sequence_GENSIM(model, mass, args.version, submit=args.submit)
            elif args.DR1:
                sequence_DR1(model, mass, args.version, submit=args.submit)
            elif args.DR2:
                sequence_DR2(model, mass, args.version, submit=args.submit)
