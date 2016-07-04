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

#include "CMSDIJET/QCDAnalysis/plugins/BHistograms.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"

using namespace std;

BHistograms::BHistograms(edm::ParameterSet const& cfg) 
{
	input_file_names_  = cfg.getParameter<std::vector<std::string> > ("file_names");
	input_tree_name_  = cfg.getParameter<std::string> ("tree_name");
	trigger_histogram_name_  = cfg.getParameter<std::string> ("trigger_histogram_name");
	fatjet_delta_eta_cut_ = cfg.getParameter<double>("fatjet_delta_eta_cut");
	current_file_ = 0;
	n_total_ = 0;
	n_pass_ = 0;
	signal_mass_ = -1.;
	if (cfg.getParameter<std::string>("data_source") == "collision_data") {
		data_source_ = ObjectIdentifiers::kCollisionData;
	} else if (cfg.getParameter<std::string>("data_source") == "simulation") {
		data_source_ = ObjectIdentifiers::kSimulation;
	} else {
		throw cms::Exception("[BHistograms::BHistograms] ERROR : data_source must be collision_data or simulation") << std::endl;
	}
	if (cfg.getParameter<std::string>("data_type") == "data") {
		data_type_ = ObjectIdentifiers::kData;
	} else if (cfg.getParameter<std::string>("data_type") == "signal") {
		data_type_ = ObjectIdentifiers::kSignal;
		signal_mass_ = cfg.getParameter<double>("signal_mass");
		std::cout << "[BHistograms::BHistograms] INFO : Signal job with mass " << signal_mass_ << std::endl;
	} else if (cfg.getParameter<std::string>("data_type") == "background") {
		data_type_ = ObjectIdentifiers::kBackground;
	} else {
		throw cms::Exception("[BHistograms::beginJob] ERROR : data_type must be collision_data or simulation") << std::endl;
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

	if (data_source_ == ObjectIdentifiers::kSimulation) {
		std::map<TString, ObjectIdentifiers::BTagWP> btag_string_to_enum;
		btag_string_to_enum["CSVL"] = ObjectIdentifiers::kCSVL;
		btag_string_to_enum["CSVM"] = ObjectIdentifiers::kCSVM;
		btag_string_to_enum["CSVT"] = ObjectIdentifiers::kCSVT;
		btag_scale_factors_[ObjectIdentifiers::kCSVL] = new TF1("sf_csvl", "0.997942*((1.+(0.00923753*x))/(1.+(0.0096119*x)))", 0., 800.);
		btag_scale_factors_[ObjectIdentifiers::kCSVM] = new TF1("sf_csvm", "(0.938887+(0.00017124*x))+(-2.76366e-07*(x*x))", 0., 800.);
		btag_scale_factors_[ObjectIdentifiers::kCSVT] = new TF1("sf_csvt", "(0.927563+(1.55479e-05*x))+(-1.90666e-07*(x*x))", 0., 800.);
		btag_configuration_ = std::pair<ObjectIdentifiers::BTagWP, ObjectIdentifiers::BTagWP>(btag_string_to_enum[cfg.getParameter<std::string>("btag_wp_1")], btag_string_to_enum[cfg.getParameter<std::string>("btag_wp_2")]);

		float bins[] = {20, 30, 40, 50, 60, 70, 80, 100, 120, 160, 210, 260, 320, 400, 500, 600, 800};
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVL] = new TH1D("btag_sf_unc_csvl", "btag_sf_unc_csvl", 16, bins);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVL]->SetBinContent(1, 0.033299);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVL]->SetBinContent(2, 0.0146768);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVL]->SetBinContent(3, 0.013803);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVL]->SetBinContent(4, 0.0170145);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVL]->SetBinContent(5, 0.0166976);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVL]->SetBinContent(6, 0.0137879);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVL]->SetBinContent(7, 0.0149072);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVL]->SetBinContent(8, 0.0153068);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVL]->SetBinContent(9, 0.0133077);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVL]->SetBinContent(10, 0.0123737);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVL]->SetBinContent(11, 0.0157152);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVL]->SetBinContent(12, 0.0175161);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVL]->SetBinContent(13, 0.0209241);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVL]->SetBinContent(14, 0.0278605);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVL]->SetBinContent(15, 0.0346928);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVL]->SetBinContent(16, 0.0350099);

		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVM] = new TH1D("btag_sf_unc_csvm", "btag_sf_unc_csvm", 16, bins);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVM]->SetBinContent(1, 0.0415707);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVM]->SetBinContent(2, 0.0204209);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVM]->SetBinContent(3, 0.0223227);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVM]->SetBinContent(4, 0.0206655);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVM]->SetBinContent(5, 0.0199325);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVM]->SetBinContent(6, 0.0174121);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVM]->SetBinContent(7, 0.0202332);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVM]->SetBinContent(8, 0.0182446);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVM]->SetBinContent(9, 0.0159777);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVM]->SetBinContent(10, 0.0218531);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVM]->SetBinContent(11, 0.0204688);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVM]->SetBinContent(12, 0.0265191);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVM]->SetBinContent(13, 0.0313175);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVM]->SetBinContent(14, 0.0415417);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVM]->SetBinContent(15, 0.0740446);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVM]->SetBinContent(16, 0.0596716);

		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVT] = new TH1D("btag_sf_unc_csvl", "btag_sf_unc_csvl", 16, bins);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVT]->SetBinContent(1, 0.0515703);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVT]->SetBinContent(2, 0.0264008);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVT]->SetBinContent(3, 0.0272757);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVT]->SetBinContent(4, 0.0275565);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVT]->SetBinContent(5, 0.0248745);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVT]->SetBinContent(6, 0.0218456);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVT]->SetBinContent(7, 0.0253845);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVT]->SetBinContent(8, 0.0239588);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVT]->SetBinContent(9, 0.0271791);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVT]->SetBinContent(10, 0.0273912);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVT]->SetBinContent(11, 0.0379822);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVT]->SetBinContent(12, 0.0411624);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVT]->SetBinContent(13, 0.0786307);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVT]->SetBinContent(14, 0.0866832);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVT]->SetBinContent(15, 0.0942053);
		btag_scale_factor_uncertainties_[ObjectIdentifiers::kCSVT]->SetBinContent(16, 0.102403);
	}
}

//////////////////////////////////////////////////////////////////////////////////////////
void BHistograms::beginJob() 
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
			std::cout << "[BHistograms::beginJob] INFO : Opening " << input_file_names_[0] << std::endl;
			TFile *f = TFile::Open(TString(input_file_names_[0]), "READ");
			TH1F *h_trigger_names = (TH1F*)f->Get(trigger_histogram_name_);
			for (int bin = 1; bin <= h_trigger_names->GetNbinsX(); ++bin) {
				indices_to_triggers_[bin - 1] = h_trigger_names->GetXaxis()->GetBinLabel(bin);
				std::cout << "[BHistograms::beginJob] INFO : Trigger index " << bin - 1 << " = " << indices_to_triggers_[bin - 1] << std::endl;
			}
			if (!h_trigger_names) {
				throw cms::Exception("[BHistograms::beginJob] ERROR : ") << "Trigger name histogram (" << trigger_histogram_name_ << ") not found in input file." << std::endl;
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
					throw cms::Exception("[BHistograms::beginJob] ERROR : ") << "Couldn't find index for trigger " << it_trig << " in TriggerNames." << std::endl;
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

	if (data_source_ == ObjectIdentifiers::kSimulation) {
		pfjet_histograms_->AddTH1D("mjj_BTagOfflineSFUp", "mjj_BTagOfflineSFUp", "m_{jj} [GeV]", 5000, 0., 5000.); // GeV
		pfjet_histograms_->AddTH1D("mjj_BTagOfflineSFDown", "mjj_BTagOfflineSFDown", "m_{jj} [GeV]", 5000, 0., 5000.); // GeV
		pfjet_histograms_->AddTH1D("mjj_JESUp", "mjj_JESUp", "m_{jj} [GeV]", 5000, 0., 5000.); // GeV
		pfjet_histograms_->AddTH1D("mjj_JESDown", "mjj_JESDown", "m_{jj} [GeV]", 5000, 0., 5000.); // GeV
		pfjet_histograms_->AddTH1D("mjj_JERUp", "mjj_JERUp", "m_{jj} [GeV]", 5000, 0., 5000.); // GeV
		pfjet_histograms_->AddTH1D("mjj_JERDown", "mjj_JERDown", "m_{jj} [GeV]", 5000, 0., 5000.); // GeV
	}


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
	if (data_source_ == ObjectIdentifiers::kSimulation) {
		fatjet_histograms_->AddTH1D("mjj_BTagOfflineSFUp", "mjj_BTagOfflineSFUp", "m_{jj} [GeV]", 5000, 0., 5000.); // GeV
		fatjet_histograms_->AddTH1D("mjj_BTagOfflineSFDown", "mjj_BTagOfflineSFDown", "m_{jj} [GeV]", 5000, 0., 5000.); // GeV
		fatjet_histograms_->AddTH1D("mjj_JESUp", "mjj_JESUp", "m_{jj} [GeV]", 5000, 0., 5000.); // GeV
		fatjet_histograms_->AddTH1D("mjj_JESDown", "mjj_JESDown", "m_{jj} [GeV]", 5000, 0., 5000.); // GeV
		fatjet_histograms_->AddTH1D("mjj_JERUp", "mjj_JERUp", "m_{jj} [GeV]", 5000, 0., 5000.); // GeV
		fatjet_histograms_->AddTH1D("mjj_JERDown", "mjj_JERDown", "m_{jj} [GeV]", 5000, 0., 5000.); // GeV
	}

	if (data_type_ == ObjectIdentifiers::kSignal) {
		pfjet_histograms_->AddTH1D("mjj_over_M", "mjj_over_M", "m_{jj} / M_{X}", 75, 0., 1.5);
		calojet_histograms_->AddTH1D("mjj_over_M", "mjj_over_M", "m_{jj} / M_{X}", 75, 0., 1.5);
		fatjet_histograms_->AddTH1D("mjj_over_M", "mjj_over_M", "m_{jj} / M_{X}", 75, 0., 1.5);

		pfjet_histograms_->AddTH1D("mjj_over_M_BTagOfflineSFUp", "mjj_over_M_BTagOfflineSFUp", "m_{jj} / M_{X}", 75, 0., 1.5); // GeV
		pfjet_histograms_->AddTH1D("mjj_over_M_BTagOfflineSFDown", "mjj_over_M_BTagOfflineSFDown", "m_{jj} / M_{X}", 75, 0., 1.5); // GeV
		pfjet_histograms_->AddTH1D("mjj_over_M_JESUp", "mjj_over_M_JESUp", "m_{jj} / M_{X}", 75, 0., 1.5); // GeV
		pfjet_histograms_->AddTH1D("mjj_over_M_JESDown", "mjj_over_M_JESDown", "m_{jj} / M_{X}", 75, 0., 1.5); // GeV
		pfjet_histograms_->AddTH1D("mjj_over_M_JERUp", "mjj_over_M_JERUp", "m_{jj} / M_{X}", 75, 0., 1.5); // GeV
		pfjet_histograms_->AddTH1D("mjj_over_M_JERDown", "mjj_over_M_JERDown", "m_{jj} / M_{X}", 75, 0., 1.5); // GeV
		fatjet_histograms_->AddTH1D("mjj_over_M_BTagOfflineSFUp", "mjj_over_M_BTagOfflineSFUp", "m_{jj} / M_{X}", 75, 0., 1.5); // GeV
		fatjet_histograms_->AddTH1D("mjj_over_M_BTagOfflineSFDown", "mjj_over_M_BTagOfflineSFDown", "m_{jj} / M_{X}", 75, 0., 1.5); // GeV
		fatjet_histograms_->AddTH1D("mjj_over_M_JESUp", "mjj_over_M_JESUp", "m_{jj} / M_{X}", 75, 0., 1.5); // GeV
		fatjet_histograms_->AddTH1D("mjj_over_M_JESDown", "mjj_over_M_JESDown", "m_{jj} / M_{X}", 75, 0., 1.5); // GeV
		fatjet_histograms_->AddTH1D("mjj_over_M_JERUp", "mjj_over_M_JERUp", "m_{jj} / M_{X}", 75, 0., 1.5); // GeV
		fatjet_histograms_->AddTH1D("mjj_over_M_JERDown", "mjj_over_M_JERDown", "m_{jj} / M_{X}", 75, 0., 1.5); // GeV

	}

	// B tag SFs
	if (data_source_ == ObjectIdentifiers::kSimulation) {

		std::vector<ObjectIdentifiers::BTagWP> btag_working_points;
		btag_working_points.push_back(ObjectIdentifiers::kCSVL);
		btag_working_points.push_back(ObjectIdentifiers::kCSVM);
		btag_working_points.push_back(ObjectIdentifiers::kCSVT);
	}
}


//////////////////////////////////////////////////////////////////////////////////////////
void BHistograms::endJob() 
{
	event_selector_->MakeCutflowHistograms(&*fs_);
	event_selector_->SaveNMinusOneHistogram(&*fs_);
	pfjet_selector_->MakeCutflowHistograms(&*fs_);
	pfjet_selector_->SaveNMinusOneHistogram(&*fs_);
	//delete event_;
	//event_ = 0;
	btag_scale_factor_uncertainties_.clear();
	std::cout << "[BHistograms::endJob] INFO : Pass / Total = " << n_pass_ << " / " << n_total_ << std::endl;
}
//////////////////////////////////////////////////////////////////////////////////////////
int BHistograms::getBin(double x, const std::vector<double>& boundaries)
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
void BHistograms::analyze(edm::Event const& evt, edm::EventSetup const& iSetup) 
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

			// Sort jets by b tag rather than pT
			//event_->sortPFJetsBTagCSV();

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
					if ((dR1 <= dR2) && (dR1 < fatjet_delta_eta_cut_)) {
						lv_fatjet[0] += lv_pfjet;
						sum_pt[0] += lv_pfjet.pt();
						dsum_pt[0] += lv_pfjet.pt() * event_->pfjet(jet_index).cor();
					} else if (dR2 < fatjet_delta_eta_cut_) {
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
				
				// Simulation weights. 
				double weight = prescale;

				// - B tag SFs
				if (data_source_ == ObjectIdentifiers::kSimulation) {
					weight *= getEventBTagSF();
				}

				global_histograms_->GetTH1F("pass_nevents")->Fill(1);
				global_histograms_->GetTH1F("pass_nevents_weighted")->Fill(1, weight);

				//double pf_mjj = (event_->pfjet(0).p4() + event_->pfjet(1).p4()).mass();
				double pf_deltaeta = event_->pfjet(0).eta() - event_->pfjet(1).eta();
				double pf_btag_csv1 = event_->pfjet(0).btag_csv();
				double pf_btag_csv2 = event_->pfjet(1).btag_csv();
				pfjet_histograms_->GetTH1D("mjj")->Fill(event_->pfmjjcor(0), weight);
				pfjet_histograms_->GetTH1D("deltaeta")->Fill(pf_deltaeta, weight);
				pfjet_histograms_->GetTH1D("pt1")->Fill(event_->pfjet(0).ptCor(), weight);
				pfjet_histograms_->GetTH1D("pt2")->Fill(event_->pfjet(1).ptCor(), weight);
				pfjet_histograms_->GetTH2D("pt1_vs_pt2")->Fill(event_->pfjet(0).ptCor(), event_->pfjet(1).ptCor(), weight);
				pfjet_histograms_->GetTH1D("eta1")->Fill(event_->pfjet(0).eta(), weight);
				pfjet_histograms_->GetTH1D("eta2")->Fill(event_->pfjet(1).eta(), weight);
				pfjet_histograms_->GetTH2F("mjj_deltaeta")->Fill(event_->pfmjjcor(0), pf_deltaeta, weight);
				pfjet_histograms_->GetTH2F("btag_csv")->Fill(pf_btag_csv1, pf_btag_csv2, weight);
				if (data_type_ == ObjectIdentifiers::kSignal) {
					pfjet_histograms_->GetTH1D("mjj_over_M")->Fill(event_->pfmjjcor(0) / signal_mass_, weight);
				}
				if (data_source_ == ObjectIdentifiers::kSimulation) {
					double weight_BTagOfflineSFUp = prescale * getEventBTagSF(1);
					double weight_BTagOfflineSFDown = prescale * getEventBTagSF(-1);
					pfjet_histograms_->GetTH1D("mjj_BTagOfflineSFUp")->Fill(event_->pfmjjcor(0), weight_BTagOfflineSFUp);
					pfjet_histograms_->GetTH1D("mjj_BTagOfflineSFDown")->Fill(event_->pfmjjcor(0), weight_BTagOfflineSFDown);
					pfjet_histograms_->GetTH1D("mjj_JESUp")->Fill(event_->pfmjjcor(1), weight);
					pfjet_histograms_->GetTH1D("mjj_JESDown")->Fill(event_->pfmjjcor(-1), weight);
					pfjet_histograms_->GetTH1D("mjj_JERUp")->Fill(0.);
					pfjet_histograms_->GetTH1D("mjj_JERDown")->Fill(0.);
					if (data_type_ == ObjectIdentifiers::kSignal) {
						pfjet_histograms_->GetTH1D("mjj_over_M_BTagOfflineSFUp")->Fill(event_->pfmjjcor(0) / signal_mass_, weight_BTagOfflineSFUp);
						pfjet_histograms_->GetTH1D("mjj_over_M_BTagOfflineSFDown")->Fill(event_->pfmjjcor(0) / signal_mass_, weight_BTagOfflineSFDown);
						pfjet_histograms_->GetTH1D("mjj_over_M_JESUp")->Fill(event_->pfmjjcor(1) / signal_mass_, weight);
						pfjet_histograms_->GetTH1D("mjj_over_M_JESDown")->Fill(event_->pfmjjcor(-1) / signal_mass_, weight);
						pfjet_histograms_->GetTH1D("mjj_over_M_JERUp")->Fill(0.);
						pfjet_histograms_->GetTH1D("mjj_over_M_JERDown")->Fill(0.);
					}
				}

				//double calo_mjj = (event_->calojet(0).p4() + event_->calojet(1).p4()).mass();
				double calo_deltaeta = event_->calojet(0).eta() - event_->calojet(1).eta();
				double calo_btag_csv1 = event_->calojet(0).btag_csv();
				double calo_btag_csv2 = event_->calojet(1).btag_csv();
				calojet_histograms_->GetTH1D("mjj")->Fill(event_->calomjjcor(0), weight);
				calojet_histograms_->GetTH1D("deltaeta")->Fill(calo_deltaeta, weight);
				calojet_histograms_->GetTH2F("mjj_deltaeta")->Fill(event_->calomjjcor(0), calo_deltaeta, weight);
				calojet_histograms_->GetTH2F("btag_csv")->Fill(calo_btag_csv1, calo_btag_csv2, weight);
				calojet_histograms_->GetTH1D("pt1")->Fill(event_->calojet(0).ptCor(), weight);
				calojet_histograms_->GetTH1D("pt2")->Fill(event_->calojet(1).ptCor(), weight);
				calojet_histograms_->GetTH2D("pt1_vs_pt2")->Fill(event_->calojet(0).ptCor(), event_->calojet(1).ptCor(), weight);
				calojet_histograms_->GetTH1D("eta1")->Fill(event_->calojet(0).eta(), weight);
				calojet_histograms_->GetTH1D("eta2")->Fill(event_->calojet(1).eta(), weight);
				if (data_type_ == ObjectIdentifiers::kSignal) {
					calojet_histograms_->GetTH1D("mjj_over_M")->Fill(event_->pfmjjcor(0) / signal_mass_, weight);
				}

				double fat_deltaeta = event_->fatjet(0).eta() - event_->fatjet(1).eta();
				double fat_btag_csv1 = event_->fatjet(0).btag_csv();
				double fat_btag_csv2 = event_->fatjet(1).btag_csv();
				fatjet_histograms_->GetTH1D("mjj")->Fill(event_->fatmjjcor(0), weight);
				fatjet_histograms_->GetTH1D("deltaeta")->Fill(fat_deltaeta, weight);
				fatjet_histograms_->GetTH1D("pt1")->Fill(event_->fatjet(0).ptCor(), weight);
				fatjet_histograms_->GetTH1D("pt2")->Fill(event_->fatjet(1).ptCor(), weight);
				fatjet_histograms_->GetTH2D("pt1_vs_pt2")->Fill(event_->fatjet(0).ptCor(), event_->fatjet(1).ptCor(), weight);
				fatjet_histograms_->GetTH1D("eta1")->Fill(event_->fatjet(0).eta(), weight);
				fatjet_histograms_->GetTH1D("eta2")->Fill(event_->fatjet(1).eta(), weight);
				fatjet_histograms_->GetTH2F("mjj_deltaeta")->Fill(event_->fatmjjcor(0), fat_deltaeta, weight);
				fatjet_histograms_->GetTH2F("btag_csv")->Fill(fat_btag_csv1, fat_btag_csv2, weight);
				if (data_type_ == ObjectIdentifiers::kSignal) {
					fatjet_histograms_->GetTH1D("mjj_over_M")->Fill(event_->pfmjjcor(0) / signal_mass_, weight);
				}
				if (data_source_ == ObjectIdentifiers::kSimulation) {
					double weight_BTagOfflineSFUp = prescale * getEventBTagSF(1);
					double weight_BTagOfflineSFDown = prescale * getEventBTagSF(-1);
					fatjet_histograms_->GetTH1D("mjj_BTagOfflineSFUp")->Fill(event_->fatmjjcor(0), weight_BTagOfflineSFUp);
					fatjet_histograms_->GetTH1D("mjj_BTagOfflineSFDown")->Fill(event_->fatmjjcor(0), weight_BTagOfflineSFDown);
					fatjet_histograms_->GetTH1D("mjj_JESUp")->Fill(event_->fatmjjcor(1), weight);
					fatjet_histograms_->GetTH1D("mjj_JESDown")->Fill(event_->fatmjjcor(-1), weight);
					fatjet_histograms_->GetTH1D("mjj_JERUp")->Fill(0.);
					fatjet_histograms_->GetTH1D("mjj_JERDown")->Fill(0.);
					if (data_type_ == ObjectIdentifiers::kSignal) {
						fatjet_histograms_->GetTH1D("mjj_over_M_BTagOfflineSFUp")->Fill(event_->fatmjjcor(0) / signal_mass_, weight_BTagOfflineSFUp);
						fatjet_histograms_->GetTH1D("mjj_over_M_BTagOfflineSFDown")->Fill(event_->fatmjjcor(0) / signal_mass_, weight_BTagOfflineSFDown);
						fatjet_histograms_->GetTH1D("mjj_over_M_JESUp")->Fill(event_->fatmjjcor(1) / signal_mass_, weight);
						fatjet_histograms_->GetTH1D("mjj_over_M_JESDown")->Fill(event_->fatmjjcor(-1) / signal_mass_, weight);
						fatjet_histograms_->GetTH1D("mjj_over_M_JERUp")->Fill(0.);
						fatjet_histograms_->GetTH1D("mjj_over_M_JERDown")->Fill(0.);
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

double BHistograms::getEventBTagSF(int uncertainty) {
	double sf1 = 1.;
	double sf2 = 1.;
	if (event_->pfjet(0).btag_csv() > event_->pfjet(1).btag_csv()) {
		sf1 = btag_scale_factors_[btag_configuration_.first]->Eval(event_->pfjet(0).pt());
		sf2 = btag_scale_factors_[btag_configuration_.second]->Eval(event_->pfjet(1).pt());
		if (uncertainty) {
			sf1 *= 1. + uncertainty * btag_scale_factor_uncertainties_[btag_configuration_.first]->GetBinContent(btag_scale_factor_uncertainties_[btag_configuration_.first]->FindBin(event_->pfjet(0).pt()));
			sf2 *= 1. + uncertainty * btag_scale_factor_uncertainties_[btag_configuration_.second]->GetBinContent(btag_scale_factor_uncertainties_[btag_configuration_.first]->FindBin(event_->pfjet(1).pt()));
		}
	} else {
		sf1 = btag_scale_factors_[btag_configuration_.first]->Eval(event_->pfjet(1).pt());
		sf2 = btag_scale_factors_[btag_configuration_.second]->Eval(event_->pfjet(0).pt());
		if (uncertainty) {
			sf1 *= 1. + uncertainty * btag_scale_factor_uncertainties_[btag_configuration_.first]->GetBinContent(btag_scale_factor_uncertainties_[btag_configuration_.first]->FindBin(event_->pfjet(1).pt()));
			sf2 *= 1. + uncertainty * btag_scale_factor_uncertainties_[btag_configuration_.second]->GetBinContent(btag_scale_factor_uncertainties_[btag_configuration_.first]->FindBin(event_->pfjet(0).pt()));
		}
	}
	return sf1 * sf2;
}
//////////////////////////////////////////////////////////////////////////////////////////

DEFINE_FWK_MODULE(BHistograms);
