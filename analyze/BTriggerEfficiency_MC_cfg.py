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
	input_files_vstring = cms.vstring('/eos/uscms/store/user/dryu/RSGravitonToBBbar_M-700_TuneZ2star_8TeV-pythia6/QCDBEventTree_RSGravitonToBBbar_M-700_v1_3/160501_234353/0000/QCDBEventTree_3.root')
else:
	input_files_vstring = cms.vstring(options.inputFiles)

##-------------------- User analyzer  --------------------------------
process.BHistograms    = cms.EDAnalyzer('BTriggerEfficiency',
	file_names             = input_files_vstring,
	tree_name              = cms.string('ak5/ProcessedTree'),
	trigger_histogram_name = cms.string('ak5/TriggerNames'),
	data_source            = cms.string('mc'),    
	max_events             = cms.int32(-1)
)

process.p = cms.Path(process.BHistograms)

