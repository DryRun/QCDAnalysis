from sys import argv
import commands
import time
import re
import os
import string
from os import listdir

import sys
sys.path.append('./')

models = ['GluGluSpin0ToBBbar', 'RSGravitonToBBbar_kMpl01']
debug = True

def GetDatasetName(model, mass, stage):
    if model == "GluGluSpin0ToBBbar":
        base1 = "GluGluSpin0ToBBbar_M_@MASS@_TuneCUEP8M1_13TeV_pythia8"
    elif model == "RSGravitonToBBbar_kMpl01":
        base1 = "RSGravitonToBBbar_kMpl01_M_@MASS@_TuneCUEP8M1_13TeV_pythia8"
    return [base1.replace("@MASS@", str(int(mass))), "dryu-" + stage, "USER"]

def GetCFIPath(model, mass):
    return "/uscms/home/dryu/Dijets/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/gen/" + GetDatasetName(model, mass, "NULL")[0] + "_cfi.py" 

def MakeCFI(model, mass, width):
    if model == "GluGluSpin0ToBBbar":
        template = open("/uscms/home/dryu/Dijets/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/gen/GluGluSpin0ToBBbar_M_X_TuneCUEP8M1_13TeV_pythia8_cfi.py.template", 'r')
    elif model == "RSGravitonToBBbar_kMpl01":
        template = open("/uscms/home/dryu/Dijets/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/gen/RSGravitonToBBbar_kMpl01_M_X_TuneCUEP8M1_13TeV_pythia8_cfi.py.template", 'r')
    cfi = open("/uscms/home/dryu/Dijets/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/gen/" + GetDatasetName(model, mass, "NULL") + "_cfi.py", 'w')

def create(mass=750 , width=0.01):

    fin = open( spin+'_cfi.py' , 'r')
    fout = open( spin.replace('_X_', '_'+str(mass)+'_')+'_cfi.py', 'w')

    for line in fin:
        if 'm0' in line:
            fout.write(line.rstrip('\',\n')+("%.0f" % mass)+'\', \n')
        elif 'mWidth' in line:
            fout.write(line.rstrip('\',\n')+("%.1f" % (mass*width))+'\', \n')
        else:
            fout.write(line)

    fout.close()
    fin.close()
    
##################

def create_GENSIM_cfg( mass ):
    command = 'cmsDriver.py Configuration/GenProduction/python/'+(spin.replace('_X_', '_'+str(mass)+'_'))+'_cfi.py'+' --fileout file:GEN-SIM.root --mc --eventcontent RAWSIM --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --conditions MCRUN2_71_V1::All --beamspot Realistic50ns13TeVCollision --step GEN,SIM --magField 38T_PostLS1 --python_filename GEN-SIM_'+str(mass)+'_cfg.py --no_exec -n 3'
    print command
    os.system(command)

#################

def create_GENSIM_crab( mass, unitsPerJob, totalUnits, version=''):

    fin = open( 'crab_GEN-SIM_cfg.py.ex', 'r')
    fout = open( 'crab_GEN-SIM_'+str(mass)+'_cfg.py', 'w')

    for line in fin:
        if 'requestName' in line:
            fout.write(line.rstrip('\n')+' \'gen-sim_'+spin+'_'+str(mass)+version+'\'\n')
        elif 'psetName' in line:
            fout.write(line.rstrip('\n')+' \'GEN-SIM_'+str(mass)+'_cfg.py\'\n')
        elif 'unitsPerJob' in line:
            fout.write(line.rstrip('\n')+' '+str(unitsPerJob)+'\n')
        elif 'totalUnits' in line:
            fout.write(line.rstrip('\n')+' '+str(totalUnits)+'\n')
        elif 'outputPrimaryDataset' in line:
            fout.write(line.rstrip('\n')+' \''+(spin.replace('_X_', '_'+str(mass)+'_'))+'\'\n')
        elif 'outputDatasetTag' in line:
            fout.write(line.rstrip('\'\n')+version+'\'\n')
        else:
            fout.write(line)
    fout.close()
    fin.close()

#################################

def submit_GENSIM_crab(mass):
    command = 'crab submit -c '+'crab_GEN-SIM_'+str(mass)+'_cfg.py'
    print command
    if debug:
        return
    os.system(command)


#################################

def sequence_GENSIM(mass,version=''):
    create(mass)
    create_GENSIM_cfg(mass)
    create_GENSIM_crab(mass, 1000, 100000, version)
    submit_GENSIM_crab(mass)

#################################

def create_DR1_cfg( mass ):
    command = 'cmsDriver.py step1 --filein file:GEN-SIM.root --fileout file:DIGI-RECO_step1.root --pileup_input "dbs:/MinBias_TuneCUETP8M1_13TeV-pythia8/RunIISummer15GS-MCRUN2_71_V1-v2/GEN-SIM" --mc --eventcontent RAWSIM --pileup 2015_25ns_FallMC_matchData_PoissonOOTPU --datatier GEN-SIM-RAW --conditions 76X_mcRun2_asymptotic_v12 --step DIGI,L1,DIGI2RAW,HLT:@frozen25ns --era Run2_25ns --python_filename DIGI-RECO_1_'+str(mass)+'_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n -1' 
    print command
    os.system(command)

#################################

def create_DR1_crab( mass, dataset, version=''):

    fin = open( 'crab_DR1_cfg.py.ex', 'r')
    fout = open( 'crab_DR1_'+str(mass)+'_cfg.py', 'w')

    for line in fin:
        if 'requestName' in line:
            fout.write(line.rstrip('\n')+' \'dr1_'+spin+'_'+str(mass)+version+'\'\n')
        elif 'psetName' in line:
            fout.write(line.rstrip('\n')+' \'DIGI-RECO_1_'+str(mass)+'_cfg.py\'\n')
        elif 'inputDataset' in line:
            fout.write(line.rstrip('\n')+' \''+dataset+'\'\n')
        elif 'outputDatasetTag' in line:
            fout.write(line.rstrip('\'\n')+version+'\'\n')
        else:
            fout.write(line)
    fout.close()
    fin.close()

#################################

def submit_DR1_crab(mass):
    command = 'crab submit -c '+'crab_DR1_'+str(mass)+'_cfg.py'
    print command
    if debug:
        return
    os.system(command)

#################################

def sequence_DR1(mass,version=''):
    create_DR1_cfg(mass)
    create_DR1_crab(mass, datasets[spin][str(mass)]['DR1'], version)
    submit_DR1_crab(mass)

#################################

def create_DR2_cfg( mass ):
    command = 'cmsDriver.py step2 --filein file:DIGI-RECO_step1.root --fileout file:DIGI-RECO.root --mc --eventcontent AODSIM,DQM --runUnscheduled --datatier AODSIM,DQMIO --conditions 76X_mcRun2_asymptotic_v12 --step RAW2DIGI,L1Reco,RECO,EI,DQM:DQMOfflinePOGMC --era Run2_25ns --python_filename DIGI-RECO_2_'+str(mass)+'_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 1'
    print command
    os.system(command)

#################################

def create_DR2_crab( mass, dataset,version=''):

    fin = open( 'crab_DR2_cfg.py.ex', 'r')
    fout = open( 'crab_DR2_'+str(mass)+'_cfg.py', 'w')

    for line in fin:
        if 'requestName' in line:
            fout.write(line.rstrip('\n')+' \'dr2_'+spin+'_'+str(mass)+version+'\'\n')
        elif 'psetName' in line:
            fout.write(line.rstrip('\n')+' \'DIGI-RECO_2_'+str(mass)+'_cfg.py\'\n')
        elif 'inputDataset' in line:
            fout.write(line.rstrip('\n')+' \''+dataset+'\'\n')
        elif 'outputDatasetTag' in line:
            fout.write(line.rstrip('\'\n')+version+'\'\n')
        else:
            fout.write(line)
    fout.close()
    fin.close()

#################################

def submit_DR2_crab(mass):
    command = 'crab submit -c '+'crab_DR2_'+str(mass)+'_cfg.py'
    print command
    if debug:
        return
    os.system(command)

#################################

def sequence_DR2(mass,version=''):
    create_DR2_cfg(mass)
    create_DR2_crab(mass, datasets[spin][str(mass)]['DR2'], version )
    submit_DR2_crab(mass)

#################################

def create_MiniAODv2_cfg( mass ):
    command = 'cmsDriver.py step1 --filein file:DIGI-RECO.root --fileout file:MiniAODv2.root --mc --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM --conditions 76X_mcRun2_asymptotic_v12 --step PAT --era Run2_25ns --python_filename MiniAODv2_'+str(mass)+'_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n -1'
    print command
    os.system(command)

#################################

def create_MiniAODv2_crab( mass, dataset, version=''):

    fin = open( 'crab_MiniAODv2_cfg.py.ex', 'r')
    fout = open( 'crab_MiniAODv2_'+str(mass)+'_cfg.py', 'w')

    for line in fin:
        if 'requestName' in line:
            fout.write(line.rstrip('\n')+' \'miniAODv2_'+spin+'_'+str(mass)+version+'\'\n')
        elif 'psetName' in line:
            fout.write(line.rstrip('\n')+' \'MiniAODv2_'+str(mass)+'_cfg.py\'\n')
        elif 'inputDataset' in line:
            fout.write(line.rstrip('\n')+' \''+dataset+'\'\n')
        elif 'outputDatasetTag' in line:
            fout.write(line.rstrip('\'\n')+version+'\'\n')
        else:
            fout.write(line)
    fout.close()
    fin.close()

#################################

def submit_MiniAODv2_crab(mass):
    command = 'crab submit -c '+'crab_MiniAODv2_'+str(mass)+'_cfg.py'
    print command
    if debug:
        return
    os.system(command)

#################################

def sequence_MiniAODv2(mass,version=''):
    create_MiniAODv2_cfg(mass)
    create_MiniAODv2_crab(mass, datasets[spin][str(mass)]['MiniAODv2'], version )
    submit_MiniAODv2_crab(mass)

################################


# finally, we run:
for mass in [ 
    #[650, ''],
    [750,''], 
    #[850,''],
    [1000,'_v2'],
    [1200,'_v2'],
    ]:
    if argv[1]=='GENSIM':
        sequence_GENSIM(mass[0],mass[1])
    elif argv[1]=='DR1':
        sequence_DR1(mass[0],mass[1])
    elif argv[1]=='DR2':
        sequence_DR2(mass[0], mass[1])
    elif argv[1]=='MiniAODv2':
        sequence_MiniAODv2(mass[0], mass[1])