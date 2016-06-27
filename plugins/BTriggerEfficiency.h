#ifndef BTriggerEfficiency_h
#define BTriggerEfficiency_h

#include "TTree.h"
#include "TH1F.h"
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
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "MyTools/RootUtils/interface/HistogramManager.h"
#include "MyTools/AnalysisTools/interface/EventSelector.h"
#include "MyTools/AnalysisTools/interface/ObjectSelector.h"
#include "MyTools/AnalysisTools/interface/ObjectTypeEnums.h"

class BTriggerEfficiency : public edm::EDAnalyzer
{
  public:
    explicit BTriggerEfficiency(edm::ParameterSet const& cfg);
    virtual void beginJob();
    virtual void analyze(edm::Event const& evt, edm::EventSetup const& iSetup);
    virtual void endJob();
    virtual ~BTriggerEfficiency() {}

  private:  
    int getBin(double x, const std::vector<double>& boundaries); 

    //---- configurable parameters --------   
    std::vector<std::string> input_file_names_;
    TString input_tree_name_;
    TString trigger_histogram_name_;
    ObjectIdentifiers::DataSource data_source_;

    bool first_event_;
    std::vector<TString> trigger_paths_; // HLT names
    std::map<TString, std::vector<int> > trigger_path_indices_;
    std::map<int, TString> trigger_index_path_;
    std::map<TString, TString> trigger_paths_hlt_name_;
    std::map<TString, TString> trigger_paths_l1_name_;
    std::vector<std::pair<TString, TString> > trigger_combinations_;
    
    edm::Service<TFileService> fs_;
    TTree* tree_; 
    TFile* current_file_;
    //TFile* input_file_;
    TDirectoryFile *input_directory_;
    //---- TREE variable --------
    QCDEvent *event_;
    ObjectSelector<QCDPFJet> *dijet_selector_;
    ObjectSelector<QCDPFJet> *pfjet_selector_;
    ObjectSelector<QCDCaloJet> *calojet_selector_;
    EventSelector<QCDEvent> *event_selector_;
    Root::HistogramManager* global_histograms_;
    std::map<TString, Root::HistogramManager*> histograms_reference_;
    std::map<TString, std::map<TString, Root::HistogramManager*> > histograms_test_;
    
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

};


#endif