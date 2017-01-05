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
#masses = [300, 600, 750, 900, 1200]
#masses = [250, 400, 500]
masses = [350]

def get_dataset_name_pieces(model, mass, stage):
    if model == "GluGluSpin0ToBBbar":
        base1 = "GluGluSpin0ToBBbar_M_@MASS@_TuneCUEP8M1_8TeV_pythia8"
    elif model == "RSGravitonToBBbar":
        base1 = "RSGravitonToBBbar_kMpl01_M_@MASS@_TuneCUEP8M1_8TeV_pythia8"
    return [base1.replace("@MASS@", str(int(mass))), "dryu-" + stage, "USER"]

def get_dataset_name(model, mass, stage):
    return "/" + "/".join(get_dataset_name_pieces(model, mass, "DR1")) + "/"

actual_gensim_names = {
    'RSGravitonToBBbar_kMpl01_M_300_TuneCUEP8M1_8TeV_pythia8':'/RSGravitonToBBbar/dryu-GEN-SIM_v1_2-8dbdf10cf61968bfa85a0639a5c60768/USER',
    'RSGravitonToBBbar_kMpl01_M_600_TuneCUEP8M1_8TeV_pythia8':'/RSGravitonToBBbar/dryu-GEN-SIM_v1_2-ba5eda0a5b5bcffc961896fda771deb1/USER',
    'RSGravitonToBBbar_kMpl01_M_750_TuneCUEP8M1_8TeV_pythia8':'/RSGravitonToBBbar/dryu-GEN-SIM_v1_2-beb3715d1689fb19768ecc1c5fdbe115/USER',
    'RSGravitonToBBbar_kMpl01_M_900_TuneCUEP8M1_8TeV_pythia8':'/RSGravitonToBBbar/dryu-GEN-SIM_v1_2-3e41a852e6bf8357e98e3479bcbd7f9c/USER',
    'RSGravitonToBBbar_kMpl01_M_1200_TuneCUEP8M1_8TeV_pythia8':'/RSGravitonToBBbar/dryu-GEN-SIM_v1_2-1f395c9a7e12a67c220e875104d5ee2a/USER',
    'GluGluSpin0ToBBbar_M_1200_TuneCUEP8M1_8TeV_pythia8':'/GluGluSpin0ToBBbar/dryu-GEN-SIM_v1_2-83af25be40b86c943b5afca6bd8bb5e4/USER',
    'GluGluSpin0ToBBbar_M_300_TuneCUEP8M1_8TeV_pythia8':'/GluGluSpin0ToBBbar/dryu-GEN-SIM_v1_2-e0d918201161801092957f0f2442e35d/USER',
    'GluGluSpin0ToBBbar_M_900_TuneCUEP8M1_8TeV_pythia8':'/GluGluSpin0ToBBbar/dryu-GEN-SIM_v1_2-9c1065b7a8ac99cb5a10424c07d5f182/USER',
    'GluGluSpin0ToBBbar_M_600_TuneCUEP8M1_8TeV_pythia8':'/GluGluSpin0ToBBbar/dryu-GEN-SIM_v1_2-bf8f96f66e8acaa508f5131e44fbc297/USER',
    'GluGluSpin0ToBBbar_M_750_TuneCUEP8M1_8TeV_pythia8':'/GluGluSpin0ToBBbar/dryu-GEN-SIM_v1_1-76ca9f00fbd35571059515ca22287825/USER',
    'RSGravitonToBBbar_kMpl01_M_250_TuneCUEP8M1_8TeV_pythia8':'/RSGravitonToBBbar_kMpl01_M_250_TuneCUEP8M1_8TeV_pythia8/dryu-GEN-SIM_v1_3-d92ccb491a895b220c6119db6ad77a82/USER',
    'RSGravitonToBBbar_kMpl01_M_400_TuneCUEP8M1_8TeV_pythia8':'/RSGravitonToBBbar_kMpl01_M_400_TuneCUEP8M1_8TeV_pythia8/dryu-GEN-SIM_v1_3-5f07103a518e2dfe4de1430df5a62586/USER',
    'RSGravitonToBBbar_kMpl01_M_500_TuneCUEP8M1_8TeV_pythia8':'/RSGravitonToBBbar_kMpl01_M_500_TuneCUEP8M1_8TeV_pythia8/dryu-GEN-SIM_v1_3-719abc4a2d7c82604a1c592c517786d2/USER',
    'GluGluSpin0ToBBbar_M_250_TuneCUEP8M1_8TeV_pythia8':'/GluGluSpin0ToBBbar_M_250_TuneCUEP8M1_8TeV_pythia8/dryu-GEN-SIM_v1_3-9c0fe13af874239b82a452a1e99c1d07/USER',
    'GluGluSpin0ToBBbar_M_400_TuneCUEP8M1_8TeV_pythia8':'/GluGluSpin0ToBBbar_M_400_TuneCUEP8M1_8TeV_pythia8/dryu-GEN-SIM_v1_3-5646f4c10e0952740354a58a642a4c32/USER',
    'GluGluSpin0ToBBbar_M_500_TuneCUEP8M1_8TeV_pythia8':'/GluGluSpin0ToBBbar_M_500_TuneCUEP8M1_8TeV_pythia8/dryu-GEN-SIM_v1_3-5e3aeb3e064217e7dc300ff2c4d72ddc/USER',

    # First try during major CRAB outage. Not sure if reliable.
    #'GluGluSpin0ToBBbar_M_350_TuneCUEP8M1_8TeV_pythia8':'/GluGluSpin0ToBBbar_M_350_TuneCUEP8M1_8TeV_pythia8/dryu-GEN-SIM_v1_0-5022fca4c09ec6a3250c982e6a691c94/USER',
    #'RSGravitonToBBbar_kMpl01_M_350_TuneCUEP8M1_8TeV_pythia8':'/RSGravitonToBBbar_kMpl01_M_350_TuneCUEP8M1_8TeV_pythia8/dryu-GEN-SIM_v1_0-2089507b266388415f62eef171c53b83/USER'
    'GluGluSpin0ToBBbar_M_350_TuneCUEP8M1_8TeV_pythia8':'/GluGluSpin0ToBBbar_M_350_TuneCUEP8M1_8TeV_pythia8/dryu-GEN-SIM_v1_0_3-5022fca4c09ec6a3250c982e6a691c94/USER',
    'RSGravitonToBBbar_kMpl01_M_350_TuneCUEP8M1_8TeV_pythia8':'/RSGravitonToBBbar_kMpl01_M_350_TuneCUEP8M1_8TeV_pythia8/dryu-GEN-SIM_v1_0_3-2089507b266388415f62eef171c53b83/USER'
}

actual_dr1_names = {
    'RSGravitonToBBbar_kMpl01_M_300_TuneCUEP8M1_8TeV_pythia8':'/RSGravitonToBBbar/dryu-DIGI-RECO-1_M_300_v1_3-e55af98865f2d4f941410801f4f54826/USER',
    'RSGravitonToBBbar_kMpl01_M_600_TuneCUEP8M1_8TeV_pythia8':'/RSGravitonToBBbar/dryu-DIGI-RECO-1_M_600_v1_3-e55af98865f2d4f941410801f4f54826/USER',
    'RSGravitonToBBbar_kMpl01_M_750_TuneCUEP8M1_8TeV_pythia8':'/RSGravitonToBBbar/dryu-DIGI-RECO-1_M_750_v1_3-e55af98865f2d4f941410801f4f54826/USER',
    'RSGravitonToBBbar_kMpl01_M_900_TuneCUEP8M1_8TeV_pythia8':'/RSGravitonToBBbar/dryu-DIGI-RECO-1_M_900_v1_3-e55af98865f2d4f941410801f4f54826/USER',
    'RSGravitonToBBbar_kMpl01_M_1200_TuneCUEP8M1_8TeV_pythia8':'/RSGravitonToBBbar/dryu-DIGI-RECO-1_M_1200_v1_3-e55af98865f2d4f941410801f4f54826/USER',
    'GluGluSpin0ToBBbar_M_1200_TuneCUEP8M1_8TeV_pythia8':'/GluGluSpin0ToBBbar/dryu-DIGI-RECO-1_M_1200_v1_3-e55af98865f2d4f941410801f4f54826/USER', 
    'GluGluSpin0ToBBbar_M_300_TuneCUEP8M1_8TeV_pythia8':'/GluGluSpin0ToBBbar/dryu-DIGI-RECO-1_M_300_v1_3-e55af98865f2d4f941410801f4f54826/USER',
    'GluGluSpin0ToBBbar_M_900_TuneCUEP8M1_8TeV_pythia8':'/GluGluSpin0ToBBbar/dryu-DIGI-RECO-1_M_900_v1_3-e55af98865f2d4f941410801f4f54826/USER',
    'GluGluSpin0ToBBbar_M_600_TuneCUEP8M1_8TeV_pythia8':'/GluGluSpin0ToBBbar/dryu-DIGI-RECO-1_M_600_v1_3-e55af98865f2d4f941410801f4f54826/USER',
    'GluGluSpin0ToBBbar_M_750_TuneCUEP8M1_8TeV_pythia8':'/GluGluSpin0ToBBbar/dryu-DIGI-RECO-1_M_750_v1_3-e55af98865f2d4f941410801f4f54826/USER',
    'RSGravitonToBBbar_kMpl01_M_250_TuneCUEP8M1_8TeV_pythia8':'/RSGravitonToBBbar_kMpl01_M_250_TuneCUEP8M1_8TeV_pythia8/dryu-DIGI-RECO-1_M_250_v1_3-e55af98865f2d4f941410801f4f54826/USER',
    'RSGravitonToBBbar_kMpl01_M_400_TuneCUEP8M1_8TeV_pythia8':'/RSGravitonToBBbar_kMpl01_M_400_TuneCUEP8M1_8TeV_pythia8/dryu-DIGI-RECO-1_M_400_v1_3-e55af98865f2d4f941410801f4f54826/USER',
    'RSGravitonToBBbar_kMpl01_M_500_TuneCUEP8M1_8TeV_pythia8':'/RSGravitonToBBbar_kMpl01_M_500_TuneCUEP8M1_8TeV_pythia8/dryu-DIGI-RECO-1_M_500_v1_3-e55af98865f2d4f941410801f4f54826/USER',
    'GluGluSpin0ToBBbar_M_500_TuneCUEP8M1_8TeV_pythia8':'/GluGluSpin0ToBBbar_M_500_TuneCUEP8M1_8TeV_pythia8/dryu-DIGI-RECO-1_M_500_v1_3-e55af98865f2d4f941410801f4f54826/USER',
    'GluGluSpin0ToBBbar_M_250_TuneCUEP8M1_8TeV_pythia8':'/GluGluSpin0ToBBbar_M_250_TuneCUEP8M1_8TeV_pythia8/dryu-DIGI-RECO-1_M_250_v1_3-e55af98865f2d4f941410801f4f54826/USER',
    'GluGluSpin0ToBBbar_M_400_TuneCUEP8M1_8TeV_pythia8':'/GluGluSpin0ToBBbar_M_400_TuneCUEP8M1_8TeV_pythia8/dryu-DIGI-RECO-1_M_400_v1_3-e55af98865f2d4f941410801f4f54826/USER',
    'GluGluSpin0ToBBbar_M_350_TuneCUEP8M1_8TeV_pythia8':'/GluGluSpin0ToBBbar_M_350_TuneCUEP8M1_8TeV_pythia8/dryu-DIGI-RECO-1_M_350_v1_0_6-25f662c8c8577d562263f1e0c47637d7/USER',
    'RSGravitonToBBbar_kMpl01_M_350_TuneCUEP8M1_8TeV_pythia8':'/RSGravitonToBBbar_kMpl01_M_350_TuneCUEP8M1_8TeV_pythia8/dryu-DIGI-RECO-1_M_350_v1_0_6-25f662c8c8577d562263f1e0c47637d7/USER',
}

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
    command = 'cmsDriver.py ' + get_CFI_path(model, mass).replace("$CMSSW_BASE/src/", "")+' --fileout file:GEN-SIM.root --mc --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --conditions START53_V7C::All --beamspot Realistic8TeVCollision --step GEN,SIM --python_filename GEN-SIM_'+model+"_"+str(mass)+'_cfg.py --no_exec -n 3'
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
            fout.write(line.rstrip('\n')+' \''+get_dataset_name_pieces(model, mass, "GEN-SIM")[0]+'\'\n')
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
        n_total = 50000
    create_GENSIM_crab(model, mass, 200, n_total, version)
    submit_GENSIM_crab(model, mass, submit)

#################################

def create_DR1_cfg(model, mass):
    command = 'cmsDriver.py step1 --filein file:GEN-SIM.root --fileout file:DIGI-RECO_step1.root --mc --eventcontent RAWSIM --pileup_input "dbs:/MinBias_TuneZ2star_8TeV-pythia6/Summer12-START50_V13-v3/GEN-SIM" --pileup 2012_Summer_50ns_PoissonOOTPU --datatier GEN-SIM-RAW --conditions START53_V19::All --step DIGI,L1,DIGI2RAW,HLT:7E33v2 --python_filename DIGI-RECO_1_'+model + "_" + str(mass)+'_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n -1' 
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
            fout.write(line.rstrip('\'\n') + "_M_" + str(mass) + "_v" + version+'\'\n')
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
    input_dataset = actual_gensim_names[get_dataset_name_pieces(model, mass, "DR1")[0]]
    create_DR1_crab(model, mass, input_dataset, version)
    submit_DR1_crab(model, mass, submit)

#################################

def create_DR2_cfg(model, mass):
    command = 'cmsDriver.py step2 --filein file:DIGI-RECO_step1.root --fileout file:DIGI-RECO.root --mc --eventcontent AODSIM,DQM --datatier AODSIM,DQMIO --conditions START53_V19::All --step RAW2DIGI,L1Reco,RECO,DQM:DQMOfflinePOGMC  --python_filename DIGI-RECO_2_'+model + "_" + str(mass)+'_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 1'
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
            fout.write(line.rstrip('\'\n') + "_M_" + str(mass) + "_v"+version+'\'\n')
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
    input_dataset = actual_dr1_names[get_dataset_name_pieces(model, mass, "DR1")[0]]
    create_DR2_crab(model, mass, input_dataset, version )
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
