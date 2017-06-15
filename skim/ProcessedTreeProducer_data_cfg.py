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

options.register('outputFile',
	'file:QCDBEventTree.root',
	VarParsing.VarParsing.multiplicity.singleton,
	VarParsing.VarParsing.varType.string,
	"Output file"
)

options.register('globalTag',
	#'FT_R_53_V18::All',
	'FT_53_V21_AN5:All',
	VarParsing.VarParsing.multiplicity.singleton,
	VarParsing.VarParsing.varType.string,
	"Global Tag"
)

# Dataset. 2012 options are:
# /JetHT/Run2012C-22Jan2013-v1/AOD
# /JetHT/Run2012C-PromptReco-v2/AOD
options.register('dataset',
	#'/JetHT/Run2012C-22Jan2013-v1/AOD', 
	#'/MultiJet/Run2012A-22Jan2013-v1/AOD',
	#'/BJetPlusX/Run2012B-22Jan2013-v1/AOD',
	'/BJetPlusX/Run2012C-22Jan2013-v1/AOD',
	#'/BJetPlusX/Run2012D-22Jan2013-v1/AOD',
	VarParsing.VarParsing.multiplicity.singleton,
	VarParsing.VarParsing.varType.string,
	"Run over a few files from specific (known) datasets"
)

#options.register('inputFilesTxt', '', VarParsing.VarParsing.multiplicity.singleto, VarParsing.VarParsing.varType.string, 'Text file of inputs')
options.register('inputFiles', 
	'', 
	VarParsing.VarParsing.multiplicity.singleton,
	VarParsing.VarParsing.varType.string,
	"List of input files"
)

options.parseArguments()

# Make list of input files
# If inputFiles exists, use it. Otherwise, go by dataset
input_files_vstring = cms.untracked.vstring("")
if options.inputFiles != '':
	input_files_vstring = cms.untracked.vstring(options.inputFiles)
else:
	if options.dataset == '/BJetPlusX/Run2012C-22Jan2013-v1/AOD':
		input_files_vstring = cms.untracked.vstring(
			'/store/data/Run2012C/BJetPlusX/AOD/22Jan2013-v1/20000/0013B80A-088E-E211-BCA9-002590596468.root',
			#input_files_vstring.append('/store/data/Run2012C/BJetPlusX/AOD/22Jan2013-v1/20000/00628EC1-2B8E-E211-A57B-00261894383E.root')
			#input_files_vstring.append('/store/data/Run2012C/BJetPlusX/AOD/22Jan2013-v1/20000/00709065-3B8E-E211-A069-002590596486.root')
			#input_files_vstring.append('/store/data/Run2012C/BJetPlusX/AOD/22Jan2013-v1/20000/0097E4DA-868E-E211-8381-00304867918E.root')
			#input_files_vstring.append('/store/data/Run2012C/BJetPlusX/AOD/22Jan2013-v1/20000/00E60307-478E-E211-8F70-00261894390B.root')
		)
	elif options.dataset == '/BJetPlusX/Run2012D-22Jan2013-v1/AOD':
		input_files_vstring = cms.untracked.vstring(
			'/store/data/Run2012C/BJetPlusX/AOD/22Jan2013-v1/20000/0013B80A-088E-E211-BCA9-002590596468.root',
		)
	else:
		print "Unknown dataset: " + options.dataset
		sys.exit(1)

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



############# processed tree producer ##################
process.TFileService = cms.Service("TFileService",fileName = cms.string(options.outputFile))

process.ak7 = cms.EDAnalyzer('ProcessedTreeProducer',
		## jet collections ###########################
		pfjets          = cms.InputTag('ak7PFJets'),
		calojets        = cms.InputTag('ak7CaloJets'),
		## database entry for the uncertainties ######
		PFPayloadName   = cms.string('AK7PF'),
		CaloPayloadName = cms.string('AK7Calo'),
		jecUncSrc       = cms.string('Summer13_V5_DATA_UncertaintySources_AK7PF.txt'),
		jecUncSrcNames  = cms.vstring('Absolute','HighPtExtra','SinglePionECAL', 'SinglePionHCAL','FlavorQCD','Time',
																	'RelativeJEREC1','RelativeJEREC2','RelativeJERHF',
																	'RelativePtBB', 'RelativePtEC1', 'RelativePtEC2', 'RelativePtHF',
																	'RelativeStatEC2','RelativeStatHF','RelativeFSR',
																	'PileUpDataMC',
																	#'PileUpOOT','PileUpPt','PileUpBias','PileUpJetRate',
																	'PileUpBB', 'PileUpEC', 'PileUpHF',
																	'SubTotalPileUp','SubTotalRelative','SubTotalPt','SubTotalMC','TotalNoFlavor','Total'),
		
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
		jecUncSrc        = 'Summer13_V5_DATA_UncertaintySources_AK5PF.txt',
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


