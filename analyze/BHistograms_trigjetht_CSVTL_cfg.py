import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing
import sys

options = VarParsing.VarParsing()
options.register('inputFiles', 
	'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012B_v1_3/160429_121519/0000/QCDBEventTree_567.root',
	VarParsing.VarParsing.multiplicity.list,
	VarParsing.VarParsing.varType.string,
	"List of input files"
)
options.register('outputFile', 
	'BHistograms_trigjetht_CSVL.root', 
	VarParsing.VarParsing.multiplicity.singleton,
	VarParsing.VarParsing.varType.string,
	"Output file"
)
options.register('dataSource',
	'collision_data',
	VarParsing.VarParsing.multiplicity.singleton,
	VarParsing.VarParsing.varType.string,
	'collision_data or simulation'
	)
options.register('dataType',
	'data',
	VarParsing.VarParsing.multiplicity.singleton,
	VarParsing.VarParsing.varType.string,
	'data, signal, or background'
	)
options.register('signalMass',
	750.,
	VarParsing.VarParsing.multiplicity.singleton,
	VarParsing.VarParsing.varType.float,
	'Signal mass hypothesis (only necessary for running over signal)'
	)
options.parseArguments()

if options.dataSource != "collision_data" and options.dataSource != "simulation":
	print "[BHistograms_BJetPlusX_loose] ERROR : dataSource must be collision_data or simulation"
	sys.exit(1)

if not options.dataType in ["data", "signal", "background"]:
	print "[BHistograms_BJetPlusX_loose] ERROR : dataType must be data, signal, or background"
	sys.exit(1)

process = cms.Process("myprocess")
process.TFileService=cms.Service("TFileService",fileName=cms.string(options.outputFile))

##-------------------- Define the source  ----------------------------
process.maxEvents = cms.untracked.PSet(
		input = cms.untracked.int32(1)
		)
process.source = cms.Source("EmptySource")

##-------------------- Cuts ------------------------------------------
# Cuts on the leading two jets
dijet_cuts = cms.VPSet(
	cms.PSet(
		name        = cms.string("MinPt"),
		parameters  = cms.vdouble(30.),
		descriptors = cms.vstring()
	),
	cms.PSet(
		name        = cms.string("MaxAbsEta"),
		parameters  = cms.vdouble(2.2),
		descriptors = cms.vstring()
	),
	cms.PSet(
		name        = cms.string("IsTightID"),
		parameters  = cms.vdouble(),
		descriptors = cms.vstring()
	),
	cms.PSet(
		name        = cms.string("MaxMuonEnergyFraction"),
		parameters  = cms.vdouble(0.8),
		descriptors = cms.vstring()
	),
)

# Cuts on all PF jets (defines the generic jet collection for e.g. making fat jets)
pfjet_cuts = cms.VPSet(
	cms.PSet(
		name        = cms.string("MinPt"),
		parameters  = cms.vdouble(30.),
		descriptors = cms.vstring()
	),
	cms.PSet(
		name        = cms.string("MaxAbsEta"),
		parameters  = cms.vdouble(5),
		descriptors = cms.vstring()
	),
	cms.PSet(
		name        = cms.string("IsLooseID"),
		parameters  = cms.vdouble(),
		descriptors = cms.vstring()
	),
)

# Cuts on calo jets
calojet_cuts = cms.VPSet(
	cms.PSet(
		name        = cms.string("MinPt"),
		parameters  = cms.vdouble(30.),
		descriptors = cms.vstring()
	)
)

# Event cuts
event_cuts = cms.VPSet(
	cms.PSet(
		name        = cms.string("TriggerOR"),
		parameters  = cms.vdouble(),
		descriptors = cms.vstring("HLT_PFHT650_v5", "HLT_PFHT650_v6", "HLT_PFHT650_v7", "HLT_PFHT650_v8", "HLT_PFHT650_v9", "HLT_PFNoPUHT650_v1", "HLT_PFNoPUHT650_v3", "HLT_PFNoPUHT650_v4", "HLT_HT750_v1", "HLT_HT750_v2", "HLT_HT750_v3", "HLT_HT750_v4", "HLT_HT750_v5", "HLT_HT750_v7")
	),
	cms.PSet(
		name        = cms.string("MaxMetOverSumEt"),
		parameters  = cms.vdouble(0.5),
		descriptors = cms.vstring()
	),
	cms.PSet(
		name        = cms.string("GoodPFDijet"),
		parameters  = cms.vdouble(),
		descriptors = cms.vstring()
	),
	cms.PSet(
		name        = cms.string("MinNCSVL"),
		parameters  = cms.vdouble(2),
		descriptors = cms.vstring()
	),
	cms.PSet(
		name        = cms.string("MinNCSVT"),
		parameters  = cms.vdouble(1),
		descriptors = cms.vstring()
	),
	cms.PSet(
		name        = cms.string("MinLeadingPFJetPt"),
		parameters  = cms.vdouble(160.),
		descriptors = cms.vstring()
	),
	cms.PSet(
		name        = cms.string("MinSubleadingPFJetPt"),
		parameters  = cms.vdouble(120.),
		descriptors = cms.vstring()
	),
	cms.PSet(
		name        = cms.string("PFDijetMaxDeltaEta"),
		parameters  = cms.vdouble(1.3),
		descriptors = cms.vstring()
	)
)

##-------------------- User analyzer  --------------------------------
process.BHistograms    = cms.EDAnalyzer('BHistograms',
	file_names             = cms.vstring(options.inputFiles),
	tree_name              = cms.string('ak5/ProcessedTree'),
	trigger_histogram_name = cms.string('ak5/TriggerNames'),
	#triggers              = cms.vstring('HLT_DiJet80Eta2p6_BTagIP3DFastPVLoose_v2:L1_DoubleJetC36', 'HLT_DiJet80Eta2p6_BTagIP3DFastPVLoose_v3:L1_DoubleJetC36', 'HLT_DiJet80Eta2p6_BTagIP3DFastPVLoose_v4:L1_DoubleJetC36', 'HLT_DiJet80Eta2p6_BTagIP3DFastPVLoose_v5:L1_DoubleJetC36', 'HLT_DiJet80Eta2p6_BTagIP3DFastPVLoose_v7:L1_DoubleJetC36'),
	#triggers              = cms.vstring(	'HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose_v2:L1_SingleJet128', 'HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose_v3:L1_SingleJet128', 'HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose_v4:L1_SingleJet128', 'HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose_v5:L1_SingleJet128', 'HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose_v7:L1_SingleJet128'),
	data_source            = cms.string(options.dataSource),  
	data_type              = cms.string(options.dataType),
	signal_mass            = cms.double(options.signalMass),  
	max_events             = cms.int32(-1),
	dijet_cuts             = dijet_cuts,
	pfjet_cuts             = pfjet_cuts,
	calojet_cuts           = calojet_cuts,
	event_cuts             = event_cuts,
	fatjet_delta_eta_cut  = cms.double(1.1),
	btag_wp_1              = cms.string('CSVT'),
	btag_wp_2              = cms.string('CSVL'),
)

process.p = cms.Path(process.BHistograms)

