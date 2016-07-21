#include <iostream>
#include <sstream>
#include <istream>
#include <fstream>
#include <iomanip>
#include <string>
#include <cmath>
#include <functional>
#include "TTree.h"
#include <vector>
#include <cassert>
#include <TLorentzVector.h>

#include "CMSDIJET/QCDAnalysis/plugins/ProcessedTreeProducer.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Common/interface/TriggerResultsByName.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/JetReco/interface/Jet.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/JetReco/interface/CaloJet.h"
#include "DataFormats/JetReco/interface/CaloJetCollection.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"
#include "DataFormats/JetReco/interface/JetExtendedAssociation.h"
#include "DataFormats/JetReco/interface/JetID.h"
#include "DataFormats/METReco/interface/PFMET.h"
#include "DataFormats/METReco/interface/PFMETCollection.h"
#include "DataFormats/METReco/interface/CaloMET.h"
#include "DataFormats/METReco/interface/CaloMETCollection.h"
#include "DataFormats/METReco/interface/HcalNoiseSummary.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

#include "DataFormats/BTauReco/interface/JetTag.h"
#include "SimDataFormats/JetMatching/interface/JetFlavour.h"
#include "SimDataFormats/JetMatching/interface/JetFlavourMatching.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"

ProcessedTreeProducer::ProcessedTreeProducer(edm::ParameterSet const& cfg) 
{
	mPFJECservice      = cfg.getParameter<std::string>               ("pfjecService");
	mCaloJECservice    = cfg.getParameter<std::string>               ("calojecService");
	mPFPayloadName     = cfg.getParameter<std::string>               ("PFPayloadName");
	mCaloPayloadName   = cfg.getParameter<std::string>               ("CaloPayloadName");
	mGoodVtxNdof       = cfg.getParameter<double>                    ("goodVtxNdof");
	mGoodVtxZ          = cfg.getParameter<double>                    ("goodVtxZ");
	mMinCaloPt         = cfg.getParameter<double>                    ("minCaloPt");
	mMinPFPt           = cfg.getParameter<double>                    ("minPFPt");
	mMinPFFatPt        = cfg.getParameter<double>                    ("minPFFatPt");
	mMaxPFFatEta       = cfg.getParameter<double>                    ("maxPFFatEta");
	mMinJJMass         = cfg.getParameter<double>                    ("minJJMass");
	mMaxY              = cfg.getParameter<double>                    ("maxY");
	mMinNCaloJets      = cfg.getParameter<int>                       ("minNCaloJets");
	mMinNPFJets        = cfg.getParameter<int>                       ("minNPFJets");
	mCaloJetID         = cfg.getParameter<edm::InputTag>             ("calojetID");
	mCaloJetExtender   = cfg.getParameter<edm::InputTag>             ("calojetExtender");
	mOfflineVertices   = cfg.getParameter<edm::InputTag>             ("offlineVertices");
	mPFJetsName        = cfg.getParameter<edm::InputTag>             ("pfjets");
	mCaloJetsName      = cfg.getParameter<edm::InputTag>             ("calojets");
	mSrcCaloRho        = cfg.getParameter<edm::InputTag>             ("srcCaloRho");
	mSrcPFRho          = cfg.getParameter<edm::InputTag>             ("srcPFRho");
	mSrcPU             = cfg.getUntrackedParameter<edm::InputTag>    ("srcPU",edm::InputTag("addPileupInfo"));
	mGenJetsName       = cfg.getUntrackedParameter<edm::InputTag>    ("genjets",edm::InputTag(""));
	mPrintTriggerMenu  = cfg.getUntrackedParameter<bool>             ("printTriggerMenu",false);
	mIsMCarlo          = cfg.getUntrackedParameter<bool>             ("isMCarlo",false);
	mUseGenInfo        = cfg.getUntrackedParameter<bool>             ("useGenInfo",false);
	mMinGenPt          = cfg.getUntrackedParameter<double>           ("minGenPt",30);
	processName_       = cfg.getParameter<std::string>               ("processName");
	triggerNames_      = cfg.getParameter<std::vector<std::string> > ("triggerName");
	triggerResultsTag_ = cfg.getParameter<edm::InputTag>             ("triggerResults");
	triggerEventTag_   = cfg.getParameter<edm::InputTag>             ("triggerEvent");
	mPFJECUncSrc       = cfg.getParameter<std::string>               ("jecUncSrc");
	mPFJECUncSrcNames  = cfg.getParameter<std::vector<std::string> > ("jecUncSrcNames");
	mJetFlavour        = cfg.getUntrackedParameter<std::string>      ("jetFlavourMatching","");
	mXsec              = cfg.getUntrackedParameter<double>           ("Xsec",0.);

}
//////////////////////////////////////////////////////////////////////////////////////////
void ProcessedTreeProducer::beginJob() 
{
	mTree = fs->make<TTree>("ProcessedTree","ProcessedTree");
	mEvent = new QCDEvent();
	mTree->Branch("events","QCDEvent",&mEvent);
	mTriggerNamesHisto = fs->make<TH1F>("TriggerNames","TriggerNames",1,0,1);
	mTriggerNamesHisto->SetBit(TH1::kCanRebin);
	for(unsigned i=0;i<triggerNames_.size();i++)
		mTriggerNamesHisto->Fill(triggerNames_[i].c_str(),1);
	mTriggerPassHisto = fs->make<TH1F>("TriggerPass","TriggerPass",1,0,1);
	mTriggerPassHisto->SetBit(TH1::kCanRebin);
	mEventsProcessedHisto = fs->make<TH1F>("EventsProcessed", "EventsProcessed", 1, 0.5, 1.5);
	isPFJecUncSet_ = false;
	isCaloJecUncSet_ = false;
	debug_counter = 0;
} 
//////////////////////////////////////////////////////////////////////////////////////////
void ProcessedTreeProducer::endJob() 
{
}
//////////////////////////////////////////////////////////////////////////////////////////
void ProcessedTreeProducer::beginRun(edm::Run const & iRun, edm::EventSetup const& iSetup)
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
			cout << "Available TriggerNames are: " << endl;
			if (mPrintTriggerMenu)
				hltConfig_.dump("Triggers");
		}
	} 
	else {
		cout << "ProcessedTreeProducer::analyze:"
				 << " config extraction failure with process name "
				 << processName_ << endl;
	}
}
//////////////////////////////////////////////////////////////////////////////////////////
void ProcessedTreeProducer::analyze(edm::Event const& event, edm::EventSetup const& iSetup) 
{ 
	mEventsProcessedHisto->Fill(1);
	++debug_counter;
	vector<QCDCaloJet>    mCaloJets;
	vector<QCDPFJet>      mPFJets;
	vector<QCDJet>        mPFFatJets;
	vector<QCDPFJet>      tmpPFJets;
	vector<LorentzVector> mGenJets;
	QCDEventHdr mEvtHdr; 
	QCDMET mCaloMet,mPFMet;
	//-------------- Basic Event Info ------------------------------
	mEvtHdr.setRun(event.id().run());
	mEvtHdr.setEvt(event.id().event());
	mEvtHdr.setLumi(event.luminosityBlock());
	mEvtHdr.setBunch(event.bunchCrossing());
	//-------------- Beam Spot --------------------------------------
	Handle<reco::BeamSpot> beamSpot;
	event.getByLabel("offlineBeamSpot", beamSpot);
	if (beamSpot.isValid())
		mEvtHdr.setBS(beamSpot->x0(),beamSpot->y0(),beamSpot->z0());
	else
		mEvtHdr.setBS(-999,-999,-999);

	//-------------- HCAL Noise Summary -----------------------------
	Handle<bool> noiseSummary; 	 
	if (!mIsMCarlo) {
		event.getByLabel(edm::InputTag("HBHENoiseFilterResultProducer","HBHENoiseFilterResult"), noiseSummary);         
		mEvtHdr.setHCALNoise(*noiseSummary);
	}
	else
		mEvtHdr.setHCALNoise(true);
	//-------------- Trigger Info -----------------------------------
	event.getByLabel(triggerResultsTag_,triggerResultsHandle_);
	if (!triggerResultsHandle_.isValid()) {
		cout << "ProcessedTreeProducer::analyze: Error in getting TriggerResults product from Event!" << endl;
		return;
	}
	event.getByLabel(triggerEventTag_,triggerEventHandle_);
	if (!triggerEventHandle_.isValid()) {
		cout << "ProcessedTreeProducer::analyze: Error in getting TriggerEvent product from Event!" << endl;
		return;
	}
	std::vector<std::vector<std::pair<std::string, int> > > L1Prescales;
	std::vector<int> HLTPrescales;
	std::vector<int> Fired;
	vector<vector<LorentzVector> > mL1Objects,mHLTObjects;
	// sanity check
	assert(triggerResultsHandle_->size() == hltConfig_.size());

	// Debug: print all triggers
	//if (debug_counter++ < 10) {
	//	for (unsigned int i = 0; i < hltConfig_.size(); ++i) {
	//		bool this_accept = triggerResultsHandle_->accept(i);
	//		const std::pair<int,int> this_prescales(hltConfig_.prescaleValues(event,iSetup,hltConfig_.triggerName(i)));
	//		std::cout << "Trigger index " << i << " / name " << hltConfig_.triggerName(i) << ": accept = " << (this_accept ? "true" : "false") << ", prescales = " << this_prescales.first << " * " << this_prescales.second << std::endl;
	//	}
	//}


	//------ loop over all trigger names ---------
	if (debug_counter < 10) {
		std::cout << "[debug] triggerNames_.size() = " << triggerNames_.size() << std::endl;
	}
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
				mTriggerPassHisto->Fill(triggerNames_[itrig].c_str(),1);
				tmpFired = 1;
			}
			//--------- modules on this trigger path--------------
			const vector<string>& moduleLabels(hltConfig_.moduleLabels(triggerIndex_[itrig]));
			const unsigned int moduleIndex(triggerResultsHandle_->index(triggerIndex_[itrig]));
			bool foundL1(false);
			for(unsigned int j=0; j<=moduleIndex; ++j) {
				const string& moduleLabel(moduleLabels[j]);
				const string  moduleType(hltConfig_.moduleType(moduleLabel));
				if (debug_counter < 10) {
					std::cout << "[debug] moduleLabel = " << moduleLabel << std::endl;
					std::cout << "[debug] moduleType = " << moduleType << std::endl;
				}
				//--------check whether the module is packed up in TriggerEvent product
				const unsigned int filterIndex(triggerEventHandle_->filterIndex(InputTag(moduleLabel,"",processName_)));
				if (filterIndex<triggerEventHandle_->sizeFilters()) {
					const Vids& VIDS (triggerEventHandle_->filterIds(filterIndex));
					const Keys& KEYS(triggerEventHandle_->filterKeys(filterIndex));
					const size_type nI(VIDS.size());
					const size_type nK(KEYS.size());
					assert(nI==nK);
					const size_type n(max(nI,nK));
					const TriggerObjectCollection& TOC(triggerEventHandle_->getObjects());
					if (foundL1) {
						for(size_type i=0; i!=n; ++i) {
							const TriggerObject& TO(TOC[KEYS[i]]);
							TLorentzVector P4;
							P4.SetPtEtaPhiM(TO.pt(),TO.eta(),TO.phi(),TO.mass());
							LorentzVector qcdhltobj(P4.Px(),P4.Py(),P4.Pz(),P4.E());
							vvHLT.push_back(qcdhltobj);
							//cout<<TO.pt()<<endl;
						}
					} else { 
						for(size_type i=0; i!=n; ++i) {
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
	mEvent->setTrigDecision(Fired);
	if (debug_counter < 10) {
		std::cout << "[ProcessedTreeProducer] DEBUG : Set trigger decision with Fired.size() = " << Fired.size() << std::endl;
		std::cout << "[ProcessedTreeProducer] DEBUG : Printing L1 prescales:" << std::endl;
		for (unsigned int i_trig = 0; i_trig < L1Prescales.size(); ++i_trig) {
			for (auto& it_trig : L1Prescales[i_trig]) {
				std::cout << "\t" << it_trig.first << " => " << it_trig.second << std::endl;
			}
		}
		std::cout << "[ProcessedTreeProducer] DEBUG : Done." << std::endl;
	}
	mEvent->setPrescales(L1Prescales,HLTPrescales);
	mEvent->setL1Obj(mL1Objects);
	mEvent->setHLTObj(mHLTObjects);
	//-------------- Vertex Info -----------------------------------
	Handle<reco::VertexCollection> recVtxs;
	event.getByLabel(mOfflineVertices,recVtxs);
	//------------- reject events without reco vertices ------------
	int VtxGood(0);
	bool isPVgood(false);
	float PVx(0),PVy(0),PVz(0),PVndof(0);
	for(VertexCollection::const_iterator i_vtx = recVtxs->begin(); i_vtx != recVtxs->end(); i_vtx++) {
		int index = i_vtx-recVtxs->begin();
		if (index == 0) {
			PVx    = i_vtx->x();
			PVy    = i_vtx->y();
			PVz    = i_vtx->z();
			PVndof = i_vtx->ndof();
		}
		if (!(i_vtx->isFake()) && i_vtx->ndof() >= mGoodVtxNdof && fabs(i_vtx->z()) <= mGoodVtxZ) {
			if (index == 0) {
				isPVgood = true;
			}
			VtxGood++;
		}
	}
	mEvtHdr.setVertices(recVtxs->size(),VtxGood);
	mEvtHdr.setPV(isPVgood,PVndof,PVx,PVy,PVz);
	//-------------- Rho ------------------------------------------------
	Handle<double> rhoCalo;
	event.getByLabel(mSrcCaloRho,rhoCalo);
	Handle<double> rhoPF;
	event.getByLabel(mSrcPFRho,rhoPF);
	mEvtHdr.setRho(*rhoCalo,*rhoPF);
	//-------------- Generator Info -------------------------------------
	Handle<GenEventInfoProduct> hEventInfo;
	//-------------- Simulated PU Info ----------------------------------

	Handle<std::vector<PileupSummaryInfo> > PupInfo;
	if (mIsMCarlo && mUseGenInfo) { 
		event.getByLabel("generator", hEventInfo);
		}
		if (hEventInfo->hasBinningValues()) {
			mEvtHdr.setPthat(hEventInfo->binningValues()[0]);
		} else {
			mEvtHdr.setPthat(-1.);
		}
		mEvtHdr.setWeight(hEventInfo->weight());
		event.getByLabel(mSrcPU, PupInfo);
		std::vector<PileupSummaryInfo>::const_iterator PUI;
		int nbx = PupInfo->size();
		int ootpuEarly(0),ootpuLate(0),intpu(0);
		float Tnpv = -1.; // new variable for computing pileup weight factor for the event
		for(PUI = PupInfo->begin(); PUI != PupInfo->end(); ++PUI) {
			if (PUI->getBunchCrossing() < 0)
				ootpuEarly += PUI->getPU_NumInteractions();
			else if (PUI->getBunchCrossing() > 0)
				ootpuLate += PUI->getPU_NumInteractions();
			else {
				intpu += PUI->getPU_NumInteractions(); 
				Tnpv = PUI->getTrueNumInteractions();
			 } 
		} 
		 
		mEvtHdr.setPU(nbx,ootpuEarly,ootpuLate,intpu);
		mEvtHdr.setTrPu(Tnpv);
		mEvtHdr.setXsec(mXsec);
	} 
	else {
		mEvtHdr.setPthat(0);
		mEvtHdr.setWeight(0); 
		mEvtHdr.setPU(0,0,0,0);
		mEvtHdr.setTrPu(0);
		mEvtHdr.setXsec(0.);
	}

	//---------------- Jets ---------------------------------------------
	mPFJEC   = JetCorrector::getJetCorrector(mPFJECservice,iSetup);
	mCALOJEC = JetCorrector::getJetCorrector(mCaloJECservice,iSetup);
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
	edm::ESHandle<JetCorrectorParametersCollection> CaloJetCorParColl;
	if (mCaloPayloadName != "" && !isCaloJecUncSet_){
		iSetup.get<JetCorrectionsRecord>().get(mCaloPayloadName,CaloJetCorParColl);    
		JetCorrectorParameters const& CaloJetCorPar = (*CaloJetCorParColl)["Uncertainty"];
		mCALOUnc = new JetCorrectionUncertainty(CaloJetCorPar);
		isCaloJecUncSet_ = true;
	}
	Handle<GenJetCollection>  genjets;
	Handle<PFJetCollection>   pfjets;
	Handle<CaloJetCollection> calojets;
	Handle<JetExtendedAssociation::Container> calojetExtender;
	Handle<ValueMap<reco::JetID> > calojetID;
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
	event.getByLabel(mCaloJetsName,calojets);
	event.getByLabel(mCaloJetExtender,calojetExtender);
	event.getByLabel(mCaloJetID,calojetID);
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
	int njets(0);
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

		if (mIsMCarlo) {
			GenJetCollection::const_iterator i_matched;
			JetFlavourMatchingCollection::const_iterator i_flavour_matched;
			float rmin(999);
			float rmin_flavour(999);
			for(GenJetCollection::const_iterator i_gen = genjets->begin(); i_gen != genjets->end(); i_gen++) {
				double deltaR = reco::deltaR(*i_pfjet,*i_gen);
				if (deltaR < rmin) {
					rmin = deltaR;
					i_matched = i_gen;
				}
			}
			
			//
			for (reco::JetFlavourMatchingCollection::const_iterator iter = jetMC->begin(); iter != jetMC->end(); iter++) {
				double deltaR = reco::deltaR(i_pfjet->eta(), i_pfjet->phi(), iter->second.getLorentzVector().Eta(), iter->second.getLorentzVector().Phi());
				 if (deltaR < rmin_flavour) {
					rmin_flavour = deltaR;
					i_flavour_matched = iter;
				}
		 }
			float bquark_3 = 0.0;
			float bquark_2 = 0.0; 
			float parton_id = 0.0;
			for (reco::GenParticleCollection::const_iterator igen_par = genParticles->begin(); igen_par != genParticles->end(); igen_par++) {
				double deltaR2 = reco::deltaR(*i_pfjet,*igen_par);       
				int pdgid = igen_par->pdgId();
				int status = igen_par->status();
				 if(deltaR2 < 0.35 && status == 3 && abs(pdgid) == 5) bquark_3 = 1.0;
				 if(deltaR2 < 0.35 && status == 2 && abs(pdgid) == 5) bquark_2 = 1.0;
				}
 
				if (fabs((*genParticles)[6].pdgId()) >= 32) parton_id = (*genParticles)[7+njets].pdgId();

	else parton_id = (*genParticles)[6+njets].pdgId();
//        cout<<"njets: "<<njets<<"\t parton: "<<parton_id<<endl;
				njets = njets + 1;
		 //
			if (genjets->size() == 0) {
				LorentzVector tmpP4(0.0,0.0,0.0,0.0);
				qcdpfjet.setGen(tmpP4,0);
				qcdpfjet.setFlavor(-99.0);
				qcdpfjet.setBstatus(-99.0, -99.0);
				qcdpfjet.setPartonId(0.0);
			}
			else{
				qcdpfjet.setGen(i_matched->p4(),rmin);
				qcdpfjet.setFlavor(i_flavour_matched->second.getFlavour());
				qcdpfjet.setBstatus(bquark_3, bquark_2);
	qcdpfjet.setPartonId(parton_id);
			}
		}
		 else {
			LorentzVector tmpP4(0.0,0.0,0.0,0.0); 
			qcdpfjet.setGen(tmpP4,0);
			qcdpfjet.setFlavor(-99.0);
			qcdpfjet.setBstatus(-99.0, -99.0);
			qcdpfjet.setPartonId(0.);
		}
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
		if (qcdpfjet.ptCor() >= mMinPFFatPt && fabs(qcdpfjet.eta()) < mMaxPFFatEta && qcdpfjet.isLooseID())
			tmpPFJets.push_back(qcdpfjet);
	}
	//----------- PFFatJets ----------------------
	sort(tmpPFJets.begin(),tmpPFJets.end(),sort_pfjets);
	if (tmpPFJets.size()>1) {
		LorentzVector lead[2], fat[2]; 
		float sumPt[2],sumPtUnc[2];
		for(unsigned i = 0; i<2; i++) {
			lead[i]     = tmpPFJets[i].p4()*tmpPFJets[i].cor();
			fat[i]      = tmpPFJets[i].p4()*tmpPFJets[i].cor();
			sumPt[i]    = tmpPFJets[i].ptCor();
			sumPtUnc[i] = tmpPFJets[i].ptCor() * tmpPFJets[i].unc();
		}
		double rmax = 1.1;
		for(unsigned i = 2; i<tmpPFJets.size(); i++) {
			LorentzVector cand = tmpPFJets[i].p4();
			double dR1 = deltaR(lead[0],cand);
			double dR2 = deltaR(lead[1],cand);
			int index(-1);
			if (dR1 < dR2 && dR1 < rmax) 
				index = 0;
			if (dR1 > dR2 && dR2 < rmax)
				index = 1;
			if (index > -1) {
				fat[index]      += cand * tmpPFJets[i].cor();
				sumPt[index]    += tmpPFJets[i].ptCor();
				sumPtUnc[index] += tmpPFJets[i].ptCor()*tmpPFJets[i].unc();
			} 
		}
		QCDJet fatJet[2];
		vector<float> uncSrc(0);
		for(unsigned i = 0; i<2; i++) { 
			fatJet[i].setP4(fat[i]);
			fatJet[i].setLooseIDFlag(tmpPFJets[i].isLooseID());
			fatJet[i].setTightIDFlag(tmpPFJets[i].isTightID());
			fatJet[i].setCor(1.0);
			fatJet[i].setArea(0.0);
			fatJet[i].setUncSrc(uncSrc); 
			//
			fatJet[i].setBtag_tche(tmpPFJets[i].btag_tche());
			fatJet[i].setBtag_tchp(tmpPFJets[i].btag_tchp());
			fatJet[i].setBtag_csv(tmpPFJets[i].btag_csv()); 
			fatJet[i].setBtag_ssvhe(tmpPFJets[i].btag_ssvhe()); 
			fatJet[i].setBtag_ssvhp(tmpPFJets[i].btag_ssvhp());
			fatJet[i].setBtag_jp(tmpPFJets[i].btag_jp());
			fatJet[i].setFlavor(tmpPFJets[i].flavor());
			fatJet[i].setBstatus(tmpPFJets[i].bstatus3(), tmpPFJets[i].bstatus2());
			fatJet[i].setPartonId(tmpPFJets[i].PartonId());
			//
			if (sumPt[i] > 0)
				fatJet[i].setUnc(sumPtUnc[i]/sumPt[i]);
			else
				fatJet[i].setUnc(0.0); 
			fatJet[i].setGen(tmpPFJets[i].genp4(),tmpPFJets[i].genR());
		}
		if (fatJet[0].pt()>fatJet[1].pt()) {
			mPFFatJets.push_back(fatJet[0]); 
			mPFFatJets.push_back(fatJet[1]);
		}
		else {
			mPFFatJets.push_back(fatJet[1]); 
			mPFFatJets.push_back(fatJet[0]);
		}
	}
	//----------- CaloJets -----------------------
	for(CaloJetCollection::const_iterator i_calojet = calojets->begin(); i_calojet != calojets->end(); i_calojet++) {
		int index = i_calojet-calojets->begin();
		edm::RefToBase<reco::Jet> calojetRef(edm::Ref<CaloJetCollection>(calojets,index));
		double scale = mCALOJEC->correction(*i_calojet,event,iSetup);
		//---- preselection -----------------
		if (fabs(i_calojet->y()) > mMaxY) continue;
		double unc(0.0);
		vector<float> uncSrc(0);
		if (mCaloPayloadName != "") {
			mCALOUnc->setJetEta(i_calojet->eta());
			mCALOUnc->setJetPt(scale * i_calojet->pt());
			unc = mCALOUnc->getUncertainty(true);
		} 
		QCDCaloJet qcdcalojet;
		qcdcalojet.setP4(i_calojet->p4());
		qcdcalojet.setCor(scale);
		qcdcalojet.setUnc(unc);
		qcdcalojet.setUncSrc(uncSrc);
		qcdcalojet.setArea(i_calojet->jetArea());
		double emf    = i_calojet->emEnergyFraction();
		int n90hits   = int((*calojetID)[calojetRef].n90Hits);
		double fHPD   = (*calojetID)[calojetRef].fHPD;
		double fRBX   = (*calojetID)[calojetRef].fRBX;
		int nTrkVtx   = JetExtendedAssociation::tracksAtVertexNumber(*calojetExtender,*i_calojet);
		int nTrkCalo  = JetExtendedAssociation::tracksAtCaloNumber(*calojetExtender,*i_calojet);		   
		bool looseID  = ((emf>0.01 || fabs(i_calojet->eta())>2.6) && (n90hits>1) && (fHPD<0.98));
		bool tightID  = ((emf>0.01 || fabs(i_calojet->eta())>2.6) && (n90hits>1) && ((fHPD<0.98 && i_calojet->pt()<=25) || (fHPD<0.95 && i_calojet->pt()>25)));
		qcdcalojet.setVar(emf,fHPD,fRBX,n90hits,nTrkCalo,nTrkVtx);
		qcdcalojet.setLooseIDFlag(looseID);
		qcdcalojet.setTightIDFlag(tightID);
		if (mIsMCarlo) {
			GenJetCollection::const_iterator i_matched;
			JetFlavourMatchingCollection::const_iterator i_flavour_matched;
			float rmin(999), rmin_flavour(999);
			for(GenJetCollection::const_iterator i_gen = genjets->begin(); i_gen != genjets->end(); i_gen++) {
				double deltaR = reco::deltaR(*i_calojet,*i_gen);
				if (deltaR < rmin) {
					rmin = deltaR;
					i_matched = i_gen;
				}
			}
			for (reco::JetFlavourMatchingCollection::const_iterator iter = jetMC->begin(); iter != jetMC->end(); iter++) {
				double deltaR = reco::deltaR(i_calojet->eta(), i_calojet->phi(), iter->second.getLorentzVector().Eta(), iter->second.getLorentzVector().Phi());
				 if (deltaR < rmin_flavour) {
					rmin_flavour = deltaR;
					i_flavour_matched = iter;
				}
		 }
			float bquark_3 = 0.0;
			float bquark_2 = 0.0;
			for (reco::GenParticleCollection::const_iterator igen_par = genParticles->begin(); igen_par != genParticles->end(); igen_par++) {
				double deltaR2 = reco::deltaR(*i_calojet,*igen_par);
				int pdgid = igen_par->pdgId();
				int status = igen_par->status();
				 if(deltaR2 < 0.35 && status == 3 && abs(pdgid) == 5) bquark_3 = 1.0;
				 if(deltaR2 < 0.35 && status == 2 && abs(pdgid) == 5) bquark_2 = 1.0;
				}


			if (genjets->size() == 0) {
				LorentzVector tmpP4(0.0,0.0,0.0,0.0);
				qcdcalojet.setGen(tmpP4,0);
				qcdcalojet.setFlavor(-99.0);
				qcdcalojet.setBstatus(-99, -99);
			}
			else{
				qcdcalojet.setGen(i_matched->p4(),rmin);
				qcdcalojet.setFlavor(i_flavour_matched->second.getFlavour());
				qcdcalojet.setBstatus(bquark_3, bquark_2);
			}
		}
		else {
			LorentzVector tmpP4(0.0,0.0,0.0,0.0); 
			qcdcalojet.setGen(tmpP4,0);
			qcdcalojet.setFlavor(-99.0);
			qcdcalojet.setBstatus(-99, -99);
		}
		
		//
		if(bTag_csv->size() == 0.){
			qcdcalojet.setBtag_tche(-99.);
			qcdcalojet.setBtag_tchp(-99.);
			qcdcalojet.setBtag_csv(-99.);
			qcdcalojet.setBtag_ssvhe(-99.);
			qcdcalojet.setBtag_ssvhp(-99.);
			qcdcalojet.setBtag_jp(-99.);
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
				double deltaR = reco::deltaR(i_calojet->eta(), i_calojet->phi(), (*i_btag).first->eta(), (*i_btag).first->phi());
				if (deltaR < rmin_btag_tchp) {
					rmin_btag_tchp = deltaR;
					i_btag_matched_tchp = i_btag;
				}
		 }
		 for (JetTagCollection::const_iterator i_btag = bTag_tche->begin(); i_btag != bTag_tche->end(); i_btag++){
				double deltaR = reco::deltaR(i_calojet->eta(), i_calojet->phi(), (*i_btag).first->eta(), (*i_btag).first->phi());
				if (deltaR < rmin_btag_tche) {
					rmin_btag_tche = deltaR;
					i_btag_matched_tche = i_btag;
				}
		 }
		for (JetTagCollection::const_iterator i_btag = bTag_csv->begin(); i_btag != bTag_csv->end(); i_btag++){
				double deltaR = reco::deltaR(i_calojet->eta(), i_calojet->phi(), (*i_btag).first->eta(), (*i_btag).first->phi());
				if (deltaR < rmin_btag_csv) {
					rmin_btag_csv = deltaR;
					i_btag_matched_csv = i_btag;
				}
		 }
		for (JetTagCollection::const_iterator i_btag = bTag_ssvhe->begin(); i_btag != bTag_ssvhe->end(); i_btag++){
				double deltaR = reco::deltaR(i_calojet->eta(), i_calojet->phi(), (*i_btag).first->eta(), (*i_btag).first->phi());
				if (deltaR < rmin_btag_ssvhe) {
					rmin_btag_ssvhe = deltaR;
					i_btag_matched_ssvhe = i_btag;
				}
		 }
		 for (JetTagCollection::const_iterator i_btag = bTag_ssvhp->begin(); i_btag != bTag_ssvhp->end(); i_btag++){
				double deltaR = reco::deltaR(i_calojet->eta(), i_calojet->phi(), (*i_btag).first->eta(), (*i_btag).first->phi());
				if (deltaR < rmin_btag_ssvhp) {
					rmin_btag_ssvhp = deltaR;
					i_btag_matched_ssvhp = i_btag;
				}
		 }
		 for (JetTagCollection::const_iterator i_btag = bTag_jp->begin(); i_btag != bTag_jp->end(); i_btag++){
				double deltaR = reco::deltaR(i_calojet->eta(), i_calojet->phi(), (*i_btag).first->eta(), (*i_btag).first->phi());
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

		 qcdcalojet.setBtag_tche(btag_tche);
		 qcdcalojet.setBtag_tchp(btag_tchp);
		 qcdcalojet.setBtag_csv(btag_csv);
		 qcdcalojet.setBtag_ssvhe(btag_ssvhe);
		 qcdcalojet.setBtag_ssvhp(btag_ssvhp);
		 qcdcalojet.setBtag_jp(btag_jp);
		 }
	//


		if (qcdcalojet.ptCor() >= mMinCaloPt)
			mCaloJets.push_back(qcdcalojet);
	}
		
	//---------------- met ---------------------------------------------
	Handle<PFMETCollection> pfmet;
	Handle<CaloMETCollection> calomet;
	event.getByLabel("pfMet",pfmet);
	event.getByLabel("met",calomet);
	mPFMet.setVar((*pfmet)[0].et(),(*pfmet)[0].sumEt(),(*pfmet)[0].phi());
	mCaloMet.setVar((*calomet)[0].et(),(*calomet)[0].sumEt(),(*calomet)[0].phi());
	//-------------- fill the tree -------------------------------------  
	sort(mCaloJets.begin(),mCaloJets.end(),sort_calojets);
	sort(mPFJets.begin(),mPFJets.end(),sort_pfjets);
	mEvent->setEvtHdr(mEvtHdr);
	mEvent->setCaloJets(mCaloJets);
	mEvent->setPFJets(mPFJets);
	mEvent->setFatJets(mPFFatJets);
	mEvent->setGenJets(mGenJets);
	mEvent->setCaloMET(mCaloMet);
	mEvent->setPFMET(mPFMet);
	mEvent->setL1Obj(mL1Objects);
	mEvent->setHLTObj(mHLTObjects);
	if ((mEvent->nPFJets() >= (unsigned)mMinNPFJets) && (mEvent->nCaloJets() >= (unsigned)mMinNCaloJets)) {
		if ((mEvent->pfmjjcor(0) >= mMinJJMass) || (mEvent->calomjjcor(0) >= mMinJJMass) || (mEvent->fatmjjcor(0) >= mMinJJMass)) {
			mTree->Fill();
		}
	}
	//if (mPFPayloadName != "") {
		//delete mPFUnc;
		//delete mPFUncSrc;
 //}
	//if (mCaloPayloadName != "")
		//delete mCALOUnc;
}
//////////////////////////////////////////////////////////////////////////////////////////
ProcessedTreeProducer::~ProcessedTreeProducer() 
{
}

DEFINE_FWK_MODULE(ProcessedTreeProducer);
