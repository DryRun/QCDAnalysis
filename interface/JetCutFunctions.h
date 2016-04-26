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

template class ObjectSelector<QCDJet>;

namespace JetCutFunctions {
	bool MinPt(const std::vector<QCDJet>& p_data, ObjectSelector<QCDJet>* p_object_selector, const int n);
	bool MaxPt(const std::vector<QCDJet>& p_data, ObjectSelector<QCDJet>* p_object_selector, const int n);
	bool MinAbsEta(const std::vector<QCDJet>& p_data, ObjectSelector<QCDJet>* p_object_selector, const int n);
	bool MaxAbsEta(const std::vector<QCDJet>& p_data, ObjectSelector<QCDJet>* p_object_selector, const int n);

	void Configure(ObjectSelector<QCDJet>* p_selector);
}

#endif
