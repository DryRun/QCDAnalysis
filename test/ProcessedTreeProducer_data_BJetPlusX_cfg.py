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
	'FT_R_53_V18::All',
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
	#'/BJetPlusX/Run2012D-22Jan2013-v1/AOD'
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
		input_files_vstring = cms.untracked.vstring('/store/data/Run2012C/BJetPlusX/AOD/22Jan2013-v1/20000/0013B80A-088E-E211-BCA9-002590596468.root',
		#input_files_vstring.append('/store/data/Run2012C/BJetPlusX/AOD/22Jan2013-v1/20000/00628EC1-2B8E-E211-A57B-00261894383E.root')
		#input_files_vstring.append('/store/data/Run2012C/BJetPlusX/AOD/22Jan2013-v1/20000/00709065-3B8E-E211-A069-002590596486.root')
		#input_files_vstring.append('/store/data/Run2012C/BJetPlusX/AOD/22Jan2013-v1/20000/0097E4DA-868E-E211-8381-00304867918E.root')
		#input_files_vstring.append('/store/data/Run2012C/BJetPlusX/AOD/22Jan2013-v1/20000/00E60307-478E-E211-8F70-00261894390B.root')
		)
	else:
		print "Unknown dataset: " + options.dataset
		sys.exit(1)


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

if options.dataset == '/BJetPlusX/Run2012C-22Jan2013-v1/AOD':
	process.source = cms.Source("PoolSource",
		fileNames = input_files_vstring,
	)

#trigger_list_btag_dijet = cms.vstring(
	'HLT_DiJet40Eta2p6_BTagIP3DFastPV_v1', 'HLT_DiJet40Eta2p6_BTagIP3DFastPV_v2', 'HLT_DiJet40Eta2p6_BTagIP3DFastPV_v3', 'HLT_DiJet40Eta2p6_BTagIP3DFastPV_v4', 'HLT_DiJet40Eta2p6_BTagIP3DFastPV_v5', 'HLT_DiJet40Eta2p6_BTagIP3DFastPV_v6', 'HLT_DiJet40Eta2p6_BTagIP3DFastPV_v7', 'HLT_DiJet40Eta2p6_BTagIP3DFastPV_v8',
	'HLT_DiJet80Eta2p6_BTagIP3DFastPVLoose_v1', 'HLT_DiJet80Eta2p6_BTagIP3DFastPVLoose_v2', 'HLT_DiJet80Eta2p6_BTagIP3DFastPVLoose_v3', 'HLT_DiJet80Eta2p6_BTagIP3DFastPVLoose_v4', 'HLT_DiJet80Eta2p6_BTagIP3DFastPVLoose_v5', 'HLT_DiJet80Eta2p6_BTagIP3DFastPVLoose_v6', 'HLT_DiJet80Eta2p6_BTagIP3DFastPVLoose_v7', 'HLT_DiJet80Eta2p6_BTagIP3DFastPVLoose_v8',
	'HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose_v1', 'HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose_v2', 'HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose_v3', 'HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose_v4', 'HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose_v5', 'HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose_v6', 'HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose_v7', 'HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose_v8',
	'HLT_Jet60Eta1p7_Jet53Eta1p7_DiBTagIP3DFastPV_v1', 'HLT_Jet60Eta1p7_Jet53Eta1p7_DiBTagIP3DFastPV_v2', 'HLT_Jet60Eta1p7_Jet53Eta1p7_DiBTagIP3DFastPV_v3', 'HLT_Jet60Eta1p7_Jet53Eta1p7_DiBTagIP3DFastPV_v4', 'HLT_Jet60Eta1p7_Jet53Eta1p7_DiBTagIP3DFastPV_v5', 'HLT_Jet60Eta1p7_Jet53Eta1p7_DiBTagIP3DFastPV_v6', 'HLT_Jet60Eta1p7_Jet53Eta1p7_DiBTagIP3DFastPV_v7', 'HLT_Jet60Eta1p7_Jet53Eta1p7_DiBTagIP3DFastPV_v8',
	'HLT_Jet80Eta1p7_Jet70Eta1p7_DiBTagIP3DFastPV_v1', 'HLT_Jet80Eta1p7_Jet70Eta1p7_DiBTagIP3DFastPV_v2', 'HLT_Jet80Eta1p7_Jet70Eta1p7_DiBTagIP3DFastPV_v3', 'HLT_Jet80Eta1p7_Jet70Eta1p7_DiBTagIP3DFastPV_v4', 'HLT_Jet80Eta1p7_Jet70Eta1p7_DiBTagIP3DFastPV_v5', 'HLT_Jet80Eta1p7_Jet70Eta1p7_DiBTagIP3DFastPV_v6', 'HLT_Jet80Eta1p7_Jet70Eta1p7_DiBTagIP3DFastPV_v7', 'HLT_Jet80Eta1p7_Jet70Eta1p7_DiBTagIP3DFastPV_v8',
	
	)
#trigger_list_btag_quadjet = cms.vstring(
	'HLT_DiPFJet80_DiPFJet30_BTagCSVd07d05_v1', 'HLT_DiPFJet80_DiPFJet30_BTagCSVd07d05_v2', 'HLT_DiPFJet80_DiPFJet30_BTagCSVd07d05_v3', 'HLT_DiPFJet80_DiPFJet30_BTagCSVd07d05_v4', 'HLT_DiPFJet80_DiPFJet30_BTagCSVd07d05_v5',
	'HLT_DiPFJet80_DiPFJet30_BTagCSVd07d05d03_v1', 'HLT_DiPFJet80_DiPFJet30_BTagCSVd07d05d03_v2', 'HLT_DiPFJet80_DiPFJet30_BTagCSVd07d05d03_v3', 'HLT_DiPFJet80_DiPFJet30_BTagCSVd07d05d03_v4', 'HLT_DiPFJet80_DiPFJet30_BTagCSVd07d05d03_v5',
	'HLT_DiPFJet80_DiPFJet30_BTagCSVd07d05d05_v1', 'HLT_DiPFJet80_DiPFJet30_BTagCSVd07d05d05_v2', 'HLT_DiPFJet80_DiPFJet30_BTagCSVd07d05d05_v3', 'HLT_DiPFJet80_DiPFJet30_BTagCSVd07d05d05_v4', 'HLT_DiPFJet80_DiPFJet30_BTagCSVd07d05d05_v5',
	'HLT_QuadJet75_55_35_20_BTagIP_VBF_v1', 'HLT_QuadJet75_55_35_20_BTagIP_VBF_v2', 'HLT_QuadJet75_55_35_20_BTagIP_VBF_v3', 'HLT_QuadJet75_55_35_20_BTagIP_VBF_v4', 'HLT_QuadJet75_55_35_20_BTagIP_VBF_v5', 'HLT_QuadJet75_55_35_20_BTagIP_VBF_v6', 'HLT_QuadJet75_55_35_20_BTagIP_VBF_v7',
	'HLT_QuadJet75_55_38_20_BTagIP_VBF_v1', 'HLT_QuadJet75_55_38_20_BTagIP_VBF_v2', 'HLT_QuadJet75_55_38_20_BTagIP_VBF_v3', 'HLT_QuadJet75_55_38_20_BTagIP_VBF_v4', 'HLT_QuadJet75_55_38_20_BTagIP_VBF_v5', 'HLT_QuadJet75_55_38_20_BTagIP_VBF_v6', 'HLT_QuadJet75_55_38_20_BTagIP_VBF_v7',
	'HLT_QuadPFJet78_61_44_31_BTagCSV_VBF_v1', 'HLT_QuadPFJet78_61_44_31_BTagCSV_VBF_v2', 'HLT_QuadPFJet78_61_44_31_BTagCSV_VBF_v3', 'HLT_QuadPFJet78_61_44_31_BTagCSV_VBF_v4', 'HLT_QuadPFJet78_61_44_31_BTagCSV_VBF_v5', 'HLT_QuadPFJet78_61_44_31_BTagCSV_VBF_v6',
	'HLT_QuadPFJet82_65_48_35_BTagCSV_VBF_v1', 'HLT_QuadPFJet82_65_48_35_BTagCSV_VBF_v2', 'HLT_QuadPFJet82_65_48_35_BTagCSV_VBF_v3', 'HLT_QuadPFJet82_65_48_35_BTagCSV_VBF_v4', 'HLT_QuadPFJet82_65_48_35_BTagCSV_VBF_v5', 'HLT_QuadPFJet82_65_48_35_BTagCSV_VBF_v6',
	)
trigger_list_btag_dijet = cms.vstring(
	'HLT_DiJet40Eta2p6_BTagIP3DFastPV_v*',
	'HLT_DiJet80Eta2p6_BTagIP3DFastPVLoose_v*',
	'HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose_v*',
	'HLT_Jet60Eta1p7_Jet53Eta1p7_DiBTagIP3DFastPV_v*',
	'HLT_Jet80Eta1p7_Jet70Eta1p7_DiBTagIP3DFastPV_v*',
	
	)
trigger_list_btag_quadjet = cms.vstring(
	'HLT_DiPFJet80_DiPFJet30_BTagCSVd07d05_v*',
	'HLT_DiPFJet80_DiPFJet30_BTagCSVd07d05d03_v*',
	'HLT_DiPFJet80_DiPFJet30_BTagCSVd07d05d05_v*',
	'HLT_QuadJet75_55_35_20_BTagIP_VBF_v*',
	'HLT_QuadJet75_55_38_20_BTagIP_VBF_v*',
	'HLT_QuadPFJet78_61_44_31_BTagCSV_VBF_v*',
	'HLT_QuadPFJet82_65_48_35_BTagCSV_VBF_v*',
	)
trigger_list_btag_all = cms.vstring()
trigger_list_btag_all.extend(trigger_list_btag_dijet)
trigger_list_btag_all.extend(trigger_list_btag_quadjet)


# Not found triggers:
# HLT_DiJet80Eta2p6_BTagIP3DLoose : not in BJetX
# HLT_DiJet40Eta2p6_BTagIP3D_v5 : not in BJetX
# HLT_Jet60Eta1p7_Jet53Eta1p7_DiBTagIP3D : not in BJetX (HLT_Jet60Eta1p7_Jet53Eta1p7_DiBTagIP3DFastPV_v5 is, though)
# HLT_Jet80Eta1p7_Jet70Eta1p7_DiBTagIP3D : not in BJetX (HLT_Jet80Eta1p7_Jet70Eta1p7_DiBTagIP3DFastPV_v5 is, though)
# HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DLoose : only in MultiJet
#'HLT_DiPFJet80_DiPFJet30_BTagCSVd07d05d03_PFDiJetPt120', # Not in BJetX
#'HLT_QuadPFJet75_55_35_20_BTagCSV_VBF_v2',
#'HLT_QuadPFJet75_55_38_20_BTagCSV_VBF_v2'



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
		triggerName     = trigger_list_btag_all,
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
		HLTPaths           = trigger_list_btag_all,
		eventSetupPathsKey = cms.string(''),
		andOr              = cms.bool(True), #----- True = OR, False = AND between the HLTPaths
		throw              = cms.bool(False)
)


process.path = cms.Path(process.hltFilter * process.HBHENoiseFilterResultProducer * process.ak5 * process.ak7)


