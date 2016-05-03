#ifndef PFJetCutFunctions_h
#define PFJetCutFunctions_h

#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>
#include <algorithm>

#include "TROOT.h"
#include "TMath.h"
#include "TPython.h"

#include "MyTools/RootUtils/interface/Constants.h"
//#include "MyTools/AnalysisTools/interface/EventSelector.h"
#include "MyTools/AnalysisTools/interface/ObjectSelector.h"
#include "CMSDIJET/QCDAnalysis/interface/QCDEvent.h"
#include "CMSDIJET/QCDAnalysis/interface/QCDJet.h"
#include "CMSDIJET/QCDAnalysis/interface/QCDPFJet.h"

template class ObjectSelector<QCDPFJet>;

namespace PFJetCutFunctions {
	bool MinPt(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MaxPt(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MinAbsEta(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MaxAbsEta(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MinChargedHadronEnergyFraction(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MaxChargedHadronEnergyFraction(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MinNeutralHadronEnergyFraction(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MaxNeutralHadronEnergyFraction(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MinPhotonEnergyFraction(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MaxPhotonEnergyFraction(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MinElectronEnergyFraction(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MaxElectronEnergyFraction(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MinMuonEnergyFraction(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MaxMuonEnergyFraction(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MinHFHadronFraction(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MaxHFHadronFraction(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MinHFEMEnergyFraction(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MaxHFEMEnergyFraction(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MinHFHadronMultiplicity(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MaxHFHadronMultiplicity(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MinHFPhotonMultiplicity(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MaxHFPhotonMultiplicity(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MinChargedHadronMultiplicity(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MaxChargedHadronMultiplicity(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MinNeutralHadronMultiplicity(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MaxNeutralHadronMultiplicity(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MinConstituents(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MaxConstituents(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MinPhotonMultiplicity(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MaxPhotonMultiplicity(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MinElectronMultiplicity(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MaxElectronMultiplicity(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MinMuonMultiplicity(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MaxMuonMultiplicity(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MinPFCandidates(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MaxPFCandidates(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MinBeta(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MaxBeta(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MinBetaStar(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MaxBetaStar(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool IsLooseID(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool IsTightID(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MinBTagWeight(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);
	bool MaxBTagWeight(const std::vector<QCDPFJet>& p_data, ObjectSelector<QCDPFJet>* p_object_selector, const int n);

	void Configure(ObjectSelector<QCDPFJet>* p_selector);
}

#endif
