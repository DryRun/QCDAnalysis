from CRABClient.UserUtilities import config
from CRABClient.UserUtilities import getUsernameFromSiteDB
config = config()

config.General.requestName = '@REQUESTNAME@'
config.General.transferLogs = True
config.General.workArea = '/home/dryu/Dijets/data/EightTeeEeVeeBee/ZPrime/Reconstruction//DR2/crab'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '@PSETNAME@'

config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.inputDataset = '@INPUTDATASET@'
config.Data.inputDBS = 'phys03'
config.Data.publication = True
config.Data.ignoreLocality = False
config.Data.outputDatasetTag = '@OUTPUTDATASETTAG@'

config.Site.storageSite = 'T3_US_Brown'
