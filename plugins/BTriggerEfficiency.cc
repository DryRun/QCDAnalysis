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
}

//////////////////////////////////////////////////////////////////////////////////////////
void BTriggerEfficiency::beginJob() 
{
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
		histograms_reference_[it_trig1]->AddTH1D("pf_mjj", "pf_mjj", "m_{jj} [GeV]", 2000, 0., 2000.);
		histograms_reference_[it_trig1]->AddTH1D("pf_mjj_160_120", "pf_mjj_160_120", "m_{jj} [GeV]", 2000, 0., 2000.);
		histograms_reference_[it_trig1]->AddTH1D("pf_mjj_80_70", "pf_mjj_80_70", "m_{jj} [GeV]", 2000, 0., 2000.);
		histograms_reference_[it_trig1]->AddTH1D("pf_deltaeta", "pf_deltaeta", "#Delta#eta(jj)", 100, -10., 10.);
		histograms_reference_[it_trig1]->AddTH1D("pf_eta1", "pf_eta1", "#eta (leading jet)", 100, -5., 5.);
		histograms_reference_[it_trig1]->AddTH1D("pf_eta2", "pf_eta2", "#eta (subleading jet)", 100, -5., 5.);
		histograms_reference_[it_trig1]->AddTH1D("pf_pt1", "pf_pt1", "p_{T} (leading jet) [GeV]", 1000, 0., 1000.);
		histograms_reference_[it_trig1]->AddTH1D("pf_pt2", "pf_pt2", "p_{T} (subleading jet) [GeV]", 1000, 0., 1000.);
		histograms_reference_[it_trig1]->AddTH2D("pf_pt1_pt2", "pf_pt1_pt2", "p_{T} (leading jet) [GeV]", 100, 0., 1000., "p_{T} (subleading jet) [GeV]", 100, 0., 1000.);
		histograms_reference_[it_trig1]->AddTH1D("pf_btag_csv1", "pf_btag_csv1", "CSV (leading jet)", 40, -2., 2.);
		histograms_reference_[it_trig1]->AddTH1D("pf_btag_csv2", "pf_btag_csv2", "CSV (subleading jet)", 40, -2., 2.);

		histograms_reference_[it_trig1]->AddTH1D("nevents_weighted", "nevents", "", 1, 0.5, 1.5);
		histograms_reference_[it_trig1]->AddTH1D("pf_mjj_weighted", "pf_mjj", "m_{jj} [GeV]", 2000, 0., 2000.);
		histograms_reference_[it_trig1]->AddTH1D("pf_mjj_160_120_weighted", "pf_mjj_160_120", "m_{jj} [GeV]", 2000, 0., 2000.);
		histograms_reference_[it_trig1]->AddTH1D("pf_mjj_80_70_weighted", "pf_mjj_80_70", "m_{jj} [GeV]", 2000, 0., 2000.);
		histograms_reference_[it_trig1]->AddTH1D("pf_deltaeta_weighted", "pf_deltaeta", "#Delta#eta(jj)", 100, -10., 10.);
		histograms_reference_[it_trig1]->AddTH1D("pf_eta1_weighted", "pf_eta1", "#eta (leading jet)", 100, -5., 5.);
		histograms_reference_[it_trig1]->AddTH1D("pf_eta2_weighted", "pf_eta2", "#eta (subleading jet)", 100, -5., 5.);
		histograms_reference_[it_trig1]->AddTH1D("pf_pt1_weighted", "pf_pt1", "p_{T} (leading jet) [GeV]", 1000, 0., 1000.);
		histograms_reference_[it_trig1]->AddTH1D("pf_pt2_weighted", "pf_pt2", "p_{T} (subleading jet) [GeV]", 1000, 0., 1000.);
		histograms_reference_[it_trig1]->AddTH2D("pf_pt1_pt2_weighted", "pf_pt1_pt2", "p_{T} (leading jet) [GeV]", 100, 0., 1000., "p_{T} (subleading jet) [GeV]", 100, 0., 1000.);
		histograms_reference_[it_trig1]->AddTH1D("pf_btag_csv1_weighted", "pf_btag_csv1", "CSV (leading jet)", 40, -2., 2.);
		histograms_reference_[it_trig1]->AddTH1D("pf_btag_csv2_weighted", "pf_btag_csv2", "CSV (subleading jet)", 40, -2., 2.);

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
			histograms_test_[it_trig1][it_trig2]->AddTH1D("pf_mjj", "pf_mjj", "m_{jj} [GeV]", 2000, 0., 2000.);
			histograms_test_[it_trig1][it_trig2]->AddTH1D("pf_mjj_160_120", "pf_mjj_160_120", "m_{jj} [GeV]", 2000, 0., 2000.);
			histograms_test_[it_trig1][it_trig2]->AddTH1D("pf_mjj_80_70", "pf_mjj_80_70", "m_{jj} [GeV]", 2000, 0., 2000.);
			histograms_test_[it_trig1][it_trig2]->AddTH1D("pf_deltaeta", "pf_deltaeta", "#Delta#eta(jj)", 100, -10., 10.);
			histograms_test_[it_trig1][it_trig2]->AddTH1D("pf_eta1", "pf_eta1", "#eta (leading jet)", 100, -5., 5.);
			histograms_test_[it_trig1][it_trig2]->AddTH1D("pf_eta2", "pf_eta2", "#eta (subleading jet)", 100, -5., 5.);
			histograms_test_[it_trig1][it_trig2]->AddTH1D("pf_pt1", "pf_pt1", "p_{T} (leading jet) [GeV]", 1000, 0., 1000.);
			histograms_test_[it_trig1][it_trig2]->AddTH1D("pf_pt2", "pf_pt2", "p_{T} (subleading jet) [GeV]", 1000, 0., 1000.);
			histograms_test_[it_trig1][it_trig2]->AddTH2D("pf_pt1_pt2", "pf_pt1_pt2", "p_{T} (leading jet) [GeV]", 100, 0., 1000., "p_{T} (subleading jet) [GeV]", 100, 0., 1000.);
			histograms_test_[it_trig1][it_trig2]->AddTH1D("pf_btag_csv1", "pf_btag_csv1", "CSV (leading jet)", 40, -2., 2.);
			histograms_test_[it_trig1][it_trig2]->AddTH1D("pf_btag_csv2", "pf_btag_csv2", "CSV (subleading jet)", 40, -2., 2.);
		}
	}
			
	f->Close();
	delete f;
	f = 0;

	// Cuts
	std::vector<TString> dijet_cuts;
	std::map<TString, std::vector<double> > dijet_cut_parameters;
	std::map<TString, std::vector<TString> > dijet_cut_descriptors;
	dijet_cuts.push_back("MinPt");
	dijet_cut_parameters["MinPt"] = std::vector<double>{30.};
	dijet_cut_descriptors["MinPt"] = std::vector<TString>();
	dijet_cuts.push_back("MaxAbsEta");
	dijet_cut_parameters["MaxAbsEta"] = std::vector<double>{2.4};
	dijet_cut_descriptors["MaxAbsEta"] = std::vector<TString>();
	dijet_cuts.push_back("IsTightID");
	dijet_cut_parameters["IsTightID"] = std::vector<double>();
	dijet_cut_descriptors["IsTightID"] = std::vector<TString>();
	dijet_cuts.push_back("MaxMuonEnergyFraction");
	dijet_cut_parameters["MaxMuonEnergyFraction"] = std::vector<double>{0.8};
	dijet_cut_descriptors["MaxMuonEnergyFraction"] = std::vector<TString>();
	dijet_cuts.push_back("MinBTagWeight");
	dijet_cut_parameters["MinBTagWeight"] = std::vector<double>{0.244};
	dijet_cut_descriptors["MinBTagWeight"] = std::vector<TString>{"csv"};
	dijet_selector_ = new ObjectSelector<QCDPFJet>;
	PFJetCutFunctions::Configure(dijet_selector_);
	for (auto& it_cut : dijet_cuts) {
		dijet_selector_->RegisterCut(it_cut, dijet_cut_descriptors[it_cut], dijet_cut_parameters[it_cut]);
	}

	// No generic PF or calo stuff for now. Maybe consider re-adding if you need fat jets. 
	//std::vector<TString> pfjet_cuts;
	//std::map<TString, std::vector<double> > pfjet_cut_parameters;
	//std::map<TString, std::vector<TString> > pfjet_cut_descriptors;
	//pfjet_cuts.push_back("MinPt");
	//pfjet_cut_parameters["MinPt"] = std::vector<double>{30.};
	//pfjet_cut_descriptors["MinPt"] = std::vector<TString>();
	//pfjet_cuts.push_back("MaxAbsEta");
	//pfjet_cut_parameters["MaxAbsEta"] = std::vector<double>{5};
	//pfjet_cut_descriptors["MaxAbsEta"] = std::vector<TString>();
	//pfjet_cuts.push_back("IsLooseID");
	//pfjet_cut_parameters["IsLooseID"] = std::vector<double>();
	//pfjet_cut_descriptors["IsLooseID"] = std::vector<TString>();

//	//pfjet_selector_ = new ObjectSelector<QCDPFJet>;
	//PFJetCutFunctions::Configure(pfjet_selector_);
	//for (auto& it_cut : pfjet_cuts) {
	//	pfjet_selector_->RegisterCut(it_cut, pfjet_cut_descriptors[it_cut], pfjet_cut_parameters[it_cut]);
	//}

//	//std::vector<TString> calojet_cuts;
	//std::map<TString, std::vector<double> > calojet_cut_parameters;
	//std::map<TString, std::vector<TString> > calojet_cut_descriptors;
	//calojet_cuts.push_back("MinPt");
	//calojet_cut_parameters["MinPt"] = std::vector<double>{30.};
	//calojet_cut_descriptors["MinPt"] = std::vector<TString>();

//	//calojet_selector_ = new ObjectSelector<QCDCaloJet>;
	//CaloJetCutFunctions::Configure(calojet_selector_);
	//for (auto& it_cut : calojet_cuts) {
	//	calojet_selector_->RegisterCut(it_cut, calojet_cut_descriptors[it_cut], calojet_cut_parameters[it_cut]);
	//}

	std::vector<TString> event_cuts;
	std::map<TString, std::vector<double> > event_cut_parameters;
	std::map<TString, std::vector<TString> > event_cut_descriptors;
	event_cuts.push_back("MaxMetOverSumEt");
	event_cut_parameters["MaxMetOverSumEt"] = std::vector<double>{0.5};
	event_cut_descriptors["MaxMetOverSumEt"] = std::vector<TString>();
	event_cuts.push_back("GoodPFDijet");
	event_cut_parameters["GoodPFDijet"] = std::vector<double>();
	event_cut_descriptors["GoodPFDijet"] = std::vector<TString>();
	//event_cuts.push_back("MinLeadingPFJetPt");
	//event_cut_parameters["MinLeadingPFJetPt"] = std::vector<double>{160.};
	//event_cut_descriptors["MinLeadingPFJetPt"] = std::vector<TString>();
	//event_cuts.push_back("MinSubleadingPFJetPt");
	//event_cut_parameters["MinSubleadingPFJetPt"] = std::vector<double>{120.};
	//event_cut_descriptors["MinSubleadingPFJetPt"] = std::vector<TString>();
	event_cuts.push_back("PFDijetMaxDeltaEta");
	event_cut_parameters["PFDijetMaxDeltaEta"] = std::vector<double>{1.3};
	event_cut_descriptors["PFDijetMaxDeltaEta"] = std::vector<TString>();

	event_selector_ = new EventSelector<QCDEvent>;
	QCDEventCutFunctions::Configure(event_selector_);
	for (auto& it_cut : event_cuts) {
		event_selector_->RegisterCut(it_cut, event_cut_descriptors[it_cut], event_cut_parameters[it_cut]);
	}
	event_selector_->AddObjectSelector(ObjectIdentifiers::kPFJet, dijet_selector_);



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

			// Correct objects?

			// Object selection
			dijet_selector_->ClassifyObjects(event_->pfjets());

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

				for (auto& ref_trigger : trigger_paths_) {
					// Loop over trigger indices associated with the trigger name (i.e. over trigger versions)
					//int test_hlt_index = -1;
					int ref_hlt_index = -1;
					bool pass_ref = false;
					for (auto& it_trig_index : trigger_path_indices_[ref_trigger]) {
						if (event_->fired(it_trig_index) == 1) {
							pass_ref = true;
							ref_hlt_index = it_trig_index;
							break;
						}
					} 
					if (pass_ref) {
						double ref_l1_prescale = event_->minPreL1(ref_hlt_index);
						double ref_hlt_prescale = event_->preHLT(ref_hlt_index);
						double ref_prescale = ref_hlt_prescale * ref_l1_prescale;
						if (ref_l1_prescale < 0) {
							std::cerr << "[BTriggerEfficiency::analyze] WARNING : Didn't find L1 prescale for HLT index " << ref_hlt_index << " / name = " << ref_trigger << std::endl;
						}
						global_histograms_->GetTH1D("trigger_counts")->Fill(ref_trigger.Data(), 1.);
						global_histograms_->GetTH1D("trigger_counts_prescale")->Fill(ref_trigger.Data(), ref_prescale);
						global_histograms_->GetTH1D("trigger_counts_L1prescale")->Fill(ref_trigger.Data(), ref_l1_prescale);
						global_histograms_->GetTH1D("trigger_counts_HLTprescale")->Fill(ref_trigger.Data(), ref_hlt_prescale);

						histograms_reference_[ref_trigger]->GetTH1D("nevents")->Fill(1);
						histograms_reference_[ref_trigger]->GetTH1D("pf_mjj")->Fill(pf_mjj);
						if (pf_pt1 > 160. && pf_pt2 > 120. && TMath::Abs(pf_eta1) < 2.4 && TMath::Abs(pf_eta2) < 2.4) {
							histograms_reference_[ref_trigger]->GetTH1D("pf_mjj_160_120")->Fill(pf_mjj);
						}
						if (pf_pt1 > 80. && pf_pt2 > 70. && TMath::Abs(pf_eta1) < 1.7 && TMath::Abs(pf_eta2) < 1.7) {
							histograms_reference_[ref_trigger]->GetTH1D("pf_mjj_80_70")->Fill(pf_mjj);
						}
						histograms_reference_[ref_trigger]->GetTH1D("pf_deltaeta")->Fill(pf_deltaeta);
						histograms_reference_[ref_trigger]->GetTH1D("pf_eta1")->Fill(pf_eta1);
						histograms_reference_[ref_trigger]->GetTH1D("pf_eta2")->Fill(pf_eta2);
						histograms_reference_[ref_trigger]->GetTH1D("pf_pt1")->Fill(pf_pt1);
						histograms_reference_[ref_trigger]->GetTH1D("pf_pt2")->Fill(pf_pt2);
						histograms_reference_[ref_trigger]->GetTH2D("pf_pt1_pt2")->Fill(pf_pt1, pf_pt2);
						histograms_reference_[ref_trigger]->GetTH1D("pf_btag_csv1")->Fill(pf_btag_csv1);
						histograms_reference_[ref_trigger]->GetTH1D("pf_btag_csv2")->Fill(pf_btag_csv2);

						histograms_reference_[ref_trigger]->GetTH1D("nevents_weighted")->Fill(1, ref_prescale);
						histograms_reference_[ref_trigger]->GetTH1D("pf_mjj_weighted")->Fill(pf_mjj, ref_prescale);
						if (pf_pt1 > 160. && pf_pt2 > 120. && TMath::Abs(pf_eta1) < 2.4 && TMath::Abs(pf_eta2) < 2.4) {
							histograms_reference_[ref_trigger]->GetTH1D("pf_mjj_160_120_weighted")->Fill(pf_mjj, ref_prescale);
						}
						if (pf_pt1 > 80. && pf_pt2 > 70. && TMath::Abs(pf_eta1) < 1.7 && TMath::Abs(pf_eta2) < 1.7) {
							histograms_reference_[ref_trigger]->GetTH1D("pf_mjj_80_70_weighted")->Fill(pf_mjj, ref_prescale);
						}
						histograms_reference_[ref_trigger]->GetTH1D("pf_deltaeta_weighted")->Fill(pf_deltaeta, ref_prescale);
						histograms_reference_[ref_trigger]->GetTH1D("pf_eta1_weighted")->Fill(pf_eta1, ref_prescale);
						histograms_reference_[ref_trigger]->GetTH1D("pf_eta2_weighted")->Fill(pf_eta2, ref_prescale);
						histograms_reference_[ref_trigger]->GetTH1D("pf_pt1_weighted")->Fill(pf_pt1, ref_prescale);
						histograms_reference_[ref_trigger]->GetTH1D("pf_pt2_weighted")->Fill(pf_pt2, ref_prescale);
						histograms_reference_[ref_trigger]->GetTH2D("pf_pt1_pt2_weighted")->Fill(pf_pt1, pf_pt2, ref_prescale);
						histograms_reference_[ref_trigger]->GetTH1D("pf_btag_csv1_weighted")->Fill(pf_btag_csv1, ref_prescale);
						histograms_reference_[ref_trigger]->GetTH1D("pf_btag_csv2_weighted")->Fill(pf_btag_csv2, ref_prescale);
						
						for (auto& test_trigger : trigger_paths_) {
							bool pass_test = false;
							for (auto& it_trig_index : trigger_path_indices_[test_trigger]) {
								if (event_->fired(it_trig_index) == 1) {
									pass_test = true;
									//test_hlt_index = it_trig_index;
									break;
								}
							} 
							if (pass_test) {
								histograms_test_[ref_trigger][test_trigger]->GetTH1D("nevents")->Fill(1);
								histograms_test_[ref_trigger][test_trigger]->GetTH1D("pf_mjj")->Fill(pf_mjj);
								if (pf_pt1 > 160. && pf_pt2 > 120. && TMath::Abs(pf_eta1) < 2.4 && TMath::Abs(pf_eta2) < 2.4) {
									histograms_test_[ref_trigger][test_trigger]->GetTH1D("pf_mjj_160_120")->Fill(pf_mjj);
								}
								if (pf_pt1 > 80. && pf_pt2 > 70. && TMath::Abs(pf_eta1) < 1.7 && TMath::Abs(pf_eta2) < 1.7) {
									histograms_test_[ref_trigger][test_trigger]->GetTH1D("pf_mjj_80_70")->Fill(pf_mjj);
								}
								histograms_test_[ref_trigger][test_trigger]->GetTH1D("pf_deltaeta")->Fill(pf_deltaeta);
								histograms_test_[ref_trigger][test_trigger]->GetTH1D("pf_eta1")->Fill(pf_eta1);
								histograms_test_[ref_trigger][test_trigger]->GetTH1D("pf_eta2")->Fill(pf_eta2);
								histograms_test_[ref_trigger][test_trigger]->GetTH1D("pf_pt1")->Fill(pf_pt1);
								histograms_test_[ref_trigger][test_trigger]->GetTH1D("pf_pt2")->Fill(pf_pt2);
								histograms_test_[ref_trigger][test_trigger]->GetTH2D("pf_pt1_pt2")->Fill(pf_pt1, pf_pt2);
								histograms_test_[ref_trigger][test_trigger]->GetTH1D("pf_btag_csv1")->Fill(pf_btag_csv1);
								histograms_test_[ref_trigger][test_trigger]->GetTH1D("pf_btag_csv2")->Fill(pf_btag_csv2);
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
