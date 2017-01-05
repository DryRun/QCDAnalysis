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
	// Simple trigger pass. 
	// p[0] = trigger index
	bool Trigger(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);

	// Multiple trigger pass.
	// p = vector of trigger indices to test
	bool TriggerOR(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool TriggerOR2(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool TriggerXOR(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);

	bool IsGoodPV(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MaxMetOverSumEt(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);

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

	// Cuts on the PF dijet system
	bool GoodPFDijet(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool PFDijetMinDeltaEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool PFDijetMaxDeltaEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MinPFMjj(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MaxPFMjj(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);

	// Cuts on the calo dijet system
	bool MinCaloMjj(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MaxCaloMjj(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool CaloDijetMinDeltaEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool CaloDijetMaxDeltaEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);

	// B tags
	bool LeadingBTagPF(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool LeadingBTagCalo(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool SubleadingBTagPF(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool SubleadingBTagCalo(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool LeadingBVetoPF(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool LeadingBVetoCalo(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool SubleadingBVetoPF(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool SubleadingBVetoCalo(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MinNCSVL(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MinNCSVM(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MinNCSVT(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);

	// Fat jet cuts. Think about whether to use normal or fat jets for these!
	bool MinLeadingPFFatJetPt(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MinSubleadingPFFatJetPt(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MaxLeadingPFFatJetEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MaxSubleadingPFFatJetEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool PFFatDijetMinDeltaEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool PFFatDijetMaxDeltaEta(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MinPFFatMjj(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool MaxPFFatMjj(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool LeadingBTagPFFat(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool SubleadingBTagPFFat(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool LeadingBVetoPFFat(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);
	bool SubleadingBVetoPFFat(const QCDEvent& p_data, EventSelector<QCDEvent>* p_event_selector);

	void Configure(EventSelector<QCDEvent>* p_event_selector);
}
#endif