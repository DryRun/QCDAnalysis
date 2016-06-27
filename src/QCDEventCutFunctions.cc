#ifndef QCDEventCutFunctions_cxx
#define QCDEventCutFunctions_cxx

#include "CMSDIJET/QCDAnalysis/interface/QCDEventCutFunctions.h"

namespace QCDEventCutFunctions {
	bool Trigger(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		int trigger_index = (int)p_event_selector->GetCutParameters("Trigger")[0];
		// Require trigger to be on
		bool trigger_on = (p_data.preHLT(trigger_index) > 0);
		bool trigger_fired = p_data.fired(trigger_index);
		return (trigger_on && trigger_fired);
	}

	bool TriggerXOR(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		int n_fired = 0;
		std::vector<int> fired_trigger_indices;
		for (auto& it_trig : p_event_selector->GetCutParameters("TriggerXOR")) {
			//bool trigger_on = (p_data.preHLT((int)it_trig) > 0);
			int trigger_fired = p_data.fired((int)it_trig);
			if (trigger_fired == 1) { // removed trigger_on because it doesn't work on MC
				++n_fired;
				fired_trigger_indices.push_back((int)it_trig);
			}
		}
		if (n_fired == 1) {
			p_event_selector->SetReturnData("TriggerXOR", fired_trigger_indices[0]);
		} else if (n_fired >= 2) {
			std::cout << "Multiple triggers fired" << std::endl;
			for (auto& it_trig : fired_trigger_indices) {
				std::cout << "\t" << it_trig << std::endl;
			}
		}
		return (n_fired == 1);
	}

	bool TriggerOR(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		int n_fired = 0;
		for (auto& it_trig : p_event_selector->GetCutParameters("TriggerOR")) {
			//bool trigger_on = (p_data.preHLT((int)it_trig) > 0);
			int trigger_fired = p_data.fired((int)it_trig);
			if (trigger_fired == 1) { // removed trigger_on because it doesn't work on MC
				++n_fired;
			}
		}
		return (n_fired >= 1);
	}

	bool MinNPFJets(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		unsigned int n_jets = p_event_selector->GetNumberOfGoodObjects(ObjectIdentifiers::kPFJet);
		p_event_selector->SetReturnData("MinNPFJets", n_jets);
		return (n_jets >= (unsigned int)(p_event_selector->GetCutParameters("MinNPFJets")[0]));
	}
	
	bool MaxNPFJets(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		unsigned int n_jets = p_event_selector->GetNumberOfGoodObjects(ObjectIdentifiers::kPFJet);
		p_event_selector->SetReturnData("MaxNPFJets", n_jets);
		return (n_jets <= (unsigned int)(p_event_selector->GetCutParameters("MaxNPFJets")[0]));
	}

	bool MinNCaloJets(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		unsigned int n_jets = p_event_selector->GetNumberOfGoodObjects(ObjectIdentifiers::kCaloJet);
		p_event_selector->SetReturnData("MinNCaloJets", n_jets);
		return n_jets >= (unsigned int)(p_event_selector->GetCutParameters("MinNCaloJets")[0]);
	}
	
	bool MaxNCaloJets(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		unsigned int n_jets = p_event_selector->GetNumberOfGoodObjects(ObjectIdentifiers::kCaloJet);
		p_event_selector->SetReturnData("MaxNCaloJets", n_jets);
		return n_jets <= (unsigned int)(p_event_selector->GetCutParameters("MaxNCaloJets")[0]);
	}

	bool MinLeadingPFJetPt(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		bool pass = true;
		int leading_pt_index;
		if (p_data.pfjet(0).ptCor() > p_data.pfjet(1).ptCor()) {
			leading_pt_index = 0;
		} else {
			leading_pt_index = 1;
		}
		if (!p_event_selector->GetObjectPass(ObjectIdentifiers::kPFJet, leading_pt_index)) {
			pass = false;
			p_event_selector->SetReturnData("MinLeadingPFJetPt", 0.);
		} else {
			pass = p_data.pfjet(leading_pt_index).ptCor() > p_event_selector->GetCutParameters("MinLeadingPFJetPt")[0];
			p_event_selector->SetReturnData("MinLeadingPFJetPt", p_data.pfjet(leading_pt_index).ptCor());
		}
		return pass;
	}

	bool MinSubleadingPFJetPt(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		bool pass = true;
		int subleading_pt_index;
		if (p_data.pfjet(0).ptCor() <= p_data.pfjet(1).ptCor()) {
			subleading_pt_index = 0;
		} else {
			subleading_pt_index = 1;
		}

		if (!p_event_selector->GetObjectPass(ObjectIdentifiers::kPFJet, subleading_pt_index)) {
			pass = false;
			p_event_selector->SetReturnData("MinSubleadingPFJetPt", 0.);
		} else {
			pass = p_data.pfjet(subleading_pt_index).ptCor() > p_event_selector->GetCutParameters("MinSubleadingPFJetPt")[0];
			p_event_selector->SetReturnData("MinSubleadingPFJetPt", p_data.pfjet(subleading_pt_index).ptCor());
		}
		return pass;
	}

	bool MaxLeadingPFJetEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		bool pass = true;
		if (!p_event_selector->GetObjectPass(ObjectIdentifiers::kPFJet, 0)) {
			pass = false;
			p_event_selector->SetReturnData("MaxLeadingPFJetEta", -100.);
		} else {
			pass = TMath::Abs(p_data.pfjet(0).eta()) < p_event_selector->GetCutParameters("MaxLeadingPFJetEta")[0];
			p_event_selector->SetReturnData("MaxLeadingPFJetEta", p_data.pfjet(0).eta());
		}
		return pass;
	}

	bool MaxSubleadingPFJetEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		bool pass = true;
		if (!p_event_selector->GetObjectPass(ObjectIdentifiers::kPFJet, 1)) {
			pass = false;
			p_event_selector->SetReturnData("MaxSubleadingPFJetEta", -100.);
		} else {
			pass = TMath::Abs(p_data.pfjet(1).eta()) < p_event_selector->GetCutParameters("MaxSubleadingPFJetEta")[0];
			p_event_selector->SetReturnData("MaxSubleadingPFJetEta", p_data.pfjet(1).eta());
		}
		return pass;
	}

	bool MinLeadingCaloJetPt(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		bool pass = true;
		int leading_pt_index;
		if (p_data.calojet(0).ptCor() > p_data.calojet(1).ptCor()) {
			leading_pt_index = 0;
		} else {
			leading_pt_index = 1;
		}
		if (!p_event_selector->GetObjectPass(ObjectIdentifiers::kCaloJet, leading_pt_index)) {
			pass = false;
			p_event_selector->SetReturnData("MinLeadingCaloJetPt", 0.);
		} else {
			pass = p_data.calojet(leading_pt_index).ptCor() > p_event_selector->GetCutParameters("MinLeadingCaloJetPt")[0];
			p_event_selector->SetReturnData("MinLeadingCaloJetPt", p_data.calojet(leading_pt_index).ptCor());
		}
		return pass;
	}

	bool MinSubleadingCaloJetPt(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		bool pass = true;
		int subleading_pt_index;
		if (p_data.calojet(0).ptCor() <= p_data.calojet(1).ptCor()) {
			subleading_pt_index = 0;
		} else {
			subleading_pt_index = 1;
		}

		if (!p_event_selector->GetObjectPass(ObjectIdentifiers::kCaloJet, subleading_pt_index)) {
			pass = false;
			p_event_selector->SetReturnData("MinSubleadingCaloJetPt", 0.);
		} else {
			pass = p_data.calojet(subleading_pt_index).ptCor() > p_event_selector->GetCutParameters("MinSubleadingCaloJetPt")[0];
			p_event_selector->SetReturnData("MinSubleadingCaloJetPt", p_data.calojet(subleading_pt_index).ptCor());
		}
		return pass;
	}

	bool MaxLeadingCaloJetEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		bool pass = true;
		if (!p_event_selector->GetObjectPass(ObjectIdentifiers::kCaloJet, 0)) {
			pass = false;
			p_event_selector->SetReturnData("MaxLeadingCaloJetEta", -100.);
		} else {
			pass = TMath::Abs(p_data.calojet(0).eta()) < p_event_selector->GetCutParameters("MaxLeadingCaloJetEta")[0];
			p_event_selector->SetReturnData("MaxLeadingCaloJetEta", p_data.calojet(0).eta());
		}
		return pass;
	}

	bool MaxSubleadingCaloJetEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		bool pass = true;
		if (!p_event_selector->GetObjectPass(ObjectIdentifiers::kCaloJet, 1)) {
			pass = false;
			p_event_selector->SetReturnData("MaxSubleadingCaloJetEta", -100.);
		} else {
			pass = TMath::Abs(p_data.calojet(1).eta()) < p_event_selector->GetCutParameters("MaxSubleadingCaloJetEta")[0];
			p_event_selector->SetReturnData("MaxSubleadingCaloJetEta", p_data.calojet(1).eta());
		}
		return pass;
	}

	bool GoodPFDijet(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		return (p_event_selector->GetObjectPass(ObjectIdentifiers::kPFJet, 0) && p_event_selector->GetObjectPass(ObjectIdentifiers::kPFJet, 1));
	}

	bool MinPFMjj(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		p_event_selector->SetReturnData("MinPFMjj", p_data.pfmjj());
		return (p_data.pfmjj() > p_event_selector->GetCutParameters("MinPFMjj")[0]);
	}

	bool MaxPFMjj(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		p_event_selector->SetReturnData("MaxPFMjj", p_data.pfmjj());
		return (p_data.pfmjj() < p_event_selector->GetCutParameters("MaxPFMjj")[0]);
	}

	bool MinCaloMjj(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		p_event_selector->SetReturnData("MinCaloMjj", p_data.calomjj());
		return (p_data.calomjj() > p_event_selector->GetCutParameters("MinCaloMjj")[0]);
	}

	bool MaxCaloMjj(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		p_event_selector->SetReturnData("MaxCaloMjj", p_data.calomjj());
		return (p_data.calomjj() < p_event_selector->GetCutParameters("MaxCaloMjj")[0]);
	}

	bool PFDijetMinDeltaEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		bool pass = true;
		if (!(p_event_selector->GetObjectPass(ObjectIdentifiers::kPFJet, 0) && p_event_selector->GetObjectPass(ObjectIdentifiers::kPFJet, 1))) {
			pass = false;
			p_event_selector->SetReturnData("PFDijetMinDeltaEta", -100.);
		} else {
			p_event_selector->SetReturnData("PFDijetMinDeltaEta", p_data.pfjet(0).eta() - p_data.pfjet(1).eta());
			pass = TMath::Abs(p_data.pfjet(0).eta() - p_data.pfjet(1).eta()) > p_event_selector->GetCutParameters("PFDijetMinDeltaEta")[0];
		}
		p_event_selector->SetReturnData("PFMjj", p_data.pfmjj());
		return pass;
	}

	bool PFDijetMaxDeltaEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		bool pass = true;
		if (!(p_event_selector->GetObjectPass(ObjectIdentifiers::kPFJet, 0) && p_event_selector->GetObjectPass(ObjectIdentifiers::kPFJet, 1))) {
			pass = false;
			p_event_selector->SetReturnData("PFDijetMaxDeltaEta", -100.);
		} else {
			p_event_selector->SetReturnData("PFDijetMaxDeltaEta", p_data.pfjet(0).eta() - p_data.pfjet(1).eta());
			pass = TMath::Abs(p_data.pfjet(0).eta() - p_data.pfjet(1).eta()) < p_event_selector->GetCutParameters("PFDijetMaxDeltaEta")[0];
		}
		p_event_selector->SetReturnData("PFMjj", p_data.pfmjj());
		return pass;
	}

	bool CaloDijetMinDeltaEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		bool pass = true;
		if (!(p_event_selector->GetObjectPass(ObjectIdentifiers::kCaloJet, 0) && p_event_selector->GetObjectPass(ObjectIdentifiers::kCaloJet, 1))) {
			pass = false;
			p_event_selector->SetReturnData("CaloDijetMinDeltaEta", -100.);
		} else {
			p_event_selector->SetReturnData("CaloDijetMinDeltaEta", p_data.calojet(0).eta() - p_data.calojet(1).eta());
			pass = TMath::Abs(p_data.calojet(0).eta() - p_data.calojet(1).eta()) > p_event_selector->GetCutParameters("CaloDijetMinDeltaEta")[0];
		}
		return pass;
	}

	bool CaloDijetMaxDeltaEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		bool pass = true;
		if (!(p_event_selector->GetObjectPass(ObjectIdentifiers::kCaloJet, 0) && p_event_selector->GetObjectPass(ObjectIdentifiers::kCaloJet, 1))) {
			pass = false;
			p_event_selector->SetReturnData("CaloDijetMaxDeltaEta", -100.);
		} else {
			p_event_selector->SetReturnData("CaloDijetMaxDeltaEta", p_data.calojet(0).eta() - p_data.calojet(1).eta());
			pass = TMath::Abs(p_data.calojet(0).eta() - p_data.calojet(1).eta()) < p_event_selector->GetCutParameters("CaloDijetMaxDeltaEta")[0];
		}
		return pass;
	}

	bool LeadingBTagPF(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		if (!p_event_selector->GetObjectPass(ObjectIdentifiers::kPFJet, 0)) {
			p_event_selector->SetReturnData("LeadingBTagPF", -100.);
			return false;
		}
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
		p_event_selector->SetReturnData("LeadingBTagPF", btag);
		return btag > p_event_selector->GetCutParameters("LeadingBTagPF")[0];
	}

	bool LeadingBTagCalo(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		if (!p_event_selector->GetObjectPass(ObjectIdentifiers::kCaloJet, 0)) {
			p_event_selector->SetReturnData("LeadingBTagCalo", -100.);
			return false;
		}
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
		p_event_selector->SetReturnData("LeadingBTagCalo", btag);
		return btag > p_event_selector->GetCutParameters("LeadingBTagCalo")[0];
	}

	bool SubleadingBTagPF(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		if (!p_event_selector->GetObjectPass(ObjectIdentifiers::kPFJet, 1)) {
			p_event_selector->SetReturnData("SubleadingBTagPF", -100.);
			return false;
		}
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
		p_event_selector->SetReturnData("SubleadingBTagPF", btag);
		return btag > p_event_selector->GetCutParameters("SubleadingBTagPF")[0];
	}

	bool SubleadingBTagCalo(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		if (!p_event_selector->GetObjectPass(ObjectIdentifiers::kCaloJet, 1)) {
			p_event_selector->SetReturnData("SubleadingBTagCalo", -100.);
			return false;
		}
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
		p_event_selector->SetReturnData("SubleadingBTagCalo", btag);
		return btag > p_event_selector->GetCutParameters("SubleadingBTagCalo")[0];
	}

	bool LeadingBVetoPF(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		if (!p_event_selector->GetObjectPass(ObjectIdentifiers::kPFJet, 0)) {
			p_event_selector->SetReturnData("LeadingBVetoPF", -100.);
			return false;
		}
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
		p_event_selector->SetReturnData("LeadingBVetoPF", btag);
		return btag < p_event_selector->GetCutParameters("LeadingBVetoPF")[0];
	}

	bool LeadingBVetoCalo(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		if (!p_event_selector->GetObjectPass(ObjectIdentifiers::kCaloJet, 0)) {
			p_event_selector->SetReturnData("LeadingBVetoCalo", -100.);
			return false;
		}
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
		p_event_selector->SetReturnData("LeadingBVetoCalo", btag);
		return btag < p_event_selector->GetCutParameters("LeadingBVetoCalo")[0];
	}

	bool SubleadingBVetoPF(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		if (!p_event_selector->GetObjectPass(ObjectIdentifiers::kPFJet, 1)) {
			p_event_selector->SetReturnData("SubleadingBVetoPF", -100.);
			return false;
		}
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
		p_event_selector->SetReturnData("SubleadingBVetoPF", btag);
		return btag < p_event_selector->GetCutParameters("SubleadingBVetoPF")[0];
	}

	bool SubleadingBVetoCalo(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		if (!p_event_selector->GetObjectPass(ObjectIdentifiers::kCaloJet, 1)) {
			p_event_selector->SetReturnData("SubleadingBVetoCalo", -100.);
			return false;
		}
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
		p_event_selector->SetReturnData("SubleadingBVetoCalo", btag);
		return btag < p_event_selector->GetCutParameters("SubleadingBVetoCalo")[0];
	}
	bool IsGoodPV(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		return p_data.evtHdr().isPVgood();
	}

	bool MaxMetOverSumEt(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		p_event_selector->SetReturnData("MaxMetOverSumEt", p_data.pfmet().met_o_sumet());
		return (p_data.pfmet().met_o_sumet() < p_event_selector->GetCutParameters("MaxMetOverSumEt")[0]);
	}

	// Fat jet cuts
	bool MinLeadingPFFatJetPt(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		int leading_pt_index;
		if (p_data.fatjet(0).pt() > p_data.fatjet(1).pt()) {
			leading_pt_index = 0;
		} else {
			leading_pt_index = 1;
		}

		p_event_selector->SetReturnData("MinLeadingPFFatJetPt", p_data.fatjet(leading_pt_index).pt());
		return (p_data.fatjet(leading_pt_index).pt() > p_event_selector->GetCutParameters("MinLeadingPFFatJetPt")[0]);
	}
	bool MinSubleadingPFFatJetPt(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		int subleading_pt_index;
		if (p_data.fatjet(0).pt() <= p_data.fatjet(1).pt()) {
			subleading_pt_index = 0;
		} else {
			subleading_pt_index = 1;
		}
		p_event_selector->SetReturnData("MinSubleadingPFFatJetPt", p_data.fatjet(subleading_pt_index).pt());
		return (p_data.fatjet(subleading_pt_index).pt() > p_event_selector->GetCutParameters("MinSubleadingPFFatJetPt")[0]);
	}
	bool MaxLeadingPFFatJetEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		p_event_selector->SetReturnData("MaxLeadingPFFatJetEta", p_data.fatjet(0).eta());
		return (TMath::Abs(p_data.fatjet(0).eta()) < p_event_selector->GetCutParameters("MaxLeadingPFFatJetEta")[0]);
	}
	bool MaxSubleadingPFFatJetEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		p_event_selector->SetReturnData("MaxSubleadingPFFatJetEta", p_data.fatjet(1).eta());
		return (TMath::Abs(p_data.fatjet(1).eta()) < p_event_selector->GetCutParameters("MaxSubleadingPFFatJetEta")[0]);
	}
	bool PFFatDijetMinDeltaEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		if (p_data.nFatJets() <= 1) {
			p_event_selector->SetReturnData("PFFatDijetMinDeltaEta", -100.);
			return false;
		}
		double delta_eta = p_data.fatjet(0).eta() - p_data.fatjet(1).eta();
		p_event_selector->SetReturnData("PFFatDijetMinDeltaEta", delta_eta);
		return (TMath::Abs(delta_eta) > p_event_selector->GetCutParameters("PFFatDijetMinDeltaEta")[0]);
	}
	bool PFFatDijetMaxDeltaEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		if (p_data.nFatJets() <= 1) {
			p_event_selector->SetReturnData("PFFatDijetMaxDeltaEta", -100.);
			return false;
		}
		double delta_eta = p_data.fatjet(0).eta() - p_data.fatjet(1).eta();
		p_event_selector->SetReturnData("PFFatDijetMaxDeltaEta", delta_eta);
		return (TMath::Abs(delta_eta) < p_event_selector->GetCutParameters("PFFatDijetMaxDeltaEta")[0]);
	}
	bool MinPFFatMjj(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		if (p_data.nFatJets() <= 1) {
			p_event_selector->SetReturnData("MinPFFatMjj", 0.);
			return false;
		}
		double mjj = (p_data.fatjet(0).p4() + p_data.fatjet(1).p4()).mass();
		p_event_selector->SetReturnData("MinPFFatMjj", mjj);
		return (mjj > p_event_selector->GetCutParameters("MinPFFatMjj")[0]);
	}
	bool MaxPFFatMjj(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		if (p_data.nFatJets() <= 1) {
			p_event_selector->SetReturnData("MaxPFFatMjj", 0.);
			return false;
		}
		double mjj = (p_data.fatjet(0).p4() + p_data.fatjet(1).p4()).mass();
		p_event_selector->SetReturnData("MaxPFFatMjj", mjj);
		return (mjj < p_event_selector->GetCutParameters("MaxPFFatMjj")[0]);
	}
	bool LeadingBTagPFFat(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		if (p_data.nFatJets() == 0) {
			p_event_selector->SetReturnData("LeadingBTagPFFat", -100.);
			return false;
		}
		float btag = 0.;
		if (p_event_selector->GetCutDescriptors("LeadingBTagPFFat")[0].EqualTo("tche")) {
			btag = p_data.fatjet(0).btag_tche();
		} else if (p_event_selector->GetCutDescriptors("LeadingBTagPFFat")[0].EqualTo("tchp")) {
			btag = p_data.fatjet(0).btag_tchp();
		} else if (p_event_selector->GetCutDescriptors("LeadingBTagPFFat")[0].EqualTo("csv")) {
			btag = p_data.fatjet(0).btag_csv();
		} else if (p_event_selector->GetCutDescriptors("LeadingBTagPFFat")[0].EqualTo("ssvhe")) {
			btag = p_data.fatjet(0).btag_ssvhe();
		} else if (p_event_selector->GetCutDescriptors("LeadingBTagPFFat")[0].EqualTo("ssvhp")) {
			btag = p_data.fatjet(0).btag_ssvhp();
		} else if (p_event_selector->GetCutDescriptors("LeadingBTagPFFat")[0].EqualTo("jp")) {
			btag = p_data.fatjet(0).btag_jp();
		} else {
			std::cerr << "[QCDEventCutFunctions::LeadingBTagPFFat] ERROR : Unknown b-tag type: " << p_event_selector->GetCutDescriptors("LeadingBTagPFFat")[0] << std::endl;
			exit(1);
		} 
		p_event_selector->SetReturnData("LeadingBTagPFFat", btag);
		return btag > p_event_selector->GetCutParameters("LeadingBTagPFFat")[0];
	}
	bool SubleadingBTagPFFat(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		if (p_data.nFatJets() <= 1) {
			p_event_selector->SetReturnData("SubleadingBTagPFFat", -100.);
			return false;
		}
		float btag = 0.;
		if (p_event_selector->GetCutDescriptors("SubleadingBTagPFFat")[0].EqualTo("tche")) {
			btag = p_data.fatjet(1).btag_tche();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBTagPFFat")[0].EqualTo("tchp")) {
			btag = p_data.fatjet(1).btag_tchp();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBTagPFFat")[0].EqualTo("csv")) {
			btag = p_data.fatjet(1).btag_csv();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBTagPFFat")[0].EqualTo("ssvhe")) {
			btag = p_data.fatjet(1).btag_ssvhe();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBTagPFFat")[0].EqualTo("ssvhp")) {
			btag = p_data.fatjet(1).btag_ssvhp();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBTagPFFat")[0].EqualTo("jp")) {
			btag = p_data.fatjet(1).btag_jp();
		} else {
			std::cerr << "[QCDEventCutFunctions::SubleadingBTagPFFat] ERROR : Unknown b-tag type: " << p_event_selector->GetCutDescriptors("SubleadingBTagPFFat")[0] << std::endl;
			exit(1);
		} 
		p_event_selector->SetReturnData("SubleadingBTagPFFat", btag);
		return btag > p_event_selector->GetCutParameters("SubleadingBTagPFFat")[0];
	}
	bool LeadingBVetoPFFat(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		if (p_data.nFatJets() == 0) {
			p_event_selector->SetReturnData("LeadingBVetoPFFat", -100.);
			return false;
		}
		float btag = 0.;
		if (p_event_selector->GetCutDescriptors("LeadingBVetoPFFat")[0].EqualTo("tche")) {
			btag = p_data.fatjet(0).btag_tche();
		} else if (p_event_selector->GetCutDescriptors("LeadingBVetoPFFat")[0].EqualTo("tchp")) {
			btag = p_data.fatjet(0).btag_tchp();
		} else if (p_event_selector->GetCutDescriptors("LeadingBVetoPFFat")[0].EqualTo("csv")) {
			btag = p_data.fatjet(0).btag_csv();
		} else if (p_event_selector->GetCutDescriptors("LeadingBVetoPFFat")[0].EqualTo("ssvhe")) {
			btag = p_data.fatjet(0).btag_ssvhe();
		} else if (p_event_selector->GetCutDescriptors("LeadingBVetoPFFat")[0].EqualTo("ssvhp")) {
			btag = p_data.fatjet(0).btag_ssvhp();
		} else if (p_event_selector->GetCutDescriptors("LeadingBVetoPFFat")[0].EqualTo("jp")) {
			btag = p_data.fatjet(0).btag_jp();
		} else {
			std::cerr << "[QCDEventCutFunctions::LeadingBVetoPFFat] ERROR : Unknown b-tag type: " << p_event_selector->GetCutDescriptors("LeadingBVetoPFFat")[0] << std::endl;
			exit(1);
		} 
		p_event_selector->SetReturnData("LeadingBVetoPFFat", btag);
		return btag < p_event_selector->GetCutParameters("LeadingBVetoPFFat")[0];
	}
	bool SubleadingBVetoPFFat(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		if (p_data.nFatJets() <= 1) {
			p_event_selector->SetReturnData("SubleadingBTagPFFat", -100.);
			return false;
		}
		float btag = 0.;
		if (p_event_selector->GetCutDescriptors("SubleadingBTagPFFat")[0].EqualTo("tche")) {
			btag = p_data.fatjet(1).btag_tche();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBTagPFFat")[0].EqualTo("tchp")) {
			btag = p_data.fatjet(1).btag_tchp();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBTagPFFat")[0].EqualTo("csv")) {
			btag = p_data.fatjet(1).btag_csv();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBTagPFFat")[0].EqualTo("ssvhe")) {
			btag = p_data.fatjet(1).btag_ssvhe();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBTagPFFat")[0].EqualTo("ssvhp")) {
			btag = p_data.fatjet(1).btag_ssvhp();
		} else if (p_event_selector->GetCutDescriptors("SubleadingBTagPFFat")[0].EqualTo("jp")) {
			btag = p_data.fatjet(1).btag_jp();
		} else {
			std::cerr << "[QCDEventCutFunctions::SubleadingBTagPFFat] ERROR : Unknown b-tag type: " << p_event_selector->GetCutDescriptors("SubleadingBTagPFFat")[0] << std::endl;
			exit(1);
		} 
		p_event_selector->SetReturnData("SubleadingBTagPFFat", btag);
		return btag < p_event_selector->GetCutParameters("SubleadingBTagPFFat")[0];
	}

	bool MinNCSVL(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		int n_csvl = 0;
		for (int i_jet = 0; i_jet <= 1; ++i_jet) {
			if (p_data.pfjet(i_jet).btag_csv() > 0.244) {
				++n_csvl;
			}
		}
		p_event_selector->SetReturnData("MinNCSVL", n_csvl);
		return n_csvl >= p_event_selector->GetCutParameters("MinNCSVL")[0];
	}
	bool MinNCSVM(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		int n_csvm = 0;
		for (int i_jet = 0; i_jet <= 1; ++i_jet) {
			if (p_data.pfjet(i_jet).btag_csv() > 0.679) {
				++n_csvm;
			}
		}
		p_event_selector->SetReturnData("MinNCSVM", n_csvm);
		return n_csvm >= p_event_selector->GetCutParameters("MinNCSVM")[0];
	}
	bool MinNCSVT(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector) {
		int n_csvt = 0;
		for (int i_jet = 0; i_jet <= 1; ++i_jet) {
			if (p_data.pfjet(i_jet).btag_csv() > 0.898) {
				++n_csvt;
			}
		}
		p_event_selector->SetReturnData("MinNCSVT", n_csvt);
		return n_csvt >= p_event_selector->GetCutParameters("MinNCSVT")[0];
	}


	void Configure(EventSelector<QCDEvent>* p_event_selector) {
		p_event_selector->AddCutFunction("Trigger", &Trigger);
		p_event_selector->AddCutFunction("TriggerOR", &TriggerOR);
		p_event_selector->AddCutFunction("TriggerXOR", &TriggerXOR);
		p_event_selector->AddCutFunction("IsGoodPV", &IsGoodPV);
		p_event_selector->AddCutFunction("MaxMetOverSumEt", &MaxMetOverSumEt);
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
		p_event_selector->AddCutFunction("PFDijetMinDeltaEta", &PFDijetMinDeltaEta);
		p_event_selector->AddCutFunction("PFDijetMaxDeltaEta", &PFDijetMaxDeltaEta);
		p_event_selector->AddCutFunction("GoodPFDijet", &GoodPFDijet);
		p_event_selector->AddCutFunction("MinPFMjj", &MinPFMjj);
		p_event_selector->AddCutFunction("MaxPFMjj", &MaxPFMjj);
		p_event_selector->AddCutFunction("MinCaloMjj", &MinCaloMjj);
		p_event_selector->AddCutFunction("MaxCaloMjj", &MaxCaloMjj);
		p_event_selector->AddCutFunction("CaloDijetMinDeltaEta", &CaloDijetMinDeltaEta);
		p_event_selector->AddCutFunction("CaloDijetMaxDeltaEta", &CaloDijetMaxDeltaEta);
		p_event_selector->AddCutFunction("LeadingBTagPF", &LeadingBTagPF);
		p_event_selector->AddCutFunction("LeadingBTagCalo", &LeadingBTagCalo);
		p_event_selector->AddCutFunction("SubleadingBTagPF", &SubleadingBTagPF);
		p_event_selector->AddCutFunction("SubleadingBTagCalo", &SubleadingBTagCalo);
		p_event_selector->AddCutFunction("LeadingBVetoPF", &LeadingBVetoPF);
		p_event_selector->AddCutFunction("LeadingBVetoCalo", &LeadingBVetoCalo);
		p_event_selector->AddCutFunction("SubleadingBVetoPF", &SubleadingBVetoPF);
		p_event_selector->AddCutFunction("SubleadingBVetoCalo", &SubleadingBVetoCalo);

		p_event_selector->AddCutFunction("MinLeadingPFFatJetPt", &MinLeadingPFFatJetPt);
		p_event_selector->AddCutFunction("MinSubleadingPFFatJetPt", &MinSubleadingPFFatJetPt);
		p_event_selector->AddCutFunction("MaxLeadingPFFatJetEta", &MaxLeadingPFFatJetEta);
		p_event_selector->AddCutFunction("MaxSubleadingPFFatJetEta", &MaxSubleadingPFFatJetEta);
		p_event_selector->AddCutFunction("PFFatDijetMinDeltaEta", &PFFatDijetMinDeltaEta);
		p_event_selector->AddCutFunction("PFFatDijetMaxDeltaEta", &PFFatDijetMaxDeltaEta);
		p_event_selector->AddCutFunction("MinPFFatMjj", &MinPFFatMjj);
		p_event_selector->AddCutFunction("MaxPFFatMjj", &MaxPFFatMjj);
		p_event_selector->AddCutFunction("LeadingBTagPFFat", &LeadingBTagPFFat);
		p_event_selector->AddCutFunction("SubleadingBTagPFFat", &SubleadingBTagPFFat);
		p_event_selector->AddCutFunction("LeadingBVetoPFFat", &LeadingBVetoPFFat);
		p_event_selector->AddCutFunction("SubleadingBVetoPFFat", &SubleadingBVetoPFFat);
		p_event_selector->AddCutFunction("MinNCSVT", &MinNCSVT);
		p_event_selector->AddCutFunction("MinNCSVM", &MinNCSVM);
		p_event_selector->AddCutFunction("MinNCSVL", &MinNCSVL);

		// N-1 histograms
		p_event_selector->AddNMinusOneHistogram("MaxMetOverSumEt", "E_{T}^{miss} / #SigmaE_{T}", 40, 0., 2.);
		p_event_selector->AddNMinusOneHistogram("MinNPFJets", "N_{jets}", 21, -0.5, 20.5);
		p_event_selector->AddNMinusOneHistogram("MaxNPFJets", "N_{jets}", 21, -0.5, 20.5);
		p_event_selector->AddNMinusOneHistogram("MinNCaloJets", "N_{jets}", 21, -0.5, 20.5);
		p_event_selector->AddNMinusOneHistogram("MaxNCaloJets", "N_{jets}", 21, -0.5, 20.5);
		p_event_selector->AddNMinusOneHistogram("MinLeadingPFJetPt", "Jet p_{T} [GeV]", 1000, 0., 1000.);
		p_event_selector->AddNMinusOneHistogram("MinSubleadingPFJetPt", "Jet p_{T} [GeV]", 1000, 0., 1000.);
		p_event_selector->AddNMinusOneHistogram("MaxLeadingPFJetEta", "Jet #eta", 100, -5., 5.);
		p_event_selector->AddNMinusOneHistogram("MaxSubleadingPFJetEta", "Jet #eta", 100, -5., 5.);
		p_event_selector->AddNMinusOneHistogram("MinLeadingCaloJetPt", "Jet p_{T} [GeV]", 1000, 0., 1000.);
		p_event_selector->AddNMinusOneHistogram("MinSubleadingCaloJetPt", "Jet p_{T} [GeV]", 1000, 0., 1000.);
		p_event_selector->AddNMinusOneHistogram("MaxLeadingCaloJetEta", "Jet #eta", 100, -5., 5.);
		p_event_selector->AddNMinusOneHistogram("MaxSubleadingCaloJetEta", "Jet #eta", 100, -5., 5.);
		p_event_selector->AddNMinusOneHistogram("PFDijetMinDeltaEta", "Dijet #Delta#eta", 100, -5., 5.);
		p_event_selector->AddNMinusOneHistogram("PFDijetMaxDeltaEta", "Dijet #Delta#eta", 100, -5., 5.);
		p_event_selector->AddNMinusOne2DHistogram("PFDijetMinDeltaEta", "PFMjj", "Dijet #Delta#eta", 100, -5., 5., "m_{jj}", 400, 0., 2000.);
		p_event_selector->AddNMinusOne2DHistogram("PFDijetMaxDeltaEta", "PFMjj", "Dijet #Delta#eta", 100, -5., 5., "m_{jj}", 400, 0., 2000.);
		p_event_selector->AddNMinusOneHistogram("MinPFMjj", "m_{jj} [GeV]", 2000, 0., 2000.);
		p_event_selector->AddNMinusOneHistogram("MaxPFMjj", "m_{jj} [GeV]", 2000, 0., 2000.);
		p_event_selector->AddNMinusOneHistogram("MinCaloMjj", "m_{jj} [GeV]", 2000, 0., 2000.);
		p_event_selector->AddNMinusOneHistogram("MaxCaloMjj", "m_{jj} [GeV]", 2000, 0., 2000.);
		p_event_selector->AddNMinusOneHistogram("CaloDijetMinDeltaEta", "Dijet #Delta#eta", 100, -5., 5.);
		p_event_selector->AddNMinusOneHistogram("CaloDijetMaxDeltaEta", "Dijet #Delta#eta", 100, -5., 5.);
		p_event_selector->AddNMinusOneHistogram("LeadingBTagPF", "Discriminant", 2000, -100., 100.);
		p_event_selector->AddNMinusOneHistogram("LeadingBTagCalo", "Discriminant", 2000, -100., 100.);
		p_event_selector->AddNMinusOneHistogram("SubleadingBTagPF", "Discriminant", 2000, -100., 100.);
		p_event_selector->AddNMinusOneHistogram("SubleadingBTagCalo", "Discriminant", 2000, -100., 100.);
		p_event_selector->AddNMinusOneHistogram("LeadingBVetoPF", "Discriminant", 2000, -100., 100.);
		p_event_selector->AddNMinusOneHistogram("LeadingBVetoCalo", "Discriminant", 2000, -100., 100.);
		p_event_selector->AddNMinusOneHistogram("SubleadingBVetoPF", "Discriminant", 2000, -100., 100.);
		p_event_selector->AddNMinusOneHistogram("SubleadingBVetoCalo", "Discriminant", 2000, -100., 100.);
		p_event_selector->AddNMinusOneHistogram("MinLeadingPFFatJetPt", "Jet p_{T} [GeV]", 1000, 0., 1000.);
		p_event_selector->AddNMinusOneHistogram("MinSubleadingPFFatJetPt", "Jet p_{T} [GeV]", 1000, 0., 1000.);
		p_event_selector->AddNMinusOneHistogram("MaxLeadingPFFatJetEta", "#eta", 100, -5., 5.);
		p_event_selector->AddNMinusOneHistogram("MaxSubleadingPFFatJetEta", "#eta", 100, -5., 5.);
		p_event_selector->AddNMinusOneHistogram("PFFatDijetMinDeltaEta", "Dijet #Delta#eta", 100, -5., 5.);
		p_event_selector->AddNMinusOneHistogram("PFFatDijetMaxDeltaEta", "Dijet #Delta#eta", 100, -5., 5.);
		p_event_selector->AddNMinusOneHistogram("MinPFFatMjj", "m_{jj} [GeV]", 2000, 0., 2000.);
		p_event_selector->AddNMinusOneHistogram("MaxPFFatMjj", "m_{jj} [GeV]", 2000, 0., 2000.);
		p_event_selector->AddNMinusOneHistogram("LeadingBTagPFFat", "Discriminant", 2000, -100., 100.);
		p_event_selector->AddNMinusOneHistogram("SubleadingBTagPFFat", "Discriminant", 2000, -100., 100.);
		p_event_selector->AddNMinusOneHistogram("LeadingBVetoPFFat", "Discriminant", 2000, -100., 100.);
		p_event_selector->AddNMinusOneHistogram("SubleadingBVetoPFFat", "Discriminant", 2000, -100., 100.);
		p_event_selector->AddNMinusOneHistogram("MinNCSVT", "NCSVT", 4, -0.5, 3.5);
		p_event_selector->AddNMinusOneHistogram("MinNCSVM", "NCSVM", 4, -0.5, 3.5);
		p_event_selector->AddNMinusOneHistogram("MinNCSVL", "NCSVL", 4, -0.5, 3.5);

		p_event_selector->SetName("QCDEventSelector");
		p_event_selector->SetObjectName("Event");
	}

}


#endif