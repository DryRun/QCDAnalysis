#include "CMSDIJET/QCDAnalysis/interface/QCDEvent.h"
//---------------------------------------------------
QCDEvent::QCDEvent()
{  
	L1Obj_.clear();
	CaloJets_.clear();
	PFJets_.clear(); 
	GenJets_.clear();
}
//---------------------------------------------------
QCDEvent::~QCDEvent()
{
}
//---------------------------------------------------
void QCDEvent::setCaloJets(const std::vector<QCDCaloJet>& fCaloJets) 
{ 
	CaloJets_.clear();
	for(unsigned i=0;i<fCaloJets.size();i++) {
		CaloJets_.push_back(fCaloJets[i]);
	}
}
//---------------------------------------------------
void QCDEvent::setPFJets(const std::vector<QCDPFJet>& fPFJets) 
{ 
	PFJets_.clear();
	for(unsigned i=0;i<fPFJets.size();i++) {
		PFJets_.push_back(fPFJets[i]);
	}
}
//---------------------------------------------------
void QCDEvent::setFatJets(const std::vector<QCDJet>& fFatJets)
{
	FatJets_.clear();
	for(unsigned i=0;i<fFatJets.size();i++) {
		FatJets_.push_back(fFatJets[i]);
	}
}
//---------------------------------------------------
void QCDEvent::setGenJets(const std::vector<LorentzVector>& fGenJets)
{
	GenJets_.clear();
	for(unsigned i=0;i<fGenJets.size();i++) {
		GenJets_.push_back(fGenJets[i]);
	}
}
void QCDEvent::setMuons(const std::vector<QCDMuon>& fMuons) {
	muons_.clear();
	for (unsigned i = 0; i < fMuons.size(); ++i) {
		muons_.push_back(fMuons[i]);
	}
}
//---------------------------------------------------
void QCDEvent::setL1Obj(const std::vector<std::vector<LorentzVector> >& fL1Obj)       
{
	L1Obj_.clear();
	for(unsigned i=0;i<fL1Obj.size();i++) {
		std::vector<LorentzVector> vv;
		for(unsigned j=0;j<fL1Obj[i].size();j++) {
			vv.push_back(fL1Obj[i][j]);
		}
		L1Obj_.push_back(vv);
	}
}
//---------------------------------------------------
void QCDEvent::setHLTObj(const std::vector<std::vector<LorentzVector> >& fHLTObj)       
{
	HLTObj_.clear();
	for(unsigned i=0;i<fHLTObj.size();i++) {
		std::vector<LorentzVector> vv;
		for(unsigned j=0;j<fHLTObj[i].size();j++) {
			vv.push_back(fHLTObj[i][j]);
		}
		HLTObj_.push_back(vv);
	}
}
//---------------------------------------------------
int QCDEvent::minPreL1(int i) {
	int min_L1_prescale = INT_MAX;
	for (std::vector<std::pair<std::string, int> >::iterator it_ps = L1Prescale_[i].begin(); it_ps != L1Prescale_[i].end(); ++it_ps) {
		if ((*it_ps).second < min_L1_prescale && (*it_ps).second > 0) {
			min_L1_prescale = (*it_ps).second;
		}
	}
	if (min_L1_prescale == INT_MAX) {
		//std::cerr << "[QCDEvent::preL1] WARNING : Failed to find prescale for index " << i << ". Returning -1." << std::endl;
		min_L1_prescale = -1;
	}
	return min_L1_prescale;
}

//---------------------------------------------------
int QCDEvent::nGoodJets(int unc, int id, float ymax, float ptmin, std::vector<QCDJet> jets) const
{
	// unc defines the uncertainty
	// id defines the jet id
	// ymax defines the maximum rapidity
	// ptmin defines the minimum jet pt
	int sign(0),counter(0);
	if (unc > 0)
		sign = 1;
	if (unc < 0)
		sign = -1;
	for(unsigned i=0;i<jets.size();i++) {
		bool passID(true);
		if (id == 1 && !jets[i].looseIDFlag())
			passID = false;
		if (id == 2 && !jets[i].tightIDFlag()) 
			passID = false;
		if (passID) {
			if (fabs(jets[i].y()) <= ymax && jets[i].ptCor()*(1+sign*jets[i].unc()) >= ptmin)
				counter++;
		}
	}
	return counter;
}
//---------------------------------------------------
float QCDEvent::genmjj() const
{
	if (GenJets_.size() < 2)
		return 0.0;
	else {
		return (GenJets_[0]+GenJets_[1]).mass();
	}
}
//---------------------------------------------------
float QCDEvent::pfmjj() const
{
	if (PFJets_.size() < 2)
		return 0.0;
	else {
		const LorentzVector& P0 = PFJets_[0].p4();
		const LorentzVector& P1 = PFJets_[1].p4();
		return (P0+P1).mass();
	}
}
//---------------------------------------------------
float QCDEvent::pfmjjcor(int k) const
{
	int sign(0);
	if (PFJets_.size() < 2)
		return 0.0;
	else {
		if (k>0)
			sign = 1;
		if (k<0)
			sign = -1;  
		const LorentzVector& P0 = PFJets_[0].p4();
		const LorentzVector& P1 = PFJets_[1].p4();
		double cor0 = PFJets_[0].cor();
		double cor1 = PFJets_[1].cor();
		double unc0 = PFJets_[0].unc();
		double unc1 = PFJets_[1].unc();
		return (cor0*(1+sign*unc0)*P0+cor1*(1+sign*unc1)*P1).mass();
	}
}
//---------------------------------------------------
float QCDEvent::pfmjjcor(int k,int src) const
{
	int sign(0);
	if (PFJets_.size() < 2)
		return 0.0;
	else {
		if (k>0)
			sign = 1;
		if (k<0)
			sign = -1;
		const LorentzVector& P0 = PFJets_[0].p4();
		const LorentzVector& P1 = PFJets_[1].p4();
		double cor0 = PFJets_[0].cor();
		double cor1 = PFJets_[1].cor();
		double unc0 = PFJets_[0].uncSrc(src);
		double unc1 = PFJets_[1].uncSrc(src);
		return (cor0*(1+sign*unc0)*P0+cor1*(1+sign*unc1)*P1).mass();
	}
}
//---------------------------------------------------
float QCDEvent::fatmjjcor(int k) const
{
	int sign(0);
	if (FatJets_.size() < 2)
		return 0.0;
	else {
		if (k>0)
			sign = 1;
		if (k<0)
			sign = -1;
		const LorentzVector& P0 = FatJets_[0].p4();
		const LorentzVector& P1 = FatJets_[1].p4();
		double cor0 = FatJets_[0].cor();
		double cor1 = FatJets_[1].cor();
		double unc0 = FatJets_[0].unc();
		double unc1 = FatJets_[1].unc();
		return (cor0*(1+sign*unc0)*P0+cor1*(1+sign*unc1)*P1).mass();
	}
}
//---------------------------------------------------
float QCDEvent::calomjj() const
{
	if (CaloJets_.size() < 2)
		return 0.0;
	else {
		const LorentzVector& P0 = CaloJets_[0].p4();
		const LorentzVector& P1 = CaloJets_[1].p4();
		return (P0+P1).mass();
	}
}
//---------------------------------------------------
float QCDEvent::calomjjcor(int k) const
{
	int sign(0);
	if (CaloJets_.size() < 2)
		return 0.0;
	else {
		if (k>0)
			sign = 1;
		if (k<0)
			sign = -1;
		const LorentzVector& P0 = CaloJets_[0].p4();
		const LorentzVector& P1 = CaloJets_[1].p4();
		double cor0 = CaloJets_[0].cor();
		double cor1 = CaloJets_[1].cor();
		double unc0 = CaloJets_[0].unc();
		double unc1 = CaloJets_[1].unc();
		return (cor0*(1+sign*unc0)*P0+cor1*(1+sign*unc1)*P1).mass();
	}
}
//---------------------------------------------------
float QCDEvent::pfmjjgen() const
{
	if (PFJets_.size() < 2)
		return 0.0;
	else {
		const LorentzVector& P0 = PFJets_[0].genp4();
		const LorentzVector& P1 = PFJets_[1].genp4();
		return (P0+P1).mass();
	}
}
//---------------------------------------------------
float QCDEvent::calomjjgen() const
{
	if (CaloJets_.size() < 2)
		return 0.0;
	else {
		const LorentzVector& P0 = CaloJets_[0].genp4();
		const LorentzVector& P1 = CaloJets_[1].genp4();
		return (P0+P1).mass();
	}
}


void QCDEvent::sortPFJetsBTagCSV() {
	sort(PFJets_.begin(),PFJets_.end(),sort_pfjets_btag_csv);
}
