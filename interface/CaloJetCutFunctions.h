#ifndef CaloJetCutFunctions_h
#define CaloJetCutFunctions_h

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
#include "CMSDIJET/QCDAnalysis/interface/QCDCaloJet.h"

template class ObjectSelector<QCDCaloJet>;

namespace CaloJetCutFunctions {
	bool MinPt(const std::vector<QCDCaloJet>& p_data, ObjectSelector<QCDCaloJet>* p_object_selector, const int n);
	bool MaxPt(const std::vector<QCDCaloJet>& p_data, ObjectSelector<QCDCaloJet>* p_object_selector, const int n);
	bool MinAbsEta(const std::vector<QCDCaloJet>& p_data, ObjectSelector<QCDCaloJet>* p_object_selector, const int n);
	bool MaxAbsEta(const std::vector<QCDCaloJet>& p_data, ObjectSelector<QCDCaloJet>* p_object_selector, const int n);
	bool IsLooseID(const std::vector<QCDCaloJet>& p_data, ObjectSelector<QCDCaloJet>* p_object_selector, const int n);
	bool IsTightID(const std::vector<QCDCaloJet>& p_data, ObjectSelector<QCDCaloJet>* p_object_selector, const int n);

	void Configure(ObjectSelector<QCDCaloJet>* p_selector);
}

#endif
