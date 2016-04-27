#ifndef QCDEventCutFunctions_cxx
#define QCDEventCutFunctions_cxx

#include "CMSDIJET/QCDAnalysis/interface/QCDEventCutFunctions.h"

namespace QCDEventCutFunctions {
	bool MinNPFJets(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		return (p_data.nPFJets() >= (unsigned int)(p_event_selector->GetCutParameters("MinNPFJets")[0]));
	}
	
	bool MaxNPFJets(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		return p_data.nPFJets() <= (unsigned int)(p_event_selector->GetCutParameters("MaxNPFJets")[0]);
	}

	bool MinNCaloJets(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		return p_data.nCaloJets() >= (unsigned int)(p_event_selector->GetCutParameters("MinNCaloJets")[0]);
	}
	
	bool MaxNCaloJets(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		return p_data.nCaloJets() <= (unsigned int)(p_event_selector->GetCutParameters("MaxNCaloJets")[0]);
	}

	bool MinLeadingPFJetPt(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		bool pass = true;
		if (p_data.nPFJets() < 1) {
			pass = false;
		} else {
			pass = p_data.calojet(0).ptCor() > p_event_selector->GetCutParameters("MinLeadingPFJetPt")[0];
		}
		return pass;
	}

	bool MinSubleadingPFJetPt(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		bool pass = true;
		if (p_data.nPFJets() < 2) {
			pass = false;
		} else {
			pass = p_data.calojet(1).ptCor() > p_event_selector->GetCutParameters("MinSubleadingPFJetPt")[0];
		}
		return pass;
	}

	bool MaxLeadingPFJetEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		bool pass = true;
		if (p_data.nPFJets() < 1) {
			pass = false;
		} else {
			pass = TMath::Abs(p_data.calojet(0).eta()) < p_event_selector->GetCutParameters("MaxLeadingPFJetEta")[0];
		}
		return pass;
	}

	bool MaxSubleadingPFJetEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		bool pass = true;
		if (p_data.nPFJets() < 2) {
			pass = false;
		} else {
			pass = TMath::Abs(p_data.calojet(1).eta()) < p_event_selector->GetCutParameters("MaxSubleadingPFJetEta")[0];
		}
		return pass;
	}

	bool MinLeadingCaloJetPt(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		bool pass = true;
		if (p_data.nCaloJets() < 1) {
			pass = false;
		} else {
			pass = p_data.calojet(0).ptCor() > p_event_selector->GetCutParameters("MinLeadingCaloJetPt")[0];
		}
		return pass;
	}

	bool MinSubleadingCaloJetPt(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		bool pass = true;
		if (p_data.nCaloJets() < 2) {
			pass = false;
		} else {
			pass = p_data.calojet(1).ptCor() > p_event_selector->GetCutParameters("MinSubleadingCaloJetPt")[0];
		}
		return pass;
	}

	bool MaxLeadingCaloJetEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		bool pass = true;
		if (p_data.nCaloJets() < 1) {
			pass = false;
		} else {
			pass = TMath::Abs(p_data.calojet(0).eta()) < p_event_selector->GetCutParameters("MaxLeadingCaloJetEta")[0];
		}
		return pass;
	}

	bool MaxSubleadingCaloJetEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		bool pass = true;
		if (p_data.nCaloJets() < 2) {
			pass = false;
		} else {
			pass = TMath::Abs(p_data.calojet(1).eta()) < p_event_selector->GetCutParameters("MaxSubleadingCaloJetEta")[0];
		}
		return pass;
	}

	bool MinPFMjj(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		return p_data.pfmjj() > p_event_selector->GetCutParameters("MinPFMjj")[0];
	}

	bool MaxPFMjj(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		return p_data.pfmjj() < p_event_selector->GetCutParameters("MinPFMjj")[0];
	}

	bool MinCaloMjj(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		return p_data.calomjj() > p_event_selector->GetCutParameters("MinCaloMjj")[0];
	}

	bool MaxCaloMjj(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		return p_data.calomjj() < p_event_selector->GetCutParameters("MinCaloMjj")[0];
	}

	bool MinPFDeltaEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		return TMath::Abs(p_data.pfjet(0).eta() - p_data.pfjet(1).eta()) > p_event_selector->GetCutParameters("MinPFDeltaEta")[0];
	}

	bool MaxPFDeltaEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		return TMath::Abs(p_data.pfjet(0).eta() - p_data.pfjet(1).eta()) < p_event_selector->GetCutParameters("MinPFDeltaEta")[0];
	}

	bool MinCaloDeltaEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		return TMath::Abs(p_data.calojet(0).eta() - p_data.calojet(1).eta()) > p_event_selector->GetCutParameters("MinCaloDeltaEta")[0];
	}

	bool MaxCaloDeltaEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		return TMath::Abs(p_data.calojet(0).eta() - p_data.calojet(1).eta()) < p_event_selector->GetCutParameters("MinCaloDeltaEta")[0];
	}

	bool LeadingBTagPF(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		float btag = 0.;
		if (p_event_selector->GetCutDescriptors("LeadingBTagPF")[0].EqualTo("tche")) {
			btag = p_data.pfjet(0).btag_tche();
		} else if (p_event_selector->GetCutDescriptors("LeadingBTagPF")[0].EqualTo("tchp")) {
			btag = p_data.pfjet(0).btag_tchp();
		} else if (p_event_selector->GetCutDescriptors("LeadingBTagPF")[0].EqualTo("csv")) {
			btag = p_data.pfjet(0).btag_csv();
		} else if (p_event_selector->GetCutDescriptors("LeadingBTagPF")[0].EqualTo("ssvhe")) {
			btag = p_data.pfjet(0).btag_ssvhe();
		} else if (p_event_selector->GetCutDescriptors("LeadingBTagPF")[0].EqualTo("ssvhp")) {
			btag = p_data.pfjet(0).btag_ssvhp();
		} else if (p_event_selector->GetCutDescriptors("LeadingBTagPF")[0].EqualTo("jp")) {
			btag = p_data.pfjet(0).btag_jp();
		} else {
			std::cerr << "[QCDEventCutFunctions::LeadingBTagPF] ERROR : Unknown b-tag type: " << p_event_selector->GetCutDescriptors("LeadingBTagPF")[0] << std::endl;
			exit(1);
		} 
		return btag > p_event_selector->GetCutParameters("LeadingBTagPF")[0];
	}

	bool LeadingBTagCalo(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		float btag = 0.;
		if (p_event_selector->GetCutDescriptors("LeadingBTagCalo")[0].EqualTo("tche")) {
			btag = p_data.calojet(0).btag_tche();
		} else if (p_event_selector->GetCutDescriptors("LeadingBTagCalo")[0].EqualTo("tchp")) {
			btag = p_data.calojet(0).btag_tchp();
		} else if (p_event_selector->GetCutDescriptors("LeadingBTagCalo")[0].EqualTo("csv")) {
			btag = p_data.calojet(0).btag_csv();
		} else if (p_event_selector->GetCutDescriptors("LeadingBTagCalo")[0].EqualTo("ssvhe")) {
			btag = p_data.calojet(0).btag_ssvhe();
		} else if (p_event_selector->GetCutDescriptors("LeadingBTagCalo")[0].EqualTo("ssvhp")) {
			btag = p_data.calojet(0).btag_ssvhp();
		} else if (p_event_selector->GetCutDescriptors("LeadingBTagCalo")[0].EqualTo("jp")) {
			btag = p_data.calojet(0).btag_jp();
		} else {
			std::cerr << "[QCDEventCutFunctions::LeadingBTagCalo] ERROR : Unknown b-tag type: " << p_event_selector->GetCutDescriptors("LeadingBTagCalo")[0] << std::endl;
			exit(1);
		} 
		return btag > p_event_selector->GetCutParameters("LeadingBTagCalo")[0];
	}

	bool SubleadingBTagPF(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		float btag = 0.;
		if (p_event_selector->GetCutDescriptors("SubleadingBTagPF")[0].EqualTo("tche")) {
			btag = p_data.pfjet(0).btag_tche();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBTagPF")[0].EqualTo("tchp")) {
			btag = p_data.pfjet(0).btag_tchp();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBTagPF")[0].EqualTo("csv")) {
			btag = p_data.pfjet(0).btag_csv();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBTagPF")[0].EqualTo("ssvhe")) {
			btag = p_data.pfjet(0).btag_ssvhe();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBTagPF")[0].EqualTo("ssvhp")) {
			btag = p_data.pfjet(0).btag_ssvhp();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBTagPF")[0].EqualTo("jp")) {
			btag = p_data.pfjet(0).btag_jp();
		} else {
			std::cerr << "[QCDEventCutFunctions::SubleadingBTagPF] ERROR : Unknown b-tag type: " << p_event_selector->GetCutDescriptors("SubleadingBTagPF")[0] << std::endl;
			exit(1);
		} 
		return btag > p_event_selector->GetCutParameters("SubleadingBTagPF")[0];
	}

	bool SubleadingBTagCalo(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		float btag = 0.;
		if (p_event_selector->GetCutDescriptors("SubleadingBTagCalo")[0].EqualTo("tche")) {
			btag = p_data.calojet(0).btag_tche();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBTagCalo")[0].EqualTo("tchp")) {
			btag = p_data.calojet(0).btag_tchp();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBTagCalo")[0].EqualTo("csv")) {
			btag = p_data.calojet(0).btag_csv();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBTagCalo")[0].EqualTo("ssvhe")) {
			btag = p_data.calojet(0).btag_ssvhe();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBTagCalo")[0].EqualTo("ssvhp")) {
			btag = p_data.calojet(0).btag_ssvhp();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBTagCalo")[0].EqualTo("jp")) {
			btag = p_data.calojet(0).btag_jp();
		} else {
			std::cerr << "[QCDEventCutFunctions::SubleadingBTagCalo] ERROR : Unknown b-tag type: " << p_event_selector->GetCutDescriptors("SubleadingBTagCalo")[0] << std::endl;
			exit(1);
		} 
		return btag > p_event_selector->GetCutParameters("SubleadingBTagCalo")[0];
	}

	bool LeadingBVetoPF(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		float btag = 0.;
		if (p_event_selector->GetCutDescriptors("LeadingBVetoPF")[0].EqualTo("tche")) {
			btag = p_data.pfjet(0).btag_tche();
		} else if (p_event_selector->GetCutDescriptors("LeadingBVetoPF")[0].EqualTo("tchp")) {
			btag = p_data.pfjet(0).btag_tchp();
		} else if (p_event_selector->GetCutDescriptors("LeadingBVetoPF")[0].EqualTo("csv")) {
			btag = p_data.pfjet(0).btag_csv();
		} else if (p_event_selector->GetCutDescriptors("LeadingBVetoPF")[0].EqualTo("ssvhe")) {
			btag = p_data.pfjet(0).btag_ssvhe();
		} else if (p_event_selector->GetCutDescriptors("LeadingBVetoPF")[0].EqualTo("ssvhp")) {
			btag = p_data.pfjet(0).btag_ssvhp();
		} else if (p_event_selector->GetCutDescriptors("LeadingBVetoPF")[0].EqualTo("jp")) {
			btag = p_data.pfjet(0).btag_jp();
		} else {
			std::cerr << "[QCDEventCutFunctions::LeadingBVetoPF] ERROR : Unknown b-tag type: " << p_event_selector->GetCutDescriptors("LeadingBVetoPF")[0] << std::endl;
			exit(1);
		} 
		return btag < p_event_selector->GetCutParameters("LeadingBVetoPF")[0];
	}

	bool LeadingBVetoCalo(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		float btag = 0.;
		if (p_event_selector->GetCutDescriptors("LeadingBVetoCalo")[0].EqualTo("tche")) {
			btag = p_data.calojet(0).btag_tche();
		} else if (p_event_selector->GetCutDescriptors("LeadingBVetoCalo")[0].EqualTo("tchp")) {
			btag = p_data.calojet(0).btag_tchp();
		} else if (p_event_selector->GetCutDescriptors("LeadingBVetoCalo")[0].EqualTo("csv")) {
			btag = p_data.calojet(0).btag_csv();
		} else if (p_event_selector->GetCutDescriptors("LeadingBVetoCalo")[0].EqualTo("ssvhe")) {
			btag = p_data.calojet(0).btag_ssvhe();
		} else if (p_event_selector->GetCutDescriptors("LeadingBVetoCalo")[0].EqualTo("ssvhp")) {
			btag = p_data.calojet(0).btag_ssvhp();
		} else if (p_event_selector->GetCutDescriptors("LeadingBVetoCalo")[0].EqualTo("jp")) {
			btag = p_data.calojet(0).btag_jp();
		} else {
			std::cerr << "[QCDEventCutFunctions::LeadingBVetoCalo] ERROR : Unknown b-tag type: " << p_event_selector->GetCutDescriptors("LeadingBVetoCalo")[0] << std::endl;
			exit(1);
		} 
		return btag < p_event_selector->GetCutParameters("LeadingBVetoCalo")[0];
	}

	bool SubleadingBVetoPF(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		float btag = 0.;
		if (p_event_selector->GetCutDescriptors("SubleadingBVetoPF")[0].EqualTo("tche")) {
			btag = p_data.pfjet(0).btag_tche();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBVetoPF")[0].EqualTo("tchp")) {
			btag = p_data.pfjet(0).btag_tchp();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBVetoPF")[0].EqualTo("csv")) {
			btag = p_data.pfjet(0).btag_csv();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBVetoPF")[0].EqualTo("ssvhe")) {
			btag = p_data.pfjet(0).btag_ssvhe();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBVetoPF")[0].EqualTo("ssvhp")) {
			btag = p_data.pfjet(0).btag_ssvhp();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBVetoPF")[0].EqualTo("jp")) {
			btag = p_data.pfjet(0).btag_jp();
		} else {
			std::cerr << "[QCDEventCutFunctions::SubleadingBVetoPF] ERROR : Unknown b-tag type: " << p_event_selector->GetCutDescriptors("SubleadingBVetoPF")[0] << std::endl;
			exit(1);
		} 
		return btag < p_event_selector->GetCutParameters("SubleadingBVetoPF")[0];
	}

	bool SubleadingBVetoCalo(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		float btag = 0.;
		if (p_event_selector->GetCutDescriptors("SubleadingBVetoCalo")[0].EqualTo("tche")) {
			btag = p_data.calojet(0).btag_tche();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBVetoCalo")[0].EqualTo("tchp")) {
			btag = p_data.calojet(0).btag_tchp();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBVetoCalo")[0].EqualTo("csv")) {
			btag = p_data.calojet(0).btag_csv();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBVetoCalo")[0].EqualTo("ssvhe")) {
			btag = p_data.calojet(0).btag_ssvhe();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBVetoCalo")[0].EqualTo("ssvhp")) {
			btag = p_data.calojet(0).btag_ssvhp();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBVetoCalo")[0].EqualTo("jp")) {
			btag = p_data.calojet(0).btag_jp();
		} else {
			std::cerr << "[QCDEventCutFunctions::SubleadingBVetoCalo] ERROR : Unknown b-tag type: " << p_event_selector->GetCutDescriptors("SubleadingBVetoCalo")[0] << std::endl;
			exit(1);
		} 
		return btag < p_event_selector->GetCutParameters("SubleadingBVetoCalo")[0];
	}
	bool IsGoodPV(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		return p_data.evtHdr().isPVgood();
	}


	void Configure(EventSelector<QCDEvent>* p_event_selector) {
		p_event_selector->AddCutFunction("MinNPFJets", &MinNPFJets);
		p_event_selector->AddCutFunction("MaxNPFJets", &MaxNPFJets);
		p_event_selector->AddCutFunction("MinNCaloJets", &MinNCaloJets);
		p_event_selector->AddCutFunction("MaxNCaloJets", &MaxNCaloJets);
		p_event_selector->AddCutFunction("MinLeadingPFJetPt", &MinLeadingPFJetPt);
		p_event_selector->AddCutFunction("MinSubleadingPFJetPt", &MinSubleadingPFJetPt);
		p_event_selector->AddCutFunction("MaxLeadingPFJetEta", &MaxLeadingPFJetEta);
		p_event_selector->AddCutFunction("MaxSubleadingPFJetEta", &MaxSubleadingPFJetEta);
		p_event_selector->AddCutFunction("MinLeadingCaloJetPt", &MinLeadingCaloJetPt);
		p_event_selector->AddCutFunction("MinSubleadingCaloJetPt", &MinSubleadingCaloJetPt);
		p_event_selector->AddCutFunction("MaxLeadingCaloJetEta", &MaxLeadingCaloJetEta);
		p_event_selector->AddCutFunction("MaxSubleadingCaloJetEta", &MaxSubleadingCaloJetEta);
		p_event_selector->AddCutFunction("MinPFMjj", &MinPFMjj);
		p_event_selector->AddCutFunction("MaxPFMjj", &MaxPFMjj);
		p_event_selector->AddCutFunction("MinCaloMjj", &MinCaloMjj);
		p_event_selector->AddCutFunction("MaxCaloMjj", &MaxCaloMjj);
		p_event_selector->AddCutFunction("MinPFDeltaEta", &MinPFDeltaEta);
		p_event_selector->AddCutFunction("MaxPFDeltaEta", &MaxPFDeltaEta);
		p_event_selector->AddCutFunction("MinCaloDeltaEta", &MinCaloDeltaEta);
		p_event_selector->AddCutFunction("MaxCaloDeltaEta", &MaxCaloDeltaEta);
		p_event_selector->AddCutFunction("LeadingBTagPF", &LeadingBTagPF);
		p_event_selector->AddCutFunction("LeadingBTagCalo", &LeadingBTagCalo);
		p_event_selector->AddCutFunction("SubleadingBTagPF", &SubleadingBTagPF);
		p_event_selector->AddCutFunction("SubleadingBTagCalo", &SubleadingBTagCalo);
		p_event_selector->AddCutFunction("LeadingBVetoPF", &LeadingBVetoPF);
		p_event_selector->AddCutFunction("LeadingBVetoCalo", &LeadingBVetoCalo);
		p_event_selector->AddCutFunction("SubleadingBVetoPF", &SubleadingBVetoPF);
		p_event_selector->AddCutFunction("SubleadingBVetoCalo", &SubleadingBVetoCalo);
		p_event_selector->AddCutFunction("IsGoodPV", &IsGoodPV);

		p_event_selector->SetObjectName("Event");
	}

}


#endif