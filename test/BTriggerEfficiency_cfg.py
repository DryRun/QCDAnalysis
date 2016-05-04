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
		'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_579.root',
		'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_954.root',
		'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_255.root',
		'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_417.root',
		'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_783.root',
		'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_538.root',
		'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_177.root',
		'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_3.root',
		'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_21.root',
		'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_722.root',
		'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_523.root',
		'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_859.root',
		'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_172.root',
		'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_5.root',
		'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012C_v1_4/160503_154243/0000/QCDBEventTree_4.root',
		)
else:
	input_files_vstring = cms.vstring(options.inputFiles)

##-------------------- User analyzer  --------------------------------
process.inclusive    = cms.EDAnalyzer('BTriggerEfficiency',
	file_names             = input_files_vstring,
	tree_name              = cms.string('ak5/ProcessedTree'),
	trigger_histogram_name = cms.string('ak5/TriggerNames'),
	data_source            = cms.string('collision_data'),    
	max_events             = cms.int32(-1)
)

process.p = cms.Path(process.inclusive)

