import FWCore.ParameterSet.Config as cms

# Process name
process = cms.Process("PDFANA")

# Max events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

# Printouts
process.MessageLogger = cms.Service("MessageLogger",
      cout = cms.untracked.PSet(
            default = cms.untracked.PSet(limit = cms.untracked.int32(-1)),
            threshold = cms.untracked.string('INFO')
      ),
      destinations = cms.untracked.vstring('cout')
)

# Input files
process.source = cms.Source("PoolSource",
      #debugVerbosity = cms.untracked.uint32(0),
      #debugFlag = cms.untracked.bool(False),
      fileNames = cms.untracked.vstring("file:/home/dryu/store/ZPrimeToCCBB_M_400_g0p25_TuneCUEP8M1_8TeV_MadgraphPythia8/DR2_1_0_3/161227_161148/0000/DIGI-RECO-step2_16.root"),
)

process.load('FWCore.MessageService.MessageLogger_cfi')
##-------------------- Communicate with the DB -----------------------
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = "START53_V27::All"
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load('RecoJets.Configuration.RecoPFJets_cff')
process.load('RecoJets.Configuration.RecoJets_cff')
##-------------------- Import the JEC services -----------------------
process.load('JetMETCorrections.Configuration.DefaultJEC_cff')
##---- Jet-Flavor Matching ------------------------------------------
process.load("PhysicsTools.JetMCAlgos.CaloJetsMCFlavour_cfi") 
process.AK5PFbyRef = process.AK5byRef.clone(jets = cms.InputTag("ak5PFJets"))
process.AK5PFbyValPhys = process.AK5byValPhys.clone(srcByReference = cms.InputTag("AK5PFbyRef"))
process.AK5PFbyValAlgo = process.AK5byValAlgo.clone(srcByReference = cms.InputTag("AK5PFbyRef"))
process.AK5PFFlavour = cms.Sequence(process.AK5PFbyRef*process.AK5PFbyValPhys*process.AK5PFbyValAlgo)

process.MessageLogger = cms.Service("MessageLogger",
      cout = cms.untracked.PSet(
            default = cms.untracked.PSet(limit = cms.untracked.int32(100)),
            threshold = cms.untracked.string('DEBUG')
      ),
      destinations = cms.untracked.vstring('cout')
)


# Produce PDF weights (maximum is 3)
process.pdfWeights = cms.EDProducer("PdfWeightProducer",
      #FixPOWHEG = cms.untracked.bool(False), # fix POWHEG (it requires cteq66* PDFs in the list)
      GenTag = cms.untracked.InputTag("genParticles"),
      PdfInfoTag = cms.untracked.InputTag("generator"),
      PdfSetNames = cms.untracked.vstring(
              "NNPDF23_nlo_as_0118.LHgrid"
            , "cteq66.LHgrid"
            , "MRST2006nnlo.LHgrid"
      ),
      useFirstAsDefault = cms.untracked.bool(True),
)

# Selector and parameters
# WMN fast selector, which requires
# the libraries and plugins fron the ElectroWeakAnalysis/WMuNu package
process.load("CMSDIJET.QCDAnalysis.PDFUncertainty.PDFUncertaintySelection_cff")

# Collect uncertainties for rate and acceptance
#process.pdfSystematics = cms.EDAnalyzer("PdfSystematicsAnalyzer",
#      SelectorPath = cms.untracked.string('PDFANA'),
#      PdfWeightTags = cms.untracked.VInputTag(
#              #"pdfWeights:NNPDF23_nlo_as_0118",
#              "pdfWeights:NNPDF23",
#              "pdfWeights:cteq66",
#              "pdfWeights:MRST2006nnlo",
#      )
#)

process.pdfUncSelector.FilterBB = cms.untracked.bool(True)

# Main path
process.pdfana = cms.Path(
    process.myPartons * 
    (process.AK5Flavour + process.AK5PFFlavour) * 
    process.pdfWeights * 
    process.selectBBEvent
)

# Collect results
#process.end = cms.EndPath(process.pdfSystematics)
