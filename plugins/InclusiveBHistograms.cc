#include <iostream>
#include <sstream>
#include <istream>
#include <fstream>
#include <iomanip>
#include <string>
#include <cmath>
#include <functional>
#include <vector>
#include <cassert>
#include <climits>
#include "TMath.h"

#include "CMSDIJET/QCDAnalysis/plugins/InclusiveBHistograms.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"

using namespace std;

InclusiveBHistograms::InclusiveBHistograms(edm::ParameterSet const& cfg) 
{
	mjj_bins_ = cfg.getParameter<std::vector<double> >("mjj_bins");
	input_file_name_  = cfg.getParameter<std::string> ("filename");
	input_tree_name_  = cfg.getParameter<std::string> ("treename");
}
//////////////////////////////////////////////////////////////////////////////////////////
void InclusiveBHistograms::beginJob() 
{
	input_file_ = TFile::Open(input_file_name_.c_str());
	tree_ = (TTree*)input_file_->Get(input_tree_name_.c_str());
	mEvent = new QCDEvent();
	TBranch *branch = tree_->GetBranch("event");
	branch->SetAddress(&mEvent);
	//--------- book histos -----------------------
	histograms_ = new Root::HistogramManager();
	histograms_->AddPrefix("h_");
	histograms_->AddTFileService(fs_);

	histograms_->AddTH1D("pf_mjj", "m_{jj} [GeV]", 5000, 0., 5000.); // GeV
	histograms_->AddTH1D("pf_deltaeta", "#Delta#eta", 100., -5., 5.);
	histograms_->AddTH2F("pf_mjj_deltaeta", "m_{jj} [GeV]" 500, 0., 5000., "#Delta#eta", 100, -5., 5.);
	histograms_->AddTH2F("pf_btag_csv", "CSV (leading)", 20, 0., 1., "CSV (subleading)", 20, 0., 1.);
}
//////////////////////////////////////////////////////////////////////////////////////////
void InclusiveBHistograms::endJob() 
{
	input_file_->Close();
}
//////////////////////////////////////////////////////////////////////////////////////////
int InclusiveBHistograms::getBin(double x, const std::vector<double>& boundaries)
{
	int i;
	int n = boundaries.size()-1;
	if (x<boundaries[0] || x>=boundaries[n])
		return -1;
	for(i=0;i<n;i++)
	 {
		 if (x>=boundaries[i] && x<boundaries[i+1])
			 return i;
	 }
	return 0;
}
//////////////////////////////////////////////////////////////////////////////////////////
void InclusiveBHistograms::analyze(edm::Event const& evt, edm::EventSetup const& iSetup) 
{ 
	unsigned int n_entries = tree_->GetEntries();
	//cout<<"File: "<<mFileName<<endl;
	//cout<<"Reading TREE: "<<NEntries<<" events"<<endl;
	int decade = 0;
	for(unsigned i=0;i<NEntries;i++) {
		double progress = 10.0*i/(1.0*NEntries);
		int k = TMath::FloorNint(progress); 
		if (k > decade) 
			cout<<10*k<<" %"<<endl;
		decade = k;          
		tree_->GetEntry(i);
		if (mUsePF) {
			if (mEvent->evtHdr().isPVgood() == 1 && mEvent->nPFJets() > 1 ) {   
				// Complex L1 prescales: choose minimum prescale
				std::vector<std::pair<std::string, int> > l1_prescales = mEvent->preL1(0);
				int min_l1_prescale = INT_MAX;
				for (std::vector<std::pair<std::string, int> >::iterator it_ps = l1_prescales.begin(); it_ps != l1_prescales.end(); ++it_ps) {
					if ((*it_ps).second < min_l1_prescale) {
						min_l1_prescale = (*it_ps).second;
					}
				}
				//int prescale = mEvent->preL1(0) * mEvent->preHLT(0);
				int prescale = min_l1_prescale * mEvent->preHLT(0);
				double ymax = TMath::Max(fabs(mEvent->pfjet(0).y()),fabs(mEvent->pfjet(1).y()));
				int ybin = getBin(ymax,mYBND);
				bool cut1 = (mEvent->pfjet(0).looseID() == 1 && mEvent->pfjet(0).ptCor() > mMinPt1);
				bool cut2 = (mEvent->pfjet(1).looseID() == 1 && mEvent->pfjet(1).ptCor() > mMinPt2);
				if (cut1 && cut2 && ybin > -1) {
					double mjj = mEvent->pfmjjcor(0);
					if (mjj >= mMinMass[ybin]) {
						mhM[ybin]->Fill(mjj);
						mhNormM[ybin]->Fill(mjj,prescale);
						if (mjj < mMaxMass[ybin]) {
							mhMETovSUMET[ybin]->Fill(mEvent->pfmet().met_o_sumet());
							mhTruncM[ybin]->Fill(mjj);
							mhNormTruncM[ybin]->Fill(mjj,prescale);
							mhYmax[ybin]->Fill(ymax);             
							for(unsigned j=0;j<2;j++) {
								mhPt[ybin]->Fill((mEvent->pfjet(j)).ptCor());
								mhY[ybin]->Fill((mEvent->pfjet(j)).y());
								mhCHF[ybin]->Fill((mEvent->pfjet(j)).chf());
								mhNHF[ybin]->Fill((mEvent->pfjet(j)).nhf());
								mhPHF[ybin]->Fill((mEvent->pfjet(j)).phf());
							}
						}
					}
				}
			}  
		}
		else {
			if (mEvent->evtHdr().isPVgood() == 1 && mEvent->nCaloJets() > 1 ) {
				// Complex L1 prescales: choose minimum prescale
				std::vector<std::pair<std::string, int> > l1_prescales = mEvent->preL1(0);
				int min_l1_prescale = INT_MAX;
				for (std::vector<std::pair<std::string, int> >::iterator it_ps = l1_prescales.begin(); it_ps != l1_prescales.end(); ++it_ps) {
					if ((*it_ps).second < min_l1_prescale) {
						min_l1_prescale = (*it_ps).second;
					}
				}
				//int prescale = mEvent->preL1(0) * mEvent->preHLT(0);
				int prescale = min_l1_prescale * mEvent->preHLT(0);
				double ymax = TMath::Max(fabs(mEvent->calojet(0).y()),fabs(mEvent->calojet(1).y()));
				int ybin = getBin(ymax,mYBND);
				bool cut1 = (mEvent->calojet(0).looseID() == 1 && mEvent->calojet(0).ptCor() > mMinPt1);
				bool cut2 = (mEvent->calojet(1).looseID() == 1 && mEvent->calojet(1).ptCor() > mMinPt2);
				if (cut1 && cut2 && ybin > -1) {
					double mjj = mEvent->calomjjcor(0);
					if (mjj >= mMinMass[ybin]) {
						mhM[ybin]->Fill(mjj);
						mhNormM[ybin]->Fill(mjj,prescale);
						if (mjj < mMaxMass[ybin]) {
							mhTruncM[ybin]->Fill(mjj);
							mhNormTruncM[ybin]->Fill(mjj,prescale);
							mhYmax[ybin]->Fill(ymax);
							mhMETovSUMET[ybin]->Fill(mEvent->calomet().met_o_sumet());
							for(unsigned j=0;j<2;j++) {
								mhPt[ybin]->Fill((mEvent->calojet(j)).ptCor());
								mhY[ybin]->Fill((mEvent->calojet(j)).y());
								mhEMF[ybin] ->Fill((mEvent->calojet(j)).emf());
								mhN90hits[ybin]->Fill((mEvent->calojet(j)).n90hits());
								mhfHPD[ybin]->Fill((mEvent->calojet(j)).fHPD());
								mhNTrkCalo[ybin]->Fill((mEvent->calojet(j)).nTrkCalo());
								mhNTrkVtx[ybin]->Fill((mEvent->calojet(j)).nTrkVtx());
							}
						}
					}
				}
			}
		}
	}
}
//////////////////////////////////////////////////////////////////////////////////////////

DEFINE_FWK_MODULE(InclusiveBHistograms);
