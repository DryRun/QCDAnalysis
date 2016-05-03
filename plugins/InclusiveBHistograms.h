#ifndef InclusiveBHistograms_h
#define InclusiveBHistograms_h

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

class InclusiveBHistograms : public edm::EDAnalyzer
{
  public:
    explicit InclusiveBHistograms(edm::ParameterSet const& cfg);
    virtual void beginJob();
    virtual void analyze(edm::Event const& evt, edm::EventSetup const& iSetup);
    virtual void endJob();
    virtual ~InclusiveBHistograms() {}

  private:  
    int getBin(double x, const std::vector<double>& boundaries); 

    //---- configurable parameters --------   
    std::vector<std::string> input_file_names_;
    TString input_tree_name_;
    TString trigger_histogram_name_;
    std::vector<std::string> trigger_list_unparsed_;
    std::vector<std::pair<TString, TString> > triggers_;
    std::vector<TString> hlt_triggers_;
    std::vector<TString> l1_triggers_;
    std::vector<int> hlt_indices_;
    std::map<int, TString> hlt_index_to_l1_name_;
    std::map<int, TString> hlt_index_to_hlt_name_;
    
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
    
    int n_total_;
    int n_pass_;
};


#endif