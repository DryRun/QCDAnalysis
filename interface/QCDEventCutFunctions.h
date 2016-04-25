#ifndef QCDEventCutFunctions_h
#define QCDEventCutFunctions_h

#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>
#include <algorithm>

#include "TROOT.h"
#include "TMath.h"
#include "TPython.h"

#include "MyTools/RootUtils/interface/Constants.h"
#include "MyTools/AnalysisTools/interface/EventSelector.h"
#include "CMSDIJET/QCDAnalysis/interface/QCDEvent.h"

template class EventSelector<QCDEvent>;

namespace QCDEventCutFunctions {
	bool MinNPFJets(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MaxNPFJets(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MinNCaloJets(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MaxNCaloJets(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MinLeadingPFJetPt(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MinSubleadingPFJetPt(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MaxLeadingPFJetEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MaxSubleadingPFJetEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MinLeadingCaloJetPt(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MinSubleadingCaloJetPt(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MaxLeadingCaloJetEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MaxSubleadingCaloJetEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MinPFMjj(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MaxPFMjj(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MinCaloMjj(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MaxCaloMjj(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MinPFDeltaEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MaxPFDeltaEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MinCaloDeltaEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MaxCaloDeltaEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool LeadingBTagPF(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool LeadingBTagCalo(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool SubleadingBTagPF(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool SubleadingBTagCalo(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool LeadingBVetoPF(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool LeadingBVetoCalo(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool SubleadingBVetoPF(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool SubleadingBVetoCalo(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);

	void Configure(EventSelector<QCDEvent>* p_event_selector);
}
#endif