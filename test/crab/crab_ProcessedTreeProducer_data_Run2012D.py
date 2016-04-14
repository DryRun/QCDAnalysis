
# example crab configuration file for one single run

##________________________________________________________________________________||
#Configurables

dataset = '/JetHT/Run2012D-22Jan2013-v1/AOD'

##________________________________________________________________________________||

jobname = "QCDEvent"
jobname += dataset[1:].replace('/','_').replace(':','_').replace('AOD','')
jobname += "_v0_2"
##________________________________________________________________________________||

from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

##________________________________________________________________________________||

config.General.requestName = jobname
config.General.workArea = 'crab_workarea'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '/uscms/home/dryu/Dijets/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/test/ProcessedTreeProducer_data_cfg.py'
config.JobType.pyCfgParams = ['outputFile=QCDEventTree.root']
config.JobType.inputFiles = ['/uscms/home/dryu/Dijets/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/test/Summer12_V2_DATA_AK5PF_UncertaintySources.txt', '/uscms/home/dryu/Dijets/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/test/Summer12_V2_DATA_AK7PF_UncertaintySources.txt']

config.Data.inputDataset = dataset
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
#config.Data.totalUnits = 20
config.Data.unitsPerJob = 20
config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions12/8TeV/Prompt/Cert_190456-208686_8TeV_PromptReco_Collisions12_JSON.txt'
config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication = True
config.Data.outputDatasetTag = 'QCDEventTree_Run2012D'

config.Site.storageSite = "T3_US_FNALLPC"
