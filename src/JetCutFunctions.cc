#ifndef JetCutFunctions_cxx
#define JetCutFunctions_cxx

#include "CMSDIJET/QCDAnalysis/interface/JetCutFunctions.h"

namespace JetCutFunctions {
	bool MinPt(const std::vector<QCDJet>& p_data, ObjectSelector<QCDJet>* p_object_selector, const int n) {
		return p_data[n].pt() >= p_object_selector->GetCutParameters("MinPt")[0];
	}
	bool MaxPt(const std::vector<QCDJet>& p_data, ObjectSelector<QCDJet>* p_object_selector, const int n) {
		return p_data[n].pt() <= p_object_selector->GetCutParameters("MaxPt")[0];
	}
	bool MinAbsEta(const std::vector<QCDJet>& p_data, ObjectSelector<QCDJet>* p_object_selector, const int n) {
		return TMath::Abs(p_data[n].eta()) >= p_object_selector->GetCutParameters("MinAbsEta")[0];
	}
	bool MaxAbsEta(const std::vector<QCDJet>& p_data, ObjectSelector<QCDJet>* p_object_selector, const int n) {
		return TMath::Abs(p_data[n].eta()) <= p_object_selector->GetCutParameters("MaxAbsEta")[0];
	}


	void Configure(ObjectSelector<QCDJet>* p_selector) {
		p_selector->AddCutFunction("MinPt", &MinPt);
		p_selector->AddCutFunction("MaxPt", &MaxPt);
		p_selector->AddCutFunction("MinAbsEta", &MinAbsEta);
		p_selector->AddCutFunction("MaxAbsEta", &MaxAbsEta);

		p_selector->SetObjectName("Jet");
		p_selector->SetObjectType(ObjectIdentifiers::kJet);
	}

}


#endif