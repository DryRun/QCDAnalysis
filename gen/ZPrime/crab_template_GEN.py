from CRABClient.UserUtilities import config
config = config()

config.General.requestName = @REQUESTNAME@
config.General.transferLogs = True

config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = @PSETNAME@
config.JobType.inputFiles = @INPUTFILES@

config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = @UNITSPERJOB@
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True
config.Data.outputPrimaryDataset = @OUTPUTDATASET@
config.Data.outputDatasetTag = 'GEN-SIM'

config.Site.storageSite = T3_US_Brown
