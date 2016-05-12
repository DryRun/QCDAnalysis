
# example crab configuration file for one single run

##________________________________________________________________________________||
#Configurables

dataset = '/BJetPlusX/Run2012B-22Jan2013-v1/AOD'
tag = "v1_3_trigeff"

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
config.JobType.psetName = '/uscms/home/dryu/Dijets/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/test/ProcessedTreeProducer_data_BJetPlusX_cfg.py'
config.JobType.pyCfgParams = ['outputFile=QCDBEventTree.root']
config.JobType.inputFiles = ['/uscms/home/dryu/Dijets/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/test/Summer12_V2_DATA_AK5PF_UncertaintySources.txt', '/uscms/home/dryu/Dijets/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/test/Summer12_V2_DATA_AK7PF_UncertaintySources.txt']

config.Data.inputDataset = dataset
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.totalUnits = 4000
config.Data.unitsPerJob = 20
config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions12/8TeV/Prompt/Cert_190456-208686_8TeV_PromptReco_Collisions12_JSON.txt'
config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication = True
config.Data.outputDatasetTag = 'QCDBEventTree_BJetPlusX_Run2012B_' + tag

config.Site.storageSite = "T3_US_FNALLPC"
