
# example crab configuration file for one single run

##________________________________________________________________________________||
#Configurables

dataset = '__DATASET__'
tag = "v2_0"

##________________________________________________________________________________||

jobname = "QCDBEvent"
jobname += dataset[1:].replace('/','_').replace(':','_').replace('AODSIM','')
jobname += "_" + tag
##________________________________________________________________________________||

from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

##________________________________________________________________________________||

config.General.requestName = jobname
config.General.workArea = 'crab_workarea'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '/uscms/home/dryu/Dijets/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/skim/ProcessedTreeProducer_data_JetHT_cfg.py'
config.JobType.pyCfgParams = ['outputFile=QCDBEventTree.root']
config.JobType.inputFiles = ['/uscms/home/dryu/Dijets/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/skim/Summer13_V5_DATA_UncertaintySources_AK5PF.txt', '/uscms/home/dryu/Dijets/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/skim/Summer13_V5_DATA_UncertaintySources_AK7PF.txt']

config.Data.inputDataset = dataset
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
#config.Data.totalUnits = 20
config.Data.unitsPerJob = 20
config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions12/8TeV/Prompt/Cert_190456-208686_8TeV_PromptReco_Collisions12_JSON.txt'
config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication = True
config.Data.outputDatasetTag = 'QCDBEventTree___NAME___' + tag

config.Site.storageSite = "T3_US_Brown"
