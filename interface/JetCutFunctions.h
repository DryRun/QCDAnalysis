#ifndef JetCutFunctions_h
#define JetCutFunctions_h

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
#include "CMSDIJET/QCDAnalysis/interface/QCDCaloJet.h"

template class ObjectSelector<QCDJet>;

namespace JetCutFunctions {
	bool MinPt(const std::vector<QCDJet>& p_data, ObjectSelector<QCDJet>* p_object_selector, const int n);
	bool MaxPt(const std::vector<QCDJet>& p_data, ObjectSelector<QCDJet>* p_object_selector, const int n);
	bool MinAbsEta(const std::vector<QCDJet>& p_data, ObjectSelector<QCDJet>* p_object_selector, const int n);
	bool MaxAbsEta(const std::vector<QCDJet>& p_data, ObjectSelector<QCDJet>* p_object_selector, const int n);
//	MinChargedHadronEnergyFraction
//	MaxChargedHadronEnergyFraction
//	MinNeutralHadronEnergyFraction
//	MaxNeutralHadronEnergyFraction
//	MinPhotonEnergyFraction
//	MaxPhotonEnergyFraction
//	MinElectronEnergyFraction
//	MaxElectronEnergyFraction
//	MinMuonEnergyFraction
//	MaxMuonEnergyFraction
//	MinHFHadronFraction
//	MaxHFHadronFraction
//	MinHFPhotonFraction
//	MaxHFPhotonFraction
//	MinHFHadronMultiplicity
//	MaxHFHadronMultiplicity
//	MinHFPhotonMultiplicity
//	MaxHFPhotonMultiplicity
//	MinChargedHadronMultiplicity
//	MaxChargedHadronMultiplicity
//	MinNeutralHadronMultiplicity
//	MaxNeutralHadronMultiplicity
//	MinPhotonMultiplicity
//	MaxPhotonMultiplicity
//	MinElectronMultiplicity
//	MaxElectronMultiplicity
//	MinMuonMultiplicity
//	MaxMuonMultiplicity
//	MinPFCandidates
//	MaxPFCandidates
//fraction of track pt coming from the signal vertex ---
//fraction of track pt NOT coming from the signal vertex ---LooseID
	void Configure(ObjectSelector<QCDJet>* p_selector);
}

#endif
