from CRABClient.UserUtilities import config
config = config()

config.General.requestName = '@REQUESTNAME@'
config.General.transferLogs = True
config.General.workArea = '/home/dryu/Dijets/data/EightTeeEeVeeBee/ZPrime/Reconstruction//GENSIM/crab'

config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = '@PSETNAME@'
config.JobType.inputFiles = @INPUTFILES@

config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = @UNITSPERJOB@
config.Data.totalUnits = @TOTALUNITS@
config.Data.publication = True
config.Data.outputPrimaryDataset = '@OUTPUTPRIMARYDATASET@'
#config.Data.outputDatasetTag = 'GEN-SIM'
config.Data.outputDatasetTag = '@OUTPUTDATASETTAG@'

#config.Site.storageSite = 'T3_US_FNALLPC'
config.Site.storageSite = 'T3_US_Brown'
