#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "FWCore/Common/interface/TriggerResultsByName.h"
#include "DataFormats/HLTReco/interface/TriggerTypeDefs.h"
#include "JetMETCorrections/Objects/interface/JetCorrector.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "AnalysisDataFormats/EWK/interface/WMuNuCandidate.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TString.h"
#include <TLorentzVector.h>
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/GeometryVector/interface/Phi.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/JetReco/interface/Jet.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/JetReco/interface/CaloJet.h"
#include "DataFormats/JetReco/interface/CaloJetCollection.h"
#include "DataFormats/JetReco/interface/JetExtendedAssociation.h"
#include "DataFormats/JetReco/interface/JetID.h"
#include "DataFormats/METReco/interface/PFMET.h"
#include "DataFormats/METReco/interface/PFMETCollection.h"
#include "DataFormats/METReco/interface/CaloMET.h"
#include "DataFormats/METReco/interface/CaloMETCollection.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "SimDataFormats/JetMatching/interface/JetFlavour.h"
#include "SimDataFormats/JetMatching/interface/JetFlavourMatching.h"
#include "DataFormats/BTauReco/interface/JetTag.h"
#include "CMSDIJET/QCDAnalysis/interface/QCDPFJet.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Math/interface/deltaR.h"

using namespace trigger;

class PDFUncertaintySelector : public edm::EDAnalyzer {
public:
  typedef reco::Particle::LorentzVector LorentzVector;

  PDFUncertaintySelector (const edm::ParameterSet &);
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
  virtual void beginJob() override;
  virtual void endJob() override;
  virtual void beginRun(edm::Run const&, edm::EventSetup const&);
private:
    static bool sort_pfjets(QCDPFJet j1, QCDPFJet j2) {
      return j1.ptCor() > j2.ptCor();
    }

  std::string mPFJECservice;
  std::string mPFPayloadName;
  std::string mPFJECUncSrc;
  std::string mJetFlavour;
  std::vector<std::string> mPFJECUncSrcNames;
  edm::InputTag mPFJetsName;
    edm::InputTag mGenJetsName;
  edm::InputTag mOfflineVertices;
  edm::InputTag mSrcPFRho;
  bool   isPFJecUncSet_;
  int    mGoodVtxNdof;
  double mGoodVtxZ  ;
    bool   mIsMCarlo;
    double mMinGenPt;
    double mMaxY;
    double mMinPFPt;
    double mMinJJMass;
    bool   mFilterBB;
  //---- TRIGGER -------------------------
  std::string   processName_;
  std::vector<std::string> triggerNames_;
  std::vector<unsigned int> triggerIndex_;
  edm::InputTag triggerResultsTag_;
  edm::InputTag triggerEventTag_;
  edm::Handle<edm::TriggerResults>   triggerResultsHandle_;
  edm::Handle<trigger::TriggerEvent> triggerEventHandle_;
  HLTConfigProvider hltConfig_;
  //---- CORRECTORS ----------------------
  const JetCorrector *mPFJEC;
  JetCorrectionUncertainty *mPFUnc;
  std::vector<JetCorrectionUncertainty*> mPFUncSrc;
  edm::InputTag mSrcPU;
  std::string mSR;

  // Weight stuff
  std::vector<edm::InputTag> pdfWeightTags_;
  unsigned int originalEvents_;
  unsigned int selectedEvents_;
  unsigned int failedEvents_;
  std::vector<int> pdfStart_;
  std::vector<double> weightedSelectedEvents_;
  std::vector<double> weighted2SelectedEvents_;
  std::vector<double> weightedEvents_;
  edm::Service<TFileService> fs;
  std::map<std::string, unsigned int> cut_results_;

  std::vector<double> nnpdfVar63Weights_;

};
