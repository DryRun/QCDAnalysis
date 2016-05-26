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
	current_file_ = 0;
	n_total_ = 0;
	n_pass_ = 0;
	signal_mass_ = -1.;
	if (cfg.getParameter<std::string>("data_source") == "collision_data") {
		data_source_ = ObjectIdentifiers::kCollisionData;
	} else if (cfg.getParameter<std::string>("data_source") == "simulation") {
		data_source_ = ObjectIdentifiers::kSimulation;
	} else {
		throw cms::Exception("[InclusiveBHistograms::InclusiveBHistograms] ERROR : data_source must be collision_data or simulation") << std::endl;
	}
	if (cfg.getParameter<std::string>("data_type") == "data") {
		data_type_ = ObjectIdentifiers::kData;
	} else if (cfg.getParameter<std::string>("data_type") == "signal") {
		data_type_ = ObjectIdentifiers::kSignal;
		signal_mass_ = cfg.getParameter<double>("signal_mass");
		std::cout << "[InclusiveBHistograms::InclusiveBHistograms] INFO : Signal job with mass " << signal_mass_ << std::endl;
	} else if (cfg.getParameter<std::string>("data_type") == "background") {
		data_type_ = ObjectIdentifiers::kBackground;
	} else {
		throw cms::Exception("[InclusiveBHistograms::beginJob] ERROR : data_type must be collision_data or simulation") << std::endl;
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
void InclusiveBHistograms::beginJob() 
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
		// For TriggerXOR, convert strings to ints
		if (it_cut.EqualTo("TriggerXOR") || it_cut.EqualTo("TriggerOR")) {
			std::vector<double> tmp_parameters;
			std::vector<TString> tmp_descriptors;
			std::cout << "[InclusiveBHistograms::beginJob] INFO : Opening " << input_file_names_[0] << std::endl;
			TFile *f = TFile::Open(TString(input_file_names_[0]), "READ");
			TH1F *h_trigger_names = (TH1F*)f->Get(trigger_histogram_name_);
			for (int bin = 1; bin <= h_trigger_names->GetNbinsX(); ++bin) {
				indices_to_triggers_[bin - 1] = h_trigger_names->GetXaxis()->GetBinLabel(bin);
				std::cout << "[InclusiveBHistograms::beginJob] INFO : Trigger index " << bin - 1 << " = " << indices_to_triggers_[bin - 1] << std::endl;
			}
			if (!h_trigger_names) {
				throw cms::Exception("[InclusiveBHistograms::beginJob] ERROR : ") << "Trigger name histogram (" << trigger_histogram_name_ << ") not found in input file." << std::endl;
			}
			for (auto& it_trig : event_cut_descriptors_[it_cut]) {
				// Look up index from histogram
				int hlt_index = -1;
				for(int bin = 1; bin <= h_trigger_names->GetNbinsX(); ++bin) {
					string ss = h_trigger_names->GetXaxis()->GetBinLabel(bin);
					if (it_trig.EqualTo(ss)) {
						hlt_index = bin - 1; // Bins start from 1, while index starts from 0
						break;
					}
				}
				if (hlt_index == -1) {
					throw cms::Exception("[InclusiveBHistograms::beginJob] ERROR : ") << "Couldn't find index for trigger " << it_trig << " in TriggerNames." << std::endl;
				} else {
					tmp_parameters.push_back(hlt_index);
				}
			} // End loop over trigger names
			event_selector_->RegisterCut(it_cut, tmp_descriptors, tmp_parameters);
		} else {
			// Normal cut registration
			event_selector_->RegisterCut(it_cut, event_cut_descriptors_[it_cut], event_cut_parameters_[it_cut]);
		}
	}
	event_selector_->AddObjectSelector(ObjectIdentifiers::kPFJet, dijet_selector_);


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
	pfjet_histograms_->AddTH1D("eta1", "eta1", "#eta (leading)", 100., -5., 5.);
	pfjet_histograms_->AddTH1D("eta2", "eta2", "#eta (subleading)", 100., -5., 5.);
	pfjet_histograms_->AddTH1D("pt1", "pt1", "p_{T} (leading) [GeV]", 1000, 0., 1000.);
	pfjet_histograms_->AddTH1D("pt2", "pt2", "p_{T} (subleading) [GeV]", 1000, 0., 1000.);
	pfjet_histograms_->AddTH2D("pt1_vs_pt2", "pt1", "p_{T} (leading) [GeV]", 100, 0., 1000., "p_{T} (subleading) [GeV]", 100, 0., 1000.);
	pfjet_histograms_->AddTH2F("mjj_deltaeta", "mjj_deltaeta", "m_{jj} [GeV]", 500, 0., 5000., "#Delta#eta", 100, -5., 5.);
	pfjet_histograms_->AddTH2F("btag_csv", "btag_csv", "CSV (leading)", 20, 0., 1., "CSV (subleading)", 20, 0., 1.);

	calojet_histograms_ = new Root::HistogramManager();
	calojet_histograms_->AddPrefix("h_calojet_");
	calojet_histograms_->AddTFileService(&fs_);
	calojet_histograms_->AddTH1D("mjj", "mjj", "m_{jj} [GeV]", 5000, 0., 5000.); // GeV
	calojet_histograms_->AddTH1D("deltaeta", "deltaeta", "#Delta#eta", 100., -5., 5.);
	calojet_histograms_->AddTH1D("eta1", "eta1", "#eta (leading)", 100., -5., 5.);
	calojet_histograms_->AddTH1D("eta2", "eta2", "#eta (subleading)", 100., -5., 5.);
	calojet_histograms_->AddTH1D("pt1", "pt1", "p_{T} (leading) [GeV]", 1000, 0., 1000.);
	calojet_histograms_->AddTH1D("pt2", "pt2", "p_{T} (subleading) [GeV]", 1000, 0., 1000.);
	calojet_histograms_->AddTH2D("pt1_vs_pt2", "pt1", "p_{T} (leading) [GeV]", 100, 0., 1000., "p_{T} (subleading) [GeV]", 100, 0., 1000.);
	calojet_histograms_->AddTH2F("mjj_deltaeta", "mjj_deltaeta", "m_{jj} [GeV]", 500, 0., 5000., "#Delta#eta", 100, -5., 5.);
	calojet_histograms_->AddTH2F("btag_csv", "btag_csv", "CSV (leading)", 20, 0., 1., "CSV (subleading)", 20, 0., 1.);

	fatjet_histograms_ = new Root::HistogramManager();
	fatjet_histograms_->AddPrefix("h_fatjet_");
	fatjet_histograms_->AddTFileService(&fs_);
	fatjet_histograms_->AddTH1D("mjj", "mjj", "m_{jj} [GeV]", 5000, 0., 5000.); // GeV
	fatjet_histograms_->AddTH1D("deltaeta", "deltaeta", "#Delta#eta", 100., -5., 5.);
	fatjet_histograms_->AddTH1D("eta1", "eta1", "#eta (leading)", 100., -5., 5.);
	fatjet_histograms_->AddTH1D("eta2", "eta2", "#eta (subleading)", 100., -5., 5.);
	fatjet_histograms_->AddTH1D("pt1", "pt1", "p_{T} (leading) [GeV]", 1000, 0., 1000.);
	fatjet_histograms_->AddTH1D("pt2", "pt2", "p_{T} (subleading) [GeV]", 1000, 0., 1000.);
	fatjet_histograms_->AddTH2D("pt1_vs_pt2", "pt1", "p_{T} (leading) [GeV]", 100, 0., 1000., "p_{T} (subleading) [GeV]", 100, 0., 1000.);
	fatjet_histograms_->AddTH2F("mjj_deltaeta", "mjj_deltaeta", "m_{jj} [GeV]", 500, 0., 5000., "#Delta#eta", 100, -5., 5.);
	fatjet_histograms_->AddTH2F("btag_csv", "btag_csv", "CSV (leading)", 20, 0., 1., "CSV (subleading)", 20, 0., 1.);

	if (data_type_ == ObjectIdentifiers::kSignal) {
		pfjet_histograms_->AddTH1D("mjj_over_M", "mjj_over_M", "m_{jj} / M_{X}", 75, 0., 1.5);
		calojet_histograms_->AddTH1D("mjj_over_M", "mjj_over_M", "m_{jj} / M_{X}", 75, 0., 1.5);
		fatjet_histograms_->AddTH1D("mjj_over_M", "mjj_over_M", "m_{jj} / M_{X}", 75, 0., 1.5);
	}
}


//////////////////////////////////////////////////////////////////////////////////////////
void InclusiveBHistograms::endJob() 
{
	event_selector_->MakeCutflowHistograms(&*fs_);
	event_selector_->SaveNMinusOneHistogram(&*fs_);
	pfjet_selector_->MakeCutflowHistograms(&*fs_);
	pfjet_selector_->SaveNMinusOneHistogram(&*fs_);
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
		TFile *f = TFile::Open(TString(it_filename), "READ");
		if (!(f->IsOpen())) {
			throw cms::Exception("Filed to open file ") << it_filename << std::endl;
		}
		tree_ = (TTree*)f->Get(input_tree_name_);
		if (!tree_) {
			throw cms::Exception("Failed to get tree ") << input_tree_name_ << " from file " << it_filename << std::endl;
		}
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
				// Get prescale
				double prescale = 1.;
				//if (data_source_ == ObjectIdentifiers::kCollisionData) {
				//	int hlt_index = (int)event_selector_->GetReturnData("TriggerOR");
				//	double prescale_L1 = event_->minPreL1(hlt_index);
				//	prescale = event_->preHLT(hlt_index) * prescale_L1;
				//} else if (data_source_ == ObjectIdentifiers::kSimulation) {
				//	prescale = 1;
				//}
				global_histograms_->GetTH1F("pass_nevents")->Fill(1);
				global_histograms_->GetTH1F("pass_nevents_weighted")->Fill(1, prescale);

				//double pf_mjj = (event_->pfjet(0).p4() + event_->pfjet(1).p4()).mass();
				double pf_deltaeta = event_->pfjet(0).eta() - event_->pfjet(1).eta();
				double pf_btag_csv1 = event_->pfjet(0).btag_csv();
				double pf_btag_csv2 = event_->pfjet(1).btag_csv();
				pfjet_histograms_->GetTH1D("mjj")->Fill(event_->pfmjjcor(0), prescale);
				pfjet_histograms_->GetTH1D("deltaeta")->Fill(pf_deltaeta, prescale);
				pfjet_histograms_->GetTH1D("pt1")->Fill(event_->pfjet(0).pt(), prescale);
				pfjet_histograms_->GetTH1D("pt2")->Fill(event_->pfjet(1).pt(), prescale);
				pfjet_histograms_->GetTH2D("pt1_vs_pt2")->Fill(event_->pfjet(0).pt(), event_->pfjet(1).pt(), prescale);
				pfjet_histograms_->GetTH1D("eta1")->Fill(event_->pfjet(0).eta(), prescale);
				pfjet_histograms_->GetTH1D("eta2")->Fill(event_->pfjet(1).eta(), prescale);
				pfjet_histograms_->GetTH2F("mjj_deltaeta")->Fill(event_->pfmjjcor(0), pf_deltaeta, prescale);
				pfjet_histograms_->GetTH2F("btag_csv")->Fill(pf_btag_csv1, pf_btag_csv2, prescale);
				if (data_type_ == ObjectIdentifiers::kSignal) {
					pfjet_histograms_->GetTH1D("mjj_over_M")->Fill(event_->pfmjjcor(0) / signal_mass_, prescale);
				}

				//double calo_mjj = (event_->calojet(0).p4() + event_->calojet(1).p4()).mass();
				double calo_deltaeta = event_->calojet(0).eta() - event_->calojet(1).eta();
				double calo_btag_csv1 = event_->calojet(0).btag_csv();
				double calo_btag_csv2 = event_->calojet(1).btag_csv();
				calojet_histograms_->GetTH1D("mjj")->Fill(event_->calomjjcor(0), prescale);
				calojet_histograms_->GetTH1D("deltaeta")->Fill(calo_deltaeta, prescale);
				calojet_histograms_->GetTH2F("mjj_deltaeta")->Fill(event_->calomjjcor(0), calo_deltaeta, prescale);
				calojet_histograms_->GetTH2F("btag_csv")->Fill(calo_btag_csv1, calo_btag_csv2, prescale);
				calojet_histograms_->GetTH1D("pt1")->Fill(event_->calojet(0).pt(), prescale);
				calojet_histograms_->GetTH1D("pt2")->Fill(event_->calojet(1).pt(), prescale);
				calojet_histograms_->GetTH2D("pt1_vs_pt2")->Fill(event_->calojet(0).pt(), event_->calojet(1).pt(), prescale);
				calojet_histograms_->GetTH1D("eta1")->Fill(event_->calojet(0).eta(), prescale);
				calojet_histograms_->GetTH1D("eta2")->Fill(event_->calojet(1).eta(), prescale);
				if (data_type_ == ObjectIdentifiers::kSignal) {
					calojet_histograms_->GetTH1D("mjj_over_M")->Fill(event_->pfmjjcor(0) / signal_mass_, prescale);
				}

				double fat_deltaeta = event_->fatjet(0).eta() - event_->fatjet(1).eta();
				double fat_btag_csv1 = event_->fatjet(0).btag_csv();
				double fat_btag_csv2 = event_->fatjet(1).btag_csv();
				fatjet_histograms_->GetTH1D("mjj")->Fill(event_->fatmjjcor(0), prescale);
				fatjet_histograms_->GetTH1D("deltaeta")->Fill(fat_deltaeta, prescale);
				fatjet_histograms_->GetTH1D("pt1")->Fill(event_->fatjet(0).pt(), prescale);
				fatjet_histograms_->GetTH1D("pt2")->Fill(event_->fatjet(1).pt(), prescale);
				fatjet_histograms_->GetTH2D("pt1_vs_pt2")->Fill(event_->fatjet(0).pt(), event_->fatjet(1).pt(), prescale);
				fatjet_histograms_->GetTH1D("eta1")->Fill(event_->fatjet(0).eta(), prescale);
				fatjet_histograms_->GetTH1D("eta2")->Fill(event_->fatjet(1).eta(), prescale);
				fatjet_histograms_->GetTH2F("mjj_deltaeta")->Fill(event_->fatmjjcor(0), fat_deltaeta, prescale);
				fatjet_histograms_->GetTH2F("btag_csv")->Fill(fat_btag_csv1, fat_btag_csv2, prescale);
				if (data_type_ == ObjectIdentifiers::kSignal) {
					fatjet_histograms_->GetTH1D("mjj_over_M")->Fill(event_->pfmjjcor(0) / signal_mass_, prescale);
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

DEFINE_FWK_MODULE(InclusiveBHistograms);
