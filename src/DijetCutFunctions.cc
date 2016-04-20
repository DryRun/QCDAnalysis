#ifndef DijetCutFunctions_cxx
#define DijetCutFunctions_cxx

#include "CMSDIJET/QCDAnalysis/interface/DijetCutFunctions.h"

namespace QCDEventCutFunctions {
	bool MinNPFJets(QCDEvent& p_data, Cutflow* p_cutflow) {
		return (p_data.nPFJets() >= (unsigned int)(p_cutflow->GetCutParameters("MinNPFJets")[0]));
	}
	
	bool MaxNPFJets(QCDEvent& p_data, Cutflow* p_cutflow) {
		return p_data.nPFJets() <= (unsigned int)(p_cutflow->GetCutParameters("MaxNPFJets")[0]);
	}

	bool MinNCaloJets(QCDEvent& p_data, Cutflow* p_cutflow) {
		return p_data.nCaloJets() >= (unsigned int)(p_cutflow->GetCutParameters("MinNCaloJets")[0]);
	}
	
	bool MaxNCaloJets(QCDEvent& p_data, Cutflow* p_cutflow) {
		return p_data.nCaloJets() <= (unsigned int)(p_cutflow->GetCutParameters("MaxNCaloJets")[0]);
	}

	bool MinLeadingPFJetPt(QCDEvent& p_data, Cutflow* p_cutflow) {
		bool pass = true;
		if (p_data.nPFJets() < 1) {
			pass = false;
		} else {
			pass = p_data.calojet(0).ptCor() > p_cutflow->GetCutParameters("MinLeadingPFJetPt")[0];
		}
		return pass;
	}

	bool MinSubleadingPFJetPt(QCDEvent& p_data, Cutflow* p_cutflow) {
		bool pass = true;
		if (p_data.nPFJets() < 2) {
			pass = false;
		} else {
			pass = p_data.calojet(1).ptCor() > p_cutflow->GetCutParameters("MinSubleadingPFJetPt")[0];
		}
		return pass;
	}

	bool MaxLeadingPFJetEta(QCDEvent& p_data, Cutflow* p_cutflow) {
		bool pass = true;
		if (p_data.nPFJets() < 1) {
			pass = false;
		} else {
			pass = TMath::Abs(p_data.calojet(0).eta()) < p_cutflow->GetCutParameters("MaxLeadingPFJetEta")[0];
		}
		return pass;
	}

	bool MaxSubleadingPFJetEta(QCDEvent& p_data, Cutflow* p_cutflow) {
		bool pass = true;
		if (p_data.nPFJets() < 2) {
			pass = false;
		} else {
			pass = TMath::Abs(p_data.calojet(1).eta()) < p_cutflow->GetCutParameters("MaxSubleadingPFJetEta")[0];
		}
		return pass;
	}

	bool MinLeadingCaloJetPt(QCDEvent& p_data, Cutflow* p_cutflow) {
		bool pass = true;
		if (p_data.nCaloJets() < 1) {
			pass = false;
		} else {
			pass = p_data.calojet(0).ptCor() > p_cutflow->GetCutParameters("MinLeadingCaloJetPt")[0];
		}
		return pass;
	}

	bool MinSubleadingCaloJetPt(QCDEvent& p_data, Cutflow* p_cutflow) {
		bool pass = true;
		if (p_data.nCaloJets() < 2) {
			pass = false;
		} else {
			pass = p_data.calojet(1).ptCor() > p_cutflow->GetCutParameters("MinSubleadingCaloJetPt")[0];
		}
		return pass;
	}

	bool MaxLeadingCaloJetEta(QCDEvent& p_data, Cutflow* p_cutflow) {
		bool pass = true;
		if (p_data.nCaloJets() < 1) {
			pass = false;
		} else {
			pass = TMath::Abs(p_data.calojet(0).eta()) < p_cutflow->GetCutParameters("MaxLeadingCaloJetEta")[0];
		}
		return pass;
	}

	bool MaxSubleadingCaloJetEta(QCDEvent& p_data, Cutflow* p_cutflow) {
		bool pass = true;
		if (p_data.nCaloJets() < 2) {
			pass = false;
		} else {
			pass = TMath::Abs(p_data.calojet(1).eta()) < p_cutflow->GetCutParameters("MaxSubleadingCaloJetEta")[0];
		}
		return pass;
	}

	bool MinPFMjj(QCDEvent& p_data, Cutflow* p_cutflow) {
		return p_data.pfmjj() > p_cutflow->GetCutParameters("MinPFMjj")[0];
	}

	bool MaxPFMjj(QCDEvent& p_data, Cutflow* p_cutflow) {
		return p_data.pfmjj() < p_cutflow->GetCutParameters("MinPFMjj")[0];
	}

	bool MinCaloMjj(QCDEvent& p_data, Cutflow* p_cutflow) {
		return p_data.calomjj() > p_cutflow->GetCutParameters("MinCaloMjj")[0];
	}

	bool MaxCaloMjj(QCDEvent& p_data, Cutflow* p_cutflow) {
		return p_data.calomjj() < p_cutflow->GetCutParameters("MinCaloMjj")[0];
	}

	bool MinPFDeltaEta(QCDEvent& p_data, Cutflow* p_cutflow) {
		return TMath::Abs(p_data.pfjet(0).eta() - p_data.pfjet(1).eta()) > p_cutflow->GetCutParameters("MinPFDeltaEta")[0];
	}

	bool MaxPFDeltaEta(QCDEvent& p_data, Cutflow* p_cutflow) {
		return TMath::Abs(p_data.pfjet(0).eta() - p_data.pfjet(1).eta()) < p_cutflow->GetCutParameters("MinPFDeltaEta")[0];
	}

	bool MinCaloDeltaEta(QCDEvent& p_data, Cutflow* p_cutflow) {
		return TMath::Abs(p_data.calojet(0).eta() - p_data.calojet(1).eta()) > p_cutflow->GetCutParameters("MinCaloDeltaEta")[0];
	}

	bool MaxCaloDeltaEta(QCDEvent& p_data, Cutflow* p_cutflow) {
		return TMath::Abs(p_data.calojet(0).eta() - p_data.calojet(1).eta()) < p_cutflow->GetCutParameters("MinCaloDeltaEta")[0];
	}

	bool LeadingBTagPF(QCDEvent& p_data, Cutflow* p_cutflow) {
		float btag = 0.;
		if (p_cutflow->GetCutDescriptors("LeadingBTagPF")[0].EqualTo("tche")) {
			btag = p_data.pfjet(0).btag_tche();
		} else if (p_cutflow->GetCutDescriptors("LeadingBTagPF")[0].EqualTo("tchp")) {
			btag = p_data.pfjet(0).btag_tchp();
		} else if (p_cutflow->GetCutDescriptors("LeadingBTagPF")[0].EqualTo("csv")) {
			btag = p_data.pfjet(0).btag_csv();
		} else if (p_cutflow->GetCutDescriptors("LeadingBTagPF")[0].EqualTo("ssvhe")) {
			btag = p_data.pfjet(0).btag_ssvhe();
		} else if (p_cutflow->GetCutDescriptors("LeadingBTagPF")[0].EqualTo("ssvhp")) {
			btag = p_data.pfjet(0).btag_ssvhp();
		} else if (p_cutflow->GetCutDescriptors("LeadingBTagPF")[0].EqualTo("jp")) {
			btag = p_data.pfjet(0).btag_jp();
		} else {
			std::cerr << "[DijetCutFunctions::LeadingBTagPF] ERROR : Unknown b-tag type: " << p_cutflow->GetCutDescriptors("LeadingBTagPF")[0] << std::endl;
			exit(1);
		} 
		return btag > p_cutflow->GetCutParameters("LeadingBTagPF")[0];
	}

	bool LeadingBTagCalo(QCDEvent& p_data, Cutflow* p_cutflow) {
		float btag = 0.;
		if (p_cutflow->GetCutDescriptors("LeadingBTagCalo")[0].EqualTo("tche")) {
			btag = p_data.calojet(0).btag_tche();
		} else if (p_cutflow->GetCutDescriptors("LeadingBTagCalo")[0].EqualTo("tchp")) {
			btag = p_data.calojet(0).btag_tchp();
		} else if (p_cutflow->GetCutDescriptors("LeadingBTagCalo")[0].EqualTo("csv")) {
			btag = p_data.calojet(0).btag_csv();
		} else if (p_cutflow->GetCutDescriptors("LeadingBTagCalo")[0].EqualTo("ssvhe")) {
			btag = p_data.calojet(0).btag_ssvhe();
		} else if (p_cutflow->GetCutDescriptors("LeadingBTagCalo")[0].EqualTo("ssvhp")) {
			btag = p_data.calojet(0).btag_ssvhp();
		} else if (p_cutflow->GetCutDescriptors("LeadingBTagCalo")[0].EqualTo("jp")) {
			btag = p_data.calojet(0).btag_jp();
		} else {
			std::cerr << "[DijetCutFunctions::LeadingBTagCalo] ERROR : Unknown b-tag type: " << p_cutflow->GetCutDescriptors("LeadingBTagCalo")[0] << std::endl;
			exit(1);
		} 
		return btag > p_cutflow->GetCutParameters("LeadingBTagCalo")[0];
	}

	bool SubleadingBTagPF(QCDEvent& p_data, Cutflow* p_cutflow) {
		float btag = 0.;
		if (p_cutflow->GetCutDescriptors("SubleadingBTagPF")[0].EqualTo("tche")) {
			btag = p_data.pfjet(0).btag_tche();
		} else if (p_cutflow->GetCutDescriptors("SubleadingBTagPF")[0].EqualTo("tchp")) {
			btag = p_data.pfjet(0).btag_tchp();
		} else if (p_cutflow->GetCutDescriptors("SubleadingBTagPF")[0].EqualTo("csv")) {
			btag = p_data.pfjet(0).btag_csv();
		} else if (p_cutflow->GetCutDescriptors("SubleadingBTagPF")[0].EqualTo("ssvhe")) {
			btag = p_data.pfjet(0).btag_ssvhe();
		} else if (p_cutflow->GetCutDescriptors("SubleadingBTagPF")[0].EqualTo("ssvhp")) {
			btag = p_data.pfjet(0).btag_ssvhp();
		} else if (p_cutflow->GetCutDescriptors("SubleadingBTagPF")[0].EqualTo("jp")) {
			btag = p_data.pfjet(0).btag_jp();
		} else {
			std::cerr << "[DijetCutFunctions::SubleadingBTagPF] ERROR : Unknown b-tag type: " << p_cutflow->GetCutDescriptors("SubleadingBTagPF")[0] << std::endl;
			exit(1);
		} 
		return btag > p_cutflow->GetCutParameters("SubleadingBTagPF")[0];
	}

	bool SubleadingBTagCalo(QCDEvent& p_data, Cutflow* p_cutflow) {
		float btag = 0.;
		if (p_cutflow->GetCutDescriptors("SubleadingBTagCalo")[0].EqualTo("tche")) {
			btag = p_data.calojet(0).btag_tche();
		} else if (p_cutflow->GetCutDescriptors("SubleadingBTagCalo")[0].EqualTo("tchp")) {
			btag = p_data.calojet(0).btag_tchp();
		} else if (p_cutflow->GetCutDescriptors("SubleadingBTagCalo")[0].EqualTo("csv")) {
			btag = p_data.calojet(0).btag_csv();
		} else if (p_cutflow->GetCutDescriptors("SubleadingBTagCalo")[0].EqualTo("ssvhe")) {
			btag = p_data.calojet(0).btag_ssvhe();
		} else if (p_cutflow->GetCutDescriptors("SubleadingBTagCalo")[0].EqualTo("ssvhp")) {
			btag = p_data.calojet(0).btag_ssvhp();
		} else if (p_cutflow->GetCutDescriptors("SubleadingBTagCalo")[0].EqualTo("jp")) {
			btag = p_data.calojet(0).btag_jp();
		} else {
			std::cerr << "[DijetCutFunctions::SubleadingBTagCalo] ERROR : Unknown b-tag type: " << p_cutflow->GetCutDescriptors("SubleadingBTagCalo")[0] << std::endl;
			exit(1);
		} 
		return btag > p_cutflow->GetCutParameters("SubleadingBTagCalo")[0];
	}

	bool LeadingBVetoPF(QCDEvent& p_data, Cutflow* p_cutflow) {
		float btag = 0.;
		if (p_cutflow->GetCutDescriptors("LeadingBVetoPF")[0].EqualTo("tche")) {
			btag = p_data.pfjet(0).btag_tche();
		} else if (p_cutflow->GetCutDescriptors("LeadingBVetoPF")[0].EqualTo("tchp")) {
			btag = p_data.pfjet(0).btag_tchp();
		} else if (p_cutflow->GetCutDescriptors("LeadingBVetoPF")[0].EqualTo("csv")) {
			btag = p_data.pfjet(0).btag_csv();
		} else if (p_cutflow->GetCutDescriptors("LeadingBVetoPF")[0].EqualTo("ssvhe")) {
			btag = p_data.pfjet(0).btag_ssvhe();
		} else if (p_cutflow->GetCutDescriptors("LeadingBVetoPF")[0].EqualTo("ssvhp")) {
			btag = p_data.pfjet(0).btag_ssvhp();
		} else if (p_cutflow->GetCutDescriptors("LeadingBVetoPF")[0].EqualTo("jp")) {
			btag = p_data.pfjet(0).btag_jp();
		} else {
			std::cerr << "[DijetCutFunctions::LeadingBVetoPF] ERROR : Unknown b-tag type: " << p_cutflow->GetCutDescriptors("LeadingBVetoPF")[0] << std::endl;
			exit(1);
		} 
		return btag < p_cutflow->GetCutParameters("LeadingBVetoPF")[0];
	}

	bool LeadingBVetoCalo(QCDEvent& p_data, Cutflow* p_cutflow) {
		float btag = 0.;
		if (p_cutflow->GetCutDescriptors("LeadingBVetoCalo")[0].EqualTo("tche")) {
			btag = p_data.calojet(0).btag_tche();
		} else if (p_cutflow->GetCutDescriptors("LeadingBVetoCalo")[0].EqualTo("tchp")) {
			btag = p_data.calojet(0).btag_tchp();
		} else if (p_cutflow->GetCutDescriptors("LeadingBVetoCalo")[0].EqualTo("csv")) {
			btag = p_data.calojet(0).btag_csv();
		} else if (p_cutflow->GetCutDescriptors("LeadingBVetoCalo")[0].EqualTo("ssvhe")) {
			btag = p_data.calojet(0).btag_ssvhe();
		} else if (p_cutflow->GetCutDescriptors("LeadingBVetoCalo")[0].EqualTo("ssvhp")) {
			btag = p_data.calojet(0).btag_ssvhp();
		} else if (p_cutflow->GetCutDescriptors("LeadingBVetoCalo")[0].EqualTo("jp")) {
			btag = p_data.calojet(0).btag_jp();
		} else {
			std::cerr << "[DijetCutFunctions::LeadingBVetoCalo] ERROR : Unknown b-tag type: " << p_cutflow->GetCutDescriptors("LeadingBVetoCalo")[0] << std::endl;
			exit(1);
		} 
		return btag < p_cutflow->GetCutParameters("LeadingBVetoCalo")[0];
	}

	bool SubleadingBVetoPF(QCDEvent& p_data, Cutflow* p_cutflow) {
		float btag = 0.;
		if (p_cutflow->GetCutDescriptors("SubleadingBVetoPF")[0].EqualTo("tche")) {
			btag = p_data.pfjet(0).btag_tche();
		} else if (p_cutflow->GetCutDescriptors("SubleadingBVetoPF")[0].EqualTo("tchp")) {
			btag = p_data.pfjet(0).btag_tchp();
		} else if (p_cutflow->GetCutDescriptors("SubleadingBVetoPF")[0].EqualTo("csv")) {
			btag = p_data.pfjet(0).btag_csv();
		} else if (p_cutflow->GetCutDescriptors("SubleadingBVetoPF")[0].EqualTo("ssvhe")) {
			btag = p_data.pfjet(0).btag_ssvhe();
		} else if (p_cutflow->GetCutDescriptors("SubleadingBVetoPF")[0].EqualTo("ssvhp")) {
			btag = p_data.pfjet(0).btag_ssvhp();
		} else if (p_cutflow->GetCutDescriptors("SubleadingBVetoPF")[0].EqualTo("jp")) {
			btag = p_data.pfjet(0).btag_jp();
		} else {
			std::cerr << "[DijetCutFunctions::SubleadingBVetoPF] ERROR : Unknown b-tag type: " << p_cutflow->GetCutDescriptors("SubleadingBVetoPF")[0] << std::endl;
			exit(1);
		} 
		return btag < p_cutflow->GetCutParameters("SubleadingBVetoPF")[0];
	}

	bool SubleadingBVetoCalo(QCDEvent& p_data, Cutflow* p_cutflow) {
		float btag = 0.;
		if (p_cutflow->GetCutDescriptors("SubleadingBVetoCalo")[0].EqualTo("tche")) {
			btag = p_data.calojet(0).btag_tche();
		} else if (p_cutflow->GetCutDescriptors("SubleadingBVetoCalo")[0].EqualTo("tchp")) {
			btag = p_data.calojet(0).btag_tchp();
		} else if (p_cutflow->GetCutDescriptors("SubleadingBVetoCalo")[0].EqualTo("csv")) {
			btag = p_data.calojet(0).btag_csv();
		} else if (p_cutflow->GetCutDescriptors("SubleadingBVetoCalo")[0].EqualTo("ssvhe")) {
			btag = p_data.calojet(0).btag_ssvhe();
		} else if (p_cutflow->GetCutDescriptors("SubleadingBVetoCalo")[0].EqualTo("ssvhp")) {
			btag = p_data.calojet(0).btag_ssvhp();
		} else if (p_cutflow->GetCutDescriptors("SubleadingBVetoCalo")[0].EqualTo("jp")) {
			btag = p_data.calojet(0).btag_jp();
		} else {
			std::cerr << "[DijetCutFunctions::SubleadingBVetoCalo] ERROR : Unknown b-tag type: " << p_cutflow->GetCutDescriptors("SubleadingBVetoCalo")[0] << std::endl;
			exit(1);
		} 
		return btag < p_cutflow->GetCutParameters("SubleadingBVetoCalo")[0];
	}

}


#endif