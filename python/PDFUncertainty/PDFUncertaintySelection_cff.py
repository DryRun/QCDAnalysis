import FWCore.ParameterSet.Config as cms

#from ElectroWeakAnalysis.WMuNu.wmunusProducer_cfi import *

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

pdfUncSelector = cms.EDAnalyzer("PDFUncertaintySelector",
	pfjets             = cms.InputTag('ak5PFJets'),
	genjets            = cms.untracked.InputTag('ak5GenJets'),
	calojetID          = cms.string('ak5JetID'),
	calojetExtender    = cms.string('ak5JetExtender'),
	pfjecService       = cms.string('ak5PFL1FastL2L3'),
	jetFlavourMatching = cms.untracked.string('AK5byValAlgo'),
	printTriggerMenu   = cms.bool(False),
	PFPayloadName      = cms.string(''),
	jecUncSrc          = cms.string(''),
	jecUncSrcNames     = cms.vstring(''),
	offlineVertices    = cms.InputTag('offlinePrimaryVertices'),
	goodVtxNdof        = cms.double(4), 
	goodVtxZ           = cms.double(24),
	srcPFRho           = cms.InputTag('kt6PFJets','rho'),
	isMCarlo           = cms.untracked.bool(True),
	FilterBB           = cms.untracked.bool(False),
	srcPU              = cms.untracked.InputTag('addPileupInfo'),
	minPFPt            = cms.double(20),
	minPFFatPt         = cms.double(10),
	maxPFFatEta        = cms.double(2.5),
	minNPFJets         = cms.int32(1),
	minJJMass          = cms.double(-1),
	processName        = cms.string('HLT'),
	triggerName        = trigger_list,
	triggerResults     = cms.InputTag("TriggerResults","","HLT"),
	triggerEvent       = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
	SR                 = cms.string('LowMass'),
    maxY            = cms.double(5.0), 
	PdfWeightTags      = cms.untracked.VInputTag(
		#"pdfWeights:NNPDF23_nlo_as_0118",
		"pdfWeights:NNPDF23nloas0118",
		"pdfWeights:CT10",
		"pdfWeights:MSTW2008nlo68cl",
	)
)

selectBBEvent = cms.Sequence(pdfUncSelector)
