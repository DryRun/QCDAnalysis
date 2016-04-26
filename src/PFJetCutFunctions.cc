#ifndef PFJetCutFunctions_cxx
#define PFJetCutFunctions_cxx

#include "CMSDIJET/QCDAnalysis/interface/PFJetCutFunctions.h"

namespace PFJetCutFunctions {
	bool MinPt(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].pt() >= p_object_selector->GetCutParameters("MinPt")[0];
	}
	bool MaxPt(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].pt() <= p_object_selector->GetCutParameters("MaxPt")[0];
	}
	bool MinAbsEta(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return TMath::Abs(p_data[n].eta()) >= p_object_selector->GetCutParameters("MinAbsEta")[0];
	}
	bool MaxAbsEta(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return TMath::Abs(p_data[n].eta()) <= p_object_selector->GetCutParameters("MaxAbsEta")[0];
	}
	bool MinChargedHadronEnergyFraction(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return ((p_data[n].chargedHadronEnergyFraction() >= p_object_selector->GetCutParameters("MinChargedHadronEnergyFraction")[0]) || TMath::Abs(p_data[n].eta()) > 2.4);
	}
	bool MaxChargedHadronEnergyFraction(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return ((p_data[n].chargedHadronEnergyFraction() <= p_object_selector->GetCutParameters("MaxChargedHadronEnergyFraction")[0]) || TMath::Abs(p_data[n].eta()) > 2.4);
	}
	bool MinNeutralHadronEnergyFraction(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].neutralHadronEnergyFraction() >= p_object_selector->GetCutParameters("MinNeutralHadronEnergyFraction")[0];
	}
	bool MaxNeutralHadronEnergyFraction(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].neutralHadronEnergyFraction() <= p_object_selector->GetCutParameters("MaxNeutralHadronEnergyFraction")[0];
	}
	bool MinPhotonEnergyFraction(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].photonEnergyFraction() >= p_object_selector->GetCutParameters("MinPhotonEnergyFraction")[0];
	}
	bool MaxPhotonEnergyFraction(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].photonEnergyFraction() <= p_object_selector->GetCutParameters("MaxPhotonEnergyFraction")[0];
	}
	bool MinElectronEnergyFraction(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].electronEnergyFraction() >= p_object_selector->GetCutParameters("MinElectronEnergyFraction")[0];
	}
	bool MaxElectronEnergyFraction(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].electronEnergyFraction() <= p_object_selector->GetCutParameters("MaxElectronEnergyFraction")[0];
	}
	bool MinMuonEnergyFraction(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].muonEnergyFraction() >= p_object_selector->GetCutParameters("MinMuonEnergyFraction")[0];
	}
	bool MaxMuonEnergyFraction(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].muonEnergyFraction() <= p_object_selector->GetCutParameters("MaxMuonEnergyFraction")[0];
	}
	bool MinHFHadronFraction(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].HFHadronEnergyFraction() >= p_object_selector->GetCutParameters("MinHFHadronFraction")[0];
	}
	bool MaxHFHadronFraction(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].HFHadronEnergyFraction() <= p_object_selector->GetCutParameters("MaxHFHadronFraction")[0];
	}
	bool MinHFEMEnergyFraction(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].HFEMEnergyFraction() >= p_object_selector->GetCutParameters("MinHFEMEnergyFraction")[0];
	}
	bool MaxHFEMEnergyFraction(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].HFEMEnergyFraction() <= p_object_selector->GetCutParameters("MaxHFEMEnergyFraction")[0];
	}
	bool MinHFHadronMultiplicity(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].HFHadronMultiplicity() >= p_object_selector->GetCutParameters("MinHFHadronMultiplicity")[0];
	}
	bool MaxHFHadronMultiplicity(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].HFHadronMultiplicity() <= p_object_selector->GetCutParameters("MaxHFHadronMultiplicity")[0];
	}
	bool MinHFEMMultiplicity(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].HFEMMultiplicity() >= p_object_selector->GetCutParameters("MinHFEMMultiplicity")[0];
	}
	bool MaxHFEMMultiplicity(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].HFEMMultiplicity() <= p_object_selector->GetCutParameters("MaxHFEMMultiplicity")[0];
	}
	bool MinChargedHadronMultiplicity(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return ((p_data[n].chargedHadronMultiplicity() >= p_object_selector->GetCutParameters("MinChargedHadronMultiplicity")[0]) || (TMath::Abs(p_data[n].eta()) > 2.4));
	}
	bool MaxChargedHadronMultiplicity(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return ((p_data[n].chargedHadronMultiplicity() <= p_object_selector->GetCutParameters("MaxChargedHadronMultiplicity")[0]) || (TMath::Abs(p_data[n].eta()) > 2.4));
	}
	bool MinNeutralHadronMultiplicity(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].neutralHadronMultiplicity() >= p_object_selector->GetCutParameters("MinNeutralHadronMultiplicity")[0];
	}
	bool MaxNeutralHadronMultiplicity(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].neutralHadronMultiplicity() <= p_object_selector->GetCutParameters("MaxNeutralHadronMultiplicity")[0];
	}
	bool MinConstituents(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].chargedHadronMultiplicity() + p_data[n].neutralHadronMultiplicity() >= p_object_selector->GetCutParameters("MinConstituents")[0];
	}
	bool MaxConstituents(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].chargedHadronMultiplicity() + p_data[n].neutralHadronMultiplicity() <= p_object_selector->GetCutParameters("MaxConstituents")[0];
	}
	bool MinPhotonMultiplicity(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].photonMultiplicity() >= p_object_selector->GetCutParameters("MinPhotonMultiplicity")[0];
	}
	bool MaxPhotonMultiplicity(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].photonMultiplicity() <= p_object_selector->GetCutParameters("MaxPhotonMultiplicity")[0];
	}
	bool MinElectronMultiplicity(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].electronMultiplicity() >= p_object_selector->GetCutParameters("MinElectronMultiplicity")[0];
	}
	bool MaxElectronMultiplicity(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].electronMultiplicity() <= p_object_selector->GetCutParameters("MaxElectronMultiplicity")[0];
	}
	bool MinMuonMultiplicity(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].muonMultiplicity() >= p_object_selector->GetCutParameters("MinMuonMultiplicity")[0];
	}
	bool MaxMuonMultiplicity(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].muonMultiplicity() <= p_object_selector->GetCutParameters("MaxMuonMultiplicity")[0];
	}
	bool MinPFCandidates(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].nPFCandidates() >= p_object_selector->GetCutParameters("MinPFCandidates")[0];
	}
	bool MaxPFCandidates(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].nPFCandidates() <= p_object_selector->GetCutParameters("MaxPFCandidates")[0];
	}
	bool MinBeta(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].beta() >= p_object_selector->GetCutParameters("MinBeta")[0];
	}
	bool MaxBeta(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].beta() <= p_object_selector->GetCutParameters("MaxBeta")[0];
	}
	bool MinBetaStar(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].betaStar() >= p_object_selector->GetCutParameters("MinBetaStar")[0];
	}
	bool MaxBetaStar(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].betaStar() <= p_object_selector->GetCutParameters("MaxBetaStar")[0];
	}
	bool IsLooseID(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].isLooseID();
	}
	bool IsTightID(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n) {
		return p_data[n].isTightID();
	}


	void Configure(ObjectSelector<QCDPFJet>* p_selector) {
		p_selector->AddCutFunction("MinPt", &MinPt);
		p_selector->AddCutFunction("MaxPt", &MaxPt);
		p_selector->AddCutFunction("MinAbsEta", &MinAbsEta);
		p_selector->AddCutFunction("MaxAbsEta", &MaxAbsEta);
		p_selector->AddCutFunction("MinChargedHadronEnergyFraction", &MinChargedHadronEnergyFraction);
		p_selector->AddCutFunction("MaxChargedHadronEnergyFraction", &MaxChargedHadronEnergyFraction);
		p_selector->AddCutFunction("MinNeutralHadronEnergyFraction", &MinNeutralHadronEnergyFraction);
		p_selector->AddCutFunction("MaxNeutralHadronEnergyFraction", &MaxNeutralHadronEnergyFraction);
		p_selector->AddCutFunction("MinPhotonEnergyFraction", &MinPhotonEnergyFraction);
		p_selector->AddCutFunction("MaxPhotonEnergyFraction", &MaxPhotonEnergyFraction);
		p_selector->AddCutFunction("MinElectronEnergyFraction", &MinElectronEnergyFraction);
		p_selector->AddCutFunction("MaxElectronEnergyFraction", &MaxElectronEnergyFraction);
		p_selector->AddCutFunction("MinMuonEnergyFraction", &MinMuonEnergyFraction);
		p_selector->AddCutFunction("MaxMuonEnergyFraction", &MaxMuonEnergyFraction);
		p_selector->AddCutFunction("MinHFHadronFraction", &MinHFHadronFraction);
		p_selector->AddCutFunction("MaxHFHadronFraction", &MaxHFHadronFraction);
		p_selector->AddCutFunction("MinHFEMEnergyFraction", &MinHFEMEnergyFraction);
		p_selector->AddCutFunction("MaxHFEMEnergyFraction", &MaxHFEMEnergyFraction);
		p_selector->AddCutFunction("MinHFHadronMultiplicity", &MinHFHadronMultiplicity);
		p_selector->AddCutFunction("MaxHFHadronMultiplicity", &MaxHFHadronMultiplicity);
		p_selector->AddCutFunction("MinHFEMMultiplicity", &MinHFEMMultiplicity);
		p_selector->AddCutFunction("MaxHFEMMultiplicity", &MaxHFEMMultiplicity);
		p_selector->AddCutFunction("MinChargedHadronMultiplicity", &MinChargedHadronMultiplicity);
		p_selector->AddCutFunction("MaxChargedHadronMultiplicity", &MaxChargedHadronMultiplicity);
		p_selector->AddCutFunction("MinNeutralHadronMultiplicity", &MinNeutralHadronMultiplicity);
		p_selector->AddCutFunction("MaxNeutralHadronMultiplicity", &MaxNeutralHadronMultiplicity);
		p_selector->AddCutFunction("MinConstituents", &MinConstituents);
		p_selector->AddCutFunction("MaxConstituents", &MaxConstituents);
		p_selector->AddCutFunction("MinPhotonMultiplicity", &MinPhotonMultiplicity);
		p_selector->AddCutFunction("MaxPhotonMultiplicity", &MaxPhotonMultiplicity);
		p_selector->AddCutFunction("MinElectronMultiplicity", &MinElectronMultiplicity);
		p_selector->AddCutFunction("MaxElectronMultiplicity", &MaxElectronMultiplicity);
		p_selector->AddCutFunction("MinMuonMultiplicity", &MinMuonMultiplicity);
		p_selector->AddCutFunction("MaxMuonMultiplicity", &MaxMuonMultiplicity);
		p_selector->AddCutFunction("MinPFCandidates", &MinPFCandidates);
		p_selector->AddCutFunction("MaxPFCandidates", &MaxPFCandidates);
		p_selector->AddCutFunction("MinBeta", &MinBeta);
		p_selector->AddCutFunction("MaxBeta", &MaxBeta);
		p_selector->AddCutFunction("MinBetaStar", &MinBetaStar);
		p_selector->AddCutFunction("MaxBetaStar", &MaxBetaStar);
		p_selector->AddCutFunction("IsLooseID", &IsLooseID);
		p_selector->AddCutFunction("IsTightID", &IsTightID);
		
		p_selector->SetObjectName("PFJet");
		p_selector->SetObjectType(ObjectIdentifiers::kJet);
	}

}


#endif