//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Fri Apr  8 11:06:11 2016 by ROOT version 5.32/00
// from TTree ProcessedTree/ProcessedTree
// found on file: ProcessedTree_data.root
//////////////////////////////////////////////////////////

#ifndef ProcessedTree_h
#define ProcessedTree_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TSelector.h>

// Header file for the classes stored in the TTree if any.
#include <Math/GenVector/PxPyPzE4D.h>

// Fixed size dimensions of array or collections stored in the TTree if any.
const Int_t kMaxCaloMet__et = 1;
const Int_t kMaxCaloMet__sumEt = 1;
const Int_t kMaxCaloMet__phi = 1;
const Int_t kMaxPFMet__et = 1;
const Int_t kMaxPFMet__sumEt = 1;
const Int_t kMaxPFMet__phi = 1;
const Int_t kMaxTriggerDecision = 1;
const Int_t kMaxL1Prescale = 1;
const Int_t kMaxHLTPrescale = 1;
const Int_t kMaxHLTObj = 1;
const Int_t kMaxL1Obj = 1;
const Int_t kMaxGenJets_ = 1;
const Int_t kMaxCaloJets_ = 84;
const Int_t kMaxCaloJets__genR = 84;
const Int_t kMaxCaloJets__cor = 84;
const Int_t kMaxCaloJets__unc = 84;
const Int_t kMaxCaloJets__uncSrc = 84;
const Int_t kMaxCaloJets__area = 84;
const Int_t kMaxCaloJets__looseID = 84;
const Int_t kMaxCaloJets__tightID = 84;
const Int_t kMaxCaloJets__btag_tche = 84;
const Int_t kMaxCaloJets__btag_tchp = 84;
const Int_t kMaxCaloJets__btag_csv = 84;
const Int_t kMaxCaloJets__btag_ssvhe = 84;
const Int_t kMaxCaloJets__btag_ssvhp = 84;
const Int_t kMaxCaloJets__btag_jp = 84;
const Int_t kMaxCaloJets__flavor = 84;
const Int_t kMaxCaloJets__status3 = 84;
const Int_t kMaxCaloJets__status2 = 84;
const Int_t kMaxCaloJets__PartonId = 84;
const Int_t kMaxCaloJets__emf = 84;
const Int_t kMaxCaloJets__fHPD = 84;
const Int_t kMaxCaloJets__fRBX = 84;
const Int_t kMaxCaloJets__n90hits = 84;
const Int_t kMaxCaloJets__nTrkCalo = 84;
const Int_t kMaxCaloJets__nTrkVtx = 84;
const Int_t kMaxPFJets_ = 75;
const Int_t kMaxPFJets__genR = 75;
const Int_t kMaxPFJets__cor = 75;
const Int_t kMaxPFJets__unc = 75;
const Int_t kMaxPFJets__uncSrc = 75;
const Int_t kMaxPFJets__area = 75;
const Int_t kMaxPFJets__looseID = 75;
const Int_t kMaxPFJets__tightID = 75;
const Int_t kMaxPFJets__btag_tche = 75;
const Int_t kMaxPFJets__btag_tchp = 75;
const Int_t kMaxPFJets__btag_csv = 75;
const Int_t kMaxPFJets__btag_ssvhe = 75;
const Int_t kMaxPFJets__btag_ssvhp = 75;
const Int_t kMaxPFJets__btag_jp = 75;
const Int_t kMaxPFJets__flavor = 75;
const Int_t kMaxPFJets__status3 = 75;
const Int_t kMaxPFJets__status2 = 75;
const Int_t kMaxPFJets__PartonId = 75;
const Int_t kMaxPFJets__chf = 75;
const Int_t kMaxPFJets__nhf = 75;
const Int_t kMaxPFJets__phf = 75;
const Int_t kMaxPFJets__elf = 75;
const Int_t kMaxPFJets__muf = 75;
const Int_t kMaxPFJets__hf_hf = 75;
const Int_t kMaxPFJets__hf_phf = 75;
const Int_t kMaxPFJets__hf_hm = 75;
const Int_t kMaxPFJets__hf_phm = 75;
const Int_t kMaxPFJets__chm = 75;
const Int_t kMaxPFJets__nhm = 75;
const Int_t kMaxPFJets__phm = 75;
const Int_t kMaxPFJets__elm = 75;
const Int_t kMaxPFJets__mum = 75;
const Int_t kMaxPFJets__ncand = 75;
const Int_t kMaxPFJets__beta = 75;
const Int_t kMaxPFJets__betaStar = 75;
const Int_t kMaxFatJets_ = 2;
const Int_t kMaxFatJets__genR = 2;
const Int_t kMaxFatJets__cor = 2;
const Int_t kMaxFatJets__unc = 2;
const Int_t kMaxFatJets__uncSrc = 2;
const Int_t kMaxFatJets__area = 2;
const Int_t kMaxFatJets__looseID = 2;
const Int_t kMaxFatJets__tightID = 2;
const Int_t kMaxFatJets__btag_tche = 2;
const Int_t kMaxFatJets__btag_tchp = 2;
const Int_t kMaxFatJets__btag_csv = 2;
const Int_t kMaxFatJets__btag_ssvhe = 2;
const Int_t kMaxFatJets__btag_ssvhp = 2;
const Int_t kMaxFatJets__btag_jp = 2;
const Int_t kMaxFatJets__flavor = 2;
const Int_t kMaxFatJets__status3 = 2;
const Int_t kMaxFatJets__status2 = 2;
const Int_t kMaxFatJets__PartonId = 2;

class ProcessedTree : public TSelector {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain

   // Declaration of leaf types
 //QCDEvent        *events;
   Bool_t          EvtHdr__mIsPVgood;
   Bool_t          EvtHdr__mHCALNoise;
   Int_t           EvtHdr__mRun;
   Int_t           EvtHdr__mEvent;
   Int_t           EvtHdr__mLumi;
   Int_t           EvtHdr__mBunch;
   Int_t           EvtHdr__mNVtx;
   Int_t           EvtHdr__mNVtxGood;
   Int_t           EvtHdr__mOOTPUEarly;
   Int_t           EvtHdr__mOOTPULate;
   Int_t           EvtHdr__mINTPU;
   Int_t           EvtHdr__mNBX;
   Float_t         EvtHdr__mPVndof;
   Float_t         EvtHdr__mTrPu;
   Float_t         EvtHdr__mPVx;
   Float_t         EvtHdr__mPVy;
   Float_t         EvtHdr__mPVz;
   Float_t         EvtHdr__mBSx;
   Float_t         EvtHdr__mBSy;
   Float_t         EvtHdr__mBSz;
   Float_t         EvtHdr__mPthat;
   Float_t         EvtHdr__mWeight;
   Float_t         EvtHdr__mCaloRho;
   Float_t         EvtHdr__mPFRho;
   Double_t        EvtHdr__mmXsec;
   Float_t         CaloMet__et_;
   Float_t         CaloMet__sumEt_;
   Float_t         CaloMet__phi_;
   Float_t         PFMet__et_;
   Float_t         PFMet__sumEt_;
   Float_t         PFMet__phi_;
   vector<int>     TriggerDecision_;
   vector<int>     L1Prescale_;
   vector<int>     HLTPrescale_;
 //vector<vector<ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double> > > > HLTObj_;
 //vector<vector<ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double> > > > L1Obj_;
   Int_t           GenJets__;
   Double_t        GenJets__fCoordinates_fX[kMaxGenJets_];   //[GenJets__]
   Double_t        GenJets__fCoordinates_fY[kMaxGenJets_];   //[GenJets__]
   Double_t        GenJets__fCoordinates_fZ[kMaxGenJets_];   //[GenJets__]
   Double_t        GenJets__fCoordinates_fT[kMaxGenJets_];   //[GenJets__]
   Int_t           CaloJets__;
   Double_t        CaloJets__P4__fCoordinates_fX[kMaxCaloJets_];   //[CaloJets__]
   Double_t        CaloJets__P4__fCoordinates_fY[kMaxCaloJets_];   //[CaloJets__]
   Double_t        CaloJets__P4__fCoordinates_fZ[kMaxCaloJets_];   //[CaloJets__]
   Double_t        CaloJets__P4__fCoordinates_fT[kMaxCaloJets_];   //[CaloJets__]
   Double_t        CaloJets__genP4__fCoordinates_fX[kMaxCaloJets_];   //[CaloJets__]
   Double_t        CaloJets__genP4__fCoordinates_fY[kMaxCaloJets_];   //[CaloJets__]
   Double_t        CaloJets__genP4__fCoordinates_fZ[kMaxCaloJets_];   //[CaloJets__]
   Double_t        CaloJets__genP4__fCoordinates_fT[kMaxCaloJets_];   //[CaloJets__]
   Float_t         CaloJets__genR_[kMaxCaloJets_];   //[CaloJets__]
   Float_t         CaloJets__cor_[kMaxCaloJets_];   //[CaloJets__]
   Float_t         CaloJets__unc_[kMaxCaloJets_];   //[CaloJets__]
   vector<float>   CaloJets__uncSrc_[kMaxCaloJets_];
   Float_t         CaloJets__area_[kMaxCaloJets_];   //[CaloJets__]
   Bool_t          CaloJets__looseID_[kMaxCaloJets_];   //[CaloJets__]
   Bool_t          CaloJets__tightID_[kMaxCaloJets_];   //[CaloJets__]
   Float_t         CaloJets__btag_tche_[kMaxCaloJets_];   //[CaloJets__]
   Float_t         CaloJets__btag_tchp_[kMaxCaloJets_];   //[CaloJets__]
   Float_t         CaloJets__btag_csv_[kMaxCaloJets_];   //[CaloJets__]
   Float_t         CaloJets__btag_ssvhe_[kMaxCaloJets_];   //[CaloJets__]
   Float_t         CaloJets__btag_ssvhp_[kMaxCaloJets_];   //[CaloJets__]
   Float_t         CaloJets__btag_jp_[kMaxCaloJets_];   //[CaloJets__]
   Float_t         CaloJets__flavor_[kMaxCaloJets_];   //[CaloJets__]
   Float_t         CaloJets__status3_[kMaxCaloJets_];   //[CaloJets__]
   Float_t         CaloJets__status2_[kMaxCaloJets_];   //[CaloJets__]
   Float_t         CaloJets__PartonId_[kMaxCaloJets_];   //[CaloJets__]
   Float_t         CaloJets__emf_[kMaxCaloJets_];   //[CaloJets__]
   Float_t         CaloJets__fHPD_[kMaxCaloJets_];   //[CaloJets__]
   Float_t         CaloJets__fRBX_[kMaxCaloJets_];   //[CaloJets__]
   Int_t           CaloJets__n90hits_[kMaxCaloJets_];   //[CaloJets__]
   Int_t           CaloJets__nTrkCalo_[kMaxCaloJets_];   //[CaloJets__]
   Int_t           CaloJets__nTrkVtx_[kMaxCaloJets_];   //[CaloJets__]
   Int_t           PFJets__;
   Double_t        PFJets__P4__fCoordinates_fX[kMaxPFJets_];   //[PFJets__]
   Double_t        PFJets__P4__fCoordinates_fY[kMaxPFJets_];   //[PFJets__]
   Double_t        PFJets__P4__fCoordinates_fZ[kMaxPFJets_];   //[PFJets__]
   Double_t        PFJets__P4__fCoordinates_fT[kMaxPFJets_];   //[PFJets__]
   Double_t        PFJets__genP4__fCoordinates_fX[kMaxPFJets_];   //[PFJets__]
   Double_t        PFJets__genP4__fCoordinates_fY[kMaxPFJets_];   //[PFJets__]
   Double_t        PFJets__genP4__fCoordinates_fZ[kMaxPFJets_];   //[PFJets__]
   Double_t        PFJets__genP4__fCoordinates_fT[kMaxPFJets_];   //[PFJets__]
   Float_t         PFJets__genR_[kMaxPFJets_];   //[PFJets__]
   Float_t         PFJets__cor_[kMaxPFJets_];   //[PFJets__]
   Float_t         PFJets__unc_[kMaxPFJets_];   //[PFJets__]
   vector<float>   PFJets__uncSrc_[kMaxPFJets_];
   Float_t         PFJets__area_[kMaxPFJets_];   //[PFJets__]
   Bool_t          PFJets__looseID_[kMaxPFJets_];   //[PFJets__]
   Bool_t          PFJets__tightID_[kMaxPFJets_];   //[PFJets__]
   Float_t         PFJets__btag_tche_[kMaxPFJets_];   //[PFJets__]
   Float_t         PFJets__btag_tchp_[kMaxPFJets_];   //[PFJets__]
   Float_t         PFJets__btag_csv_[kMaxPFJets_];   //[PFJets__]
   Float_t         PFJets__btag_ssvhe_[kMaxPFJets_];   //[PFJets__]
   Float_t         PFJets__btag_ssvhp_[kMaxPFJets_];   //[PFJets__]
   Float_t         PFJets__btag_jp_[kMaxPFJets_];   //[PFJets__]
   Float_t         PFJets__flavor_[kMaxPFJets_];   //[PFJets__]
   Float_t         PFJets__status3_[kMaxPFJets_];   //[PFJets__]
   Float_t         PFJets__status2_[kMaxPFJets_];   //[PFJets__]
   Float_t         PFJets__PartonId_[kMaxPFJets_];   //[PFJets__]
   Float_t         PFJets__chf_[kMaxPFJets_];   //[PFJets__]
   Float_t         PFJets__nhf_[kMaxPFJets_];   //[PFJets__]
   Float_t         PFJets__phf_[kMaxPFJets_];   //[PFJets__]
   Float_t         PFJets__elf_[kMaxPFJets_];   //[PFJets__]
   Float_t         PFJets__muf_[kMaxPFJets_];   //[PFJets__]
   Float_t         PFJets__hf_hf_[kMaxPFJets_];   //[PFJets__]
   Float_t         PFJets__hf_phf_[kMaxPFJets_];   //[PFJets__]
   Int_t           PFJets__hf_hm_[kMaxPFJets_];   //[PFJets__]
   Int_t           PFJets__hf_phm_[kMaxPFJets_];   //[PFJets__]
   Int_t           PFJets__chm_[kMaxPFJets_];   //[PFJets__]
   Int_t           PFJets__nhm_[kMaxPFJets_];   //[PFJets__]
   Int_t           PFJets__phm_[kMaxPFJets_];   //[PFJets__]
   Int_t           PFJets__elm_[kMaxPFJets_];   //[PFJets__]
   Int_t           PFJets__mum_[kMaxPFJets_];   //[PFJets__]
   Int_t           PFJets__ncand_[kMaxPFJets_];   //[PFJets__]
   Float_t         PFJets__beta_[kMaxPFJets_];   //[PFJets__]
   Float_t         PFJets__betaStar_[kMaxPFJets_];   //[PFJets__]
   Int_t           FatJets__;
   Double_t        FatJets__P4__fCoordinates_fX[kMaxFatJets_];   //[FatJets__]
   Double_t        FatJets__P4__fCoordinates_fY[kMaxFatJets_];   //[FatJets__]
   Double_t        FatJets__P4__fCoordinates_fZ[kMaxFatJets_];   //[FatJets__]
   Double_t        FatJets__P4__fCoordinates_fT[kMaxFatJets_];   //[FatJets__]
   Double_t        FatJets__genP4__fCoordinates_fX[kMaxFatJets_];   //[FatJets__]
   Double_t        FatJets__genP4__fCoordinates_fY[kMaxFatJets_];   //[FatJets__]
   Double_t        FatJets__genP4__fCoordinates_fZ[kMaxFatJets_];   //[FatJets__]
   Double_t        FatJets__genP4__fCoordinates_fT[kMaxFatJets_];   //[FatJets__]
   Float_t         FatJets__genR_[kMaxFatJets_];   //[FatJets__]
   Float_t         FatJets__cor_[kMaxFatJets_];   //[FatJets__]
   Float_t         FatJets__unc_[kMaxFatJets_];   //[FatJets__]
   vector<float>   FatJets__uncSrc_[kMaxFatJets_];
   Float_t         FatJets__area_[kMaxFatJets_];   //[FatJets__]
   Bool_t          FatJets__looseID_[kMaxFatJets_];   //[FatJets__]
   Bool_t          FatJets__tightID_[kMaxFatJets_];   //[FatJets__]
   Float_t         FatJets__btag_tche_[kMaxFatJets_];   //[FatJets__]
   Float_t         FatJets__btag_tchp_[kMaxFatJets_];   //[FatJets__]
   Float_t         FatJets__btag_csv_[kMaxFatJets_];   //[FatJets__]
   Float_t         FatJets__btag_ssvhe_[kMaxFatJets_];   //[FatJets__]
   Float_t         FatJets__btag_ssvhp_[kMaxFatJets_];   //[FatJets__]
   Float_t         FatJets__btag_jp_[kMaxFatJets_];   //[FatJets__]
   Float_t         FatJets__flavor_[kMaxFatJets_];   //[FatJets__]
   Float_t         FatJets__status3_[kMaxFatJets_];   //[FatJets__]
   Float_t         FatJets__status2_[kMaxFatJets_];   //[FatJets__]
   Float_t         FatJets__PartonId_[kMaxFatJets_];   //[FatJets__]

   // List of branches
   TBranch        *b_events_EvtHdr__mIsPVgood;   //!
   TBranch        *b_events_EvtHdr__mHCALNoise;   //!
   TBranch        *b_events_EvtHdr__mRun;   //!
   TBranch        *b_events_EvtHdr__mEvent;   //!
   TBranch        *b_events_EvtHdr__mLumi;   //!
   TBranch        *b_events_EvtHdr__mBunch;   //!
   TBranch        *b_events_EvtHdr__mNVtx;   //!
   TBranch        *b_events_EvtHdr__mNVtxGood;   //!
   TBranch        *b_events_EvtHdr__mOOTPUEarly;   //!
   TBranch        *b_events_EvtHdr__mOOTPULate;   //!
   TBranch        *b_events_EvtHdr__mINTPU;   //!
   TBranch        *b_events_EvtHdr__mNBX;   //!
   TBranch        *b_events_EvtHdr__mPVndof;   //!
   TBranch        *b_events_EvtHdr__mTrPu;   //!
   TBranch        *b_events_EvtHdr__mPVx;   //!
   TBranch        *b_events_EvtHdr__mPVy;   //!
   TBranch        *b_events_EvtHdr__mPVz;   //!
   TBranch        *b_events_EvtHdr__mBSx;   //!
   TBranch        *b_events_EvtHdr__mBSy;   //!
   TBranch        *b_events_EvtHdr__mBSz;   //!
   TBranch        *b_events_EvtHdr__mPthat;   //!
   TBranch        *b_events_EvtHdr__mWeight;   //!
   TBranch        *b_events_EvtHdr__mCaloRho;   //!
   TBranch        *b_events_EvtHdr__mPFRho;   //!
   TBranch        *b_events_EvtHdr__mmXsec;   //!
   TBranch        *b_events_CaloMet__et_;   //!
   TBranch        *b_events_CaloMet__sumEt_;   //!
   TBranch        *b_events_CaloMet__phi_;   //!
   TBranch        *b_events_PFMet__et_;   //!
   TBranch        *b_events_PFMet__sumEt_;   //!
   TBranch        *b_events_PFMet__phi_;   //!
   TBranch        *b_events_TriggerDecision_;   //!
   TBranch        *b_events_L1Prescale_;   //!
   TBranch        *b_events_HLTPrescale_;   //!
   TBranch        *b_events_GenJets__;   //!
   TBranch        *b_GenJets__fCoordinates_fX;   //!
   TBranch        *b_GenJets__fCoordinates_fY;   //!
   TBranch        *b_GenJets__fCoordinates_fZ;   //!
   TBranch        *b_GenJets__fCoordinates_fT;   //!
   TBranch        *b_events_CaloJets__;   //!
   TBranch        *b_CaloJets__P4__fCoordinates_fX;   //!
   TBranch        *b_CaloJets__P4__fCoordinates_fY;   //!
   TBranch        *b_CaloJets__P4__fCoordinates_fZ;   //!
   TBranch        *b_CaloJets__P4__fCoordinates_fT;   //!
   TBranch        *b_CaloJets__genP4__fCoordinates_fX;   //!
   TBranch        *b_CaloJets__genP4__fCoordinates_fY;   //!
   TBranch        *b_CaloJets__genP4__fCoordinates_fZ;   //!
   TBranch        *b_CaloJets__genP4__fCoordinates_fT;   //!
   TBranch        *b_CaloJets__genR_;   //!
   TBranch        *b_CaloJets__cor_;   //!
   TBranch        *b_CaloJets__unc_;   //!
   TBranch        *b_CaloJets__uncSrc_;   //!
   TBranch        *b_CaloJets__area_;   //!
   TBranch        *b_CaloJets__looseID_;   //!
   TBranch        *b_CaloJets__tightID_;   //!
   TBranch        *b_CaloJets__btag_tche_;   //!
   TBranch        *b_CaloJets__btag_tchp_;   //!
   TBranch        *b_CaloJets__btag_csv_;   //!
   TBranch        *b_CaloJets__btag_ssvhe_;   //!
   TBranch        *b_CaloJets__btag_ssvhp_;   //!
   TBranch        *b_CaloJets__btag_jp_;   //!
   TBranch        *b_CaloJets__flavor_;   //!
   TBranch        *b_CaloJets__status3_;   //!
   TBranch        *b_CaloJets__status2_;   //!
   TBranch        *b_CaloJets__PartonId_;   //!
   TBranch        *b_CaloJets__emf_;   //!
   TBranch        *b_CaloJets__fHPD_;   //!
   TBranch        *b_CaloJets__fRBX_;   //!
   TBranch        *b_CaloJets__n90hits_;   //!
   TBranch        *b_CaloJets__nTrkCalo_;   //!
   TBranch        *b_CaloJets__nTrkVtx_;   //!
   TBranch        *b_events_PFJets__;   //!
   TBranch        *b_PFJets__P4__fCoordinates_fX;   //!
   TBranch        *b_PFJets__P4__fCoordinates_fY;   //!
   TBranch        *b_PFJets__P4__fCoordinates_fZ;   //!
   TBranch        *b_PFJets__P4__fCoordinates_fT;   //!
   TBranch        *b_PFJets__genP4__fCoordinates_fX;   //!
   TBranch        *b_PFJets__genP4__fCoordinates_fY;   //!
   TBranch        *b_PFJets__genP4__fCoordinates_fZ;   //!
   TBranch        *b_PFJets__genP4__fCoordinates_fT;   //!
   TBranch        *b_PFJets__genR_;   //!
   TBranch        *b_PFJets__cor_;   //!
   TBranch        *b_PFJets__unc_;   //!
   TBranch        *b_PFJets__uncSrc_;   //!
   TBranch        *b_PFJets__area_;   //!
   TBranch        *b_PFJets__looseID_;   //!
   TBranch        *b_PFJets__tightID_;   //!
   TBranch        *b_PFJets__btag_tche_;   //!
   TBranch        *b_PFJets__btag_tchp_;   //!
   TBranch        *b_PFJets__btag_csv_;   //!
   TBranch        *b_PFJets__btag_ssvhe_;   //!
   TBranch        *b_PFJets__btag_ssvhp_;   //!
   TBranch        *b_PFJets__btag_jp_;   //!
   TBranch        *b_PFJets__flavor_;   //!
   TBranch        *b_PFJets__status3_;   //!
   TBranch        *b_PFJets__status2_;   //!
   TBranch        *b_PFJets__PartonId_;   //!
   TBranch        *b_PFJets__chf_;   //!
   TBranch        *b_PFJets__nhf_;   //!
   TBranch        *b_PFJets__phf_;   //!
   TBranch        *b_PFJets__elf_;   //!
   TBranch        *b_PFJets__muf_;   //!
   TBranch        *b_PFJets__hf_hf_;   //!
   TBranch        *b_PFJets__hf_phf_;   //!
   TBranch        *b_PFJets__hf_hm_;   //!
   TBranch        *b_PFJets__hf_phm_;   //!
   TBranch        *b_PFJets__chm_;   //!
   TBranch        *b_PFJets__nhm_;   //!
   TBranch        *b_PFJets__phm_;   //!
   TBranch        *b_PFJets__elm_;   //!
   TBranch        *b_PFJets__mum_;   //!
   TBranch        *b_PFJets__ncand_;   //!
   TBranch        *b_PFJets__beta_;   //!
   TBranch        *b_PFJets__betaStar_;   //!
   TBranch        *b_events_FatJets__;   //!
   TBranch        *b_FatJets__P4__fCoordinates_fX;   //!
   TBranch        *b_FatJets__P4__fCoordinates_fY;   //!
   TBranch        *b_FatJets__P4__fCoordinates_fZ;   //!
   TBranch        *b_FatJets__P4__fCoordinates_fT;   //!
   TBranch        *b_FatJets__genP4__fCoordinates_fX;   //!
   TBranch        *b_FatJets__genP4__fCoordinates_fY;   //!
   TBranch        *b_FatJets__genP4__fCoordinates_fZ;   //!
   TBranch        *b_FatJets__genP4__fCoordinates_fT;   //!
   TBranch        *b_FatJets__genR_;   //!
   TBranch        *b_FatJets__cor_;   //!
   TBranch        *b_FatJets__unc_;   //!
   TBranch        *b_FatJets__uncSrc_;   //!
   TBranch        *b_FatJets__area_;   //!
   TBranch        *b_FatJets__looseID_;   //!
   TBranch        *b_FatJets__tightID_;   //!
   TBranch        *b_FatJets__btag_tche_;   //!
   TBranch        *b_FatJets__btag_tchp_;   //!
   TBranch        *b_FatJets__btag_csv_;   //!
   TBranch        *b_FatJets__btag_ssvhe_;   //!
   TBranch        *b_FatJets__btag_ssvhp_;   //!
   TBranch        *b_FatJets__btag_jp_;   //!
   TBranch        *b_FatJets__flavor_;   //!
   TBranch        *b_FatJets__status3_;   //!
   TBranch        *b_FatJets__status2_;   //!
   TBranch        *b_FatJets__PartonId_;   //!

   ProcessedTree(TTree * /*tree*/ =0) : fChain(0) { }
   virtual ~ProcessedTree() { }
   virtual Int_t   Version() const { return 2; }
   virtual void    Begin(TTree *tree);
   virtual void    SlaveBegin(TTree *tree);
   virtual void    Init(TTree *tree);
   virtual Bool_t  Notify();
   virtual Bool_t  Process(Long64_t entry);
   virtual Int_t   GetEntry(Long64_t entry, Int_t getall = 0) { return fChain ? fChain->GetTree()->GetEntry(entry, getall) : 0; }
   virtual void    SetOption(const char *option) { fOption = option; }
   virtual void    SetObject(TObject *obj) { fObject = obj; }
   virtual void    SetInputList(TList *input) { fInput = input; }
   virtual TList  *GetOutputList() const { return fOutput; }
   virtual void    SlaveTerminate();
   virtual void    Terminate();

   ClassDef(ProcessedTree,0);
};

#endif

#ifdef ProcessedTree_cxx
void ProcessedTree::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("EvtHdr_.mIsPVgood", &EvtHdr__mIsPVgood, &b_events_EvtHdr__mIsPVgood);
   fChain->SetBranchAddress("EvtHdr_.mHCALNoise", &EvtHdr__mHCALNoise, &b_events_EvtHdr__mHCALNoise);
   fChain->SetBranchAddress("EvtHdr_.mRun", &EvtHdr__mRun, &b_events_EvtHdr__mRun);
   fChain->SetBranchAddress("EvtHdr_.mEvent", &EvtHdr__mEvent, &b_events_EvtHdr__mEvent);
   fChain->SetBranchAddress("EvtHdr_.mLumi", &EvtHdr__mLumi, &b_events_EvtHdr__mLumi);
   fChain->SetBranchAddress("EvtHdr_.mBunch", &EvtHdr__mBunch, &b_events_EvtHdr__mBunch);
   fChain->SetBranchAddress("EvtHdr_.mNVtx", &EvtHdr__mNVtx, &b_events_EvtHdr__mNVtx);
   fChain->SetBranchAddress("EvtHdr_.mNVtxGood", &EvtHdr__mNVtxGood, &b_events_EvtHdr__mNVtxGood);
   fChain->SetBranchAddress("EvtHdr_.mOOTPUEarly", &EvtHdr__mOOTPUEarly, &b_events_EvtHdr__mOOTPUEarly);
   fChain->SetBranchAddress("EvtHdr_.mOOTPULate", &EvtHdr__mOOTPULate, &b_events_EvtHdr__mOOTPULate);
   fChain->SetBranchAddress("EvtHdr_.mINTPU", &EvtHdr__mINTPU, &b_events_EvtHdr__mINTPU);
   fChain->SetBranchAddress("EvtHdr_.mNBX", &EvtHdr__mNBX, &b_events_EvtHdr__mNBX);
   fChain->SetBranchAddress("EvtHdr_.mPVndof", &EvtHdr__mPVndof, &b_events_EvtHdr__mPVndof);
   fChain->SetBranchAddress("EvtHdr_.mTrPu", &EvtHdr__mTrPu, &b_events_EvtHdr__mTrPu);
   fChain->SetBranchAddress("EvtHdr_.mPVx", &EvtHdr__mPVx, &b_events_EvtHdr__mPVx);
   fChain->SetBranchAddress("EvtHdr_.mPVy", &EvtHdr__mPVy, &b_events_EvtHdr__mPVy);
   fChain->SetBranchAddress("EvtHdr_.mPVz", &EvtHdr__mPVz, &b_events_EvtHdr__mPVz);
   fChain->SetBranchAddress("EvtHdr_.mBSx", &EvtHdr__mBSx, &b_events_EvtHdr__mBSx);
   fChain->SetBranchAddress("EvtHdr_.mBSy", &EvtHdr__mBSy, &b_events_EvtHdr__mBSy);
   fChain->SetBranchAddress("EvtHdr_.mBSz", &EvtHdr__mBSz, &b_events_EvtHdr__mBSz);
   fChain->SetBranchAddress("EvtHdr_.mPthat", &EvtHdr__mPthat, &b_events_EvtHdr__mPthat);
   fChain->SetBranchAddress("EvtHdr_.mWeight", &EvtHdr__mWeight, &b_events_EvtHdr__mWeight);
   fChain->SetBranchAddress("EvtHdr_.mCaloRho", &EvtHdr__mCaloRho, &b_events_EvtHdr__mCaloRho);
   fChain->SetBranchAddress("EvtHdr_.mPFRho", &EvtHdr__mPFRho, &b_events_EvtHdr__mPFRho);
   fChain->SetBranchAddress("EvtHdr_.mmXsec", &EvtHdr__mmXsec, &b_events_EvtHdr__mmXsec);
   fChain->SetBranchAddress("CaloMet_.et_", &CaloMet__et_, &b_events_CaloMet__et_);
   fChain->SetBranchAddress("CaloMet_.sumEt_", &CaloMet__sumEt_, &b_events_CaloMet__sumEt_);
   fChain->SetBranchAddress("CaloMet_.phi_", &CaloMet__phi_, &b_events_CaloMet__phi_);
   fChain->SetBranchAddress("PFMet_.et_", &PFMet__et_, &b_events_PFMet__et_);
   fChain->SetBranchAddress("PFMet_.sumEt_", &PFMet__sumEt_, &b_events_PFMet__sumEt_);
   fChain->SetBranchAddress("PFMet_.phi_", &PFMet__phi_, &b_events_PFMet__phi_);
   fChain->SetBranchAddress("TriggerDecision_", &TriggerDecision_, &b_events_TriggerDecision_);
   fChain->SetBranchAddress("L1Prescale_", &L1Prescale_, &b_events_L1Prescale_);
   fChain->SetBranchAddress("HLTPrescale_", &HLTPrescale_, &b_events_HLTPrescale_);
   fChain->SetBranchAddress("GenJets_", &GenJets__, &b_events_GenJets__);
   fChain->SetBranchAddress("GenJets_.fCoordinates.fX", &GenJets__fCoordinates_fX, &b_GenJets__fCoordinates_fX);
   fChain->SetBranchAddress("GenJets_.fCoordinates.fY", &GenJets__fCoordinates_fY, &b_GenJets__fCoordinates_fY);
   fChain->SetBranchAddress("GenJets_.fCoordinates.fZ", &GenJets__fCoordinates_fZ, &b_GenJets__fCoordinates_fZ);
   fChain->SetBranchAddress("GenJets_.fCoordinates.fT", &GenJets__fCoordinates_fT, &b_GenJets__fCoordinates_fT);
   fChain->SetBranchAddress("CaloJets_", &CaloJets__, &b_events_CaloJets__);
   fChain->SetBranchAddress("CaloJets_.P4_.fCoordinates.fX", CaloJets__P4__fCoordinates_fX, &b_CaloJets__P4__fCoordinates_fX);
   fChain->SetBranchAddress("CaloJets_.P4_.fCoordinates.fY", CaloJets__P4__fCoordinates_fY, &b_CaloJets__P4__fCoordinates_fY);
   fChain->SetBranchAddress("CaloJets_.P4_.fCoordinates.fZ", CaloJets__P4__fCoordinates_fZ, &b_CaloJets__P4__fCoordinates_fZ);
   fChain->SetBranchAddress("CaloJets_.P4_.fCoordinates.fT", CaloJets__P4__fCoordinates_fT, &b_CaloJets__P4__fCoordinates_fT);
   fChain->SetBranchAddress("CaloJets_.genP4_.fCoordinates.fX", CaloJets__genP4__fCoordinates_fX, &b_CaloJets__genP4__fCoordinates_fX);
   fChain->SetBranchAddress("CaloJets_.genP4_.fCoordinates.fY", CaloJets__genP4__fCoordinates_fY, &b_CaloJets__genP4__fCoordinates_fY);
   fChain->SetBranchAddress("CaloJets_.genP4_.fCoordinates.fZ", CaloJets__genP4__fCoordinates_fZ, &b_CaloJets__genP4__fCoordinates_fZ);
   fChain->SetBranchAddress("CaloJets_.genP4_.fCoordinates.fT", CaloJets__genP4__fCoordinates_fT, &b_CaloJets__genP4__fCoordinates_fT);
   fChain->SetBranchAddress("CaloJets_.genR_", CaloJets__genR_, &b_CaloJets__genR_);
   fChain->SetBranchAddress("CaloJets_.cor_", CaloJets__cor_, &b_CaloJets__cor_);
   fChain->SetBranchAddress("CaloJets_.unc_", CaloJets__unc_, &b_CaloJets__unc_);
   fChain->SetBranchAddress("CaloJets_.uncSrc_", CaloJets__uncSrc_, &b_CaloJets__uncSrc_);
   fChain->SetBranchAddress("CaloJets_.area_", CaloJets__area_, &b_CaloJets__area_);
   fChain->SetBranchAddress("CaloJets_.looseID_", CaloJets__looseID_, &b_CaloJets__looseID_);
   fChain->SetBranchAddress("CaloJets_.tightID_", CaloJets__tightID_, &b_CaloJets__tightID_);
   fChain->SetBranchAddress("CaloJets_.btag_tche_", CaloJets__btag_tche_, &b_CaloJets__btag_tche_);
   fChain->SetBranchAddress("CaloJets_.btag_tchp_", CaloJets__btag_tchp_, &b_CaloJets__btag_tchp_);
   fChain->SetBranchAddress("CaloJets_.btag_csv_", CaloJets__btag_csv_, &b_CaloJets__btag_csv_);
   fChain->SetBranchAddress("CaloJets_.btag_ssvhe_", CaloJets__btag_ssvhe_, &b_CaloJets__btag_ssvhe_);
   fChain->SetBranchAddress("CaloJets_.btag_ssvhp_", CaloJets__btag_ssvhp_, &b_CaloJets__btag_ssvhp_);
   fChain->SetBranchAddress("CaloJets_.btag_jp_", CaloJets__btag_jp_, &b_CaloJets__btag_jp_);
   fChain->SetBranchAddress("CaloJets_.flavor_", CaloJets__flavor_, &b_CaloJets__flavor_);
   fChain->SetBranchAddress("CaloJets_.status3_", CaloJets__status3_, &b_CaloJets__status3_);
   fChain->SetBranchAddress("CaloJets_.status2_", CaloJets__status2_, &b_CaloJets__status2_);
   fChain->SetBranchAddress("CaloJets_.PartonId_", CaloJets__PartonId_, &b_CaloJets__PartonId_);
   fChain->SetBranchAddress("CaloJets_.emf_", CaloJets__emf_, &b_CaloJets__emf_);
   fChain->SetBranchAddress("CaloJets_.fHPD_", CaloJets__fHPD_, &b_CaloJets__fHPD_);
   fChain->SetBranchAddress("CaloJets_.fRBX_", CaloJets__fRBX_, &b_CaloJets__fRBX_);
   fChain->SetBranchAddress("CaloJets_.n90hits_", CaloJets__n90hits_, &b_CaloJets__n90hits_);
   fChain->SetBranchAddress("CaloJets_.nTrkCalo_", CaloJets__nTrkCalo_, &b_CaloJets__nTrkCalo_);
   fChain->SetBranchAddress("CaloJets_.nTrkVtx_", CaloJets__nTrkVtx_, &b_CaloJets__nTrkVtx_);
   fChain->SetBranchAddress("PFJets_", &PFJets__, &b_events_PFJets__);
   fChain->SetBranchAddress("PFJets_.P4_.fCoordinates.fX", PFJets__P4__fCoordinates_fX, &b_PFJets__P4__fCoordinates_fX);
   fChain->SetBranchAddress("PFJets_.P4_.fCoordinates.fY", PFJets__P4__fCoordinates_fY, &b_PFJets__P4__fCoordinates_fY);
   fChain->SetBranchAddress("PFJets_.P4_.fCoordinates.fZ", PFJets__P4__fCoordinates_fZ, &b_PFJets__P4__fCoordinates_fZ);
   fChain->SetBranchAddress("PFJets_.P4_.fCoordinates.fT", PFJets__P4__fCoordinates_fT, &b_PFJets__P4__fCoordinates_fT);
   fChain->SetBranchAddress("PFJets_.genP4_.fCoordinates.fX", PFJets__genP4__fCoordinates_fX, &b_PFJets__genP4__fCoordinates_fX);
   fChain->SetBranchAddress("PFJets_.genP4_.fCoordinates.fY", PFJets__genP4__fCoordinates_fY, &b_PFJets__genP4__fCoordinates_fY);
   fChain->SetBranchAddress("PFJets_.genP4_.fCoordinates.fZ", PFJets__genP4__fCoordinates_fZ, &b_PFJets__genP4__fCoordinates_fZ);
   fChain->SetBranchAddress("PFJets_.genP4_.fCoordinates.fT", PFJets__genP4__fCoordinates_fT, &b_PFJets__genP4__fCoordinates_fT);
   fChain->SetBranchAddress("PFJets_.genR_", PFJets__genR_, &b_PFJets__genR_);
   fChain->SetBranchAddress("PFJets_.cor_", PFJets__cor_, &b_PFJets__cor_);
   fChain->SetBranchAddress("PFJets_.unc_", PFJets__unc_, &b_PFJets__unc_);
   fChain->SetBranchAddress("PFJets_.uncSrc_", PFJets__uncSrc_, &b_PFJets__uncSrc_);
   fChain->SetBranchAddress("PFJets_.area_", PFJets__area_, &b_PFJets__area_);
   fChain->SetBranchAddress("PFJets_.looseID_", PFJets__looseID_, &b_PFJets__looseID_);
   fChain->SetBranchAddress("PFJets_.tightID_", PFJets__tightID_, &b_PFJets__tightID_);
   fChain->SetBranchAddress("PFJets_.btag_tche_", PFJets__btag_tche_, &b_PFJets__btag_tche_);
   fChain->SetBranchAddress("PFJets_.btag_tchp_", PFJets__btag_tchp_, &b_PFJets__btag_tchp_);
   fChain->SetBranchAddress("PFJets_.btag_csv_", PFJets__btag_csv_, &b_PFJets__btag_csv_);
   fChain->SetBranchAddress("PFJets_.btag_ssvhe_", PFJets__btag_ssvhe_, &b_PFJets__btag_ssvhe_);
   fChain->SetBranchAddress("PFJets_.btag_ssvhp_", PFJets__btag_ssvhp_, &b_PFJets__btag_ssvhp_);
   fChain->SetBranchAddress("PFJets_.btag_jp_", PFJets__btag_jp_, &b_PFJets__btag_jp_);
   fChain->SetBranchAddress("PFJets_.flavor_", PFJets__flavor_, &b_PFJets__flavor_);
   fChain->SetBranchAddress("PFJets_.status3_", PFJets__status3_, &b_PFJets__status3_);
   fChain->SetBranchAddress("PFJets_.status2_", PFJets__status2_, &b_PFJets__status2_);
   fChain->SetBranchAddress("PFJets_.PartonId_", PFJets__PartonId_, &b_PFJets__PartonId_);
   fChain->SetBranchAddress("PFJets_.chf_", PFJets__chf_, &b_PFJets__chf_);
   fChain->SetBranchAddress("PFJets_.nhf_", PFJets__nhf_, &b_PFJets__nhf_);
   fChain->SetBranchAddress("PFJets_.phf_", PFJets__phf_, &b_PFJets__phf_);
   fChain->SetBranchAddress("PFJets_.elf_", PFJets__elf_, &b_PFJets__elf_);
   fChain->SetBranchAddress("PFJets_.muf_", PFJets__muf_, &b_PFJets__muf_);
   fChain->SetBranchAddress("PFJets_.hf_hf_", PFJets__hf_hf_, &b_PFJets__hf_hf_);
   fChain->SetBranchAddress("PFJets_.hf_phf_", PFJets__hf_phf_, &b_PFJets__hf_phf_);
   fChain->SetBranchAddress("PFJets_.hf_hm_", PFJets__hf_hm_, &b_PFJets__hf_hm_);
   fChain->SetBranchAddress("PFJets_.hf_phm_", PFJets__hf_phm_, &b_PFJets__hf_phm_);
   fChain->SetBranchAddress("PFJets_.chm_", PFJets__chm_, &b_PFJets__chm_);
   fChain->SetBranchAddress("PFJets_.nhm_", PFJets__nhm_, &b_PFJets__nhm_);
   fChain->SetBranchAddress("PFJets_.phm_", PFJets__phm_, &b_PFJets__phm_);
   fChain->SetBranchAddress("PFJets_.elm_", PFJets__elm_, &b_PFJets__elm_);
   fChain->SetBranchAddress("PFJets_.mum_", PFJets__mum_, &b_PFJets__mum_);
   fChain->SetBranchAddress("PFJets_.ncand_", PFJets__ncand_, &b_PFJets__ncand_);
   fChain->SetBranchAddress("PFJets_.beta_", PFJets__beta_, &b_PFJets__beta_);
   fChain->SetBranchAddress("PFJets_.betaStar_", PFJets__betaStar_, &b_PFJets__betaStar_);
   fChain->SetBranchAddress("FatJets_", &FatJets__, &b_events_FatJets__);
   fChain->SetBranchAddress("FatJets_.P4_.fCoordinates.fX", FatJets__P4__fCoordinates_fX, &b_FatJets__P4__fCoordinates_fX);
   fChain->SetBranchAddress("FatJets_.P4_.fCoordinates.fY", FatJets__P4__fCoordinates_fY, &b_FatJets__P4__fCoordinates_fY);
   fChain->SetBranchAddress("FatJets_.P4_.fCoordinates.fZ", FatJets__P4__fCoordinates_fZ, &b_FatJets__P4__fCoordinates_fZ);
   fChain->SetBranchAddress("FatJets_.P4_.fCoordinates.fT", FatJets__P4__fCoordinates_fT, &b_FatJets__P4__fCoordinates_fT);
   fChain->SetBranchAddress("FatJets_.genP4_.fCoordinates.fX", FatJets__genP4__fCoordinates_fX, &b_FatJets__genP4__fCoordinates_fX);
   fChain->SetBranchAddress("FatJets_.genP4_.fCoordinates.fY", FatJets__genP4__fCoordinates_fY, &b_FatJets__genP4__fCoordinates_fY);
   fChain->SetBranchAddress("FatJets_.genP4_.fCoordinates.fZ", FatJets__genP4__fCoordinates_fZ, &b_FatJets__genP4__fCoordinates_fZ);
   fChain->SetBranchAddress("FatJets_.genP4_.fCoordinates.fT", FatJets__genP4__fCoordinates_fT, &b_FatJets__genP4__fCoordinates_fT);
   fChain->SetBranchAddress("FatJets_.genR_", FatJets__genR_, &b_FatJets__genR_);
   fChain->SetBranchAddress("FatJets_.cor_", FatJets__cor_, &b_FatJets__cor_);
   fChain->SetBranchAddress("FatJets_.unc_", FatJets__unc_, &b_FatJets__unc_);
   fChain->SetBranchAddress("FatJets_.uncSrc_", FatJets__uncSrc_, &b_FatJets__uncSrc_);
   fChain->SetBranchAddress("FatJets_.area_", FatJets__area_, &b_FatJets__area_);
   fChain->SetBranchAddress("FatJets_.looseID_", FatJets__looseID_, &b_FatJets__looseID_);
   fChain->SetBranchAddress("FatJets_.tightID_", FatJets__tightID_, &b_FatJets__tightID_);
   fChain->SetBranchAddress("FatJets_.btag_tche_", FatJets__btag_tche_, &b_FatJets__btag_tche_);
   fChain->SetBranchAddress("FatJets_.btag_tchp_", FatJets__btag_tchp_, &b_FatJets__btag_tchp_);
   fChain->SetBranchAddress("FatJets_.btag_csv_", FatJets__btag_csv_, &b_FatJets__btag_csv_);
   fChain->SetBranchAddress("FatJets_.btag_ssvhe_", FatJets__btag_ssvhe_, &b_FatJets__btag_ssvhe_);
   fChain->SetBranchAddress("FatJets_.btag_ssvhp_", FatJets__btag_ssvhp_, &b_FatJets__btag_ssvhp_);
   fChain->SetBranchAddress("FatJets_.btag_jp_", FatJets__btag_jp_, &b_FatJets__btag_jp_);
   fChain->SetBranchAddress("FatJets_.flavor_", FatJets__flavor_, &b_FatJets__flavor_);
   fChain->SetBranchAddress("FatJets_.status3_", FatJets__status3_, &b_FatJets__status3_);
   fChain->SetBranchAddress("FatJets_.status2_", FatJets__status2_, &b_FatJets__status2_);
   fChain->SetBranchAddress("FatJets_.PartonId_", FatJets__PartonId_, &b_FatJets__PartonId_);
}

Bool_t ProcessedTree::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

#endif // #ifdef ProcessedTree_cxx
