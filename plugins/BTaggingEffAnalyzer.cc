// -*- C++ -*-
//
// Package:    BTaggingEffAnalyzer
// Class:      BTaggingEffAnalyzer
// 
/**\class BTaggingEffAnalyzer BTaggingEffAnalyzer.cc Analysis/EDSHyFT/plugins/BTaggingEffAnalyzer.cc

 Description: [one line class summary]

 Implementation:
		 [Notes on implementation]
*/
//
// Original Author:  Dinko Ferencek
//         Created:  Thu Oct  4 20:25:54 CDT 2012
// $Id$
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/JetReco/interface/Jet.h"
//#include "DataFormats/JetReco/interface/PFJetCollection.h"
//#include "DataFormats/JetReco/interface/PFJet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "MyTools/RootUtils/interface/HistogramManager.h"
#include "TH2D.h"


//
// class declaration
//

class BTaggingEffAnalyzer : public edm::EDAnalyzer {
	 public:
			explicit BTaggingEffAnalyzer(const edm::ParameterSet&);
			~BTaggingEffAnalyzer();

			static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


	 private:
			virtual void beginJob() ;
			virtual void analyze(const edm::Event&, const edm::EventSetup&);
			virtual void endJob() ;

			virtual void beginRun(edm::Run const&, edm::EventSetup const&);
			virtual void endRun(edm::Run const&, edm::EventSetup const&);
			virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
			virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

			// ----------member data ---------------------------
			const edm::InputTag jets_tag_;
			const std::string   discriminator_tag_;
			std::vector<double>  discriminator_values_;
			const int     pt_nbins_;
			const double  pt_min_;
			const double  pt_max_;
			const int     eta_nbins_;
			const double  eta_min_;
			const double  eta_max_;
			edm::Service<TFileService>  fs_;
			std::map<double, Root::HistogramManager*> histograms_;
};

//
// constants, enums and typedefs
//
typedef std::vector<pat::Jet> PatJetCollection;

//
// static data member definitions
//

//
// constructors and destructor
//
BTaggingEffAnalyzer::BTaggingEffAnalyzer(const edm::ParameterSet& iConfig) :

	jets_tag_(iConfig.getParameter<edm::InputTag>("JetsTag")),
	discriminator_tag_(iConfig.getParameter<std::string>("DiscriminatorTag")),
	discriminator_values_(iConfig.getParameter<std::vector<double> >("DiscriminatorValues")),
	pt_nbins_(iConfig.getParameter<int>("PtNBins")),
	pt_min_(iConfig.getParameter<double>("PtMin")),
	pt_max_(iConfig.getParameter<double>("PtMax")),
	eta_nbins_(iConfig.getParameter<int>("EtaNBins")),
	eta_min_(iConfig.getParameter<double>("EtaMin")),
	eta_max_(iConfig.getParameter<double>("EtaMax"))

{
	 //now do what ever initialization is needed
}


BTaggingEffAnalyzer::~BTaggingEffAnalyzer()
{
 
	 // do anything here that needs to be done at desctruction time
	 // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
BTaggingEffAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
	edm::Handle<PatJetCollection> jets;
	iEvent.getByLabel(jets_tag_,jets);

	// loop over jets
	for(PatJetCollection::const_iterator it_jet = jets->begin(); it_jet != jets->end(); ++it_jet)
	{
		std::cout << "[debug] pt = " << it_jet->pt() << std::endl;
		std::cout << "[debug] eta = " << it_jet->eta() << std::endl;
		std::cout << "[debug] flavor = " << it_jet->partonFlavour() << std::endl;
		std::cout << "[debug] bDiscriminator = " << it_jet->bDiscriminator(discriminator_tag_.c_str()) << std::endl;
		int partonFlavor = it_jet->partonFlavour();
		for (auto& it_wp : discriminator_values_) {
			if( abs(partonFlavor)==5 )
			{
				histograms_[it_wp]->GetTH2D("BTaggingEff_Denom_b")->Fill(it_jet->pt(), it_jet->eta());
				if( it_jet->bDiscriminator(discriminator_tag_.c_str()) >= it_wp ) histograms_[it_wp]->GetTH2D("BTaggingEff_Num_b")->Fill(it_jet->pt(), it_jet->eta());
			}
			else if( abs(partonFlavor)==4 )
			{
				histograms_[it_wp]->GetTH2D("BTaggingEff_Denom_c")->Fill(it_jet->pt(), it_jet->eta());
				if( it_jet->bDiscriminator(discriminator_tag_.c_str()) >= it_wp ) histograms_[it_wp]->GetTH2D("BTaggingEff_Num_c")->Fill(it_jet->pt(), it_jet->eta());
			}
			else
			{
				histograms_[it_wp]->GetTH2D("BTaggingEff_Denom_udsg")->Fill(it_jet->pt(), it_jet->eta());
				if( it_jet->bDiscriminator(discriminator_tag_.c_str()) >= it_wp ) histograms_[it_wp]->GetTH2D("BTaggingEff_Num_udsg")->Fill(it_jet->pt(), it_jet->eta());
			}
		}
	}
}


// ------------ method called once each job just before starting event loop  ------------
void 
BTaggingEffAnalyzer::beginJob()
{
	 for (auto& it_wp : discriminator_values_) {
		histograms_[it_wp] = new Root::HistogramManager();
		if (it_wp == 0.244) {
			histograms_[it_wp]->AddPrefix("h_csvl_");
		} else if (it_wp == 0.679) {
			histograms_[it_wp]->AddPrefix("h_csvm_");
		} else if (it_wp == 0.898) {
			histograms_[it_wp]->AddPrefix("h_csvt_");
		} else {
			TString prefix = "h_csv_";
			prefix += it_wp;
			prefix += "_";
			histograms_[it_wp]->AddPrefix(prefix);
		}
		histograms_[it_wp]->AddTFileService(&fs_);
		histograms_[it_wp]->AddTH2D("BTaggingEff_Denom_b", ";p_{T} [GeV];#eta", "p_{T} [GeV]", pt_nbins_, pt_min_, pt_max_, "#eta", eta_nbins_, eta_min_, eta_max_);
		histograms_[it_wp]->AddTH2D("BTaggingEff_Denom_c", ";p_{T} [GeV];#eta", "p_{T} [GeV]", pt_nbins_, pt_min_, pt_max_, "#eta", eta_nbins_, eta_min_, eta_max_);
		histograms_[it_wp]->AddTH2D("BTaggingEff_Denom_udsg", ";p_{T} [GeV];#eta", "p_{T} [GeV]", pt_nbins_, pt_min_, pt_max_, "#eta", eta_nbins_, eta_min_, eta_max_);
		histograms_[it_wp]->AddTH2D("BTaggingEff_Num_b", ";p_{T} [GeV];#eta", "p_{T} [GeV]", pt_nbins_, pt_min_, pt_max_, "#eta", eta_nbins_, eta_min_, eta_max_);
		histograms_[it_wp]->AddTH2D("BTaggingEff_Num_c", ";p_{T} [GeV];#eta", "p_{T} [GeV]", pt_nbins_, pt_min_, pt_max_, "#eta", eta_nbins_, eta_min_, eta_max_);
		histograms_[it_wp]->AddTH2D("BTaggingEff_Num_udsg", ";p_{T} [GeV];#eta", "p_{T} [GeV]", pt_nbins_, pt_min_, pt_max_, "#eta", eta_nbins_, eta_min_, eta_max_);
	 }

}

// ------------ method called once each job just after ending the event loop  ------------
void 
BTaggingEffAnalyzer::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
void 
BTaggingEffAnalyzer::beginRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
BTaggingEffAnalyzer::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
BTaggingEffAnalyzer::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
BTaggingEffAnalyzer::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
BTaggingEffAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
	//The following says we do not know what parameters are allowed so do no validation
	// Please change this to state exactly what you do use, even if it is no parameters
	edm::ParameterSetDescription desc;
	desc.setUnknown();
	descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(BTaggingEffAnalyzer);
