#ifndef CaloJetCutFunctions_cxx
#define CaloJetCutFunctions_cxx

#include "CMSDIJET/QCDAnalysis/interface/CaloJetCutFunctions.h"

namespace CaloJetCutFunctions {
	bool MinPt(const std::vector<QCDCaloJet>& p_data, ObjectSelector<QCDCaloJet>* p_object_selector, const int n) {
		return p_data[n].pt() >= p_object_selector->GetCutParameters("MinPt")[0];
	}
	bool MaxPt(const std::vector<QCDCaloJet>& p_data, ObjectSelector<QCDCaloJet>* p_object_selector, const int n) {
		return p_data[n].pt() <= p_object_selector->GetCutParameters("MaxPt")[0];
	}
	bool MinAbsEta(const std::vector<QCDCaloJet>& p_data, ObjectSelector<QCDCaloJet>* p_object_selector, const int n) {
		return TMath::Abs(p_data[n].eta()) >= p_object_selector->GetCutParameters("MinAbsEta")[0];
	}
	bool MaxAbsEta(const std::vector<QCDCaloJet>& p_data, ObjectSelector<QCDCaloJet>* p_object_selector, const int n) {
		return TMath::Abs(p_data[n].eta()) <= p_object_selector->GetCutParameters("MaxAbsEta")[0];
	}
	bool IsLooseIDFlag(const std::vector<QCDCaloJet>& p_data, ObjectSelector<QCDCaloJet>* p_object_selector, const int n) {
		return p_data[n].looseIDFlag();
	}
	bool IsTightIDFlag(const std::vector<QCDCaloJet>& p_data, ObjectSelector<QCDCaloJet>* p_object_selector, const int n) {
		return p_data[n].tightIDFlag();
	}


	void Configure(ObjectSelector<QCDCaloJet>* p_selector) {
		p_selector->AddCutFunction("MinPt", &MinPt);
		p_selector->AddCutFunction("MaxPt", &MaxPt);
		p_selector->AddCutFunction("MinAbsEta", &MinAbsEta);
		p_selector->AddCutFunction("MaxAbsEta", &MaxAbsEta);

		p_selector->SetObjectName("CaloJet");
		p_selector->SetObjectType(ObjectIdentifiers::kJet);
	}

}


#endif