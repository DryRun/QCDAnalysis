#define HIDE_TRIGGER
#include "CMSDIJET/QCDAnalysis/interface/PDFUncertaintySelector.h"

using namespace edm;
using namespace std;
using namespace reco;

PDFUncertaintySelector::PDFUncertaintySelector( const ParameterSet & cfg )
{
  mPFJECservice      = cfg.getParameter<std::string>("pfjecService");
  mPFPayloadName     = cfg.getParameter<std::string>               ("PFPayloadName");
  mOfflineVertices   = cfg.getParameter<edm::InputTag>             ("offlineVertices");
  mPFJetsName        = cfg.getParameter<edm::InputTag>             ("pfjets");
  mSrcPFRho          = cfg.getParameter<edm::InputTag>             ("srcPFRho");
  mSrcPU             = cfg.getUntrackedParameter<edm::InputTag>    ("srcPU",edm::InputTag("addPileupInfo"));
  triggerNames_      = cfg.getParameter<std::vector<std::string> > ("triggerName");
  triggerResultsTag_ = cfg.getParameter<edm::InputTag>             ("triggerResults");
  triggerEventTag_   = cfg.getParameter<edm::InputTag>             ("triggerEvent");
  mPFJECUncSrc       = cfg.getParameter<std::string>               ("jecUncSrc");
  mPFJECUncSrcNames  = cfg.getParameter<std::vector<std::string> > ("jecUncSrcNames");
  mJetFlavour        = cfg.getUntrackedParameter<std::string>      ("jetFlavourMatching","");
  mSR                = cfg.getParameter<std::string>("SR");
  mGoodVtxNdof       = cfg.getParameter<double>                    ("goodVtxNdof");
  mGoodVtxZ          = cfg.getParameter<double>                    ("goodVtxZ");
  mMinJJMass         = cfg.getParameter<double>                    ("minJJMass");
  mGenJetsName       = cfg.getUntrackedParameter<edm::InputTag>    ("genjets",edm::InputTag(""));
  mIsMCarlo          = cfg.getUntrackedParameter<bool>             ("isMCarlo",false);
  mFilterBB          = cfg.getUntrackedParameter<bool>             ("FilterBB",false);
  mMinPFPt           = cfg.getParameter<double>                    ("minPFPt");
  mMinJJMass         = cfg.getParameter<double>                    ("minJJMass");
  mMinPFPt           = cfg.getParameter<double>                    ("minPFPt");
  pdfWeightTags_     = cfg.getUntrackedParameter<std::vector<edm::InputTag> > ("PdfWeightTags");
  mMaxY              = cfg.getParameter<double>                    ("maxY");
}

void PDFUncertaintySelector::beginRun(edm::Run const & iRun, edm::EventSetup const& iSetup)
{
  bool changed(true);
  if (hltConfig_.init(iRun,iSetup,processName_,changed)) {
    if (changed) {
      // check if trigger names in (new) config
      cout<<"New trigger menu found !!!"<<endl;
      triggerIndex_.clear(); 
      const unsigned int n(hltConfig_.size());
      for(unsigned itrig=0;itrig<triggerNames_.size();itrig++) {
        triggerIndex_.push_back(hltConfig_.triggerIndex(triggerNames_[itrig]));
        cout<<triggerNames_[itrig]<<" "<<triggerIndex_[itrig]<<" ";  
        if (triggerIndex_[itrig] >= n)
          cout<<"does not exist in the current menu"<<endl;
        else
          cout<<"exists"<<endl;
      }
    }
  } 
  else {
    cout << "ProcessedTreeProducer::analyze:"
         << " config extraction failure with process name "
         << processName_ << endl;
  }
}

void PDFUncertaintySelector::beginJob() {
  isPFJecUncSet_ = false;
  originalEvents_ = 0;
  selectedEvents_ = 0;
  failedEvents_ = 0;
  edm::LogInfo("PDFAnalysis") << "PDF uncertainties will be determined for the following sets: ";
  for (unsigned int i=0; i<pdfWeightTags_.size(); ++i) {
        edm::LogInfo("PDFAnalysis") << "\t" << pdfWeightTags_[i].instance();
        pdfStart_.push_back(-1);
  }
}


void PDFUncertaintySelector::endJob() {
  edm::LogInfo("PDFUncertaintySelector") << "\tIn endJob()";
  edm::LogInfo("PDFUncertaintySelector") << "originalEvents_ = " << originalEvents_;
  edm::LogInfo("PDFUncertaintySelector") << "selectedEvents_ = " << selectedEvents_;
  edm::LogInfo("PDFUncertaintySelector") << "failedEvents_ = " << failedEvents_;

  for (auto& it_cut : cut_results_) {
    std::cout << "[PDFUncertaintySelector] N(cut pass) " << it_cut.first << " = " << it_cut.second << std::endl;
  }
  if (originalEvents_==0) {
        edm::LogInfo("PDFUncertaintySelector") << "NO EVENTS => NO RESULTS";
        return;
  }
  if (selectedEvents_==0) {
        edm::LogInfo("PDFUncertaintySelector") << "NO SELECTED EVENTS => NO RESULTS";
        edm::LogInfo("PDFUncertaintySelector") << "originalEvents_ = " << originalEvents_;
        edm::LogInfo("PDFUncertaintySelector") << "selectedEvents_ = " << selectedEvents_;
        edm::LogInfo("PDFUncertaintySelector") << "failedEvents_ = " << failedEvents_;
        return;
  }

  TH1D *h_acceptance_central = fs->make<TH1D>("AcceptanceCentral","AcceptanceCentral",1,0,1);
  std::vector<TH1D*> h_acceptance_alt;
  for (unsigned int i=0; i<pdfWeightTags_.size(); ++i) {
    TString hname = "Acceptance_";
    hname += pdfWeightTags_[i].instance();
    hname = hname.ReplaceAll(" ", "");
    h_acceptance_alt.push_back(fs->make<TH1D>(hname, hname, 1, 0., 1));
  }

  edm::LogInfo("PDFUncertaintySelector") << "\n>>>> Begin of PDF weight systematics summary >>>>";
  edm::LogInfo("PDFUncertaintySelector") << "Total number of analyzed data: " << originalEvents_ << " [events]";
  double originalAcceptance = double(selectedEvents_)/originalEvents_;
  edm::LogInfo("PDFUncertaintySelector") << "Total number of selected data: " << selectedEvents_ << " [events], corresponding to acceptance: [" << originalAcceptance*100 << " +- " << 100*sqrt( originalAcceptance*(1.-originalAcceptance)/originalEvents_) << "] %";

  h_acceptance_central->SetBinContent(1, originalAcceptance);
  h_acceptance_central->SetBinError(1, sqrt( originalAcceptance*(1.-originalAcceptance)/originalEvents_));

  edm::LogInfo("PDFUncertaintySelector") << "\n>>>>> PDF UNCERTAINTIES ON RATE >>>>>>";
  for (unsigned int i=0; i<pdfWeightTags_.size(); ++i) {
    bool nnpdfFlag = (pdfWeightTags_[i].instance().substr(0,5)=="NNPDF");
    unsigned int nmembers = weightedSelectedEvents_.size()-pdfStart_[i];
    if (i<pdfWeightTags_.size()-1) nmembers = pdfStart_[i+1] - pdfStart_[i];
    unsigned int npairs = (nmembers-1)/2;
    edm::LogInfo("PDFUncertaintySelector") << "RATE Results for PDF set " << pdfWeightTags_[i].instance() << " ---->";

    double events_central = weightedSelectedEvents_[pdfStart_[i]]; 
    edm::LogInfo("PDFUncertaintySelector") << "\tEstimate for central PDF member: " << int(events_central) << " [events]";
    double events2_central = weighted2SelectedEvents_[pdfStart_[i]];
    edm::LogInfo("PDFUncertaintySelector") << "\ti.e. [" << std::setprecision(4) << 100*(events_central-selectedEvents_)/selectedEvents_ << " +- " <<
        100*sqrt(events2_central-events_central+selectedEvents_*(1-originalAcceptance))/selectedEvents_ 
    << "] % relative variation with respect to original PDF";

    if (npairs>0) {
          edm::LogInfo("PDFUncertaintySelector") << "\tNumber of eigenvectors for uncertainty estimation: " << npairs;
      double wplus = 0.;
      double wminus = 0.;
      unsigned int nplus = 0;
      unsigned int nminus = 0;
      for (unsigned int j=0; j<npairs; ++j) {
          double wa = weightedSelectedEvents_[pdfStart_[i]+2*j+1]/events_central-1.;
          double wb = weightedSelectedEvents_[pdfStart_[i]+2*j+2]/events_central-1.; 
          if (nnpdfFlag) {
                if (wa>0.) {
                      wplus += wa*wa; 
                      nplus++;
                } else {
                      //wminus += wa*wa;
                      //nminus++;
                }
                if (wb>0.) {
                      wplus += wb*wb; 
                      nplus++;
                } else {
                      //wminus += wb*wb;
                      //nminus++;
                }
          } else {
                if (wa>wb) {
                      //if (wa<0.) wa = 0.;
                      //if (wb>0.) wb = 0.;
                      if (wa > 0) {
                        wplus += wa*wa;
                      }
                      if (wb > 0) {
                        wminus += wb*wb;
                      }
                } else {
                      //if (wb<0.) wb = 0.;
                      //if (wa>0.) wa = 0.;
                      if (wb > 0) {
                        wplus += wb*wb;
                      }
                      if (wa > 0) {
                        wminus += wa*wa;
                      }
                }
          }
      }
      if (wplus>0) wplus = sqrt(wplus);
      if (wminus>0) wminus = sqrt(wminus);
      if (nnpdfFlag) {
          if (nplus>0) wplus /= sqrt(nplus);
          if (nminus>0) wminus /= sqrt(nminus);
      }
      edm::LogInfo("PDFUncertaintySelector") << "\tRelative uncertainty with respect to central member: +" << std::setprecision(4) << 100.*wplus << " / -" << std::setprecision(4) << 100.*wminus << " [%]";
    } else {
          edm::LogInfo("PDFUncertaintySelector") << "\tNO eigenvectors for uncertainty estimation";
    }
  }

  edm::LogInfo("PDFUncertaintySelector") << "\n>>>>> PDF UNCERTAINTIES ON ACCEPTANCE >>>>>>";
  for (unsigned int i=0; i<pdfWeightTags_.size(); ++i) {
    bool nnpdfFlag = (pdfWeightTags_[i].instance().substr(0,5)=="NNPDF");
    unsigned int nmembers = weightedEvents_.size()-pdfStart_[i];
    if (i<pdfWeightTags_.size()-1) nmembers = pdfStart_[i+1] - pdfStart_[i];
    unsigned int npairs = (nmembers-1)/2;
    edm::LogInfo("PDFUncertaintySelector") << "ACCEPTANCE Results for PDF set " << pdfWeightTags_[i].instance() << " ---->";

    std::cout << "[debug] Unweighted acceptance = " << selectedEvents_ << " / " << originalEvents_  << " = " << (double)selectedEvents_ / originalEvents_ << std::endl;

    double acc_central = 0.;
    double acc2_central = 0.;
    if (weightedEvents_[pdfStart_[i]]>0) {
          acc_central = weightedSelectedEvents_[pdfStart_[i]]/weightedEvents_[pdfStart_[i]]; 
          acc2_central = weighted2SelectedEvents_[pdfStart_[i]]/weightedEvents_[pdfStart_[i]]; 
    }
    double waverage = weightedEvents_[pdfStart_[i]]/originalEvents_;
    double acc_central_err = sqrt((acc2_central/waverage-acc_central*acc_central)/originalEvents_);
    edm::LogInfo("PDFUncertaintySelector") << "\tEstimate for central PDF member acceptance: [" << acc_central*100 << " +- " << 
    100*acc_central_err
    << "] %";
    h_acceptance_alt[i]->SetBinContent(1, acc_central);
    h_acceptance_alt[i]->SetBinError(1, acc_central_err);

    double xi = acc_central-originalAcceptance;
    double deltaxi = (acc2_central-(originalAcceptance+2*xi+xi*xi))/originalEvents_;
    if (deltaxi>0) deltaxi = sqrt(deltaxi); //else deltaxi = 0.;
    edm::LogInfo("PDFUncertaintySelector") << "\ti.e. [" << std::setprecision(4) << 100*xi/originalAcceptance << " +- " << std::setprecision(4) << 100*deltaxi/originalAcceptance << "] % relative variation with respect to the original PDF";

    if (npairs>0) {
          edm::LogInfo("PDFUncertaintySelector") << "\tNumber of eigenvectors for uncertainty estimation: " << npairs;
      std::cout << "[debug] Acceptance with central pdf (variation " << pdfStart_[i] << ") = " << weightedSelectedEvents_[pdfStart_[i]] << " / " << weightedEvents_[pdfStart_[i]] << " = " << (weightedSelectedEvents_[pdfStart_[i]]/weightedEvents_[pdfStart_[i]]) << std::endl;

      double wplus = 0.;
      double wminus = 0.;
      unsigned int nplus = 0;
      unsigned int nminus = 0;
      for (unsigned int j=0; j<npairs; ++j) {
          double wa = 0.;
          if (weightedEvents_[pdfStart_[i]+2*j+1]>0) {
            std::cout << "[debug] Acceptance with pdf variation " << 2*j+1 << " = " << weightedSelectedEvents_[pdfStart_[i]+2*j+1] << " / " << weightedEvents_[pdfStart_[i]+2*j+1] << " = " << (weightedSelectedEvents_[pdfStart_[i]+2*j+1]/weightedEvents_[pdfStart_[i]+2*j+1]) << std::endl;
            wa = (weightedSelectedEvents_[pdfStart_[i]+2*j+1]/weightedEvents_[pdfStart_[i]+2*j+1])/acc_central-1.;
          }
          double wb = 0.;
          if (weightedEvents_[pdfStart_[i]+2*j+2]>0) {
            std::cout << "[debug] Acceptance with pdf variation " << 2*j+2 << " = " << weightedSelectedEvents_[pdfStart_[i]+2*j+2] << " / " << weightedEvents_[pdfStart_[i]+2*j+2] << " = " << (weightedSelectedEvents_[pdfStart_[i]+2*j+2]/weightedEvents_[pdfStart_[i]+2*j+2]) << std::endl;
            wb = (weightedSelectedEvents_[pdfStart_[i]+2*j+2]/weightedEvents_[pdfStart_[i]+2*j+2])/acc_central-1.;
          }
          if (nnpdfFlag) {
                if (wa>0.) {
                      wplus += wa*wa; 
                      nplus++;
                } else {
                      wminus += wa*wa;
                      nminus++;
                }
                if (wb>0.) {
                      wplus += wb*wb; 
                      nplus++;
                } else {
                      wminus += wb*wb;
                      nminus++;
                }
          } else {
                if (wa>wb) {
                      if (wa<0.) wa = 0.;
                      if (wb>0.) wb = 0.;
                      wplus += wa*wa;
                      wminus += wb*wb;
                } else {
                      if (wb<0.) wb = 0.;
                      if (wa>0.) wa = 0.;
                      wplus += wb*wb;
                      wminus += wa*wa;
                }
          }
      }
      if (wplus>0) wplus = sqrt(wplus);
      if (wminus>0) wminus = sqrt(wminus);
      if (nnpdfFlag) {
          if (nplus>0) wplus /= sqrt(nplus);
          if (nminus>0) wminus /= sqrt(nminus);
      }
      edm::LogInfo("PDFUncertaintySelector") << "\tRelative uncertainty with respect to central member: +" << std::setprecision(4) << 100.*wplus << " / -" << std::setprecision(4) << 100.*wminus << " [%]";
    } else {
          edm::LogInfo("PDFUncertaintySelector") << "\tNO eigenvectors for uncertainty estimation";
    }
  }
  std::cout << "[debug] Printing nnpdfVar63Weights_" << std::endl;
  for (auto& it_weight : nnpdfVar63Weights_) {
    std::cout << it_weight << std::endl;
  }
  std::cout << "[debug] Printing large nnpdfVar63Weights_" << std::endl;
  for (auto& it_weight : nnpdfVar63Weights_) {
    if (TMath::Abs(it_weight) > 10.) {
      std::cout << it_weight << std::endl;
    }
  }
  edm::LogInfo("PDFUncertaintySelector") << ">>>> End of PDF weight systematics summary >>>>";

}

void PDFUncertaintySelector::analyze (const Event & event, const EventSetup & iSetup) {
  std::vector<QCDPFJet>      mPFJets;
  std::vector<LorentzVector> mGenJets;
  Handle<reco::BeamSpot> beamSpot;
  event.getByLabel("offlineBeamSpot", beamSpot);
  if (!beamSpot.isValid()) {
    std::cout << "[PDFUncertaintySelector::analyze] WARNING : Skipping event because beamspot is invalid.";
    return;
  }

  //-------------- Trigger Info -----------------------------------
  #ifndef HIDE_TRIGGER
  event.getByLabel(triggerResultsTag_,triggerResultsHandle_);
  if (!triggerResultsHandle_.isValid()) {
    cout << "ProcessedTreeProducer::analyze: Error in getting TriggerResults product from Event! Skipping event." << endl;
    return;
  }
  event.getByLabel(triggerEventTag_,triggerEventHandle_);
  if (!triggerEventHandle_.isValid()) {
    cout << "ProcessedTreeProducer::analyze: Error in getting TriggerEvent product from Event! Skipping event." << endl;
    return;
  }
  std::vector<std::vector<std::pair<std::string, int> > > L1Prescales;
  std::vector<int> HLTPrescales;
  std::vector<int> Fired;
  vector<vector<LorentzVector> > mL1Objects,mHLTObjects;
  // sanity check
  if (triggerResultsHandle_->size() != hltConfig_.size()) {
    std::cerr << "[PDFUncertaintySelector::filter] ERROR : triggerResultsHandle_->size() = " << triggerResultsHandle_->size() << " != hltConfig_.size() = " << hltConfig_.size() << std::endl;
  }
  assert(triggerResultsHandle_->size() == hltConfig_.size());

  //------ loop over all trigger names ---------
  for(unsigned itrig=0; itrig<triggerNames_.size(); itrig++) {
    bool accept(false);
    //int preL1(-1);
    std::vector<std::pair<std::string, int> > preL1;
    int preHLT(-1);
    int tmpFired(-1); 
    vector<LorentzVector> vvL1,vvHLT; 

    if (triggerIndex_[itrig] < hltConfig_.size()) {
      accept = triggerResultsHandle_->accept(triggerIndex_[itrig]);
      //const std::pair<int,int> prescales(hltConfig_.prescaleValues(event,iSetup,triggerNames_[itrig]));
      const std::pair<std::vector<std::pair<std::string,int> >,int> prescales_detailed = hltConfig_.prescaleValuesInDetail(event,iSetup,triggerNames_[itrig]);
      preL1  = prescales_detailed.first;
      preHLT = prescales_detailed.second;
      if (!accept)
        tmpFired = 0;
      else {
        tmpFired = 1;
      }
      //--------- modules on this trigger path--------------
      const vector<string>& moduleLabels(hltConfig_.moduleLabels(triggerIndex_[itrig]));
      const unsigned int moduleIndex(triggerResultsHandle_->index(triggerIndex_[itrig]));
      bool foundL1(false);
      for(unsigned int j=0; j<=moduleIndex; ++j) {
        const string& moduleLabel(moduleLabels[j]);
        const string  moduleType(hltConfig_.moduleType(moduleLabel));

        //--------check whether the module is packed up in TriggerEvent product
        const unsigned int filterIndex(triggerEventHandle_->filterIndex(InputTag(moduleLabel,"",processName_)));
        if (filterIndex<triggerEventHandle_->sizeFilters()) {
          const Vids& VIDS (triggerEventHandle_->filterIds(filterIndex));
          const Keys& KEYS(triggerEventHandle_->filterKeys(filterIndex));
          const size_type nI(VIDS.size());
          const size_type nK(KEYS.size());
          assert(nI==nK);
          const trigger::size_type n(max(nI,nK));
          const TriggerObjectCollection& TOC(triggerEventHandle_->getObjects());
          if (foundL1) {
            for(trigger::size_type i=0; i!=n; ++i) {
              const TriggerObject& TO(TOC[KEYS[i]]);
              TLorentzVector P4;
              P4.SetPtEtaPhiM(TO.pt(),TO.eta(),TO.phi(),TO.mass());
              LorentzVector qcdhltobj(P4.Px(),P4.Py(),P4.Pz(),P4.E());
              vvHLT.push_back(qcdhltobj);
              //cout<<TO.pt()<<endl;
            }
          } else { 
            for(trigger::size_type i=0; i!=n; ++i) {
              const TriggerObject& TO(TOC[KEYS[i]]);
              TLorentzVector P4;
              P4.SetPtEtaPhiM(TO.pt(),TO.eta(),TO.phi(),TO.mass());
              LorentzVector qcdl1obj(P4.Px(),P4.Py(),P4.Pz(),P4.E());
              vvL1.push_back(qcdl1obj);
              //cout<<TO.pt()<<endl;  
            }
            foundL1 = true; 
          }
        }
      }// loop over modules
    }// if the trigger exists in the menu
    //std::cout << "[debug] " << triggerNames_[itrig] << " " << triggerIndex_[itrig] << " " << accept << " " << tmpFired << std::endl;
    Fired.push_back(tmpFired);
    L1Prescales.push_back(preL1);
    HLTPrescales.push_back(preHLT);
    mL1Objects.push_back(vvL1);
    mHLTObjects.push_back(vvHLT);
  }// loop over trigger names  
  #endif

  //-------------- Vertex Info -----------------------------------
  Handle<reco::VertexCollection> recVtxs;
  event.getByLabel(mOfflineVertices,recVtxs);
  //------------- reject events without reco vertices ------------
  int VtxGood(0);
  for(VertexCollection::const_iterator i_vtx = recVtxs->begin(); i_vtx != recVtxs->end(); i_vtx++) {
    if (!(i_vtx->isFake()) && i_vtx->ndof() >= mGoodVtxNdof && fabs(i_vtx->z()) <= mGoodVtxZ) {
      VtxGood++;
    }
  }

  //---------------- Jets ---------------------------------------------
  mPFJEC   = JetCorrector::getJetCorrector(mPFJECservice, iSetup);
  edm::ESHandle<JetCorrectorParametersCollection> PFJetCorParColl;
  if (mPFPayloadName != "" && !isPFJecUncSet_){
    iSetup.get<JetCorrectionsRecord>().get(mPFPayloadName,PFJetCorParColl); 
    JetCorrectorParameters const& PFJetCorPar = (*PFJetCorParColl)["Uncertainty"];
    mPFUnc = new JetCorrectionUncertainty(PFJetCorPar);
    if (mPFJECUncSrc != "") {
      for(unsigned isrc=0;isrc<mPFJECUncSrcNames.size();isrc++) {
        JetCorrectorParameters *par = new JetCorrectorParameters(mPFJECUncSrc,mPFJECUncSrcNames[isrc]); 
        JetCorrectionUncertainty *tmpUnc = new JetCorrectionUncertainty(*par);
        mPFUncSrc.push_back(tmpUnc);
      }
    }
    isPFJecUncSet_ = true;
  }
  Handle<GenJetCollection>  genjets;
  Handle<PFJetCollection>   pfjets;
  Handle<JetFlavourMatchingCollection> jetMC;
  Handle<std::vector<reco::GenParticle> > genParticles;
  // B-tag
  Handle<JetTagCollection> bTag_tchp;
  Handle<JetTagCollection> bTag_tche;
  Handle<JetTagCollection> bTag_csv;
  Handle<JetTagCollection> bTag_ssvhp;
  Handle<JetTagCollection> bTag_ssvhe;
  Handle<JetTagCollection> bTag_jp;
  event.getByLabel("trackCountingHighPurBJetTags", bTag_tchp);
  event.getByLabel("trackCountingHighEffBJetTags", bTag_tche);
  event.getByLabel("combinedSecondaryVertexBJetTags", bTag_csv);
  event.getByLabel("simpleSecondaryVertexHighPurBJetTags", bTag_ssvhp);
  event.getByLabel("simpleSecondaryVertexHighEffBJetTags", bTag_ssvhe);
  event.getByLabel("jetProbabilityBJetTags", bTag_jp);
  //

  event.getByLabel(mPFJetsName,pfjets);
  if (mIsMCarlo) {
    event.getByLabel(mGenJetsName,genjets);
    event.getByLabel(mJetFlavour, jetMC);
    event.getByLabel("genParticles",genParticles); 
    for(GenJetCollection::const_iterator i_gen = genjets->begin(); i_gen != genjets->end(); i_gen++) {
      if (i_gen->pt() > mMinGenPt && fabs(i_gen->y()) < mMaxY) {
        mGenJets.push_back(i_gen->p4());
      }
    }
  }

  // For Z' samples, filter on Z(bb)
  if (mIsMCarlo && mFilterBB) {
    for (reco::GenParticleCollection::const_iterator igen_par = genParticles->begin(); igen_par != genParticles->end(); igen_par++) {
      int pdgid = igen_par->pdgId();
      int status = igen_par->status();
      if (pdgid == 10030 && status == 62) {
        int daughter0_pdgid = igen_par->daughter(0)->pdgId();
        int daughter1_pdgid = igen_par->daughter(1)->pdgId();
        if (fabs(daughter0_pdgid) != 5 || fabs(daughter1_pdgid) != 5) {
          //std::cerr << "[ProcessedTreeProducer::analyze] DEBUG : Skipping event with Z' daughters " << daughter0_pdgid << ", " << daughter1_pdgid << std::endl;
          std::cout << "[PDFUncertaintySelector::analyze] WARNING : Skipping event because we are filtering for Z'(bb)." << std::endl;
          return;
        } else {
          break;
          //std::cerr << "[ProcessedTreeProducer::analyze] DEBUG : Accepting event with Z' daughters " << daughter0_pdgid << ", " << daughter1_pdgid << std::endl;
        }
      }
    }
  }
  //----------- PFJets -------------------------
  for(PFJetCollection::const_iterator i_pfjet = pfjets->begin(); i_pfjet != pfjets->end(); i_pfjet++) {
    QCDPFJet qcdpfjet;
    //int index = i_pfjet-pfjets->begin();
    //edm::RefToBase<reco::Jet> pfjetRef(edm::Ref<PFJetCollection>(pfjets,index));
    double scale = mPFJEC->correction(*i_pfjet,event,iSetup);
    //---- preselection -----------------
    if (fabs(i_pfjet->y()) > mMaxY) continue;
    //---- vertex association -----------
    //---- get the vector of tracks -----
    reco::TrackRefVector vTrks(i_pfjet->getTrackRefs());
    float sumTrkPt(0.0),sumTrkPtBeta(0.0),sumTrkPtBetaStar(0.0),beta(0.0),betaStar(0.0);
    //---- loop over the tracks of the jet ----
    for(reco::TrackRefVector::const_iterator i_trk = vTrks.begin(); i_trk != vTrks.end(); i_trk++) {
      if (recVtxs->size() == 0) break;
      sumTrkPt += (*i_trk)->pt();
      //---- loop over all vertices ----------------------------
      for(unsigned ivtx = 0;ivtx < recVtxs->size();ivtx++) {
        //---- loop over the tracks associated with the vertex ---
        if (!((*recVtxs)[ivtx].isFake()) && (*recVtxs)[ivtx].ndof() >= mGoodVtxNdof && fabs((*recVtxs)[ivtx].z()) <= mGoodVtxZ) {
          for(reco::Vertex::trackRef_iterator i_vtxTrk = (*recVtxs)[ivtx].tracks_begin(); i_vtxTrk != (*recVtxs)[ivtx].tracks_end(); ++i_vtxTrk) {
            //---- match the jet track to the track from the vertex ----
            reco::TrackRef trkRef(i_vtxTrk->castTo<reco::TrackRef>());
            //---- check if the tracks match -------------------------
            if (trkRef == (*i_trk)) {
              if (ivtx == 0) {
                sumTrkPtBeta += (*i_trk)->pt();
              }
              else {
                sumTrkPtBetaStar += (*i_trk)->pt();
              }   
              break;
            }
          }
        } 
      }
    }
    if (sumTrkPt > 0) {
      beta     = sumTrkPtBeta/sumTrkPt;
      betaStar = sumTrkPtBetaStar/sumTrkPt;
    }
    qcdpfjet.setBeta(beta);
    qcdpfjet.setBetaStar(betaStar);
    //---- jec uncertainty --------------
    double unc(0.0);
    vector<float> uncSrc(0);
    if (mPFPayloadName != "") {
      mPFUnc->setJetEta(i_pfjet->eta());
      mPFUnc->setJetPt(scale * i_pfjet->pt());
      unc = mPFUnc->getUncertainty(true);
    }
    if (mPFJECUncSrc != "") {
      for(unsigned isrc=0;isrc<mPFJECUncSrcNames.size();isrc++) {
        mPFUncSrc[isrc]->setJetEta(i_pfjet->eta());
        mPFUncSrc[isrc]->setJetPt(scale * i_pfjet->pt());
        float unc1 = mPFUncSrc[isrc]->getUncertainty(true);
        uncSrc.push_back(unc1);
      }
    }
    qcdpfjet.setP4(i_pfjet->p4());
    qcdpfjet.setCor(scale);
    qcdpfjet.setUnc(unc);
    qcdpfjet.setUncSrc(uncSrc);
    qcdpfjet.setArea(i_pfjet->jetArea());
    //double chf   = i_pfjet->chargedHadronEnergyFraction();
    //double nhf   = (i_pfjet->neutralHadronEnergy() + i_pfjet->HFHadronEnergy())/i_pfjet->energy();
    //double phf   = i_pfjet->photonEnergyFraction();
    //double elf   = i_pfjet->electronEnergyFraction();
    //double muf   = i_pfjet->muonEnergyFraction();
    //double hf_hf = i_pfjet->HFHadronEnergyFraction();
    //double hf_phf= i_pfjet->HFEMEnergyFraction();
    //int hf_hm    = i_pfjet->HFHadronMultiplicity();
    //int hf_phm   = i_pfjet->HFEMMultiplicity();
    //int chm      = i_pfjet->chargedHadronMultiplicity();
    //int nhm      = i_pfjet->neutralHadronMultiplicity();
    //int phm      = i_pfjet->photonMultiplicity();
    //int elm      = i_pfjet->electronMultiplicity();
    //int mum      = i_pfjet->muonMultiplicity();
    //int npr      = i_pfjet->chargedMultiplicity() + i_pfjet->neutralMultiplicity();
    qcdpfjet.setChargedHadronEnergy(i_pfjet->chargedHadronEnergy());
    qcdpfjet.setNeutralHadronEnergy(i_pfjet->neutralHadronEnergy());
    qcdpfjet.setPhotonEnergy(i_pfjet->photonEnergy());
    qcdpfjet.setElectronEnergy(i_pfjet->electronEnergy());
    qcdpfjet.setMuonEnergy(i_pfjet->muonEnergy());
    qcdpfjet.setHFHadronEnergy(i_pfjet->HFHadronEnergy());
    qcdpfjet.setHFEMEnergy(i_pfjet->HFEMEnergy());
    qcdpfjet.setChargedHadronMultiplicity(i_pfjet->chargedHadronMultiplicity());
    qcdpfjet.setNeutralHadronMultiplicity(i_pfjet->neutralHadronMultiplicity());
    qcdpfjet.setPhotonMultiplicity(i_pfjet->photonMultiplicity());
    qcdpfjet.setElectronMultiplicity(i_pfjet->electronMultiplicity());
    qcdpfjet.setMuonMultiplicity(i_pfjet->muonMultiplicity());
    qcdpfjet.setHFHadronMultiplicity(i_pfjet->HFHadronMultiplicity());
    qcdpfjet.setHFEMMultiplicity(i_pfjet->HFEMMultiplicity());
    qcdpfjet.setChargedEmEnergy(i_pfjet->chargedEmEnergy());
    qcdpfjet.setChargedMuEnergy(i_pfjet->chargedMuEnergy());
    qcdpfjet.setNeutralEmEnergy(i_pfjet->neutralEmEnergy());
    qcdpfjet.setChargedMultiplicity(i_pfjet->chargedMultiplicity());
    qcdpfjet.setNeutralMultiplicity(i_pfjet->neutralMultiplicity());
    qcdpfjet.setLooseIDFlag(qcdpfjet.isLooseID());
    qcdpfjet.setTightIDFlag(qcdpfjet.isTightID());

    //
    if(bTag_csv->size() == 0.){
      qcdpfjet.setBtag_tche(-99.);
      qcdpfjet.setBtag_tchp(-99.);
      qcdpfjet.setBtag_csv(-99.);
      qcdpfjet.setBtag_ssvhe(-99.);
      qcdpfjet.setBtag_ssvhp(-99.);
      qcdpfjet.setBtag_jp(-99.);
    }
    else{
    JetTagCollection::const_iterator i_btag_matched_tchp;
    JetTagCollection::const_iterator i_btag_matched_tche;
    JetTagCollection::const_iterator i_btag_matched_csv;
    JetTagCollection::const_iterator i_btag_matched_ssvhe;
    JetTagCollection::const_iterator i_btag_matched_ssvhp;
    JetTagCollection::const_iterator i_btag_matched_jp;
    float rmin_btag_tchp(999), rmin_btag_tche(999), rmin_btag_csv(999), rmin_btag_ssvhe(999), rmin_btag_ssvhp(999), rmin_btag_jp(999);
    for (JetTagCollection::const_iterator i_btag = bTag_tchp->begin(); i_btag != bTag_tchp->end(); i_btag++){
        double deltaR = reco::deltaR(i_pfjet->eta(), i_pfjet->phi(), (*i_btag).first->eta(), (*i_btag).first->phi());
        if (deltaR < rmin_btag_tchp) {
          rmin_btag_tchp = deltaR;
          i_btag_matched_tchp = i_btag;
        }
     }
     for (JetTagCollection::const_iterator i_btag = bTag_tche->begin(); i_btag != bTag_tche->end(); i_btag++){
        double deltaR = reco::deltaR(i_pfjet->eta(), i_pfjet->phi(), (*i_btag).first->eta(), (*i_btag).first->phi());
        if (deltaR < rmin_btag_tche) {
          rmin_btag_tche = deltaR;
          i_btag_matched_tche = i_btag;
        }
     }
    for (JetTagCollection::const_iterator i_btag = bTag_csv->begin(); i_btag != bTag_csv->end(); i_btag++){
        double deltaR = reco::deltaR(i_pfjet->eta(), i_pfjet->phi(), (*i_btag).first->eta(), (*i_btag).first->phi());
        if (deltaR < rmin_btag_csv) {
          rmin_btag_csv = deltaR;
          i_btag_matched_csv = i_btag;
        }
     }
     for (JetTagCollection::const_iterator i_btag = bTag_ssvhe->begin(); i_btag != bTag_ssvhe->end(); i_btag++){
        double deltaR = reco::deltaR(i_pfjet->eta(), i_pfjet->phi(), (*i_btag).first->eta(), (*i_btag).first->phi());
        if (deltaR < rmin_btag_ssvhe) {
          rmin_btag_ssvhe = deltaR;
          i_btag_matched_ssvhe = i_btag;
        }
     }
     for (JetTagCollection::const_iterator i_btag = bTag_ssvhp->begin(); i_btag != bTag_ssvhp->end(); i_btag++){
        double deltaR = reco::deltaR(i_pfjet->eta(), i_pfjet->phi(), (*i_btag).first->eta(), (*i_btag).first->phi());
        if (deltaR < rmin_btag_ssvhp) {
          rmin_btag_ssvhp = deltaR;
          i_btag_matched_ssvhp = i_btag;
        }
     }
     for (JetTagCollection::const_iterator i_btag = bTag_jp->begin(); i_btag != bTag_jp->end(); i_btag++){
        double deltaR = reco::deltaR(i_pfjet->eta(), i_pfjet->phi(), (*i_btag).first->eta(), (*i_btag).first->phi());
        if (deltaR < rmin_btag_jp) {
          rmin_btag_jp = deltaR;
          i_btag_matched_jp = i_btag;
        }
     }

     double btag_tche  = (*i_btag_matched_tche).second;
     double btag_tchp  = (*i_btag_matched_tchp).second;
     double btag_csv   = (*i_btag_matched_csv).second;
     double btag_ssvhe = (*i_btag_matched_ssvhe).second;
     double btag_ssvhp = (*i_btag_matched_ssvhp).second;
     double btag_jp    = (*i_btag_matched_jp).second; 

     qcdpfjet.setBtag_tche(btag_tche);
     qcdpfjet.setBtag_tchp(btag_tchp);
     qcdpfjet.setBtag_csv(btag_csv);
     qcdpfjet.setBtag_ssvhe(btag_ssvhe);
     qcdpfjet.setBtag_ssvhp(btag_ssvhp);
     qcdpfjet.setBtag_jp(btag_jp);
     }
  //
    if (qcdpfjet.ptCor() >= mMinPFPt)
      mPFJets.push_back(qcdpfjet);
  }
  sort(mPFJets.begin(),mPFJets.end(),sort_pfjets);

  // Selection
  // - Jet pT (160/120 or 80/70)
  // - Jet eta (<2.2 or <1.7)
  // - b-tagging (2 CSVM)
  // - DeltaEta (<1.3)
  bool pass = false;
  if (mPFJets.size() < 2) {
    std::cout << "[debug] Event fail because PFJets.size < 2" << std::endl;
    pass = false;
  } else {
    std::map<TString, bool> cut_results;
    if (mSR == "LowMass") {
      cut_results["pt"] = (mPFJets[0].pt() > 80. && mPFJets[1].pt() > 70.);
      cut_results["eta"] = (TMath::Abs(mPFJets[0].eta()) < 1.7 && TMath::Abs(mPFJets[1].eta()) < 1.7);
    } else if (mSR == "HighMass") {
      cut_results["pt"] = (mPFJets[0].pt() > 160. && mPFJets[1].pt() > 120.);
      cut_results["eta"] = (TMath::Abs(mPFJets[0].eta()) < 2.2 && TMath::Abs(mPFJets[1].eta()) < 2.2);
    } else {
      std::cerr << "ERROR : mSR must be LowMass or HighMass. Found " << mSR << std::endl;
      exit(1);
    }
    cut_results["btag"] = (mPFJets[0].btag_csv() > 0.679 && mPFJets[1].btag_csv() > 0.679);
    cut_results["deltaeta"] = (TMath::Abs(mPFJets[0].eta() - mPFJets[1].eta()) < 1.3);
    pass = cut_results["pt"] && cut_results["eta"] && cut_results["btag"] && cut_results["deltaeta"];

    // Save cut results
    for (auto& it_cut : cut_results) {
      cut_results_[it_cut.first.Data()] += it_cut.second;
    }
    //if (!pass) {
    //    std::cout << "[debug] Event fails. Cuts:" << std::endl;
    //    for (auto& it_cut : cut_results) {
    //      std::cout << "\t" << it_cut.first << " => " << it_cut.second << std::endl;;
    //    }
    //} else {
    //    std::cout << "[debug] Event passes." << std::endl;
    //}
  }

  // Do weight computations
  edm::Handle<std::vector<double> > weightHandle;
  for (unsigned int i=0; i<pdfWeightTags_.size(); ++i) {
        if (!event.getByLabel(pdfWeightTags_[i], weightHandle)) {
              std::cout << "WARNING: some weights not found! " << pdfWeightTags_[i] << std::endl;;
              edm::LogError("PDFUncertaintySelector") << ">>> WARNING: some weights not found! " << pdfWeightTags_[i];
              edm::LogError("PDFUncertaintySelector") << ">>> But maybe OK, if you are prefiltering!";
              edm::LogError("PDFUncertaintySelector") << ">>> If things are OK, this warning should disappear after a while!";
              return;
              //return false;
        }
  }

  originalEvents_++;
  if (pass) {
    //std::cout << "[debug] Event pass" << std::endl;
    ++selectedEvents_;
  } else {
    //std::cout << "[debug] Event fail" << std::endl;
    ++failedEvents_;
  }
  for (unsigned int i=0; i<pdfWeightTags_.size(); ++i) {
    if (!event.getByLabel(pdfWeightTags_[i], weightHandle)) return;//return false;
    std::vector<double> weights = (*weightHandle);
    unsigned int nmembers = weights.size();
    // Skip events with ginormous weights
    bool bad_weight_event = false;
    for (unsigned int j=0; j<nmembers; ++j) {
      if (TMath::Abs(weights[j]) > 20.) {
        bad_weight_event = true;
        std::cout << "[PDFUncertaintySelector::analyze] WARNING : Skippingg this event for PDF set " << pdfWeightTags_[i].instance() << " due to very large weight: " << weights[j] << std::endl;
        break;
      }
    }
    if (bad_weight_event) {
      continue;
    }
    // Set up arrays the first time weights are read
    if (pdfStart_[i]<0) {
      pdfStart_[i] = weightedEvents_.size();
      for (unsigned int j=0; j<nmembers; ++j) {
          weightedEvents_.push_back(0.);
          weightedSelectedEvents_.push_back(0.);
          weighted2SelectedEvents_.push_back(0.);
      }
    }

    for (unsigned int j=0; j<nmembers; ++j) {
      //std::cout << "[debug] Weight for " << pdfWeightTags_[i] << " / member " << j << " = " << weights[j] << std::endl;
      if (TMath::Abs(weights[j] - 1.) > 0.5) {
        std::cout << "[PDFUncertaintySelector::analyze] WARNING : Large weight found at position " << j << " : " << weights[j] << std::endl;
      }

      if (pdfWeightTags_[i].instance().substr(0,5)=="NNPDF" && j==63) {
        nnpdfVar63Weights_.push_back(weights[j]);
      }
      weightedEvents_[pdfStart_[i]+j] += weights[j];
      if (pass) {
        weightedSelectedEvents_[pdfStart_[i]+j] += weights[j];
        weighted2SelectedEvents_[pdfStart_[i]+j] += weights[j]*weights[j];
      }
    }

    /*
    printf("\n>>>>>>>>> Run %8d Event %d, members %3d PDF set %s : Weights >>>> \n", ev.id().run(), ev.id().event(), nmembers, pdfWeightTags_[i].instance().data());
    for (unsigned int i=0; i<nmembers; i+=5) {
    for (unsigned int j=0; ((j<5)&&(i+j<nmembers)); ++j) {
    printf(" %2d: %7.4f", i+j, weights[i+j]);
    }
    safe_printf("\n");
    }
    */
  }
}
#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(PDFUncertaintySelector);