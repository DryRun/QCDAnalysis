#ifndef PDFUncertainty_h
#define PDFUncertainty_h

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

class PDFUncertainty : public edm::EDAnalyzer
{
  public:
	explicit PDFUncertainty(edm::ParameterSet const& cfg);
	virtual void beginJob();
	virtual void analyze(edm::Event const& evt, edm::EventSetup const& iSetup);
	virtual void endJob();
	virtual ~PDFUncertainty() {}

  private:  
	//---- configurable parameters --------   
	float signal_mass_;
	std::vector<std::string> input_file_names_;
	TString input_tree_name_;
	
	edm::Service<TFileService> fs_;
	TTree* tree_; 
	TFile* current_file_;
	TDirectoryFile *input_directory_;
	QCDEvent *event_;
	
};


#endif