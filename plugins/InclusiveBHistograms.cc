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
	input_file_names_  = cfg.getParameter<std::vector<std::string> > ("file_names");
	input_tree_name_  = cfg.getParameter<std::string> ("tree_name");
	trigger_histogram_name_  = cfg.getParameter<std::string> ("trigger_histogram_name");
	trigger_list_unparsed_ = cfg.getParameter<std::vector<std::string> >("triggers");
	current_file_ = 0;
	n_total_ = 0;
	n_pass_ = 0;
}

//////////////////////////////////////////////////////////////////////////////////////////
void InclusiveBHistograms::beginJob() 
{
	// Parse HLT and L1 names from trigger list, and look up indices from histogram named trigger_histogram_name_
	for (auto& it_trig : trigger_list_unparsed_) {
		std::cout << "[InclusiveBHistograms::beginJob] DEBUG : Parsing " << it_trig << std::endl;
		std::vector<std::string> tokens;
		std::size_t start = 0, end = 0;
		while ((end = it_trig.find(':', start)) != std::string::npos) {
    		tokens.push_back(it_trig.substr(start, end - start));
			start = end + 1;
		}
		tokens.push_back(it_trig.substr(start));
		if (tokens.size() != 2) {
			throw cms::Exception("[InclusiveBHistograms::beginJob] ERROR : Failed to parse two words out of string ") << it_trig << std::endl;
		}
		triggers_.push_back(std::make_pair<TString, TString>(tokens[0], tokens[1]));
		hlt_triggers_.push_back(tokens[0]);
		l1_triggers_.push_back(tokens[1]);
	}

	TFile *f = new TFile(TString(input_file_names_[0]), "READ");
	TH1F *h_trigger_names = (TH1F*)f->Get(trigger_histogram_name_);
	if (!h_trigger_names) {
		throw cms::Exception("[InclusiveBHistograms::beginJob] ERROR : ") << "Trigger name histogram (" << trigger_histogram_name_ << ") not found in input file." << std::endl;
	}
	std::cout << "Finding HLT trigger index" << std::endl;
	for (auto& it_trig : triggers_) {
		int hlt_index = -1;
		for(int bin = 1; bin <= h_trigger_names->GetNbinsX(); ++bin) {
			string ss = h_trigger_names->GetXaxis()->GetBinLabel(bin);
			if (it_trig.first.EqualTo(ss)) {
				hlt_index = bin - 1; // Bins start from 1, while index starts from 0
				break;
			}
		}
		if (hlt_index == -1) {
			throw cms::Exception("]InclusiveBHistograms::beginJob] ERROR : ") << "Couldn't find index for trigger " << it_trig.first << " in TriggerNames." << std::endl;
		} else {
			hlt_indices_.push_back(hlt_index);
			hlt_index_to_hlt_name_[hlt_index] = it_trig.first;
			hlt_index_to_l1_name_[hlt_index] = it_trig.second; // Record L1 name corresponding to the HLT index
		}
	}

	std::cout << "List of triggers and indices:" << std::endl;
	for (auto& it_index_name : hlt_index_to_hlt_name_) {
		std::cout << "\t" << it_index_name.first << " = " << it_index_name.second << std::endl;
	}
	f->Close();
	delete f;
	f = 0;

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
	event_cuts.push_back("TriggerXOR");
	event_cut_parameters["TriggerXOR"] = std::vector<double>();
	for (auto& it_trig_index : hlt_indices_) {
		event_cut_parameters["TriggerXOR"].push_back((double)it_trig_index);
	}
	event_cut_descriptors["TriggerXOR"] = std::vector<TString>();
	event_cuts.push_back("MaxMetOverSumEt");
	event_cut_parameters["MaxMetOverSumEt"] = std::vector<double>{0.5};
	event_cut_descriptors["MaxMetOverSumEt"] = std::vector<TString>();
	event_cuts.push_back("MinLeadingPFJetPt");
	event_cut_parameters["MinLeadingPFJetPt"] = std::vector<double>{25.};
	event_cut_descriptors["MinLeadingPFJetPt"] = std::vector<TString>();
	event_cuts.push_back("MinSubleadingPFJetPt");
	event_cut_parameters["MinSubleadingPFJetPt"] = std::vector<double>{25.};
	event_cut_descriptors["MinSubleadingPFJetPt"] = std::vector<TString>();
	event_cuts.push_back("PFDijetTightID");
	event_cut_parameters["PFDijetTightID"] = std::vector<double>();
	event_cut_descriptors["PFDijetTightID"] = std::vector<TString>();
	event_cuts.push_back("PFDijetMaxAbsEta");
	event_cut_parameters["PFDijetMaxAbsEta"] = std::vector<double>{2.5};
	event_cut_descriptors["PFDijetMaxAbsEta"] = std::vector<TString>();
	event_cuts.push_back("PFDijetMaxMuonEnergyFraction");
	event_cut_parameters["PFDijetMaxMuonEnergyFraction"] = std::vector<double>{0.8};
	event_cut_descriptors["PFDijetMaxMuonEnergyFraction"] = std::vector<TString>();
	event_cuts.push_back("PFDijetMaxDeltaEta");
	event_cut_parameters["PFDijetMaxDeltaEta"] = std::vector<double>{1.3};
	event_cut_descriptors["PFDijetMaxDeltaEta"] = std::vector<TString>();

	event_selector_ = new EventSelector<QCDEvent>;
	QCDEventCutFunctions::Configure(event_selector_);
	for (auto& it_cut : event_cuts) {
		event_selector_->RegisterCut(it_cut, event_cut_descriptors[it_cut], event_cut_parameters[it_cut]);
	}
	event_selector_->AddObjectSelector(ObjectIdentifiers::kPFJet, pfjet_selector_);


	//--------- Histograms -----------------------
	global_histograms_ = new Root::HistogramManager();
	global_histograms_->AddPrefix("h_");
	global_histograms_->AddTFileService(&fs_);
	global_histograms_->AddTH1F("input_nevents", "input_nevents", "", 1, 0.5, 1.5);
	global_histograms_->AddTH1F("pass_nevents", "pass_nevents", "", 1, 0.5, 1.5);
	global_histograms_->AddTH1F("pass_nevents_weighted", "pass_nevents_weighted", "", 1, 0.5, 1.5);

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
	calojet_histograms_->AddTH1D("mjj", "mjj", "m_{jj} [GeV]", 5000, 0., 5000.); // GeV
	calojet_histograms_->AddTH1D("deltaeta", "deltaeta", "#Delta#eta", 100., -5., 5.);
	calojet_histograms_->AddTH2F("mjj_deltaeta", "mjj_deltaeta", "m_{jj} [GeV]", 500, 0., 5000., "#Delta#eta", 100, -5., 5.);
	calojet_histograms_->AddTH2F("btag_csv", "btag_csv", "CSV (leading)", 20, 0., 1., "CSV (subleading)", 20, 0., 1.);
}


//////////////////////////////////////////////////////////////////////////////////////////
void InclusiveBHistograms::endJob() 
{
	event_selector_->MakeCutflowHistograms(&*fs_);
	event_selector_->SaveNMinusOneHistogram(&*fs_);
	//delete event_;
	//event_ = 0;
	std::cout << "[InclusiveBHistograms::endJob] INFO : Pass / Total = " << n_pass_ << " / " << n_total_ << std::endl;
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
	for (auto& it_filename : input_file_names_) {
		TFile *f = new TFile(TString(it_filename), "READ");
		tree_ = (TTree*)f->Get(input_tree_name_);
		event_ = new QCDEvent();
		tree_->SetBranchStatus("*", 1);
		tree_->SetBranchAddress("events", &event_);

		unsigned int n_entries = tree_->GetEntries();
		//cout<<"File: "<<mFileName<<endl;
		//cout<<"Reading TREE: "<<NEntries<<" events"<<endl;
		int decade = 0;
		for (unsigned int entry = 0; entry < n_entries; ++entry) {
			++n_total_;
			global_histograms_->GetTH1F("input_nevents")->Fill(1);
			double progress = 10.0 * entry / (1.0 * n_entries);
			int k = TMath::FloorNint(progress); 
			if (k > decade) {
				std::cout << 10*k << " %" << std::endl;
			}
			decade = k;          
			tree_->GetEntry(entry);

			// Correct objects?

			// Object selection
			pfjet_selector_->ClassifyObjects(event_->pfjets());

			// Event selection
			event_selector_->ProcessEvent(event_);

			if (event_selector_->Pass()) {
				++n_pass_;
				// Get prescale
				int hlt_index = (int)event_selector_->GetReturnData("TriggerXOR");
				TString L1_name = hlt_index_to_l1_name_[hlt_index];
				double prescale_L1 = -10;
				for (auto& it_l1 : event_->preL1(hlt_index)) {
					if (L1_name.EqualTo(it_l1.first)) {
						prescale_L1 = it_l1.second;
					}
				}
				if (prescale_L1 == -10) {
					throw cms::Exception("[InclusiveBHistograms::analyze] ERROR : Couldn't find L1 prescale for HLT trigger name ") << hlt_index_to_hlt_name_[hlt_index] << " / L1 name " << hlt_index_to_l1_name_[hlt_index] << std::endl;
				}
				double prescale = event_->preHLT(hlt_index) * prescale_L1;
				global_histograms_->GetTH1F("pass_nevents")->Fill(1);
				global_histograms_->GetTH1F("pass_nevents_weighted")->Fill(1, prescale);

				double pf_mjj = (event_->pfjet(0).p4() + event_->pfjet(1).p4()).mass();
				double pf_deltaeta = event_->pfjet(0).eta() - event_->pfjet(1).eta();
				double pf_btag_csv1 = event_->pfjet(0).btag_csv();
				double pf_btag_csv2 = event_->pfjet(1).btag_csv();
				pfjet_histograms_->GetTH1D("mjj")->Fill(pf_mjj, prescale);
				pfjet_histograms_->GetTH1D("deltaeta")->Fill(pf_deltaeta, prescale);
				pfjet_histograms_->GetTH2F("mjj_deltaeta")->Fill(pf_mjj, pf_deltaeta, prescale);
				pfjet_histograms_->GetTH2F("btag_csv")->Fill(pf_btag_csv1, pf_btag_csv2, prescale);

				double calo_mjj = (event_->calojet(0).p4() + event_->calojet(1).p4()).mass();
				double calo_deltaeta = event_->calojet(0).eta() - event_->calojet(1).eta();
				double calo_btag_csv1 = event_->calojet(0).btag_csv();
				double calo_btag_csv2 = event_->calojet(1).btag_csv();
				calojet_histograms_->GetTH1D("mjj")->Fill(calo_mjj, prescale);
				calojet_histograms_->GetTH1D("deltaeta")->Fill(calo_deltaeta, prescale);
				calojet_histograms_->GetTH2F("mjj_deltaeta")->Fill(calo_mjj, calo_deltaeta, prescale);
				calojet_histograms_->GetTH2F("btag_csv")->Fill(calo_btag_csv1, calo_btag_csv2, prescale);

			}
		}
		f->Close();
		delete f;
		f = 0;
		delete event_;
		event_ = 0;
	} // End loop over input files
}
//////////////////////////////////////////////////////////////////////////////////////////

DEFINE_FWK_MODULE(InclusiveBHistograms);
