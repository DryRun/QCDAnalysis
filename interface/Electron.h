#ifndef Electron_h
#define Electron_h
#include "DataFormats/ElectronReco/interface/Electron.h"
//-------- Generic Electron class for QCD analyses ---------------
class Electron 
{
   public:
     typedef reco::Particle::LorentzVector LorentzVector;
     //------------ Constructor ------------------------------
     Electron() {}
     //------------ Destructor -------------------------------
     ~Electron() {}
     //------------ Sett methods -----------------------------
     void setP4(LorentzVector fP4) {P4_ = fP4;}
     void setGen(LorentzVector fP4, float fgenR) {genP4_ = fP4;genR_ = fgenR;}
     void setIsLooseElectron(bool p_loose_id) { loose_id_ =  p_loose_id;}
     void setIsTightElectron(bool p_tight_id) { tight_id_ = p_tight_id;}
     void setIsolationR03(ElectronIsolation p_isolation) { isolationR03_ = p_isolation; }
     void setIsolationR05(ElectronIsolation p_isolation) { isolationR05_ = p_isolation; }
     void setPfIsolationR03(ElectronPFIsolation p_isolation) { pfIsolationR03_ = p_isolation; }
     void setPfMeanDRIsoProfileR03(ElectronPFIsolation p_isolation) { pfMeanDRIsoProfileR03_ = p_isolation; }
     void setPfSumDRIsoProfileR03(ElectronPFIsolation p_isolation) { pfSumDRIsoProfileR03_ = p_isolation; }
     void setPfIsolationR04(ElectronPFIsolation p_isolation) { pfIsolationR04_ = p_isolation; }
     void setPfMeanDRIsoProfileR04(ElectronPFIsolation p_isolation) { pfMeanDRIsoProfileR04_ = p_isolation; }
     void setPfSumDRIsoProfileR04(ElectronPFIsolation p_isolation) { pfSumDRIsoProfileR04_ = p_isolation; }

     //------------ Get methods ------------------------------
     const LorentzVector& p4()    const {return P4_;}
     const LorentzVector& genp4() const {return genP4_;}
     const bool isLooseID const {return loose_id_;}
     const bool isTightID const {return tight_id_;}
     const ElectronIsolation isolationR03 const {return isolationR03_;}
     const ElectronIsolation isolationR05 const {return isolationR05_;}
     const ElectronPFIsolation pfIsolationR03 const {return pfIsolationR03_;}
     const ElectronPFIsolation pfMeanDRIsoProfileR03 const {return pfMeanDRIsoProfileR03_;}
     const ElectronPFIsolation pfSumDRIsoProfileR03 const {return pfSumDRIsoProfileR03_;}
     const ElectronPFIsolation pfIsolationR04 const {return pfIsolationR04_;}
     const ElectronPFIsolation pfMeanDRIsoProfileR04 const {return pfMeanDRIsoProfileR04_;}
     const ElectronPFIsolation pfSumDRIsoProfileR04 const {return pfSumDRIsoProfileR04_;}

   private:
     //------ jet 4-momentum vector------------------
     LorentzVector P4_;
     //------ matched genjet 4-momentum vector-------
     LorentzVector genP4_;

     bool loose_id_;
     bool tight_id_;

     ElectronIsolation isolationR03_;
     ElectronIsolation isolationR05_;
     ElectronPFIsolation pfIsolationR03_;
     ElectronPFIsolation pfMeanDRIsoProfileR03_;
     ElectronPFIsolation pfSumDRIsoProfileR03_;
     ElectronPFIsolation pfIsolationR04_;
     ElectronPFIsolation pfMeanDRIsoProfileR04_;
     ElectronPFIsolation pfSumDRIsoProfileR04_;

};
#endif
