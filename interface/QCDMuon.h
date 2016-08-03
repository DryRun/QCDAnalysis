#ifndef QCDMuon_h
#define QCDMuon_h
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonIsolation.h"
#include "DataFormats/MuonReco/interface/MuonPFIsolation.h"
//-------- Generic Muon class for QCD analyses ---------------
class QCDMuon 
{
   public:
     typedef reco::Particle::LorentzVector LorentzVector;
     //------------ Constructor ------------------------------
     QCDMuon() {}
     //------------ Destructor -------------------------------
     ~QCDMuon() {}
     //------------ Sett methods -----------------------------
     void setP4(LorentzVector fP4) {P4_ = fP4;}
     void setGen(LorentzVector fP4, float fgenR) {genP4_ = fP4; genR_ = fgenR;}
     void setIsLooseMuon(bool p_loose_id) { loose_id_ =  p_loose_id;}
     void setIsTightMuon(bool p_tight_id) { tight_id_ = p_tight_id;}
     void setIsolationR03(reco::MuonIsolation p_isolation) { isolationR03_ = p_isolation; }
     void setIsolationR05(reco::MuonIsolation p_isolation) { isolationR05_ = p_isolation; }
     void setPfIsolationR03(reco::MuonPFIsolation p_isolation) { pfIsolationR03_ = p_isolation; }
     void setPfMeanDRIsoProfileR03(reco::MuonPFIsolation p_isolation) { pfMeanDRIsoProfileR03_ = p_isolation; }
     void setPfSumDRIsoProfileR03(reco::MuonPFIsolation p_isolation) { pfSumDRIsoProfileR03_ = p_isolation; }
     void setPfIsolationR04(reco::MuonPFIsolation p_isolation) { pfIsolationR04_ = p_isolation; }
     void setPfMeanDRIsoProfileR04(reco::MuonPFIsolation p_isolation) { pfMeanDRIsoProfileR04_ = p_isolation; }
     void setPfSumDRIsoProfileR04(reco::MuonPFIsolation p_isolation) { pfSumDRIsoProfileR04_ = p_isolation; }

     //------------ Get methods ------------------------------
     const LorentzVector& p4()    const {return P4_;}
     const LorentzVector& genp4() const {return genP4_;}
     const bool isLooseID() const {return loose_id_;}
     const bool isTightID() const {return tight_id_;}
     const reco::MuonIsolation isolationR03() const {return isolationR03_;}
     const reco::MuonIsolation isolationR05() const {return isolationR05_;}
     const reco::MuonPFIsolation pfIsolationR03() const {return pfIsolationR03_;}
     //const reco::MuonPFIsolation pfMeanDRIsoProfileR03() const {return pfMeanDRIsoProfileR03_;}
     //const reco::MuonPFIsolation pfSumDRIsoProfileR03() const {return pfSumDRIsoProfileR03_;}
     const reco::MuonPFIsolation pfIsolationR04() const {return pfIsolationR04_;}
     //const reco::MuonPFIsolation pfMeanDRIsoProfileR04() const {return pfMeanDRIsoProfileR04_;}
     //const reco::MuonPFIsolation pfSumDRIsoProfileR04() const {return pfSumDRIsoProfileR04_;}

   private:
     //------ jet 4-momentum vector------------------
     LorentzVector P4_;
     //------ matched genjet 4-momentum vector-------
     LorentzVector genP4_;
     float genR_;

     bool loose_id_;
     bool tight_id_;

     reco::MuonIsolation isolationR03_;
     reco::MuonIsolation isolationR05_;
     reco::MuonPFIsolation pfIsolationR03_;
     reco::MuonPFIsolation pfMeanDRIsoProfileR03_;
     reco::MuonPFIsolation pfSumDRIsoProfileR03_;
     reco::MuonPFIsolation pfIsolationR04_;
     reco::MuonPFIsolation pfMeanDRIsoProfileR04_;
     reco::MuonPFIsolation pfSumDRIsoProfileR04_;

};
#endif
