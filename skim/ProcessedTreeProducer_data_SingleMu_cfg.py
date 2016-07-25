import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

#------------------------------------------------------------------------------------
# Options
#------------------------------------------------------------------------------------

options = VarParsing.VarParsing()

options.register('maxEvents',
	1000, #default value
	VarParsing.VarParsing.multiplicity.singleton,
	VarParsing.VarParsing.varType.int,
	"Number of events to process"
)

options.register('skipEvents',
	0,
	VarParsing.VarParsing.multiplicity.singleton,
	VarParsing.VarParsing.varType.int,
	"Number of events to skip"
)


options.register('outputFile',
	'file:QCDBEventTree.root',
	VarParsing.VarParsing.multiplicity.singleton,
	VarParsing.VarParsing.varType.string,
	"Output file"
)

options.register('globalTag',
	'FT_R_53_V18::All',
	VarParsing.VarParsing.multiplicity.singleton,
	VarParsing.VarParsing.varType.string,
	"Global Tag"
)

#options.register('inputFilesTxt', '', VarParsing.VarParsing.multiplicity.singleto, VarParsing.VarParsing.varType.string, 'Text file of inputs')
options.register('inputFiles', 
	'root://cmsxrootd-site.fnal.gov//store/data/Run2012C/SingleMu/AOD/22Jan2013-v1/20000/000A8B8E-2875-E211-BC1E-00259073E3D6.root', 
	VarParsing.VarParsing.multiplicity.singleton,
	VarParsing.VarParsing.varType.string,
	"List of input files"
)


options.register('eventsToSkip',
	'', #default value
	VarParsing.VarParsing.multiplicity.list,
	VarParsing.VarParsing.varType.string,
	"Skip specific events"
)

options.register('lumisToSkip',
	'',
	VarParsing.VarParsing.multiplicity.list,
	VarParsing.VarParsing.varType.string,
	"Skip specific lumisections"
)


options.parseArguments()

# Make list of input files
# If inputFiles exists, use it. Otherwise, go by dataset
input_files_vstring = cms.untracked.vstring("")
if options.inputFiles != '':
	input_files_vstring = cms.untracked.vstring(options.inputFiles)

# All 2012 triggers requiring 2 jets and a b tag.
trigger_list = cms.vstring(
	'HLT_Mu12_v16', 'HLT_Mu12_v17', 'HLT_Mu12_v18', 
	'HLT_Mu12_eta2p1_DiCentral_20_v2', 'HLT_Mu12_eta2p1_DiCentral_20_v3', 'HLT_Mu12_eta2p1_DiCentral_20_v5', 'HLT_Mu12_eta2p1_DiCentral_20_v7', 'HLT_Mu12_eta2p1_DiCentral_20_v8', 
	'HLT_Mu12_eta2p1_DiCentral_40_20_v2', 'HLT_Mu12_eta2p1_DiCentral_40_20_v3', 'HLT_Mu12_eta2p1_DiCentral_40_20_v5', 'HLT_Mu12_eta2p1_DiCentral_40_20_v7', 'HLT_Mu12_eta2p1_DiCentral_40_20_v8', 
	'HLT_Mu12_eta2p1_DiCentral_40_20_BTagIP3D1stTrack_v2', 'HLT_Mu12_eta2p1_DiCentral_40_20_BTagIP3D1stTrack_v3', 'HLT_Mu12_eta2p1_DiCentral_40_20_BTagIP3D1stTrack_v5', 'HLT_Mu12_eta2p1_DiCentral_40_20_BTagIP3D1stTrack_v7', 'HLT_Mu12_eta2p1_DiCentral_40_20_BTagIP3D1stTrack_v8', 
	'HLT_Mu12_eta2p1_DiCentral_40_20_DiBTagIP3D1stTrack_v2', 'HLT_Mu12_eta2p1_DiCentral_40_20_DiBTagIP3D1stTrack_v3', 'HLT_Mu12_eta2p1_DiCentral_40_20_DiBTagIP3D1stTrack_v5', 'HLT_Mu12_eta2p1_DiCentral_40_20_DiBTagIP3D1stTrack_v7', 'HLT_Mu12_eta2p1_DiCentral_40_20_DiBTagIP3D1stTrack_v8', 
	'HLT_Mu12_eta2p1_L1Mu10erJetC12WdEtaPhi1DiJetsC_v3', 'HLT_Mu12_eta2p1_L1Mu10erJetC12WdEtaPhi1DiJetsC_v5', 'HLT_Mu12_eta2p1_L1Mu10erJetC12WdEtaPhi1DiJetsC_v6', 'HLT_Mu12_eta2p1_L1Mu10erJetC12WdEtaPhi1DiJetsC_v7', 
	'HLT_Mu15_eta2p1_v3', 'HLT_Mu15_eta2p1_v4', 'HLT_Mu15_eta2p1_v5', 
	'HLT_Mu15_eta2p1_DiCentral_20_v1', 
	'HLT_Mu15_eta2p1_DiCentral_40_20_v1', 
	'HLT_Mu15_eta2p1_L1Mu10erJetC12WdEtaPhi1DiJetsC_v1', 'HLT_Mu15_eta2p1_L1Mu10erJetC12WdEtaPhi1DiJetsC_v2', 'HLT_Mu15_eta2p1_L1Mu10erJetC12WdEtaPhi1DiJetsC_v3', 
	'HLT_Mu15_eta2p1_TriCentral_40_20_20_v2', 'HLT_Mu15_eta2p1_TriCentral_40_20_20_v3', 'HLT_Mu15_eta2p1_TriCentral_40_20_20_v5', 'HLT_Mu15_eta2p1_TriCentral_40_20_20_v7', 'HLT_Mu15_eta2p1_TriCentral_40_20_20_v8', 
	'HLT_Mu15_eta2p1_TriCentral_40_20_20_BTagIP3D1stTrack_v2', 'HLT_Mu15_eta2p1_TriCentral_40_20_20_BTagIP3D1stTrack_v3', 'HLT_Mu15_eta2p1_TriCentral_40_20_20_BTagIP3D1stTrack_v5', 'HLT_Mu15_eta2p1_TriCentral_40_20_20_BTagIP3D1stTrack_v7', 'HLT_Mu15_eta2p1_TriCentral_40_20_20_BTagIP3D1stTrack_v8', 
	'HLT_Mu15_eta2p1_TriCentral_40_20_20_DiBTagIP3D1stTrack_v2', 'HLT_Mu15_eta2p1_TriCentral_40_20_20_DiBTagIP3D1stTrack_v3', 'HLT_Mu15_eta2p1_TriCentral_40_20_20_DiBTagIP3D1stTrack_v5', 'HLT_Mu15_eta2p1_TriCentral_40_20_20_DiBTagIP3D1stTrack_v7', 'HLT_Mu15_eta2p1_TriCentral_40_20_20_DiBTagIP3D1stTrack_v8', 
	'HLT_Mu17_eta2p1_TriCentralPFNoPUJet30_v1', 
	'HLT_Mu17_eta2p1_TriCentralPFNoPUJet30_30_20_v1', 'HLT_Mu17_eta2p1_TriCentralPFNoPUJet30_30_20_v2', 
	'HLT_Mu17_eta2p1_TriCentralPFNoPUJet45_35_25_v1', 'HLT_Mu17_eta2p1_TriCentralPFNoPUJet45_35_25_v2', 
	'HLT_Mu17_eta2p1_TriCentralPFNoPUJet50_40_30_v1', 
	'HLT_Mu18_CentralPFJet30_CentralPFJet25_v1', 
	'HLT_Mu18_PFJet30_PFJet25_Deta3_CentralPFJet25_v1', 
	'HLT_Mu24_v14', 'HLT_Mu24_v15', 'HLT_Mu24_v16', 
	'HLT_Mu24_CentralPFJet30_CentralPFJet25_v1', 'HLT_Mu24_CentralPFJet30_CentralPFJet25_v2', 'HLT_Mu24_CentralPFJet30_CentralPFJet25_v3', 'HLT_Mu24_CentralPFJet30_CentralPFJet25_v4', 
	'HLT_Mu24_PFJet30_PFJet25_Deta3_CentralPFJet25_v1', 'HLT_Mu24_PFJet30_PFJet25_Deta3_CentralPFJet25_v2', 'HLT_Mu24_PFJet30_PFJet25_Deta3_CentralPFJet25_v3', 'HLT_Mu24_PFJet30_PFJet25_Deta3_CentralPFJet25_v4', 
	'HLT_Mu24_eta2p1_v3', 'HLT_Mu24_eta2p1_v4', 'HLT_Mu24_eta2p1_v5', 
	'HLT_Mu30_v14', 'HLT_Mu30_v15', 'HLT_Mu30_v16', 
	'HLT_Mu30_eta2p1_v3', 'HLT_Mu30_eta2p1_v4', 'HLT_Mu30_eta2p1_v5', 
	'HLT_Mu40_v12', 'HLT_Mu40_v13', 'HLT_Mu40_v14', 
	'HLT_Mu40_eta2p1_v9', 'HLT_Mu40_eta2p1_v10', 'HLT_Mu40_eta2p1_v11', 
	'HLT_Mu40_eta2p1_Track50_dEdx3p6_v3', 'HLT_Mu40_eta2p1_Track50_dEdx3p6_v4', 'HLT_Mu40_eta2p1_Track50_dEdx3p6_v5', 
	'HLT_Mu40_eta2p1_Track60_dEdx3p7_v3', 'HLT_Mu40_eta2p1_Track60_dEdx3p7_v4', 'HLT_Mu40_eta2p1_Track60_dEdx3p7_v5', 
	'HLT_Mu5_v18', 'HLT_Mu5_v19', 'HLT_Mu5_v20', 
	'HLT_Mu50_eta2p1_v6', 'HLT_Mu50_eta2p1_v7', 'HLT_Mu50_eta2p1_v8', 
)

process = cms.Process("Ana")
process.load('FWCore.MessageService.MessageLogger_cfi')
##-------------------- Communicate with the DB -----------------------
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
# process.GlobalTag.globaltag = 'GR_R_52_V9::All' # I think I'm going to use the one for 2013 reprocessing, as seen in DAS
#process.GlobalTag.globaltag = 'FT_R_53_V18::All'
process.GlobalTag.globaltag = options.globalTag
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
		input = cms.untracked.int32(options.maxEvents)
)

#############   Format MessageLogger #################
process.MessageLogger.cerr.FwkReport.reportEvery = 100
#############   Define the source file ###############

process.source = cms.Source("PoolSource",
	fileNames = input_files_vstring,
)
if options.eventsToSkip != '':
	process.source.eventsToSkip = cms.untracked.VEventRange(options.eventsToSkip)
if options.lumisToSkip != '':
	process.source.lumisToSkip = cms.untracked.VLuminosityBlockRange(options.lumisToSkip)
if options.skipEvents != 0:
    process.source.skipEvents = cms.untracked.uint32(options.skipEvents)



############# processed tree producer ##################
process.TFileService = cms.Service("TFileService",fileName = cms.string(options.outputFile))

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
		triggerName     = trigger_list,
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
		HLTPaths           = trigger_list,
		eventSetupPathsKey = cms.string(''),
		andOr              = cms.bool(True), #----- True = OR, False = AND between the HLTPaths
		throw              = cms.bool(False)
)


process.path = cms.Path(process.hltFilter * process.HBHENoiseFilterResultProducer * process.ak5 * process.ak7)


