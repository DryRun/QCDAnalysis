import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing()

options.register('maxEvents',
    -1, #default value
    VarParsing.VarParsing.multiplicity.singleton,
    VarParsing.VarParsing.varType.int,
    "Number of events to process"
)
options.register('inputFiles',
    '/QCD_Pt-600to800_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM', 
    VarParsing.VarParsing.multiplicity.list,
    VarParsing.VarParsing.varType.string,
    "Input files"
)
options.register('outputFile',
  'pdf_output.root',
    VarParsing.VarParsing.multiplicity.singleton,
    VarParsing.VarParsing.varType.string,
)
options.register('SR',
    'LowMass',
    VarParsing.VarParsing.multiplicity.singleton,
    VarParsing.VarParsing.varType.string,
)
options.parseArguments()

process = cms.Process("PDFANA")
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)
process.MessageLogger = cms.Service("MessageLogger",
      cout = cms.untracked.PSet(
            default = cms.untracked.PSet(limit = cms.untracked.int32(-1)),
            threshold = cms.untracked.string('INFO')
      ),
      destinations = cms.untracked.vstring('cout')
)
process.source = cms.Source("PoolSource",
      #debugVerbosity = cms.untracked.uint32(0),
      #debugFlag = cms.untracked.bool(False),
      fileNames = cms.untracked.vstring(options.inputFiles),
)
process.TFileService = cms.Service("TFileService",fileName = cms.string(options.outputFile))

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
            , "CT10.LHgrid"
            , "MSTW2008nlo68cl.LHgrid"
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
process.pdfUncSelector = cms.untracked.string(options.SR)

# Main path
process.pdfana = cms.Path(
    process.myPartons * 
    (process.AK5Flavour + process.AK5PFFlavour) * 
    process.pdfWeights * 
    process.selectBBEvent
)

# Collect results
#process.end = cms.EndPath(process.pdfSystematics)
