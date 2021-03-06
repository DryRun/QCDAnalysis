import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

#------------------------------------------------------------------------------------
# Options
#------------------------------------------------------------------------------------

options = VarParsing.VarParsing()

options.register('maxEvents',
    -1, #default value
    VarParsing.VarParsing.multiplicity.singleton,
    VarParsing.VarParsing.varType.int,
    "Number of events to process"
)

options.register('outputFile',
    'file:QCDBEventTree.root',
    VarParsing.VarParsing.multiplicity.singleton,
    VarParsing.VarParsing.varType.string,
    "Output file"
)

options.register('globalTag',
    #'START53_V7G::All',
    'START53_V27::All',
    VarParsing.VarParsing.multiplicity.singleton,
    VarParsing.VarParsing.varType.string,
    "Global Tag"
)

# Dataset.
options.register('inputFiles',
    '/QCD_Pt-600to800_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM', 
    VarParsing.VarParsing.multiplicity.list,
    VarParsing.VarParsing.varType.string,
    "Global Tag"
)

options.register('FilterBB',
    False,
    VarParsing.VarParsing.multiplicity.singleton,
    VarParsing.VarParsing.varType.bool,
    "Filter on BB events (Z' only)",
    )

options.parseArguments()

# All 2012 triggers requiring 2 jets and a b tag.
trigger_list = cms.vstring(
    'HLT_HT200_v1', 'HLT_HT200_v2', 'HLT_HT200_v3', 'HLT_HT200_v4', 'HLT_HT200_v6', 'HLT_HT250_v1', 'HLT_HT250_v2', 'HLT_HT250_v3', 'HLT_HT250_v4', 'HLT_HT250_v5', 'HLT_HT250_v7', 'HLT_HT300_v1', 'HLT_HT300_v2', 'HLT_HT300_v3', 'HLT_HT300_v4', 'HLT_HT300_v5', 'HLT_HT300_v7', 'HLT_HT350_v1', 'HLT_HT350_v2', 'HLT_HT350_v3', 'HLT_HT350_v4', 'HLT_HT350_v5', 'HLT_HT350_v7', 'HLT_HT400_v1', 'HLT_HT400_v2', 'HLT_HT400_v3', 'HLT_HT400_v4', 'HLT_HT400_v5', 'HLT_HT400_v7', 'HLT_HT450_v1', 'HLT_HT450_v2', 'HLT_HT450_v3', 'HLT_HT450_v4', 'HLT_HT450_v5', 'HLT_HT450_v7', 'HLT_HT500_v1', 'HLT_HT500_v2', 'HLT_HT500_v3', 'HLT_HT500_v4', 'HLT_HT500_v5', 'HLT_HT500_v7', 'HLT_HT550_v1', 'HLT_HT550_v2', 'HLT_HT550_v3', 'HLT_HT550_v4', 'HLT_HT550_v5', 'HLT_HT550_v7', 'HLT_HT650_v1', 'HLT_HT650_v2', 'HLT_HT650_v3', 'HLT_HT650_v4', 'HLT_HT650_v5', 'HLT_HT650_v7', 'HLT_HT750_v1', 'HLT_HT750_v2', 'HLT_HT750_v3', 'HLT_HT750_v4', 'HLT_HT750_v5', 'HLT_HT750_v7', 'HLT_PFHT350_v3', 'HLT_PFHT350_v4', 'HLT_PFHT350_v5', 'HLT_PFHT350_v6', 'HLT_PFHT350_v7', 'HLT_PFHT650_v5', 'HLT_PFHT650_v6', 'HLT_PFHT650_v7', 'HLT_PFHT650_v8', 'HLT_PFHT650_v9', 'HLT_PFHT650_DiCentralPFJet80_CenPFJet40_v3', 'HLT_PFHT650_DiCentralPFJet80_CenPFJet40_v4', 'HLT_PFHT650_DiCentralPFJet80_CenPFJet40_v5', 'HLT_PFHT650_DiCentralPFJet80_CenPFJet40_v6', 'HLT_PFHT650_DiCentralPFJet80_CenPFJet40_v7', 'HLT_PFHT700_v3', 'HLT_PFHT700_v4', 'HLT_PFHT700_v5', 'HLT_PFHT700_v6', 'HLT_PFHT700_v7', 'HLT_PFHT750_v3', 'HLT_PFHT750_v4', 'HLT_PFHT750_v5', 'HLT_PFHT750_v6', 'HLT_PFHT750_v7', 'HLT_PFJet320_v3', 'HLT_PFJet320_v4', 'HLT_PFJet320_v5', 'HLT_PFJet320_v6', 'HLT_PFJet320_v8', 'HLT_PFJet320_v9', 'HLT_PFJet40_v3', 'HLT_PFJet40_v4', 'HLT_PFJet40_v5', 'HLT_PFJet40_v6', 'HLT_PFJet40_v7', 'HLT_PFJet40_v8', 'HLT_PFJet400_v3', 'HLT_PFJet400_v4', 'HLT_PFJet400_v5', 'HLT_PFJet400_v6', 'HLT_PFJet400_v8', 'HLT_PFJet400_v9', 'HLT_PFJet80_v3', 'HLT_PFJet80_v4', 'HLT_PFJet80_v5', 'HLT_PFJet80_v6', 'HLT_PFJet80_v8', 'HLT_PFJet80_v9', 'HLT_PFNoPUHT350_v1', 'HLT_PFNoPUHT350_v3', 'HLT_PFNoPUHT350_v4', 'HLT_PFNoPUHT650_v1', 'HLT_PFNoPUHT650_v3', 'HLT_PFNoPUHT650_v4', 'HLT_PFNoPUHT650_DiCentralPFNoPUJet80_CenPFNoPUJet40_v1', 'HLT_PFNoPUHT650_DiCentralPFNoPUJet80_CenPFNoPUJet40_v3', 'HLT_PFNoPUHT650_DiCentralPFNoPUJet80_CenPFNoPUJet40_v4', 'HLT_PFNoPUHT700_v1', 'HLT_PFNoPUHT700_v3', 'HLT_PFNoPUHT700_v4', 'HLT_PFNoPUHT750_v1', 'HLT_PFNoPUHT750_v3', 'HLT_PFNoPUHT750_v4',
    'HLT_DiJet40Eta2p6_BTagIP3D_v2', 'HLT_DiJet40Eta2p6_BTagIP3D_v3', 
    'HLT_DiJet40Eta2p6_BTagIP3DFastPV_v2', 'HLT_DiJet40Eta2p6_BTagIP3DFastPV_v3', 'HLT_DiJet40Eta2p6_BTagIP3DFastPV_v4', 'HLT_DiJet40Eta2p6_BTagIP3DFastPV_v5', 'HLT_DiJet40Eta2p6_BTagIP3DFastPV_v7', 
    'HLT_DiJet80Eta2p6_BTagIP3DFastPVLoose_v2', 'HLT_DiJet80Eta2p6_BTagIP3DFastPVLoose_v3', 'HLT_DiJet80Eta2p6_BTagIP3DFastPVLoose_v4', 'HLT_DiJet80Eta2p6_BTagIP3DFastPVLoose_v5', 'HLT_DiJet80Eta2p6_BTagIP3DFastPVLoose_v7', 
    'HLT_DiJet80Eta2p6_BTagIP3DLoose_v2', 'HLT_DiJet80Eta2p6_BTagIP3DLoose_v3', 
    'HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose_v2', 'HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose_v3', 'HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose_v4', 'HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose_v5', 'HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose_v7', 
    'HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DLoose_v2', 'HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DLoose_v3', 
    'HLT_Jet60Eta1p7_Jet53Eta1p7_DiBTagIP3D_v2', 'HLT_Jet60Eta1p7_Jet53Eta1p7_DiBTagIP3D_v3', 
    'HLT_Jet60Eta1p7_Jet53Eta1p7_DiBTagIP3DFastPV_v2', 'HLT_Jet60Eta1p7_Jet53Eta1p7_DiBTagIP3DFastPV_v3', 'HLT_Jet60Eta1p7_Jet53Eta1p7_DiBTagIP3DFastPV_v4', 'HLT_Jet60Eta1p7_Jet53Eta1p7_DiBTagIP3DFastPV_v5', 'HLT_Jet60Eta1p7_Jet53Eta1p7_DiBTagIP3DFastPV_v7', 
    'HLT_Jet80Eta1p7_Jet70Eta1p7_DiBTagIP3D_v2', 'HLT_Jet80Eta1p7_Jet70Eta1p7_DiBTagIP3D_v3', 
    'HLT_Jet80Eta1p7_Jet70Eta1p7_DiBTagIP3DFastPV_v2', 'HLT_Jet80Eta1p7_Jet70Eta1p7_DiBTagIP3DFastPV_v3', 'HLT_Jet80Eta1p7_Jet70Eta1p7_DiBTagIP3DFastPV_v4', 'HLT_Jet80Eta1p7_Jet70Eta1p7_DiBTagIP3DFastPV_v5', 'HLT_Jet80Eta1p7_Jet70Eta1p7_DiBTagIP3DFastPV_v7',
    'HLT_L1DoubleJet36Central_v6', 'HLT_L1DoubleJet36Central_v7'
)

process = cms.Process("Ana")
process.load('FWCore.MessageService.MessageLogger_cfi')
##-------------------- Communicate with the DB -----------------------
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = options.globalTag
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load('RecoJets.Configuration.RecoPFJets_cff')
process.load('RecoJets.Configuration.RecoJets_cff')
##-------------------- Import the JEC services -----------------------
process.load('JetMETCorrections.Configuration.DefaultJEC_cff')
##---- Jet-Flavor Matching ------------------------------------------
process.load("PhysicsTools.JetMCAlgos.CaloJetsMCFlavour_cfi") 
#############   Set the number of events #############
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)
#############   Format MessageLogger #################
process.MessageLogger.cerr.FwkReport.reportEvery = 100
#############   Define the source file ###############

input_file_vstring = cms.untracked.vstring(options.inputFiles)

#if "file:" in options.inputFiles or "/store" in options.inputFiles:
#elif options.inputFiles == "/QCD_Pt-600to800_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM":
#    input_file_vstring = cms.untracked.vstring('/store/mc/Summer12_DR53X/QCD_Pt-600to800_TuneZ2star_8TeV_pythia6/AODSIM/PU_S10_START53_V7A-v2/00000/00BA1E5C-2008-E211-9F96-002618943951.root')
#elif options.inputFiles == "/RSGravitonToBBbar_M-700_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM":
#    input_file_vstring = cms.untracked.vstring('/store/mc/Summer12_DR53X/RSGravitonToBBbar_M-700_TuneZ2star_8TeV-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/86359ACA-8110-E211-B7C5-BCAEC50971E3.root')
#else:
#    print "Unknown input dataset"
#    sys.exit(1)

process.source = cms.Source("PoolSource",
    fileNames = input_file_vstring
)
#'/store/mc/Summer12_DR53X/RSGravitonToBBbar_M-700_TuneZ2star_8TeV-pythia6/AODSIM/PU_S10_START53_V7A-v1/00000/16766FED-2C10-E211-8E0E-00259073E438.root',
##'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_0.root',  
##'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_1000GeV_21.root',  
##'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_33.root',  
##'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_10.root',  
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_22.root',  
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_34.root',  
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_46.root', 
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_11.root',  
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_23.root',  
##'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_35.root', 
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_12.root',  
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_36.root',  
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_13.root',  
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_25.root',  
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_24.root',
##'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_1000GeV_37.root', 
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_47.root', 
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_48.root',
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_49.root', 
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_14.root',  
##'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_1000GeV_26.root',  
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_38.root',  
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_4.root', 
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_15.root',  
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_27.root',  
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_39.root',  
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_5.root', 
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_16.root',  
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_28.root',  
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_3.root',   
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_6.root', 
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_17.root', 
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_29.root',  
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_40.root',  
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_7.root', 
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_18.root',  
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_2.root',   
##'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_1000GeV_41.root',  
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_8.root', 
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_19.root',  
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_30.root',  
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_42.root',  
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_9.root', 
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_1.root',   
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_31.root', 
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_43.root',  
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_20.root',  
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_32.root',  
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_44.root',  
#'file:/uscmst1b_scratch/lpc1/3DayLifetime/sertac/BStarToJJ_PYTHIA8_Tune4C_2000GeV_45.root',

############# processed tree producer ##################
#process.TFileService = cms.Service("TFileService",fileName = cms.string('/uscmst1b_scratch/lpc1/3DayLifetime/sertac/ProcessedTree_BStarToJJ_2000GeV_newJEC.root'))
process.TFileService = cms.Service("TFileService",fileName = cms.string(options.outputFile))

process.ak7 = cms.EDAnalyzer('ProcessedTreeProducer',
    ## jet collections ###########################
    pfjets          = cms.InputTag('ak7PFJets'),
    calojets        = cms.InputTag('ak7CaloJets'),
    genjets         = cms.untracked.InputTag('ak7GenJets'),
    ## database entry for the uncertainties ######
    PFPayloadName   = cms.string(''),
    CaloPayloadName = cms.string(''),
    jecUncSrc = cms.string(''),
    jecUncSrcNames = cms.vstring(''),
    #jecUncSrc       = cms.string('Summer13_V5_MC_Uncertainty_AK7PF'),
    #jecUncSrcNames  = cms.vstring('Absolute','HighPtExtra','SinglePionECAL', 'SinglePionHCAL','FlavorQCD','Time',
    #                                'RelativeJEREC1','RelativeJEREC2','RelativeJERHF',
    #                                'RelativePtBB', 'RelativePtEC1', 'RelativePtEC2', 'RelativePtHF',
    #                                'RelativeStatEC2','RelativeStatHF','RelativeFSR',
    #                                'PileUpDataMC',
    #                                #'PileUpOOT','PileUpPt','PileUpBias','PileUpJetRate',
    #                                'PileUpBB', 'PileUpEC', 'PileUpHF',
    #                                'SubTotalPileUp','SubTotalRelative','SubTotalPt','SubTotalMC','TotalNoFlavor','Total'),
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
    ## MC $ Generator flags ######################
    isMCarlo        = cms.untracked.bool(True),
    useGenInfo      = cms.untracked.bool(True),
    FilterBB        = cms.untracked.bool(options.FilterBB),
    ## simulated PU ##############################
    srcPU           = cms.untracked.InputTag('addPileupInfo'),
    ## preselection cuts #########################
    maxY            = cms.double(5.0), 
    minPFPt         = cms.double(20),
    minPFFatPt      = cms.double(10),
    maxPFFatEta     = cms.double(2.5),
    minCaloPt       = cms.double(20),
    minGenPt        = cms.untracked.double(20),
    minNPFJets      = cms.int32(1),
    minNCaloJets    = cms.int32(1), 
    minJJMass       = cms.double(-1),
    ## trigger ###################################
    printTriggerMenu = cms.untracked.bool(True),
    processName     = cms.string('HLT'),
    triggerName     = trigger_list,
    triggerResults  = cms.InputTag("TriggerResults","","HLT"),
    triggerEvent    = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    ## jec services ##############################
    pfjecService    = cms.string('ak7PFL1FastL2L3'),
    calojecService  = cms.string('ak7CaloL1FastL2L3'),
    ## Jet-Flavor Matching #######################
    jetFlavourMatching     = cms.untracked.string('AK7byValAlgo'),
    ## Cross section ############################
    Xsec            = cms.untracked.double(1)
)

process.ak5 = process.ak7.clone(
    pfjets           = 'ak5PFJets',
    calojets         = 'ak5CaloJets',
    genjets          = 'ak5GenJets',
    calojetID        = 'ak5JetID',
    calojetExtender  = 'ak5JetExtender',
    pfjecService     = 'ak5PFL1FastL2L3',
    calojecService   = 'ak5CaloL1FastL2L3',
    jetFlavourMatching = 'AK5byValAlgo',
    printTriggerMenu = False ,
    #jecUncSrc       = cms.string('Summer13_V5_MC_Uncertainty_AK5PF'),    
)

#process.path = cms.Path(process.ak7 * process.ak5)
##
process.AK7PFbyRef = process.AK7byRef.clone(jets = cms.InputTag("ak7PFJets"))
process.AK7PFbyValPhys = process.AK7byValPhys.clone(srcByReference = cms.InputTag("AK7PFbyRef"))
process.AK7PFbyValAlgo = process.AK7byValAlgo.clone(srcByReference = cms.InputTag("AK7PFbyRef"))
process.AK7PFFlavour = cms.Sequence(process.AK7PFbyRef*process.AK7PFbyValPhys*process.AK7PFbyValAlgo)

process.AK5PFbyRef = process.AK5byRef.clone(jets = cms.InputTag("ak5PFJets"))
process.AK5PFbyValPhys = process.AK5byValPhys.clone(srcByReference = cms.InputTag("AK5PFbyRef"))
process.AK5PFbyValAlgo = process.AK5byValAlgo.clone(srcByReference = cms.InputTag("AK5PFbyRef"))
process.AK5PFFlavour = cms.Sequence(process.AK5PFbyRef*process.AK5PFbyValPhys*process.AK5PFbyValAlgo)

process.path = cms.Path(process.myPartons * (process.AK7Flavour + process.AK7PFFlavour) * (process.AK5Flavour + process.AK5PFFlavour) * process.ak7 * process.ak5)

