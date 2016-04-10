import FWCore.ParameterSet.Config as cms

process = cms.Process("Ana")
process.load('FWCore.MessageService.MessageLogger_cfi')
##-------------------- Communicate with the DB -----------------------
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
# process.GlobalTag.globaltag = 'GR_R_52_V9::All' # I think I'm going to use the one for 2013 reprocessing, as seen in DAS
process.GlobalTag.globaltag = 'FT_R_53_V18::All'
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
#process.load('Configuration.StandardSequences.Geometry_cff')
process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load('RecoJets.Configuration.RecoPFJets_cff')
process.load('RecoJets.Configuration.RecoJets_cff')
process.load('CommonTools/RecoAlgos/HBHENoiseFilterResultProducer_cfi')
##-------------------- Import the JEC services -----------------------
process.load('JetMETCorrections.Configuration.DefaultJEC_cff')
#############   Set the number of events #############
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(500)
)
#############   Format MessageLogger #################
process.MessageLogger.cerr.FwkReport.reportEvery = 100
#############   Define the source file ###############
process.source = cms.Source("PoolSource",
#    fileNames = cms.untracked.vstring('/store/data/Run2012A/Jet/AOD/PromptReco-v1/000/190/645/DEC9A907-9182-E111-9A70-001D09F291D7.root')
   fileNames = cms.untracked.vstring(
  #    '/store/data/Run2012B/JetHT/AOD/PromptReco-v1/000/194/210/1039974D-94A0-E111-858C-0019B9F581C9.root',
#   '/store/data/Run2012B/JetHT/AOD/PromptReco-v1/000/194/790/D8C1E75A-11A7-E111-893C-002481E0D83E.root',
   #'/store/data/Run2012A/HT/AOD/PromptReco-v1/000/191/226/E6A324AB-DB87-E111-8AE1-001D09F290CE.root',
   #'/store/data/Run2012A/HT/AOD/PromptReco-v1/000/191/062/D683897F-E786-E111-81E4-BCAEC518FF63.root',   
   #'/store/data/Run2012B/JetHT/AOD/PromptReco-v1/000/196/362/76D24624-E7B8-E111-8562-0019B9F72CE5.root'
   #'/store/data/Run2012C/JetHT/AOD/22Jan2013-v1/20000/00021EB1-1C6A-E211-99E9-002590596498.root', 
   'file:/uscms/home/dryu/Dijets/data/AOD/00021EB1-1C6A-E211-99E9-002590596498.root'
)
)
############# processed tree producer ##################
process.TFileService = cms.Service("TFileService",fileName = cms.string('ProcessedTree_data.root'))

process.ak7 = cms.EDAnalyzer('ProcessedTreeProducer',
    ## jet collections ###########################
    pfjets          = cms.InputTag('ak7PFJets'),
    calojets        = cms.InputTag('ak7CaloJets'),
    ## database entry for the uncertainties ######
    PFPayloadName   = cms.string('AK7PF'),
    CaloPayloadName = cms.string('AK7Calo'),
    jecUncSrc       = cms.string('Summer12_V2_DATA_AK7PF_UncertaintySources.txt'),
    jecUncSrcNames  = cms.vstring('Absolute','HighPtExtra','SinglePion','Flavor','Time',
                                  'RelativeJEREC1','RelativeJEREC2','RelativeJERHF',
                                  'RelativeStatEC2','RelativeStatHF','RelativeFSR',
                                  'PileUpDataMC','PileUpOOT','PileUpPt','PileUpBias','PileUpJetRate',
                                  'SubTotalPileUp','SubTotalRelative','SubTotalPt','SubTotalDataMC','Total'),
    
    ## calojet ID and extender for the JTA #######
    calojetID       = cms.InputTag('ak7JetID'),
    calojetExtender = cms.InputTag('ak7JetExtender'),
    ## set the conditions for good Vtx counting ##
    offlineVertices = cms.InputTag('offlinePrimaryVertices'),
    goodVtxNdof     = cms.double(4), 
    goodVtxZ        = cms.double(24),
    ## rho #######################################
    srcCaloRho      = cms.InputTag('kt6CaloJets','rho'),
    srcPFRho        = cms.InputTag('kt6PFJets','rho'),
    ## preselection cuts #########################
    maxY            = cms.double(5.0), 
    minPFPt         = cms.double(20),
    minPFFatPt      = cms.double(10),
    maxPFFatEta     = cms.double(2.5),
    minCaloPt       = cms.double(20),
    minNPFJets      = cms.int32(1),
    minNCaloJets    = cms.int32(1), 
    minJJMass       = cms.double(-1),
    ## trigger ###################################
    printTriggerMenu = cms.untracked.bool(True),
    processName     = cms.string('HLT'),
    triggerName     = cms.vstring('HLT_PFJet40_v3','HLT_PFJet40_v4','HLT_PFJet40_v5',
                                  'HLT_PFJet80_v3','HLT_PFJet80_v4','HLT_PFJet80_v5',
                                  'HLT_PFJet140_v3','HLT_PFJet140_v4','HLT_PFJet140_v5',
                                  'HLT_PFJet200_v3','HLT_PFJet200_v4','HLT_PFJet200_v5',
                                  'HLT_PFJet260_v3','HLT_PFJet260_v4','HLT_PFJet260_v5',
                                  'HLT_PFJet320_v3','HLT_PFJet320_v4','HLT_PFJet320_v5', 
                                  'HLT_PFJet400_v3','HLT_PFJet400_v4','HLT_PFJet400_v5',
                                  'HLT_HT200_v1','HLT_HT200_v2','HLT_HT200_v3','HLT_HT200_v4','HLT_HT200_v5',
                                  'HLT_HT250_v1','HLT_HT250_v2','HLT_HT250_v3','HLT_HT250_v4','HLT_HT250_v5',
                                  'HLT_HT300_v1','HLT_HT300_v2','HLT_HT300_v3','HLT_HT300_v4','HLT_HT300_v5',
                                   'HLT_HT350_v1','HLT_HT350_v2','HLT_HT350_v3','HLT_HT350_v4','HLT_HT350_v5',
                                   'HLT_HT400_v1','HLT_HT400_v2','HLT_HT400_v3','HLT_HT400_v4','HLT_HT400_v5',
                                   'HLT_HT450_v1','HLT_HT450_v2','HLT_HT450_v3','HLT_HT450_v4','HLT_HT450_v5',
                                   'HLT_HT500_v1','HLT_HT500_v2','HLT_HT500_v3','HLT_HT500_v4','HLT_HT500_v5',
                                   'HLT_HT550_v1','HLT_HT550_v2','HLT_HT550_v3','HLT_HT550_v4','HLT_HT550_v5',
                                   'HLT_HT650_v1','HLT_HT650_v2','HLT_HT650_v3','HLT_HT650_v4','HLT_HT650_v5',
                                   'HLT_HT750_v1','HLT_HT750_v2','HLT_HT750_v3','HLT_HT750_v4','HLT_HT750_v5',  
				   'HLT_PFNoPUHT650_v1','HLT_PFNoPUHT650_v2',
           #'HLT_PFNoPUHT650_v3', note: this causes an error per event! The L1T name has two triggers with "OR" in between, which makes the trigger tool unhappy.
           'HLT_PFNoPUHT650_v4','HLT_PFNoPUHT650_v5',  
                                   'HLT_PFNoPUHT700_v1','HLT_PFNoPUHT700_v2',
                                   #'HLT_PFNoPUHT700_v3',
                                   'HLT_PFNoPUHT700_v4','HLT_PFNoPUHT700_v5',
                                   'HLT_PFNoPUHT750_v1','HLT_PFNoPUHT750_v2',
                                   #'HLT_PFNoPUHT750_v3',
                                   'HLT_PFNoPUHT750_v4','HLT_PFNoPUHT750_v5',
                                   'HLT_FatDiPFJetMass750_DR1p1_Deta1p5_v2','HLT_FatDiPFJetMass750_DR1p1_Deta1p5_v3','HLT_FatDiPFJetMass750_DR1p1_Deta1p5_v4','HLT_FatDiPFJetMass750_DR1p1_Deta1p5_v5','HLT_FatDiPFJetMass750_DR1p1_Deta1p5_v6','HLT_FatDiPFJetMass750_DR1p1_Deta1p5_v7',
      #  'HLT_HT200(_v[0-9])?$','HLT_HT250(_v[0-9])?$','HLT_HT300(_v[0-9])?$','HLT_HT350(_v[0-9])?$','HLT_HT400(_v[0-9])?$','HLT_HT450(_v[0-9])?$','HLT_HT500(_v[0-9])?$','HLT_HT550(_v[0-9])?$','HLT_HT650(_v[0-9])?$','HLT_HT750(_v[0-9])?$','HLT_FatDiPFJetMass750_DR1p1_Deta1p5(_v[0-9])?$','HLT_PFHT650(_v[0-9])?$'
                               #   'HLT_PFJet200_v*','HLT_PFJet260_v*','HLT_PFJet320_v*',
                               #   'HLT_PFJet400_v*','HLT_HT200_v*','HLT_HT250_v*',
                               #   'HLT_HT300_v*','HLT_HT400_v*','HLT_HT450_v*',
                               #   'HLT_HT500_v*','HLT_HT550_v*','HLT_HT650_v*',
                               #   'HLT_HT750_v*','HLT_FatDiPFJetMass750_DR1p1_Deta1p5_v*','HLT_PFHT750_v*'
    ),
    triggerResults  = cms.InputTag("TriggerResults","","HLT"),
    triggerEvent    = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    ## jec services ##############################
    pfjecService    = cms.string('ak7PFL1FastL2L3Residual'),
    calojecService  = cms.string('ak7CaloL1L2L3Residual')
#    Xsec = cms.double(0.0)
)

process.ak5 = process.ak7.clone(
    pfjets           = 'ak5PFJets',
    calojets         = 'ak5CaloJets',
    PFPayloadName    = 'AK5PF',
    CaloPayloadName  = 'AK5Calo',
    jecUncSrc        = 'Summer12_V2_DATA_AK5PF_UncertaintySources.txt',
    calojetID        = 'ak5JetID',
    calojetExtender  = 'ak5JetExtender',
    pfjecService     = 'ak5PFL1FastL2L3Residual',
    calojecService   = 'ak5CaloL1L2L3Residual',
    printTriggerMenu = False 
)

############# hlt filter #########################
process.hltFilter = cms.EDFilter('HLTHighLevel',
    TriggerResultsTag  = cms.InputTag('TriggerResults','','HLT'),
    HLTPaths           = cms.vstring(
 'HLT_PFJet40_v*','HLT_PFJet80_v*','HLT_PFJet140_v*','HLT_PFJet200_v*','HLT_PFJet260_v*','HLT_PFJet320_v*','HLT_PFJet400_v*','HLT_HT200_v*','HLT_HT250_v*','HLT_HT300_v*','HLT_HT350_v*','HLT_HT400_v*','HLT_HT450_v*','HLT_HT500_v*','HLT_HT550_v*','HLT_HT650_v*','HLT_HT750_v*','HLT_FatDiPFJetMass750_DR1p1_Deta1p5_v*','HLT_PFHT700_v*','HLT_PFHT750_v*','HLT_PFNoPUHT650_v*','HLT_PFNoPUHT700_v*','HLT_PFNoPUHT750_v*'
    ),
    eventSetupPathsKey = cms.string(''),
    andOr              = cms.bool(True), #----- True = OR, False = AND between the HLTPaths
    throw              = cms.bool(False)
)


process.path = cms.Path(process.hltFilter * process.HBHENoiseFilterResultProducer * process.ak5 * process.ak7)


