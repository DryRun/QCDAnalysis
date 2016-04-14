#ifndef DijetCutFunctions_h
#define DijetCutFunctions_h

#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>
#include <algorithm>

#include "TROOT.h"
#include "TMath.h"
#include "TPython.h"

#include "MyTools/RootUtils/interface/Constants.h"
#include "MyTools/AnalysisTools/interface/Cutflow.h"
#include "CMSDIJET/QCDAnalysis/interface/QCDEvent.h"

namespace QCDEventCutFunctions {
	bool MinNPFJets(QCDEvent& p_data, Cutflow* p_cutflow);
	bool MaxNPFJets(QCDEvent& p_data, Cutflow* p_cutflow);
	bool MinNCaloJets(QCDEvent& p_data, Cutflow* p_cutflow);
	bool MaxNCaloJets(QCDEvent& p_data, Cutflow* p_cutflow);
	bool MinPFMjj(QCDEvent& p_data, Cutflow* p_cutflow);
	bool MaxPFMjj(QCDEvent& p_data, Cutflow* p_cutflow);
	bool MinCaloMjj(QCDEvent& p_data, Cutflow* p_cutflow);
	bool MaxCaloMjj(QCDEvent& p_data, Cutflow* p_cutflow);
	bool MinPFDeltaEta(QCDEvent& p_data, Cutflow* p_cutflow);
	bool MaxPFDeltaEta(QCDEvent& p_data, Cutflow* p_cutflow);
	bool MinCaloDeltaEta(QCDEvent& p_data, Cutflow* p_cutflow);
	bool MaxCaloDeltaEta(QCDEvent& p_data, Cutflow* p_cutflow);
	bool LeadingBTagPF(QCDEvent& p_data, Cutflow* p_cutflow);
	bool LeadingBTagCalo(QCDEvent& p_data, Cutflow* p_cutflow);
	bool SubleadingBTagPF(QCDEvent& p_data, Cutflow* p_cutflow);
	bool SubleadingBTagCalo(QCDEvent& p_data, Cutflow* p_cutflow);
	bool LeadingBVetoPF(QCDEvent& p_data, Cutflow* p_cutflow);
	bool LeadingBVetoCalo(QCDEvent& p_data, Cutflow* p_cutflow);
	bool SubleadingBVetoPF(QCDEvent& p_data, Cutflow* p_cutflow);
	bool SubleadingBVetoCalo(QCDEvent& p_data, Cutflow* p_cutflow) ;
}
#endif