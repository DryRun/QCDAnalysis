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

#include "CMSDIJET/QCDAnalysis/plugins/BTriggerEfficiency.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"

using namespace std;

BTriggerEfficiency::BTriggerEfficiency(edm::ParameterSet const& cfg) 
{
	input_file_names_  = cfg.getParameter<std::vector<std::string> > ("file_names");
	input_tree_name_  = cfg.getParameter<std::string> ("tree_name");
	trigger_histogram_name_  = cfg.getParameter<std::string> ("trigger_histogram_name");
	current_file_ = 0;
	n_total_ = 0;
	n_pass_ = 0;
	if (cfg.getParameter<std::string>("data_source") == "collision_data") {
		data_source_ = ObjectIdentifiers::kCollisionData;
	} else if (cfg.getParameter<std::string>("data_source") == "simulation") {
		data_source_ = ObjectIdentifiers::kSimulation;
	} else {
		std::cerr << "[BTriggerEfficiency::BTriggerEfficiency] ERROR : Unknown data source: " << cfg.getParameter<std::string>("data_source") << std::endl;
		exit(1);
	}

	// Cuts
	std::vector<edm::ParameterSet> dijet_vps = cfg.getParameter<std::vector<edm::ParameterSet> >("dijet_cuts");
	for (auto& it_cut : dijet_vps) {
		std::string cut_name = it_cut.getParameter<std::string>("name");
		dijet_cuts_.push_back(cut_name);
		dijet_cut_parameters_[cut_name] = it_cut.getParameter<std::vector<double> >("parameters");
		std::vector<std::string> tmp_vstring = it_cut.getParameter<std::vector<std::string> >("descriptors");
		for (auto& it_str : tmp_vstring) {
			dijet_cut_descriptors_[cut_name].push_back(it_str);
		}
	}
	std::vector<edm::ParameterSet> pfjet_vps = cfg.getParameter<std::vector<edm::ParameterSet> >("pfjet_cuts");
	for (auto& it_cut : pfjet_vps) {
		std::string cut_name = it_cut.getParameter<std::string>("name");
		pfjet_cuts_.push_back(cut_name);
		pfjet_cut_parameters_[cut_name] = it_cut.getParameter<std::vector<double> >("parameters");
		std::vector<std::string> tmp_vstring = it_cut.getParameter<std::vector<std::string> >("descriptors");
		for (auto& it_str : tmp_vstring) {
			pfjet_cut_descriptors_[cut_name].push_back(it_str);
		}
	}
	std::vector<edm::ParameterSet> calojet_vps = cfg.getParameter<std::vector<edm::ParameterSet> >("calojet_cuts");
	for (auto& it_cut : calojet_vps) {
		std::string cut_name = it_cut.getParameter<std::string>("name");
		calojet_cuts_.push_back(cut_name);
		calojet_cut_parameters_[cut_name] = it_cut.getParameter<std::vector<double> >("parameters");
		std::vector<std::string> tmp_vstring = it_cut.getParameter<std::vector<std::string> >("descriptors");
		for (auto& it_str : tmp_vstring) {
			calojet_cut_descriptors_[cut_name].push_back(it_str);
		}
	}
	std::vector<edm::ParameterSet> event_vps = cfg.getParameter<std::vector<edm::ParameterSet> >("event_cuts");
	for (auto& it_cut : event_vps) {
		std::string cut_name = it_cut.getParameter<std::string>("name");
		event_cuts_.push_back(cut_name);
		event_cut_parameters_[cut_name] = it_cut.getParameter<std::vector<double> >("parameters");
		std::vector<std::string> tmp_vstring = it_cut.getParameter<std::vector<std::string> >("descriptors");
		for (auto& it_str : tmp_vstring) {
			event_cut_descriptors_[cut_name].push_back(it_str);
		}
	}

}

//////////////////////////////////////////////////////////////////////////////////////////
void BTriggerEfficiency::beginJob() 
{
	// Setup selector objects
	dijet_selector_ = new ObjectSelector<QCDPFJet>;
	PFJetCutFunctions::Configure(dijet_selector_);
	for (auto& it_cut : dijet_cuts_) {
		dijet_selector_->RegisterCut(it_cut, dijet_cut_descriptors_[it_cut], dijet_cut_parameters_[it_cut]);
	}

	pfjet_selector_ = new ObjectSelector<QCDPFJet>;
	PFJetCutFunctions::Configure(pfjet_selector_);
	for (auto& it_cut : pfjet_cuts_) {
		pfjet_selector_->RegisterCut(it_cut, pfjet_cut_descriptors_[it_cut], pfjet_cut_parameters_[it_cut]);
	}


	calojet_selector_ = new ObjectSelector<QCDCaloJet>;
	CaloJetCutFunctions::Configure(calojet_selector_);
	for (auto& it_cut : calojet_cuts_) {
		calojet_selector_->RegisterCut(it_cut, calojet_cut_descriptors_[it_cut], calojet_cut_parameters_[it_cut]);
	}


	event_selector_ = new EventSelector<QCDEvent>;
	QCDEventCutFunctions::Configure(event_selector_);
	for (auto& it_cut : event_cuts_) {
		event_selector_->RegisterCut(it_cut, event_cut_descriptors_[it_cut], event_cut_parameters_[it_cut]);
	}
	event_selector_->AddObjectSelector(ObjectIdentifiers::kPFJet, dijet_selector_);

	//--------- Histograms -----------------------
	global_histograms_ = new Root::HistogramManager();
	global_histograms_->AddPrefix("h_");
	global_histograms_->AddTFileService(&fs_);
	global_histograms_->AddTH1F("input_nevents", "input_nevents", "", 1, 0.5, 1.5);
	global_histograms_->AddTH1F("pass_nevents", "pass_nevents", "", 1, 0.5, 1.5);

	// Get all trigger names and corresponding indices. Different versions of triggers are lumped together.
	TFile *f = new TFile(TString(input_file_names_[0]), "READ");
	TH1F *h_trigger_names = (TH1F*)f->Get(trigger_histogram_name_);
	if (!h_trigger_names) {
		throw cms::Exception("[BTriggerEfficiency::beginJob] ERROR : ") << "Trigger name histogram (" << trigger_histogram_name_ << ") not found in input file." << std::endl;
	}
	for (int bin = 1; bin <= h_trigger_names->GetNbinsX(); ++bin) {
		TString this_trigger = h_trigger_names->GetXaxis()->GetBinLabel(bin);
		if (!(this_trigger.EqualTo(""))) {
			TString this_trigger_unversioned = this_trigger(0, this_trigger.Length() - 3);
			std::cout << "[debug] this_trigger = " << this_trigger << std::endl;
			std::cout << "[debug] this_trigger_unversioned = " << this_trigger_unversioned << std::endl;
			if (std::find(trigger_paths_.begin(), trigger_paths_.end(), this_trigger_unversioned) == trigger_paths_.end()) {
				trigger_paths_.push_back(this_trigger_unversioned);
			}
			trigger_path_indices_[this_trigger_unversioned].push_back(bin - 1);
			trigger_index_path_[bin - 1] = this_trigger_unversioned;
			std::cout << "[BTriggerEfficiency::beginJob] INFO : Found trigger " << this_trigger << " / index = " << bin - 1 << std::endl;
		}
	}

	std::cout << "[BTriggerEfficiency::beginJob] INFO : Printing list of triggers:" << std::endl;
	for (auto& it_trig : trigger_paths_) {
		std::cout << "[BTriggerEfficiency::beginJob] INFO : \t" << it_trig << std::endl;
	}

	// Make list of all combinations
	global_histograms_->AddTH1D("trigger_counts", "trigger_counts", "", (int)(trigger_paths_.size()), 0.5, trigger_paths_.size() + 0.5);
	global_histograms_->AddTH1D("trigger_counts_prescale", "trigger_counts_prescale", "", (int)(trigger_paths_.size()), 0.5, trigger_paths_.size() + 0.5);
	global_histograms_->AddTH1D("trigger_counts_L1prescale", "trigger_counts_L1prescale", "", (int)(trigger_paths_.size()), 0.5, trigger_paths_.size() + 0.5);
	global_histograms_->AddTH1D("trigger_counts_HLTprescale", "trigger_counts_HLTprescale", "", (int)(trigger_paths_.size()), 0.5, trigger_paths_.size() + 0.5);
	for (auto& it_trig1 : trigger_paths_) {
		histograms_reference_[it_trig1] = new Root::HistogramManager();
		histograms_reference_[it_trig1]->AddPrefix("h_ref" + it_trig1 + "_");
		histograms_reference_[it_trig1]->AddTFileService(&fs_);
		histograms_reference_[it_trig1]->AddTH1D("nevents", "nevents", "", 1, 0.5, 1.5);
		histograms_reference_[it_trig1]->AddTH1D("pfjet_mjj", "pf_mjj", "m_{jj} [GeV]", 2000, 0., 2000.);
		histograms_reference_[it_trig1]->AddTH1D("pfjet_mjj_160_120", "pf_mjj_160_120", "m_{jj} [GeV]", 2000, 0., 2000.);
		histograms_reference_[it_trig1]->AddTH1D("pfjet_mjj_80_70", "pf_mjj_80_70", "m_{jj} [GeV]", 2000, 0., 2000.);
		histograms_reference_[it_trig1]->AddTH1D("pfjet_deltaeta", "pf_deltaeta", "#Delta#eta(jj)", 100, -10., 10.);
		histograms_reference_[it_trig1]->AddTH1D("pfjet_eta1", "pf_eta1", "#eta (leading jet)", 100, -5., 5.);
		histograms_reference_[it_trig1]->AddTH1D("pfjet_eta2", "pf_eta2", "#eta (subleading jet)", 100, -5., 5.);
		histograms_reference_[it_trig1]->AddTH1D("pfjet_pt1", "pf_pt1", "p_{T} (leading jet) [GeV]", 1000, 0., 1000.);
		histograms_reference_[it_trig1]->AddTH1D("pfjet_pt2", "pf_pt2", "p_{T} (subleading jet) [GeV]", 1000, 0., 1000.);
		histograms_reference_[it_trig1]->AddTH2D("pfjet_pt1_pt2", "pf_pt1_pt2", "p_{T} (leading jet) [GeV]", 100, 0., 1000., "p_{T} (subleading jet) [GeV]", 100, 0., 1000.);
		histograms_reference_[it_trig1]->AddTH1D("pfjet_btag_csv1", "pf_btag_csv1", "CSV (leading jet)", 40, -2., 2.);
		histograms_reference_[it_trig1]->AddTH1D("pfjet_btag_csv2", "pf_btag_csv2", "CSV (subleading jet)", 40, -2., 2.);

		histograms_reference_[it_trig1]->AddTH1D("fatjet_mjj", "pf_mjj", "m_{jj} [GeV]", 2000, 0., 2000.);
		histograms_reference_[it_trig1]->AddTH1D("fatjet_mjj_160_120", "pf_mjj_160_120", "m_{jj} [GeV]", 2000, 0., 2000.);
		histograms_reference_[it_trig1]->AddTH1D("fatjet_mjj_80_70", "pf_mjj_80_70", "m_{jj} [GeV]", 2000, 0., 2000.);
		histograms_reference_[it_trig1]->AddTH1D("fatjet_deltaeta", "pf_deltaeta", "#Delta#eta(jj)", 100, -10., 10.);
		histograms_reference_[it_trig1]->AddTH1D("fatjet_eta1", "pf_eta1", "#eta (leading jet)", 100, -5., 5.);
		histograms_reference_[it_trig1]->AddTH1D("fatjet_eta2", "pf_eta2", "#eta (subleading jet)", 100, -5., 5.);
		histograms_reference_[it_trig1]->AddTH1D("fatjet_pt1", "pf_pt1", "p_{T} (leading jet) [GeV]", 1000, 0., 1000.);
		histograms_reference_[it_trig1]->AddTH1D("fatjet_pt2", "pf_pt2", "p_{T} (subleading jet) [GeV]", 1000, 0., 1000.);
		histograms_reference_[it_trig1]->AddTH2D("fatjet_pt1_pt2", "pf_pt1_pt2", "p_{T} (leading jet) [GeV]", 100, 0., 1000., "p_{T} (subleading jet) [GeV]", 100, 0., 1000.);
		histograms_reference_[it_trig1]->AddTH1D("fatjet_btag_csv1", "pf_btag_csv1", "CSV (leading jet)", 40, -2., 2.);
		histograms_reference_[it_trig1]->AddTH1D("fatjet_btag_csv2", "pf_btag_csv2", "CSV (subleading jet)", 40, -2., 2.);

		histograms_reference_[it_trig1]->AddTH1D("nevents_weighted", "nevents", "", 1, 0.5, 1.5);
		histograms_reference_[it_trig1]->AddTH1D("pfjet_mjj_weighted", "pf_mjj", "m_{jj} [GeV]", 2000, 0., 2000.);
		histograms_reference_[it_trig1]->AddTH1D("pfjet_mjj_160_120_weighted", "pf_mjj_160_120", "m_{jj} [GeV]", 2000, 0., 2000.);
		histograms_reference_[it_trig1]->AddTH1D("pfjet_mjj_80_70_weighted", "pf_mjj_80_70", "m_{jj} [GeV]", 2000, 0., 2000.);
		histograms_reference_[it_trig1]->AddTH1D("pfjet_deltaeta_weighted", "pf_deltaeta", "#Delta#eta(jj)", 100, -10., 10.);
		histograms_reference_[it_trig1]->AddTH1D("pfjet_eta1_weighted", "pf_eta1", "#eta (leading jet)", 100, -5., 5.);
		histograms_reference_[it_trig1]->AddTH1D("pfjet_eta2_weighted", "pf_eta2", "#eta (subleading jet)", 100, -5., 5.);
		histograms_reference_[it_trig1]->AddTH1D("pfjet_pt1_weighted", "pf_pt1", "p_{T} (leading jet) [GeV]", 1000, 0., 1000.);
		histograms_reference_[it_trig1]->AddTH1D("pfjet_pt2_weighted", "pf_pt2", "p_{T} (subleading jet) [GeV]", 1000, 0., 1000.);
		histograms_reference_[it_trig1]->AddTH2D("pfjet_pt1_pt2_weighted", "pf_pt1_pt2", "p_{T} (leading jet) [GeV]", 100, 0., 1000., "p_{T} (subleading jet) [GeV]", 100, 0., 1000.);
		histograms_reference_[it_trig1]->AddTH1D("pfjet_btag_csv1_weighted", "pf_btag_csv1", "CSV (leading jet)", 40, -2., 2.);
		histograms_reference_[it_trig1]->AddTH1D("pfjet_btag_csv2_weighted", "pf_btag_csv2", "CSV (subleading jet)", 40, -2., 2.);

		histograms_reference_[it_trig1]->AddTH1D("fatjet_mjj_weighted", "pf_mjj", "m_{jj} [GeV]", 2000, 0., 2000.);
		histograms_reference_[it_trig1]->AddTH1D("fatjet_mjj_160_120_weighted", "pf_mjj_160_120", "m_{jj} [GeV]", 2000, 0., 2000.);
		histograms_reference_[it_trig1]->AddTH1D("fatjet_mjj_80_70_weighted", "pf_mjj_80_70", "m_{jj} [GeV]", 2000, 0., 2000.);
		histograms_reference_[it_trig1]->AddTH1D("fatjet_deltaeta_weighted", "pf_deltaeta", "#Delta#eta(jj)", 100, -10., 10.);
		histograms_reference_[it_trig1]->AddTH1D("fatjet_eta1_weighted", "pf_eta1", "#eta (leading jet)", 100, -5., 5.);
		histograms_reference_[it_trig1]->AddTH1D("fatjet_eta2_weighted", "pf_eta2", "#eta (subleading jet)", 100, -5., 5.);
		histograms_reference_[it_trig1]->AddTH1D("fatjet_pt1_weighted", "pf_pt1", "p_{T} (leading jet) [GeV]", 1000, 0., 1000.);
		histograms_reference_[it_trig1]->AddTH1D("fatjet_pt2_weighted", "pf_pt2", "p_{T} (subleading jet) [GeV]", 1000, 0., 1000.);
		histograms_reference_[it_trig1]->AddTH2D("fatjet_pt1_pt2_weighted", "pf_pt1_pt2", "p_{T} (leading jet) [GeV]", 100, 0., 1000., "p_{T} (subleading jet) [GeV]", 100, 0., 1000.);
		histograms_reference_[it_trig1]->AddTH1D("fatjet_btag_csv1_weighted", "pf_btag_csv1", "CSV (leading jet)", 40, -2., 2.);
		histograms_reference_[it_trig1]->AddTH1D("fatjet_btag_csv2_weighted", "pf_btag_csv2", "CSV (subleading jet)", 40, -2., 2.);

		global_histograms_->GetTH1D("trigger_counts")->GetXaxis()->SetBinLabel(std::find(trigger_paths_.begin(), trigger_paths_.end(), it_trig1) - trigger_paths_.begin() + 1, it_trig1);
		global_histograms_->GetTH1D("trigger_counts_prescale")->GetXaxis()->SetBinLabel(std::find(trigger_paths_.begin(), trigger_paths_.end(), it_trig1) - trigger_paths_.begin() + 1, it_trig1);
		global_histograms_->GetTH1D("trigger_counts_L1prescale")->GetXaxis()->SetBinLabel(std::find(trigger_paths_.begin(), trigger_paths_.end(), it_trig1) - trigger_paths_.begin() + 1, it_trig1);
		global_histograms_->GetTH1D("trigger_counts_HLTprescale")->GetXaxis()->SetBinLabel(std::find(trigger_paths_.begin(), trigger_paths_.end(), it_trig1) - trigger_paths_.begin() + 1, it_trig1);
		for (auto& it_trig2 : trigger_paths_) {
			trigger_combinations_.push_back(std::make_pair(it_trig1, it_trig2));
			histograms_test_[it_trig1][it_trig2] = new Root::HistogramManager();
			histograms_test_[it_trig1][it_trig2]->AddTFileService(&fs_);
			histograms_test_[it_trig1][it_trig2]->AddPrefix("h_test" + it_trig2 + "_ref" + it_trig1 + "_");
			histograms_test_[it_trig1][it_trig2]->AddTH1D("nevents", "nevents", "", 1, 0.5, 1.5);
			histograms_test_[it_trig1][it_trig2]->AddTH1D("pfjet_mjj", "pf_mjj", "m_{jj} [GeV]", 2000, 0., 2000.);
			histograms_test_[it_trig1][it_trig2]->AddTH1D("pfjet_mjj_160_120", "pf_mjj_160_120", "m_{jj} [GeV]", 2000, 0., 2000.);
			histograms_test_[it_trig1][it_trig2]->AddTH1D("pfjet_mjj_80_70", "pf_mjj_80_70", "m_{jj} [GeV]", 2000, 0., 2000.);
			histograms_test_[it_trig1][it_trig2]->AddTH1D("pfjet_deltaeta", "pf_deltaeta", "#Delta#eta(jj)", 100, -10., 10.);
			histograms_test_[it_trig1][it_trig2]->AddTH1D("pfjet_eta1", "pf_eta1", "#eta (leading jet)", 100, -5., 5.);
			histograms_test_[it_trig1][it_trig2]->AddTH1D("pfjet_eta2", "pf_eta2", "#eta (subleading jet)", 100, -5., 5.);
			histograms_test_[it_trig1][it_trig2]->AddTH1D("pfjet_pt1", "pf_pt1", "p_{T} (leading jet) [GeV]", 1000, 0., 1000.);
			histograms_test_[it_trig1][it_trig2]->AddTH1D("pfjet_pt2", "pf_pt2", "p_{T} (subleading jet) [GeV]", 1000, 0., 1000.);
			histograms_test_[it_trig1][it_trig2]->AddTH2D("pfjet_pt1_pt2", "pf_pt1_pt2", "p_{T} (leading jet) [GeV]", 100, 0., 1000., "p_{T} (subleading jet) [GeV]", 100, 0., 1000.);
			histograms_test_[it_trig1][it_trig2]->AddTH1D("pfjet_btag_csv1", "pf_btag_csv1", "CSV (leading jet)", 40, -2., 2.);
			histograms_test_[it_trig1][it_trig2]->AddTH1D("pfjet_btag_csv2", "pf_btag_csv2", "CSV (subleading jet)", 40, -2., 2.);

			histograms_test_[it_trig1][it_trig2]->AddTH1D("fatjet_mjj", "pf_mjj", "m_{jj} [GeV]", 2000, 0., 2000.);
			histograms_test_[it_trig1][it_trig2]->AddTH1D("fatjet_mjj_160_120", "pf_mjj_160_120", "m_{jj} [GeV]", 2000, 0., 2000.);
			histograms_test_[it_trig1][it_trig2]->AddTH1D("fatjet_mjj_80_70", "pf_mjj_80_70", "m_{jj} [GeV]", 2000, 0., 2000.);
			histograms_test_[it_trig1][it_trig2]->AddTH1D("fatjet_deltaeta", "pf_deltaeta", "#Delta#eta(jj)", 100, -10., 10.);
			histograms_test_[it_trig1][it_trig2]->AddTH1D("fatjet_eta1", "pf_eta1", "#eta (leading jet)", 100, -5., 5.);
			histograms_test_[it_trig1][it_trig2]->AddTH1D("fatjet_eta2", "pf_eta2", "#eta (subleading jet)", 100, -5., 5.);
			histograms_test_[it_trig1][it_trig2]->AddTH1D("fatjet_pt1", "pf_pt1", "p_{T} (leading jet) [GeV]", 1000, 0., 1000.);
			histograms_test_[it_trig1][it_trig2]->AddTH1D("fatjet_pt2", "pf_pt2", "p_{T} (subleading jet) [GeV]", 1000, 0., 1000.);
			histograms_test_[it_trig1][it_trig2]->AddTH2D("fatjet_pt1_pt2", "pf_pt1_pt2", "p_{T} (leading jet) [GeV]", 100, 0., 1000., "p_{T} (subleading jet) [GeV]", 100, 0., 1000.);
			histograms_test_[it_trig1][it_trig2]->AddTH1D("fatjet_btag_csv1", "pf_btag_csv1", "CSV (leading jet)", 40, -2., 2.);
			histograms_test_[it_trig1][it_trig2]->AddTH1D("fatjet_btag_csv2", "pf_btag_csv2", "CSV (subleading jet)", 40, -2., 2.);
		}
	}
			
	f->Close();
	delete f;
	f = 0;
}


//////////////////////////////////////////////////////////////////////////////////////////
void BTriggerEfficiency::endJob() 
{
	event_selector_->MakeCutflowHistograms(&*fs_);
	event_selector_->SaveNMinusOneHistogram(&*fs_);
	//delete event_;
	//event_ = 0;
	std::cout << "[BTriggerEfficiency::endJob] INFO : Pass / Total = " << n_pass_ << " / " << n_total_ << std::endl;
}
//////////////////////////////////////////////////////////////////////////////////////////
int BTriggerEfficiency::getBin(double x, const std::vector<double>& boundaries)
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
void BTriggerEfficiency::analyze(edm::Event const& evt, edm::EventSetup const& iSetup) 
{ 
	// Get total number of events
	int total_events = 0;
	for (auto& it_filename : input_file_names_) {
		TFile *f = new TFile(TString(it_filename), "READ");
		tree_ = (TTree*)f->Get(input_tree_name_);
		total_events += tree_->GetEntriesFast();
		f->Close();
		delete f;
	}
	int output_every = TMath::FloorNint(total_events / 20);


	for (auto& it_filename : input_file_names_) {
		TFile *f = new TFile(TString(it_filename), "READ");
		tree_ = (TTree*)f->Get(input_tree_name_);
		event_ = new QCDEvent();
		tree_->SetBranchStatus("*", 1);
		tree_->SetBranchAddress("events", &event_);

		unsigned int n_entries = tree_->GetEntries();
		//cout<<"File: "<<mFileName<<endl;
		//cout<<"Reading TREE: "<<NEntries<<" events"<<endl;
		for (unsigned int entry = 0; entry < n_entries; ++entry) {
			++n_total_;
			if (n_total_ % output_every == 0) {
				std::cout << "On event " << n_total_ << " / " << total_events << std::endl;
			}

			global_histograms_->GetTH1F("input_nevents")->Fill(1);
			tree_->GetEntry(entry);

			// Object selection
			dijet_selector_->ClassifyObjects(event_->pfjets());
			pfjet_selector_->ClassifyObjects(event_->pfjets());

			// Recompute fat jets
			if (event_->nPFJets() >= 2) {
				reco::Particle::LorentzVector lv_fatjet[2];
				lv_fatjet[0] = event_->pfjet(0).p4() * event_->pfjet(0).cor();
				lv_fatjet[1] = event_->pfjet(1).p4() * event_->pfjet(1).cor();
				double sum_pt[2];
				sum_pt[0] = lv_fatjet[0].pt();
				sum_pt[1] = lv_fatjet[1].pt();
				double dsum_pt[2];
				dsum_pt[0] = lv_fatjet[0].pt() * event_->pfjet(0).unc();
				dsum_pt[1] = lv_fatjet[1].pt() * event_->pfjet(1).unc();
				for (unsigned int jet_index = 2; jet_index < event_->nPFJets(); ++jet_index) {
					if (!(pfjet_selector_->GetObjectPass(jet_index))) {
						continue;
					}
					reco::Particle::LorentzVector lv_pfjet = event_->pfjet(jet_index).p4() * event_->pfjet(jet_index).cor();
					double dR1 = deltaR(lv_fatjet[0], lv_pfjet);
					double dR2 = deltaR(lv_fatjet[1], lv_pfjet);
					if ((dR1 <= dR2) && (dR1 < 1.1)) {
						lv_fatjet[0] += lv_pfjet;
						sum_pt[0] += lv_pfjet.pt();
						dsum_pt[0] += lv_pfjet.pt() * event_->pfjet(jet_index).cor();
					} else if (dR2 < 1.1) {
						lv_fatjet[1] += lv_pfjet;
						sum_pt[1] += lv_pfjet.pt();
						dsum_pt[1] += lv_pfjet.pt() * event_->pfjet(jet_index).cor();
					}
				}
				QCDJet fatJet[2];
				vector<float> uncSrc(0);
				for(unsigned i = 0; i < 2; i++) { 
					fatJet[i].setP4(lv_fatjet[i]);
					fatJet[i].setLooseIDFlag(event_->pfjet(i).isLooseID());
					fatJet[i].setTightIDFlag(event_->pfjet(i).isTightID());
					fatJet[i].setCor(1.0);
					fatJet[i].setArea(0.0);
					fatJet[i].setUncSrc(uncSrc); 
					//
					fatJet[i].setBtag_tche(event_->pfjet(i).btag_tche());
					fatJet[i].setBtag_tchp(event_->pfjet(i).btag_tchp());
					fatJet[i].setBtag_csv(event_->pfjet(i).btag_csv()); 
					fatJet[i].setBtag_ssvhe(event_->pfjet(i).btag_ssvhe()); 
					fatJet[i].setBtag_ssvhp(event_->pfjet(i).btag_ssvhp());
					fatJet[i].setBtag_jp(event_->pfjet(i).btag_jp());
					fatJet[i].setFlavor(event_->pfjet(i).flavor());
					fatJet[i].setBstatus(event_->pfjet(i).bstatus3(), event_->pfjet(i).bstatus2());
					fatJet[i].setPartonId(event_->pfjet(i).PartonId());
					//
					if (sum_pt[i] > 0) {
						fatJet[i].setUnc(dsum_pt[i]/sum_pt[i]);
					} else {
						fatJet[i].setUnc(0.0); 
					}
					fatJet[i].setGen(event_->pfjet(i).genp4(),event_->pfjet(i).genR());
				}
				std::vector<QCDJet> fat_jets_vector;
				if (fatJet[0].pt()>fatJet[1].pt()) {
					fat_jets_vector.push_back(fatJet[0]); 
					fat_jets_vector.push_back(fatJet[1]);
				}
				else {
					fat_jets_vector.push_back(fatJet[1]); 
					fat_jets_vector.push_back(fatJet[0]);
				}
	      		event_->setFatJets(fat_jets_vector);
	      	} else {
	      		// Set an empty vector
				std::vector<QCDJet> fat_jets_vector;
	      		event_->setFatJets(fat_jets_vector);
	      	}

			// Event selection
			event_selector_->ProcessEvent(event_);

			if (event_selector_->Pass()) {
				++n_pass_;
				global_histograms_->GetTH1F("pass_nevents")->Fill(1);

				// Calculate kinematics
				double pf_mjj = (event_->pfjet(0).p4() + event_->pfjet(1).p4()).mass();
				double pf_deltaeta = event_->pfjet(0).eta() - event_->pfjet(1).eta();
				double pf_btag_csv1 = event_->pfjet(0).btag_csv();
				double pf_btag_csv2 = event_->pfjet(1).btag_csv();
				double pf_pt1 = event_->pfjet(0).pt();
				double pf_pt2 = event_->pfjet(1).pt();
				double pf_eta1 = event_->pfjet(0).eta();
				double pf_eta2 = event_->pfjet(1).eta();

				double fat_mjj = (event_->fatjet(0).p4() + event_->fatjet(1).p4()).mass();
				double fat_deltaeta = event_->fatjet(0).eta() - event_->fatjet(1).eta();
				double fat_btag_csv1 = event_->fatjet(0).btag_csv();
				double fat_btag_csv2 = event_->fatjet(1).btag_csv();
				double fat_pt1 = event_->fatjet(0).pt();
				double fat_pt2 = event_->fatjet(1).pt();
				double fat_eta1 = event_->fatjet(0).eta();
				double fat_eta2 = event_->fatjet(1).eta();

				for (auto& ref_trigger : trigger_paths_) {
					// Loop over trigger indices associated with the trigger name (i.e. over trigger versions)
					//int test_hlt_index = -1;
					int ref_hlt_index = -1;
					bool pass_ref = false;
					for (auto& it_trig_index : trigger_path_indices_[ref_trigger]) {
						if (data_source_ == ObjectIdentifiers::kCollisionData) {
							if (event_->fired(it_trig_index) == 1) {
								pass_ref = true;
								ref_hlt_index = it_trig_index;
								break;
							}
						} else {
							// Simulation doesn't have trigger yet... 
							pass_ref = true;
							ref_hlt_index = 0;
						}
					} 
					if (pass_ref) {
						double ref_l1_prescale  = (data_source_ == ObjectIdentifiers::kCollisionData ? event_->minPreL1(ref_hlt_index) : 1);
						double ref_hlt_prescale = (data_source_ == ObjectIdentifiers::kCollisionData ? event_->preHLT(ref_hlt_index) : 1);
						double ref_prescale     = (data_source_ == ObjectIdentifiers::kCollisionData ? ref_hlt_prescale * ref_l1_prescale : 1);
						if (ref_l1_prescale < 0) {
							std::cerr << "[BTriggerEfficiency::analyze] WARNING : Didn't find L1 prescale for HLT index " << ref_hlt_index << " / name = " << ref_trigger << std::endl;
						}
						global_histograms_->GetTH1D("trigger_counts")->Fill(ref_trigger.Data(), 1.);
						global_histograms_->GetTH1D("trigger_counts_prescale")->Fill(ref_trigger.Data(), ref_prescale);
						global_histograms_->GetTH1D("trigger_counts_L1prescale")->Fill(ref_trigger.Data(), ref_l1_prescale);
						global_histograms_->GetTH1D("trigger_counts_HLTprescale")->Fill(ref_trigger.Data(), ref_hlt_prescale);

						histograms_reference_[ref_trigger]->GetTH1D("nevents")->Fill(1);
						histograms_reference_[ref_trigger]->GetTH1D("pfjet_mjj")->Fill(pf_mjj);
						histograms_reference_[ref_trigger]->GetTH1D("fatjet_mjj")->Fill(fat_mjj);
						if (pf_pt1 > 160. && pf_pt2 > 120. && TMath::Abs(pf_eta1) < 2.2 && TMath::Abs(pf_eta2) < 2.2) {
							histograms_reference_[ref_trigger]->GetTH1D("pfjet_mjj_160_120")->Fill(pf_mjj);
							histograms_reference_[ref_trigger]->GetTH1D("fatjet_mjj_160_120")->Fill(fat_mjj);
						}
						if (pf_pt1 > 80. && pf_pt2 > 70. && TMath::Abs(pf_eta1) < 1.7 && TMath::Abs(pf_eta2) < 1.7) {
							histograms_reference_[ref_trigger]->GetTH1D("pfjet_mjj_80_70")->Fill(pf_mjj);
							histograms_reference_[ref_trigger]->GetTH1D("fatjet_mjj_80_70")->Fill(fat_mjj);
						}
						histograms_reference_[ref_trigger]->GetTH1D("pfjet_deltaeta")->Fill(pf_deltaeta);
						histograms_reference_[ref_trigger]->GetTH1D("pfjet_eta1")->Fill(pf_eta1);
						histograms_reference_[ref_trigger]->GetTH1D("pfjet_eta2")->Fill(pf_eta2);
						histograms_reference_[ref_trigger]->GetTH1D("pfjet_pt1")->Fill(pf_pt1);
						histograms_reference_[ref_trigger]->GetTH1D("pfjet_pt2")->Fill(pf_pt2);
						histograms_reference_[ref_trigger]->GetTH2D("pfjet_pt1_pt2")->Fill(pf_pt1, pf_pt2);
						histograms_reference_[ref_trigger]->GetTH1D("pfjet_btag_csv1")->Fill(pf_btag_csv1);
						histograms_reference_[ref_trigger]->GetTH1D("pfjet_btag_csv2")->Fill(pf_btag_csv2);


						histograms_reference_[ref_trigger]->GetTH1D("fatjet_deltaeta")->Fill(fat_deltaeta);
						histograms_reference_[ref_trigger]->GetTH1D("fatjet_eta1")->Fill(fat_eta1);
						histograms_reference_[ref_trigger]->GetTH1D("fatjet_eta2")->Fill(fat_eta2);
						histograms_reference_[ref_trigger]->GetTH1D("fatjet_pt1")->Fill(fat_pt1);
						histograms_reference_[ref_trigger]->GetTH1D("fatjet_pt2")->Fill(fat_pt2);
						histograms_reference_[ref_trigger]->GetTH2D("fatjet_pt1_pt2")->Fill(fat_pt1, fat_pt2);
						histograms_reference_[ref_trigger]->GetTH1D("fatjet_btag_csv1")->Fill(fat_btag_csv1);
						histograms_reference_[ref_trigger]->GetTH1D("fatjet_btag_csv2")->Fill(fat_btag_csv2);

						histograms_reference_[ref_trigger]->GetTH1D("nevents_weighted")->Fill(1, ref_prescale);
						histograms_reference_[ref_trigger]->GetTH1D("pfjet_mjj_weighted")->Fill(pf_mjj, ref_prescale);
						histograms_reference_[ref_trigger]->GetTH1D("fatjet_mjj_weighted")->Fill(fat_mjj, ref_prescale);
						if (pf_pt1 > 160. && pf_pt2 > 120. && TMath::Abs(pf_eta1) < 2.2 && TMath::Abs(pf_eta2) < 2.2) {
							histograms_reference_[ref_trigger]->GetTH1D("pfjet_mjj_160_120_weighted")->Fill(pf_mjj, ref_prescale);
							histograms_reference_[ref_trigger]->GetTH1D("fatjet_mjj_160_120_weighted")->Fill(fat_mjj, ref_prescale);
						}
						if (pf_pt1 > 80. && pf_pt2 > 70. && TMath::Abs(pf_eta1) < 1.7 && TMath::Abs(pf_eta2) < 1.7) {
							histograms_reference_[ref_trigger]->GetTH1D("pfjet_mjj_80_70_weighted")->Fill(pf_mjj, ref_prescale);
							histograms_reference_[ref_trigger]->GetTH1D("fatjet_mjj_80_70_weighted")->Fill(fat_mjj, ref_prescale);
						}
						histograms_reference_[ref_trigger]->GetTH1D("pfjet_deltaeta_weighted")->Fill(pf_deltaeta, ref_prescale);
						histograms_reference_[ref_trigger]->GetTH1D("pfjet_eta1_weighted")->Fill(pf_eta1, ref_prescale);
						histograms_reference_[ref_trigger]->GetTH1D("pfjet_eta2_weighted")->Fill(pf_eta2, ref_prescale);
						histograms_reference_[ref_trigger]->GetTH1D("pfjet_pt1_weighted")->Fill(pf_pt1, ref_prescale);
						histograms_reference_[ref_trigger]->GetTH1D("pfjet_pt2_weighted")->Fill(pf_pt2, ref_prescale);
						histograms_reference_[ref_trigger]->GetTH2D("pfjet_pt1_pt2_weighted")->Fill(pf_pt1, pf_pt2, ref_prescale);
						histograms_reference_[ref_trigger]->GetTH1D("pfjet_btag_csv1_weighted")->Fill(pf_btag_csv1, ref_prescale);
						histograms_reference_[ref_trigger]->GetTH1D("pfjet_btag_csv2_weighted")->Fill(pf_btag_csv2, ref_prescale);

						histograms_reference_[ref_trigger]->GetTH1D("fatjet_deltaeta_weighted")->Fill(fat_deltaeta, ref_prescale);
						histograms_reference_[ref_trigger]->GetTH1D("fatjet_eta1_weighted")->Fill(fat_eta1, ref_prescale);
						histograms_reference_[ref_trigger]->GetTH1D("fatjet_eta2_weighted")->Fill(fat_eta2, ref_prescale);
						histograms_reference_[ref_trigger]->GetTH1D("fatjet_pt1_weighted")->Fill(fat_pt1, ref_prescale);
						histograms_reference_[ref_trigger]->GetTH1D("fatjet_pt2_weighted")->Fill(fat_pt2, ref_prescale);
						histograms_reference_[ref_trigger]->GetTH2D("fatjet_pt1_pt2_weighted")->Fill(fat_pt1, fat_pt2, ref_prescale);
						histograms_reference_[ref_trigger]->GetTH1D("fatjet_btag_csv1_weighted")->Fill(fat_btag_csv1, ref_prescale);
						histograms_reference_[ref_trigger]->GetTH1D("fatjet_btag_csv2_weighted")->Fill(fat_btag_csv2, ref_prescale);
						
						for (auto& test_trigger : trigger_paths_) {
							bool pass_test = false;
							if (data_source_ == ObjectIdentifiers::kCollisionData) {
								for (auto& it_trig_index : trigger_path_indices_[test_trigger]) {
									if (event_->fired(it_trig_index) == 1) {
										pass_test = true;
										//test_hlt_index = it_trig_index;
										break;
									}
								} 
							} else {
								pass_test = true;
							}
							if (pass_test) {
								histograms_test_[ref_trigger][test_trigger]->GetTH1D("nevents")->Fill(1);
								histograms_test_[ref_trigger][test_trigger]->GetTH1D("pfjet_mjj")->Fill(pf_mjj);
								histograms_test_[ref_trigger][test_trigger]->GetTH1D("fatjet_mjj")->Fill(fat_mjj);
								if (pf_pt1 > 160. && pf_pt2 > 120. && TMath::Abs(pf_eta1) < 2.2 && TMath::Abs(pf_eta2) < 2.2) {
									histograms_test_[ref_trigger][test_trigger]->GetTH1D("pfjet_mjj_160_120")->Fill(pf_mjj);
									histograms_test_[ref_trigger][test_trigger]->GetTH1D("fatjet_mjj_160_120")->Fill(fat_mjj);
								}
								if (pf_pt1 > 80. && pf_pt2 > 70. && TMath::Abs(pf_eta1) < 1.7 && TMath::Abs(pf_eta2) < 1.7) {
									histograms_test_[ref_trigger][test_trigger]->GetTH1D("pfjet_mjj_80_70")->Fill(pf_mjj);
									histograms_test_[ref_trigger][test_trigger]->GetTH1D("fatjet_mjj_80_70")->Fill(fat_mjj);
								}
								histograms_test_[ref_trigger][test_trigger]->GetTH1D("pfjet_deltaeta")->Fill(fat_deltaeta);
								histograms_test_[ref_trigger][test_trigger]->GetTH1D("pfjet_eta1")->Fill(fat_eta1);
								histograms_test_[ref_trigger][test_trigger]->GetTH1D("pfjet_eta2")->Fill(fat_eta2);
								histograms_test_[ref_trigger][test_trigger]->GetTH1D("pfjet_pt1")->Fill(fat_pt1);
								histograms_test_[ref_trigger][test_trigger]->GetTH1D("pfjet_pt2")->Fill(fat_pt2);
								histograms_test_[ref_trigger][test_trigger]->GetTH2D("pfjet_pt1_pt2")->Fill(fat_pt1, fat_pt2);
								histograms_test_[ref_trigger][test_trigger]->GetTH1D("pfjet_btag_csv1")->Fill(fat_btag_csv1);
								histograms_test_[ref_trigger][test_trigger]->GetTH1D("pfjet_btag_csv2")->Fill(fat_btag_csv2);

								histograms_test_[ref_trigger][test_trigger]->GetTH1D("fatjet_deltaeta")->Fill(fat_deltaeta);
								histograms_test_[ref_trigger][test_trigger]->GetTH1D("fatjet_eta1")->Fill(fat_eta1);
								histograms_test_[ref_trigger][test_trigger]->GetTH1D("fatjet_eta2")->Fill(fat_eta2);
								histograms_test_[ref_trigger][test_trigger]->GetTH1D("fatjet_pt1")->Fill(fat_pt1);
								histograms_test_[ref_trigger][test_trigger]->GetTH1D("fatjet_pt2")->Fill(fat_pt2);
								histograms_test_[ref_trigger][test_trigger]->GetTH2D("fatjet_pt1_pt2")->Fill(fat_pt1, fat_pt2);
								histograms_test_[ref_trigger][test_trigger]->GetTH1D("fatjet_btag_csv1")->Fill(fat_btag_csv1);
								histograms_test_[ref_trigger][test_trigger]->GetTH1D("fatjet_btag_csv2")->Fill(fat_btag_csv2);
							}
						}
					}
				}
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

DEFINE_FWK_MODULE(BTriggerEfficiency);
