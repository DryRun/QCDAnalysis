import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing()
options.register('inputFiles', 
	'', 
	VarParsing.VarParsing.multiplicity.singleton,
	VarParsing.VarParsing.varType.string,
	"List of input files"
)
options.parseArguments()




process = cms.Process("myprocess")
process.TFileService=cms.Service("TFileService",fileName=cms.string('InclusiveBHistograms.root'))

##-------------------- Define the source  ----------------------------
process.maxEvents = cms.untracked.PSet(
		input = cms.untracked.int32(1)
		)
process.source = cms.Source("EmptySource")

##-------------------- User analyzer  --------------------------------
process.inclusive    = cms.EDAnalyzer('InclusiveBHistograms',
	file_names             = cms.vstring(
	'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012B_v1_3/160429_121519/0000/QCDBEventTree_567.root',
	'/uscms/home/dryu/eosdir/BJetPlusX/QCDBEventTree_BJetPlusX_Run2012B_v1_3/160429_121519/0000/QCDBEventTree_585.root',
	),
	tree_name              = cms.string('ak5/ProcessedTree'),
	trigger_histogram_name = cms.string('ak5/TriggerNames'),
	#triggers               = cms.vstring('HLT_DiJet80Eta2p6_BTagIP3DFastPVLoose_v2:L1_DoubleJetC36', 'HLT_DiJet80Eta2p6_BTagIP3DFastPVLoose_v3:L1_DoubleJetC36', 'HLT_DiJet80Eta2p6_BTagIP3DFastPVLoose_v4:L1_DoubleJetC36', 'HLT_DiJet80Eta2p6_BTagIP3DFastPVLoose_v5:L1_DoubleJetC36', 'HLT_DiJet80Eta2p6_BTagIP3DFastPVLoose_v7:L1_DoubleJetC36'),
	triggers = cms.vstring(	'HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose_v2:L1_SingleJet128', 'HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose_v3:L1_SingleJet128', 'HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose_v4:L1_SingleJet128', 'HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose_v5:L1_SingleJet128', 'HLT_Jet160Eta2p4_Jet120Eta2p4_DiBTagIP3DFastPVLoose_v7:L1_SingleJet128'),
	data_source            = cms.string('collision_data'),    
	max_events             = cms.int32(-1)
)

process.p = cms.Path(process.inclusive)

