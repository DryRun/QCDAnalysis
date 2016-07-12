#ifndef BHistograms_h
#define BHistograms_h

#include "TTree.h"
#include "TH1F.h"
#include "TF1.h"
#include "TFile.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "CMSDIJET/QCDAnalysis/interface/QCDJet.h"
#include "CMSDIJET/QCDAnalysis/interface/QCDEvent.h"
#include "CMSDIJET/QCDAnalysis/interface/QCDEventHdr.h"
#include "CMSDIJET/QCDAnalysis/interface/QCDCaloJet.h"
#include "CMSDIJET/QCDAnalysis/interface/QCDPFJet.h"
#include "CMSDIJET/QCDAnalysis/interface/QCDMET.h"
#include "CMSDIJET/QCDAnalysis/interface/PFJetCutFunctions.h"
#include "CMSDIJET/QCDAnalysis/interface/CaloJetCutFunctions.h"
#include "CMSDIJET/QCDAnalysis/interface/QCDEventCutFunctions.h"
#include "CMSDIJET/QCDAnalysis/interface/Systematics.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "MyTools/RootUtils/interface/HistogramManager.h"
#include "MyTools/AnalysisTools/interface/EventSelector.h"
#include "MyTools/AnalysisTools/interface/ObjectSelector.h"

class BHistograms : public edm::EDAnalyzer
{
  public:
	explicit BHistograms(edm::ParameterSet const& cfg);
	virtual void beginJob();
	virtual void analyze(edm::Event const& evt, edm::EventSetup const& iSetup);
	virtual void endJob();
	virtual ~BHistograms() {}

  private:  
	double getEventBTagSF(int uncertainty = 0);

	int getBin(double x, const std::vector<double>& boundaries); 

	//---- configurable parameters --------   
	ObjectIdentifiers::DataSource data_source_;
	ObjectIdentifiers::DataType data_type_;
	float signal_mass_;
	std::vector<std::string> input_file_names_;
	TString input_tree_name_;
	TString trigger_histogram_name_;
	//std::vector<std::string> trigger_list_unparsed_;
	std::vector<TString> triggers_;
	//std::vector<TString> hlt_triggers_;
	//std::vector<TString> l1_triggers_;
	std::vector<int> trigger_indices_;
	std::map<TString, int> triggers_to_indices_;
	std::map<int, TString> indices_to_triggers_;
	//std::map<int, TString> hlt_index_to_l1_name_;
	//std::map<int, TString> hlt_index_to_hlt_name_;
	
	edm::Service<TFileService> fs_;
	TTree* tree_; 
	TFile* current_file_;
	//TFile* input_file_;
	TDirectoryFile *input_directory_;
	std::vector<TH1F*> mhMETovSUMET,mhM,mhNormM,mhTruncM,mhNormTruncM,mhPt,mhY,mhYmax;
	std::vector<TH1F*> mhCHF,mhNHF,mhPHF,mhN90hits,mhEMF,mhNTrkCalo,mhNTrkVtx,mhfHPD;
	//---- TREE variable --------
	QCDEvent *event_;
	ObjectSelector<QCDPFJet> *dijet_selector_; // Selection for the leading two jets
	ObjectSelector<QCDPFJet> *pfjet_selector_; // Selection for remaining jets
	ObjectSelector<QCDCaloJet> *calojet_selector_;
	EventSelector<QCDEvent> *event_selector_;
	Root::HistogramManager* global_histograms_;
	Root::HistogramManager* pfjet_histograms_;
	Root::HistogramManager* calojet_histograms_;
	Root::HistogramManager* fatjet_histograms_;
	TH1F* h_trigger_names_;
	
	int n_total_;
	int n_pass_;

	// Cut values
	double fatjet_delta_eta_cut_;
	
	std::vector<TString> dijet_cuts_;
	std::map<TString, std::vector<double> > dijet_cut_parameters_;
	std::map<TString, std::vector<TString> > dijet_cut_descriptors_;

	std::vector<TString> pfjet_cuts_;
	std::map<TString, std::vector<double> > pfjet_cut_parameters_;
	std::map<TString, std::vector<TString> > pfjet_cut_descriptors_;

	std::vector<TString> calojet_cuts_;
	std::map<TString, std::vector<double> > calojet_cut_parameters_;
	std::map<TString, std::vector<TString> > calojet_cut_descriptors_;

	std::vector<TString> event_cuts_;
	std::map<TString, std::vector<double> > event_cut_parameters_;
	std::map<TString, std::vector<TString> > event_cut_descriptors_;

	// B tag SFs
	std::pair<ObjectIdentifiers::BTagWP, ObjectIdentifiers::BTagWP> btag_configuration_;
	//std::map<ObjectIdentifiers::BTagWP, TH2D*> btag_efficiency_histograms_;
	std::map<ObjectIdentifiers::BTagWP, TF1*> btag_scale_factors_;
	std::map<ObjectIdentifiers::BTagWP, TH1D*> btag_scale_factor_uncertainties_;
};


#endif