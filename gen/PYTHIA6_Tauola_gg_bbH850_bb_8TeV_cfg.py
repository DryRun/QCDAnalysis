# Auto generated configuration file
# using: 
# Revision: 1.381.2.28 
# Source: /local/reps/CMSSW/CMSSW/Configuration/PyReleaseValidation/python/ConfigBuilder.py,v 
# with command line options: CMSDIJET/QCDAnalysis/python/PYTHIA6_Tauola_gg_bbH850_bb_8TeV_cff.py --python_filename /uscms/home/dryu/Dijets/CMSSW_5_3_32_patch3/src/CMSDIJET/QCDAnalysis/gen/PYTHIA6_Tauola_gg_bbH850_bb_8TeV_cfg.py --fileout file:PYTHIA6_Tauola_gg_bbH850_bb_8TeV_FastSim_RECOSIM.root --step GEN,FASTSIM,HLT:7E33v2 --mc --eventcontent RECOSIM --datatier GEN-SIM-DIGI-RECO --pileup 2012_Startup_inTimeOnly --geometry DB --conditions auto:mc --beamspot Realistic8TeVCollision --no_exec -n 1000
import FWCore.ParameterSet.Config as cms

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
    input = cms.untracked.int32(1000)
)

# Input source
process.source = cms.Source("EmptySource")

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.381.2.28 $'),
    annotation = cms.untracked.string('CMSDIJET/QCDAnalysis/python/PYTHIA6_Tauola_gg_bbH850_bb_8TeV_cff.py nevts:1000'),
    name = cms.untracked.string('PyReleaseValidation')
)

# Output definition

process.RECOSIMoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.RECOSIMEventContent.outputCommands,
    fileName = cms.untracked.string('file:PYTHIA6_Tauola_gg_bbH850_bb_8TeV_FastSim_RECOSIM.root'),
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

process.generator = cms.EDFilter("Pythia6GeneratorFilter",
    ExternalDecays = cms.PSet(
        Tauola = cms.untracked.PSet(
            UseTauolaPolarization = cms.bool(True),
            InputCards = cms.PSet(
                mdtau = cms.int32(0),
                pjak2 = cms.int32(0),
                pjak1 = cms.int32(0)
            )
        ),
        parameterSets = cms.vstring('Tauola')
    ),
    maxEventsToPrint = cms.untracked.int32(5),
    pythiaPylistVerbosity = cms.untracked.int32(0),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(8000.0),
    crossSection = cms.untracked.double(1.0),
    UseExternalGenerators = cms.untracked.bool(True),
    PythiaParameters = cms.PSet(
        pythiaUESettings = cms.vstring('MSTU(21)=1     ! Check on possible errors during program execution', 
            'MSTJ(22)=2     ! Decay those unstable particles', 
            'PARJ(71)=10 .  ! for which ctau  10 mm', 
            'MSTP(33)=0     ! no K factors in hard cross sections', 
            'MSTP(2)=1      ! which order running alphaS', 
            'MSTP(51)=10042 ! structure function chosen (external PDF CTEQ6L1)', 
            'MSTP(52)=2     ! work with LHAPDF', 
            'PARP(82)=1.921 ! pt cutoff for multiparton interactions', 
            'PARP(89)=1800. ! sqrts for which PARP82 is set', 
            'PARP(90)=0.227 ! Multiple interactions: rescaling power', 
            'MSTP(95)=6     ! CR (color reconnection parameters)', 
            'PARP(77)=1.016 ! CR', 
            'PARP(78)=0.538 ! CR', 
            'PARP(80)=0.1   ! Prob. colored parton from BBR', 
            'PARP(83)=0.356 ! Multiple interactions: matter distribution parameter', 
            'PARP(84)=0.651 ! Multiple interactions: matter distribution parameter', 
            'PARP(62)=1.025 ! ISR cutoff', 
            'MSTP(91)=1     ! Gaussian primordial kT', 
            'PARP(93)=10.0  ! primordial kT-max', 
            'MSTP(81)=21    ! multiple parton interactions 1 is Pythia default', 
            'MSTP(82)=4     ! Defines the multi-parton model'),
        processParameters = cms.vstring('MSEL=0         ! User defined processes', 
            'MSUB(186)= 1   ! gg->QQbarH (MSSM)', 
            'KFPR(186,2)= 5 ! Q = b Registered by Alexandre.Nikitenko@cern.ch', 
            'IMSS(1)= 1     ! MSSM with parameters', 
            'RMSS(5)= 30.   ! tan beta', 
            'RMSS(19)= 850 ! m_A', 
            'RMSS(1)= 100.  ! M1', 
            'RMSS(2)= 200.  ! M2', 
            'RMSS(3)= 800.  ! Mg', 
            'RMSS(4)= 200.  ! mu', 
            'RMSS(6)= 1000.  ! MS', 
            'RMSS(7)= 1000.  ! MS', 
            'RMSS(8)= 1000.  ! MS', 
            'RMSS(9)= 1000.  ! MS', 
            'RMSS(10)= 1000.  ! MS', 
            'RMSS(11)= 1000.  ! MS', 
            'RMSS(12)= 1000.  ! MS', 
            'RMSS(13)= 1000.  ! MS', 
            'RMSS(14)= 1000.  ! MS', 
            'RMSS(15)= 2000.  ! Ab', 
            'RMSS(16)= 2000.  ! At', 
            'RMSS(17)= 2000.  ! Atau', 
            'MDME(420,1)=0  ! Higgs(H) decay into d              dbar', 
            'MDME(421,1)=0  ! Higgs(H) decay into u              ubar', 
            'MDME(422,1)=0  ! Higgs(H) decay into s              sbar', 
            'MDME(423,1)=0  ! Higgs(H) decay into c              cbar', 
            'MDME(424,1)=1  ! Higgs(H) decay into b              bbar', 
            'MDME(425,1)=0  ! Higgs(H) decay into t              tbar', 
            'MDME(426,1)=0  ! Higgs(H) decay into b              bbar', 
            'MDME(427,1)=0  ! Higgs(H) decay into t              tbar', 
            'MDME(428,1)=0  ! Higgs(H) decay into e-             e+', 
            'MDME(429,1)=0  ! Higgs(H) decay into mu-            mu+', 
            'MDME(430,1)=0  ! Higgs(H) decay into tau-           tau+', 
            'MDME(431,1)=0  ! Higgs(H) decay into tau-           tau+', 
            'MDME(432,1)=0  ! Higgs(H) decay into g              g', 
            'MDME(433,1)=0  ! Higgs(H) decay into gamma          gamma', 
            'MDME(434,1)=0  ! Higgs(H) decay into gamma          Z0', 
            'MDME(435,1)=0  ! Higgs(H) decay into Z0             Z0', 
            'MDME(436,1)=0  ! Higgs(H) decay into W+             W-', 
            'MDME(437,1)=0  ! Higgs(H) decay into Z0             h0', 
            'MDME(438,1)=0  ! Higgs(H) decay into h0             h0', 
            'MDME(439,1)=0  ! Higgs(H) decay into W+             H-', 
            'MDME(440,1)=0  ! Higgs(H) decay into H+             W-', 
            'MDME(441,1)=0  ! Higgs(H) decay into Z0             A0', 
            'MDME(442,1)=0  ! Higgs(H) decay into h0             A0', 
            'MDME(443,1)=0  ! Higgs(H) decay into A0             A0', 
            'MDME(444,1)=0  ! Higgs(H) decay into ~chi_10        ~chi_10', 
            'MDME(445,1)=0  ! Higgs(H) decay into ~chi_20        ~chi_10', 
            'MDME(446,1)=0  ! Higgs(H) decay into ~chi_20        ~chi_20', 
            'MDME(447,1)=0  ! Higgs(H) decay into ~chi_30        ~chi_10', 
            'MDME(448,1)=0  ! Higgs(H) decay into ~chi_30        ~chi_20', 
            'MDME(449,1)=0  ! Higgs(H) decay into ~chi_30        ~chi_30', 
            'MDME(450,1)=0  ! Higgs(H) decay into ~chi_40        ~chi_10', 
            'MDME(451,1)=0  ! Higgs(H) decay into ~chi_40        ~chi_20', 
            'MDME(452,1)=0  ! Higgs(H) decay into ~chi_40        ~chi_30', 
            'MDME(453,1)=0  ! Higgs(H) decay into ~chi_40        ~chi_40', 
            'MDME(454,1)=0  ! Higgs(H) decay into ~chi_1+        ~chi_1-', 
            'MDME(455,1)=0  ! Higgs(H) decay into ~chi_1+        ~chi_2-', 
            'MDME(456,1)=0  ! Higgs(H) decay into ~chi_2+        ~chi_1-', 
            'MDME(457,1)=0  ! Higgs(H) decay into ~chi_2+        ~chi_2-', 
            'MDME(458,1)=0  ! Higgs(H) decay into ~d_L           ~d_Lbar', 
            'MDME(459,1)=0  ! Higgs(H) decay into ~d_R           ~d_Rbar', 
            'MDME(460,1)=0  ! Higgs(H) decay into ~d_L           ~d_Rbar', 
            'MDME(461,1)=0  ! Higgs(H) decay into ~d_Lbar        ~d_R', 
            'MDME(462,1)=0  ! Higgs(H) decay into ~u_L           ~u_Lbar', 
            'MDME(463,1)=0  ! Higgs(H) decay into ~u_R           ~u_Rbar', 
            'MDME(464,1)=0  ! Higgs(H) decay into ~u_L           ~u_Rbar', 
            'MDME(465,1)=0  ! Higgs(H) decay into ~u_Lbar        ~u_R', 
            'MDME(466,1)=0  ! Higgs(H) decay into ~s_L           ~s_Lbar', 
            'MDME(467,1)=0  ! Higgs(H) decay into ~s_R           ~s_Rbar', 
            'MDME(468,1)=0  ! Higgs(H) decay into ~s_L           ~s_Rbar', 
            'MDME(469,1)=0  ! Higgs(H) decay into ~s_Lbar        ~s_R', 
            'MDME(470,1)=0  ! Higgs(H) decay into ~c_L           ~c_Lbar', 
            'MDME(471,1)=0  ! Higgs(H) decay into ~c_R           ~c_Rbar', 
            'MDME(472,1)=0  ! Higgs(H) decay into ~c_L           ~c_Rbar', 
            'MDME(473,1)=0  ! Higgs(H) decay into ~c_Lbar        ~c_R', 
            'MDME(474,1)=0  ! Higgs(H) decay into ~b_1           ~b_1bar', 
            'MDME(475,1)=0  ! Higgs(H) decay into ~b_2           ~b_2bar', 
            'MDME(476,1)=0  ! Higgs(H) decay into ~b_1           ~b_2bar', 
            'MDME(477,1)=0  ! Higgs(H) decay into ~b_1bar        ~b_2', 
            'MDME(478,1)=0  ! Higgs(H) decay into ~t_1           ~t_1bar', 
            'MDME(479,1)=0  ! Higgs(H) decay into ~t_2           ~t_2bar', 
            'MDME(480,1)=0  ! Higgs(H) decay into ~t_1           ~t_2bar', 
            'MDME(481,1)=0  ! Higgs(H) decay into ~t_1bar        ~t_2', 
            'MDME(482,1)=0  ! Higgs(H) decay into ~e_L-          ~e_L+', 
            'MDME(483,1)=0  ! Higgs(H) decay into ~e_R-          ~e_R+', 
            'MDME(484,1)=0  ! Higgs(H) decay into ~e_L-          ~e_R+', 
            'MDME(485,1)=0  ! Higgs(H) decay into ~e_L+          ~e_R-', 
            'MDME(486,1)=0  ! Higgs(H) decay into ~nu_eL         ~nu_eLbar', 
            'MDME(487,1)=0  ! Higgs(H) decay into ~nu_eR         ~nu_eRbar', 
            'MDME(488,1)=0  ! Higgs(H) decay into ~nu_eL         ~nu_eRbar', 
            'MDME(489,1)=0  ! Higgs(H) decay into ~nu_eLbar      ~nu_eR', 
            'MDME(490,1)=0  ! Higgs(H) decay into ~mu_L-         ~mu_L+', 
            'MDME(491,1)=0  ! Higgs(H) decay into ~mu_R-         ~mu_R+', 
            'MDME(492,1)=0  ! Higgs(H) decay into ~mu_L-         ~mu_R+', 
            'MDME(493,1)=0  ! Higgs(H) decay into ~mu_L+         ~mu_R-', 
            'MDME(494,1)=0  ! Higgs(H) decay into ~nu_muL        ~nu_muLbar', 
            'MDME(495,1)=0  ! Higgs(H) decay into ~nu_muR        ~nu_muRbar', 
            'MDME(496,1)=0  ! Higgs(H) decay into ~nu_muL        ~nu_muRbar', 
            'MDME(497,1)=0  ! Higgs(H) decay into ~nu_muLbar     ~nu_muR', 
            'MDME(498,1)=0  ! Higgs(H) decay into ~tau_1-        ~tau_1+', 
            'MDME(499,1)=0  ! Higgs(H) decay into ~tau_1-        ~tau_1+', 
            'MDME(500,1)=0  ! Higgs(H) decay into ~tau_1-        ~tau_1+', 
            'MDME(501,1)=0  ! Higgs(H) decay into ~tau_1-        ~tau_1+', 
            'MDME(502,1)=0  ! Higgs(H) decay into ~tau_2-        ~tau_2+'),
        parameterSets = cms.vstring('pythiaUESettings', 
            'processParameters')
    )
)


process.ProductionFilterSequence = cms.Sequence(process.generator)

# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen_genonly)
process.reconstruction = cms.Path(process.reconstructionWithFamos)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.RECOSIMoutput_step = cms.EndPath(process.RECOSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step)
process.schedule.extend(process.HLTSchedule)
process.schedule.extend([process.reconstruction,process.RECOSIMoutput_step])
# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path)._seq = process.ProductionFilterSequence * getattr(process,path)._seq 

# customisation of the process.

# Automatic addition of the customisation function from HLTrigger.Configuration.customizeHLTforMC
from HLTrigger.Configuration.customizeHLTforMC import customizeHLTforMC 

#call to customisation function customizeHLTforMC imported from HLTrigger.Configuration.customizeHLTforMC
process = customizeHLTforMC(process)

# End of customisation functions
