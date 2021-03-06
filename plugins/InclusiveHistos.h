#ifndef InclusiveHistos_h
#define InclusiveHistos_h

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "CMSDIJET/QCDAnalysis/interface/QCDJet.h"
#include "CMSDIJET/QCDAnalysis/interface/QCDEvent.h"
#include "CMSDIJET/QCDAnalysis/interface/QCDEventHdr.h"
#include "CMSDIJET/QCDAnalysis/interface/QCDCaloJet.h"
#include "CMSDIJET/QCDAnalysis/interface/QCDPFJet.h"
#include "CMSDIJET/QCDAnalysis/interface/QCDMET.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TTree.h"
#include "TChain.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TFile.h"
#include "TProfile.h"

class InclusiveHistos : public edm::EDAnalyzer 
{
  public:
    explicit InclusiveHistos(edm::ParameterSet const& cfg);
    virtual void beginJob();
    virtual void analyze(edm::Event const& evt, edm::EventSetup const& iSetup);
    virtual void endJob();
    virtual ~InclusiveHistos();

  private:  
    int getBin(double x, const std::vector<double>& boundaries); 
    int findRun(int x, const std::vector<int>& runs);
    //---- configurable parameters --------   
    bool   mIsMC;
    bool   mApplyHBEHfilter;
    int    mNEvents;
    double mMaxBetaStar;
    double mMaxMETovSumET;
    std::vector<double> mMinPt;
    std::string mTreeName,mDirName,mPUHistName,mPUFileName,mLogName;
    std::vector<double> mYBND,mPTBND;
    std::vector<std::string> mTriggers;
    std::vector<std::string> mFileNames;
    std::vector<std::vector<int> > mTrigIndex;    

    edm::Service<TFileService> fs;
    TFile    *mPUf;
    TH1F     *mBSx,*mBSy,*mBSz,*mNPV,*mPVx,*mPVy,*mPVz,*mPUh,*mGenPU,*hAux[100][6];
    TH1F     *mNPFJets[100][6],*mNCaloJets[100][6],*mNPFNormJets[100][6],*mNCaloNormJets[100][6];
    TH1F     *mPFJetMulti[100],*mCaloJetMulti[100],*mPFMETovSUMET[100],*mCaloMETovSUMET[100];
    TH1F     *mGenPt[6],*mGenX[6],*mPFPt[100][6],*mPFPtPU[100][6],*mPFNormPt[100][6],*mPFX[100][6],*mPFNormX[100][6],*mPFEventsX[100][6],
             *mCaloPt[100][6],*mCaloNormPt[100][6],*mCaloX[100][6],*mCaloNormX[100][6],
             *mCHF[100][6],*mNHF[100][6],*mPHF[100][6],*mELF[100][6],*mMUF[100][6],*mBetaStar[100][6],*mJEC[100][6],
             *mN90hits[100][6],*mEMF[100][6],*mNTrkCalo[100][6],*mNTrkVtx[100][6],*mfHPD[100][6];
    TProfile *mNvtxVsRun; 
    TProfile *mEMFVsRun[100][6],*mNTrkCaloVsRun[100][6],*mNTrkVtxVsRun[100][6];
    TProfile *mNHFVsRun[100][6],*mPHFVsRun[100][6],*mCHFVsRun[100][6],*mELFVsRun[100][6],*mMUFVsRun[100][6];
    TProfile *mCaloRhoVsRun,*mPFRhoVsRun,*mCaloRhoVsNPV,*mPFRhoVsNPV; 
    TH2F     *mPFPtVsNPV[100][6],*mCaloPtVsNPV[100][6];
    //---- TREE variable --------
    QCDEvent *mEvent;
    
};

#endif
