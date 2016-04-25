# example crab configuration file for one single run

##________________________________________________________________________________||
#Configurables

dataset = '/QCD_Pt-600to800_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM'
tag = "vTEST5"

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
config.JobType.psetName = '/uscms/home/dryu/Dijets/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/test/ProcessedTreeProducer_mc_BJetPlusX_cfg.py'
config.JobType.pyCfgParams = ['outputFile=QCDBEventTree.root']
config.JobType.inputFiles = ['/uscms/home/dryu/Dijets/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/test/Summer12_V2_DATA_AK5PF_UncertaintySources.txt', '/uscms/home/dryu/Dijets/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/test/Summer12_V2_DATA_AK7PF_UncertaintySources.txt']

config.Data.inputDataset = dataset
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.totalUnits = 20
config.Data.unitsPerJob = 2
#config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions12/8TeV/Prompt/Cert_190456-208686_8TeV_PromptReco_Collisions12_JSON.txt'
config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication = True
config.Data.outputDatasetTag = 'QCDBEventTree_QCD_Pt-600to800_' + tag

#config.Site.storageSite = "T3_US_FNALLPC"
config.Site.storageSite = "T3_US_Brown"
config.Site.blacklist = "T1_US_FNAL_Disk"
