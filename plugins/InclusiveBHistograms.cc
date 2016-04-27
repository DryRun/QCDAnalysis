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
	trigger_ = std::make_pair<std::string, std::string>(cfg.getParameter<std::string>("HLT"), cfg.getParameter<std::string>("L1"));
}
//////////////////////////////////////////////////////////////////////////////////////////
void InclusiveBHistograms::beginJob() 
{
	input_file_ = TFile::Open(input_file_name_.c_str());
	tree_ = (TTree*)input_file_->Get(input_tree_name_.c_str());
	event_ = new QCDEvent();
	TBranch *branch = tree_->GetBranch("event");
	branch->SetAddress(&event_);

	// Cuts
	std::vector<TString> pfjet_cuts;
	std::map<TString, std::vector<double> > pfjet_cut_parameters;
	std::map<TString, std::vector<TString> > pfjet_cut_descriptors;
	pfjet_cuts.push_back("MinPt");
	pfjet_cut_parameters["MinPt"] = std::vector<double>{30.};
	pfjet_cut_descriptors["MinPt"] = std::vector<TString>();
	pfjet_cuts.push_back("MaxAbsEta");
	pfjet_cut_parameters["MaxAbsEta"] = std::vector<double>{5};
	pfjet_cut_descriptors["MaxAbsEta"] = std::vector<TString>();
	pfjet_cuts.push_back("IsLooseID");
	pfjet_cut_parameters["IsLooseID"] = std::vector<double>();
	pfjet_cut_descriptors["IsLooseID"] = std::vector<TString>();

	pfjet_selector_ = new ObjectSelector<QCDPFJet>;
	PFJetCutFunctions::Configure(pfjet_selector_);
	for (auto& it_cut : pfjet_cuts) {
		pfjet_selector_->RegisterCut(it_cut, pfjet_cut_descriptors[it_cut], pfjet_cut_parameters[it_cut]);
	}

	std::vector<TString> calojet_cuts;
	std::map<TString, std::vector<double> > calojet_cut_parameters;
	std::map<TString, std::vector<TString> > calojet_cut_descriptors;
	calojet_cuts.push_back("MinPt");
	calojet_cut_parameters["MinPt"] = std::vector<double>{30.};
	calojet_cut_descriptors["MinPt"] = std::vector<TString>();

	calojet_selector_ = new ObjectSelector<QCDCaloJet>;
	CaloJetCutFunctions::Configure(calojet_selector_);
	for (auto& it_cut : calojet_cuts) {
		calojet_selector_->RegisterCut(it_cut, calojet_cut_descriptors[it_cut], calojet_cut_parameters[it_cut]);
	}

	std::vector<TString> event_cuts;
	std::map<TString, std::vector<double> > event_cut_parameters;
	std::map<TString, std::vector<TString> > event_cut_descriptors;
	event_cuts.push_back("LeadingJetPt");
	event_cut_parameters["LeadingJetPt"] = std::vector<double>{25.};
	event_cut_descriptors["LeadingJetPt"] = std::vector<TString>();
	event_cuts.push_back("SubleadingJetPt");
	event_cut_parameters["SubleadingJetPt"] = std::vector<double>{25.};
	event_cut_descriptors["SubleadingJetPt"] = std::vector<TString>();
	event_cuts.push_back("DijetTightID");
	event_cut_parameters["DijetTightID"] = std::vector<double>();
	event_cut_descriptors["DijetTightID"] = std::vector<TString>();
	event_cuts.push_back("DijetMaxAbsEta");
	event_cut_parameters["DijetMaxAbsEta"] = std::vector<double>{2.5};
	event_cut_descriptors["DijetMaxAbsEta"] = std::vector<TString>();
	event_cut_parameters["DijetMaxMuonEnergyFraction"] = std::vector<double>{0.8};
	event_cut_descriptors["DijetMaxMuonEnergyFraction"] = std::vector<TString>();
	event_cut_parameters["DijetMaxDeltaEta"] = std::vector<double>{1.3};
	event_cut_descriptors["DijetMaxDeltaEta"] = std::vector<TString>();
	event_cut_parameters["MaxMetOverSumEt"] = std::vector<double>{0.5};
	event_cut_descriptors["MaxMetOverSumEt"] = std::vector<TString>();

	event_selector_ = new EventSelector<QCDEvent>;
	QCDEventCutFunctions::Configure(event_selector_);
	for (auto& it_cut : event_cuts) {
		event_selector_->RegisterCut(it_cut, event_cut_descriptors[it_cut], event_cut_parameters[it_cut]);
	}
	event_selector_->AddObjectSelector(ObjectIdentifiers::kJet, pfjet_selector_);


	//--------- Histograms -----------------------
	global_histograms_ = new Root::HistogramManager();
	global_histograms_->AddPrefix("h_");
	global_histograms_->AddTFileService(&fs_);

	pfjet_histograms_ = new Root::HistogramManager();
	pfjet_histograms_->AddPrefix("h_pfjet_");
	pfjet_histograms_->AddTFileService(&fs_);
	pfjet_histograms_->AddTH1D("mjj", "mjj", "m_{jj} [GeV]", 5000, 0., 5000.); // GeV
	pfjet_histograms_->AddTH1D("deltaeta", "deltaeta", "#Delta#eta", 100., -5., 5.);
	pfjet_histograms_->AddTH2F("mjj_deltaeta", "mjj_deltaeta", "m_{jj} [GeV]", 500, 0., 5000., "#Delta#eta", 100, -5., 5.);
	pfjet_histograms_->AddTH2F("btag_csv", "btag_csv", "CSV (leading)", 20, 0., 1., "CSV (subleading)", 20, 0., 1.);

	calojet_histograms_ = new Root::HistogramManager();
	calojet_histograms_->AddPrefix("h_calojet_");
	calojet_histograms_->AddTFileService(&fs_);
	calojet_histograms_->AddTH1D("calo_mjj", "calo_mjj", "m_{jj} [GeV]", 5000, 0., 5000.); // GeV
	calojet_histograms_->AddTH1D("calo_deltaeta", "calo_deltaeta", "#Delta#eta", 100., -5., 5.);
	calojet_histograms_->AddTH2F("calo_mjj_deltaeta", "calo_mjj_deltaeta", "m_{jj} [GeV]", 500, 0., 5000., "#Delta#eta", 100, -5., 5.);
	calojet_histograms_->AddTH2F("calo_btag_csv", "calo_btag_csv", "CSV (leading)", 20, 0., 1., "CSV (subleading)", 20, 0., 1.);

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
	for (unsigned int i = 0; i < n_entries; i++) {
		double progress = 10.0 * i / (1.0 * n_entries);
		int k = TMath::FloorNint(progress); 
		if (k > decade) {
			std::cout << 10*k << " %" << std::endl;
		}
		decade = k;          
		tree_->GetEntry(i);

		// Correct objects?

		// Object selection
		pfjet_selector_->ClassifyObjects(event_->pfjets());

		// Event selection
		event_selector_->ProcessEvent(event_);

		if (event_selector_->Pass()) {
			
		}

		// Complex L1 prescales: choose minimum prescale
		std::vector<std::pair<std::string, int> > l1_prescales = event_->preL1(0);
		int min_l1_prescale = INT_MAX;
		for (std::vector<std::pair<std::string, int> >::iterator it_ps = l1_prescales.begin(); it_ps != l1_prescales.end(); ++it_ps) {
			if ((*it_ps).second < min_l1_prescale) {
				min_l1_prescale = (*it_ps).second;
			}
		}
		//int prescale = event_->preL1(0) * event_->preHLT(0);
		//int prescale = min_l1_prescale * event_->preHLT(0);

		// PF jets
		if (event_->evtHdr().isPVgood() == 1 && event_->nPFJets() > 1 ) { 
		}  

		// Calo jets
		if (event_->evtHdr().isPVgood() == 1 && event_->nCaloJets() > 1 ) {
		}
	}
}
//////////////////////////////////////////////////////////////////////////////////////////

DEFINE_FWK_MODULE(InclusiveBHistograms);
