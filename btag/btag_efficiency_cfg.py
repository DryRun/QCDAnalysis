import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing
import sys

options = VarParsing.VarParsing()
options.register('inputFiles', 
	'file:/uscms/home/dryu/Dijets/CMSSW_5_3_32_patch3/src/PhysicsTools/PatAlgos/test/patTuple_standard.root',
	VarParsing.VarParsing.multiplicity.list,
	VarParsing.VarParsing.varType.string,
	"List of input files"
)
options.register('outputFile', 
	'BTagEfficiency.root', 
	VarParsing.VarParsing.multiplicity.singleton,
	VarParsing.VarParsing.varType.string,
	"Output file"
)
options.parseArguments()

process = cms.Process("myprocess")
process.TFileService=cms.Service("TFileService",fileName=cms.string(options.outputFile))

##-------------------- Define the source  ----------------------------
process.maxEvents = cms.untracked.PSet(
		input = cms.untracked.int32(-1)
		)
process.source = cms.Source("PoolSource",
	fileNames = cms.untracked.vstring(options.inputFiles),
)


##-------------------- User analyzer  --------------------------------
process.BTagEfficiency    = cms.EDAnalyzer('BTaggingEffAnalyzer',
	JetsTag             = cms.InputTag('cleanPatJetsAK5PF'),
	DiscriminatorTag    = cms.string('combinedSecondaryVertexBJetTags'),
	DiscriminatorValues = cms.vdouble(0.244, 0.679, 0.898),
	PtNBins             = cms.int32(800),
	PtMin               = cms.double(0.),
	PtMax               = cms.double(8000.),
	EtaNBins            = cms.int32(50),
	EtaMin              = cms.double(-2.5),
	EtaMax              = cms.double(2.5),
)

process.p = cms.Path(process.BTagEfficiency)

