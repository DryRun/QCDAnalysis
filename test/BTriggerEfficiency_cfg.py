import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing()
options.register('inputFiles', 
	'/eos/uscms/store/user/dryu/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012B_v1_3_trigeff/160502_150041/0000/QCDBEventTree_13.root',
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

