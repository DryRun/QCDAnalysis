import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing()
options.register('inputFiles', 
	[],
	VarParsing.VarParsing.multiplicity.list,
	VarParsing.VarParsing.varType.string,
	'Input files'
)
options.register('outputFile', 
	#'~/Dijets/data/EightTeeEeVeeBee/TriggerEfficiency/BTriggerEfficiency_test.root', 
	'BTriggerEfficiency_test.root', 
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


process = cms.Process("myprocess")
process.TFileService=cms.Service("TFileService",fileName=cms.string(options.outputFile))

##-------------------- Define the source  ----------------------------
process.maxEvents = cms.untracked.PSet(
		input = cms.untracked.int32(1)
		)
process.source = cms.Source("EmptySource")

if len(options.inputFiles) == 0:
	input_files_vstring = cms.vstring('/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_498.root',
		#'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_579.root',
		#'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_954.root',
		#'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_255.root',
		#'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_417.root',
		#'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_783.root',
		#'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_538.root',
		#'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_177.root',
		#'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_3.root',
		#'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_21.root',
		#'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_722.root',
		#'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_523.root',
		#'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_859.root',
		#'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_172.root',
		#'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_5.root',
		#'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_4.root',
		)
else:
	input_files_vstring = cms.vstring(options.inputFiles)

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
	cms.PSet(
		name = cms.string("MinBTagWeight"),
		parameters = cms.vdouble(0.898),
		descriptors = cms.vstring("csv")
	)
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
		parameters  = cms.vdouble(1.1),
		descriptors = cms.vstring()
	)
)

##-------------------- User analyzer  --------------------------------
process.BHistograms    = cms.EDAnalyzer('BTriggerEfficiency',
	file_names             = input_files_vstring,
	tree_name              = cms.string('ak5/ProcessedTree'),
	trigger_histogram_name = cms.string('ak5/TriggerNames'),
	data_source            = cms.string('collision_data'),    
	max_events             = cms.int32(-1),
	dijet_cuts             = dijet_cuts,
	pfjet_cuts             = pfjet_cuts,
	calojet_cuts           = calojet_cuts,
	event_cuts             = event_cuts,
	fatjet_delta_eta_cut   = cms.double(1.1),
)

process.p = cms.Path(process.BHistograms)

