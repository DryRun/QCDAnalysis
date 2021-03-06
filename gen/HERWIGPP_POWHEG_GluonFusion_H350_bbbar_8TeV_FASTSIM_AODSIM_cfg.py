# Auto generated configuration file
# using: 
# Revision: 1.381.2.28 
# Source: /local/reps/CMSSW/CMSSW/Configuration/PyReleaseValidation/python/ConfigBuilder.py,v 
# with command line options: CMSDIJET/QCDAnalysis/python/HERWIGPP_POWHEG_GluonFusion_H350_bbbar_8TeV_cff.py --python_filename /uscms/home/dryu/Dijets/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/gen/HERWIGPP_POWHEG_GluonFusion_H350_bbbar_8TeV_FASTSIM_AODSIM_cfg.py --fileout file:HERWIGPP_POWHEG_GluonFusion_H350_bbbar_8TeV_FASTSIM_AODSIM.root --step GEN,FASTSIM,HLT:7E33v2 --mc --eventcontent AODSIM --datatier GEN-SIM-DIGI-RECO --pileup 2012_Startup_inTimeOnly --geometry DB --conditions auto:mc --beamspot Realistic8TeVCollision --no_exec -n 5000
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing
#------------------------------------------------------------------------------------
# Options
#------------------------------------------------------------------------------------
options = VarParsing.VarParsing()
options.parseArguments()

process = cms.Process('HLT')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('FastSimulation.Configuration.EventContent_cff')
process.load('FastSimulation.PileUpProducer.PileUpSimulator_2012_Startup_inTimeOnly_cff')
process.load('FastSimulation.Configuration.Geometries_MC_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('FastSimulation.Configuration.FamosSequences_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedParameters_cfi')
process.load('HLTrigger.Configuration.HLT_7E33v2_Famos_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(5000)
)

# Input source
process.source = cms.Source("EmptySource")

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('\\$Revision: 1.3 $'),
    annotation = cms.untracked.string('HERWIGPP/POWHEG: (H->bb)(W->lnu), m(H)=125 GeV, l=e or mu or tau'),
    name = cms.untracked.string('\\$Source: /local/reps/CMSSW/CMSSW/Configuration/GenProduction/python/EightTeV/HERWIGPP_POWHEG_H125_bbbar_W_lnu_8TeV_cff.py,v $')
)

# Output definition

process.AODSIMoutput = cms.OutputModule("PoolOutputModule",
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    outputCommands = process.AODSIMEventContent.outputCommands,
    fileName = cms.untracked.string('file:HERWIGPP_POWHEG_GluonFusion_H350_bbbar_8TeV_FASTSIM_AODSIM.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN-SIM-DIGI-RECO')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    )
)

# Additional output definition

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
process.famosSimHits.SimulateCalorimetry = True
process.famosSimHits.SimulateTracking = True
process.simulation = cms.Sequence(process.simulationWithFamos)
process.HLTEndSequence = cms.Sequence(process.reconstructionWithFamos)
process.Realistic8TeVCollisionVtxSmearingParameters.type = cms.string("BetaFunc")
process.famosSimHits.VertexGenerator = process.Realistic8TeVCollisionVtxSmearingParameters
process.famosPileUp.VertexGenerator = process.Realistic8TeVCollisionVtxSmearingParameters
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:mc', '')

process.generator = cms.EDFilter("ThePEGGeneratorFilter",
    ue_2_3 = cms.vstring('cd /Herwig/UnderlyingEvent', 
        'set KtCut:MinKT 4.0', 
        'set UECuts:MHatMin 8.0', 
        'set MPIHandler:InvRadius 1.5', 
        'cd /'),
    pdfMRST2001 = cms.vstring('cd /Herwig/Partons', 
        'create Herwig::MRST MRST2001 HwMRST.so', 
        'setup MRST2001 ${HERWIGPATH}/PDF/mrst/2001/lo2002.dat', 
        'set MRST2001:RemnantHandler HadronRemnants', 
        'cp MRST2001 cmsPDFSet', 
        'cd /'),
    ue_2_4 = cms.vstring('cd /Herwig/UnderlyingEvent', 
        'set KtCut:MinKT 4.3', 
        'set UECuts:MHatMin 8.6', 
        'set MPIHandler:InvRadius 1.2', 
        'cd /'),
    cm7TeV = cms.vstring('set /Herwig/Generators/LHCGenerator:EventHandler:LuminosityFunction:Energy 7000.0', 
        'set /Herwig/Shower/Evolver:IntrinsicPtGaussian 2.0*GeV'),
    powhegDefaults = cms.vstring('cp /Herwig/Partons/MRST-NLO /cmsPDFSet', 
        'set /Herwig/Particles/p+:PDF    /Herwig/Partons/MRST-NLO', 
        'set /Herwig/Particles/pbar-:PDF /Herwig/Partons/MRST-NLO', 
        'create Herwig::O2AlphaS O2AlphaS', 
        'set /Herwig/Generators/LHCGenerator:StandardModelParameters:QCD/RunningAlphaS O2AlphaS', 
        'cd /Herwig/Shower', 
        'set KinematicsReconstructor:ReconstructionOption General', 
        'create Herwig::PowhegEvolver PowhegEvolver HwPowhegShower.so', 
        'set ShowerHandler:Evolver PowhegEvolver', 
        'set PowhegEvolver:ShowerModel ShowerModel', 
        'set PowhegEvolver:SplittingGenerator SplittingGenerator', 
        'set PowhegEvolver:MECorrMode 0', 
        'create Herwig::DrellYanHardGenerator DrellYanHardGenerator', 
        'set DrellYanHardGenerator:ShowerAlpha AlphaQCD', 
        'insert PowhegEvolver:HardGenerator 0 DrellYanHardGenerator', 
        'create Herwig::GGtoHHardGenerator GGtoHHardGenerator', 
        'set GGtoHHardGenerator:ShowerAlpha AlphaQCD', 
        'insert PowhegEvolver:HardGenerator 0 GGtoHHardGenerator'),
    reweightConstant = cms.vstring('mkdir /Herwig/Weights', 
        'cd /Herwig/Weights', 
        'create ThePEG::ReweightConstant reweightConstant ReweightConstant.so', 
        'cd /', 
        'set /Herwig/Weights/reweightConstant:C 1', 
        'insert SimpleQCD:Reweights[0] /Herwig/Weights/reweightConstant'),
    lheDefaultPDFs = cms.vstring('cd /Herwig/EventHandlers', 
        'set LHEReader:PDFA /cmsPDFSet', 
        'set LHEReader:PDFB /cmsPDFSet', 
        'cd /'),
    lheDefaults = cms.vstring('cd /Herwig/Cuts', 
        'create ThePEG::Cuts NoCuts', 
        'cd /Herwig/EventHandlers', 
        'create ThePEG::LesHouchesInterface LHEReader', 
        'set LHEReader:Cuts /Herwig/Cuts/NoCuts', 
        'create ThePEG::LesHouchesEventHandler LHEHandler', 
        'set LHEHandler:WeightOption VarWeight', 
        'set LHEHandler:PartonExtractor /Herwig/Partons/QCDExtractor', 
        'set LHEHandler:CascadeHandler /Herwig/Shower/ShowerHandler', 
        'set LHEHandler:HadronizationHandler /Herwig/Hadronization/ClusterHadHandler', 
        'set LHEHandler:DecayHandler /Herwig/Decays/DecayHandler', 
        'insert LHEHandler:LesHouchesReaders 0 LHEReader', 
        'cd /Herwig/Generators', 
        'set LHCGenerator:EventHandler /Herwig/EventHandlers/LHEHandler', 
        'cd /Herwig/Shower', 
        'set Evolver:HardVetoScaleSource Read', 
        'set Evolver:MECorrMode No', 
        'cd /'),
    cmsDefaults = cms.vstring('+pdfMRST2001', 
        '+cm14TeV', 
        '+ue_2_3', 
        '+basicSetup', 
        '+setParticlesStableForDetector'),
    pdfMRST2008LOss = cms.vstring('cp /Herwig/Partons/MRST /Herwig/Partons/cmsPDFSet'),
    generatorModule = cms.string('/Herwig/Generators/LHCGenerator'),
    basicSetup = cms.vstring('cd /Herwig/Generators', 
        'create ThePEG::RandomEngineGlue /Herwig/RandomGlue', 
        'set LHCGenerator:RandomNumberGenerator /Herwig/RandomGlue', 
        'set LHCGenerator:NumberOfEvents 10000000', 
        'set LHCGenerator:DebugLevel 1', 
        'set LHCGenerator:PrintEvent 0', 
        'set LHCGenerator:MaxErrors 10000', 
        'cd /Herwig/Particles', 
        'set p+:PDF /Herwig/Partons/cmsPDFSet', 
        'set pbar-:PDF /Herwig/Partons/cmsPDFSet', 
        'set K0:Width 1e300*GeV', 
        'set Kbar0:Width 1e300*GeV', 
        'cd /'),
    run = cms.string('LHC'),
    repository = cms.string('HerwigDefaults.rpo'),
    cm14TeV = cms.vstring('set /Herwig/Generators/LHCGenerator:EventHandler:LuminosityFunction:Energy 14000.0', 
        'set /Herwig/Shower/Evolver:IntrinsicPtGaussian 2.2*GeV'),
    dataLocation = cms.string('${HERWIGPATH}'),
    pdfCTEQ5L = cms.vstring('cd /Herwig/Partons', 
        'create ThePEG::LHAPDF CTEQ5L ThePEGLHAPDF.so', 
        'set CTEQ5L:PDFName cteq5l.LHgrid', 
        'set CTEQ5L:RemnantHandler HadronRemnants', 
        'cp CTEQ5L cmsPDFSet', 
        'cd /'),
    setParticlesStableForDetector = cms.vstring('cd /Herwig/Particles', 
        'set mu-:Stable Stable', 
        'set mu+:Stable Stable', 
        'set Sigma-:Stable Stable', 
        'set Sigmabar+:Stable Stable', 
        'set Lambda0:Stable Stable', 
        'set Lambdabar0:Stable Stable', 
        'set Sigma+:Stable Stable', 
        'set Sigmabar-:Stable Stable', 
        'set Xi-:Stable Stable', 
        'set Xibar+:Stable Stable', 
        'set Xi0:Stable Stable', 
        'set Xibar0:Stable Stable', 
        'set Omega-:Stable Stable', 
        'set Omegabar+:Stable Stable', 
        'set pi+:Stable Stable', 
        'set pi-:Stable Stable', 
        'set K+:Stable Stable', 
        'set K-:Stable Stable', 
        'set K_S0:Stable Stable', 
        'set K_L0:Stable Stable', 
        'cd /'),
    reweightPthat = cms.vstring('mkdir /Herwig/Weights', 
        'cd /Herwig/Weights', 
        'create ThePEG::ReweightMinPT reweightMinPT ReweightMinPT.so', 
        'cd /', 
        'set /Herwig/Weights/reweightMinPT:Power 4.5', 
        'set /Herwig/Weights/reweightMinPT:Scale 15*GeV', 
        'insert SimpleQCD:Reweights[0] /Herwig/Weights/reweightMinPT'),
    cm10TeV = cms.vstring('set /Herwig/Generators/LHCGenerator:EventHandler:LuminosityFunction:Energy 10000.0', 
        'set /Herwig/Shower/Evolver:IntrinsicPtGaussian 2.1*GeV'),
    cm8TeV = cms.vstring('set /Herwig/Generators/LHCGenerator:EventHandler:LuminosityFunction:Energy 8000.0', 
        'set /Herwig/Shower/Evolver:IntrinsicPtGaussian 2.0*GeV'),
    pdfCTEQ6L1 = cms.vstring('cd /Herwig/Partons', 
        'create ThePEG::LHAPDF CTEQ6L1 ThePEGLHAPDF.so', 
        'set CTEQ6L1:PDFName cteq6ll.LHpdf', 
        'set CTEQ6L1:RemnantHandler HadronRemnants', 
        'cp CTEQ6L1 cmsPDFSet', 
        'cd /'),
    eventHandlers = cms.string('/Herwig/EventHandlers'),
    configFiles = cms.vstring(),
    pdfCTEQ6M = cms.vstring('mkdir /LHAPDF', 
        'cd /LHAPDF', 
        'create ThePEG::LHAPDF CTEQ6M', 
        'set CTEQ6M:PDFName cteq6mE.LHgrid', 
        'set CTEQ6M:RemnantHandler /Herwig/Partons/HadronRemnants', 
        'cp CTEQ6M /cmsPDFSet', 
        'cd /'),
    parameterSets = cms.vstring('cm8TeV', 
        'powhegNewDefaults', 
        'GluonFusionHbbParameters', 
        'basicSetup', 
        'setParticlesStableForDetector'),
    powhegNewDefaults = cms.vstring('#  Need to use an NLO PDF', 
        '#  and strong coupling', 
        'cp /Herwig/Partons/MRST-NLO /Herwig/Partons/cmsPDFSet', 
        'create Herwig::O2AlphaS O2AlphaS', 
        'set /Herwig/Generators/LHCGenerator:StandardModelParameters:QCD/RunningAlphaS O2AlphaS', 
        '#  Setup the POWHEG shower', 
        'cd /Herwig/Shower', 
        'set Evolver:HardEmissionMode POWHEG', 
        '# higgs + W (N.B. if considering all W decay modes useful to set )', 
        '#           (jet pT cut to zero so no cut on W decay products    )', 
        '# insert SimpleQCD:MatrixElements[0] PowhegMEPP2WH', 
        '# set /Herwig/Cuts/JetKtCut:MinKT 0.0*GeV', 
        '# higgs + Z (N.B. if considering all Z decay modes useful to set )', 
        '#           (jet pT cut to zero so no cut on Z decay products    )', 
        '# insert SimpleQCD:MatrixElements[0] PowhegMEPP2ZH', 
        '# set /Herwig/Cuts/JetKtCut:MinKT 0.0*GeV', 
        '# gg/qqbar -> Higgs', 
        '# insert SimpleQCD:MatrixElements[0] PowhegMEHiggs', 
        '# Weak boson pair production: WW / ZZ / WZ / W+Z [WpZ] / W-Z [WmZ]', 
        '# insert SimpleQCD:MatrixElements[0] PowhegMEPP2VV', 
        '# set PowhegMEPP2VV:Process WpZ'),
    GluonFusionHbbParameters = cms.vstring('cd /Herwig/MatrixElements/', 
        'insert SimpleQCD:MatrixElements[0] PowhegMEHiggs', 
        'set /Herwig/Particles/h0:NominalMass 350.*GeV', 
        'set /Herwig/Particles/h0/h0->b,bbar;:OnOff On', 
        'set /Herwig/Particles/h0/h0->W+,W-;:OnOff Off', 
        'set /Herwig/Particles/h0/h0->tau-,tau+;:OnOff Off', 
        'set /Herwig/Particles/h0/h0->g,g;:OnOff Off', 
        'set /Herwig/Particles/h0/h0->c,cbar;:OnOff Off', 
        'set /Herwig/Particles/h0/h0->Z0,Z0;:OnOff Off', 
        'set /Herwig/Particles/h0/h0->gamma,gamma;:OnOff Off', 
        'set /Herwig/Particles/h0/h0->mu-,mu+;:OnOff Off', 
        'set /Herwig/Particles/h0/h0->t,tbar;:OnOff Off')
)


# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen_genonly)
process.reconstruction = cms.Path(process.reconstructionWithFamos)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.AODSIMoutput_step = cms.EndPath(process.AODSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step)
process.schedule.extend(process.HLTSchedule)
process.schedule.extend([process.reconstruction,process.AODSIMoutput_step])
# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path)._seq = process.generator * getattr(process,path)._seq 

# customisation of the process.

# Automatic addition of the customisation function from HLTrigger.Configuration.customizeHLTforMC
from HLTrigger.Configuration.customizeHLTforMC import customizeHLTforMC 

#call to customisation function customizeHLTforMC imported from HLTrigger.Configuration.customizeHLTforMC
process = customizeHLTforMC(process)

# End of customisation functions
