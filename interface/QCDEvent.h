#ifndef QCDEvent_h
#define QCDEvent_h
#include "CMSDIJET/QCDAnalysis/interface/QCDJet.h"
#include "CMSDIJET/QCDAnalysis/interface/QCDMET.h"
#include "CMSDIJET/QCDAnalysis/interface/QCDCaloJet.h"
#include "CMSDIJET/QCDAnalysis/interface/QCDPFJet.h"
#include "CMSDIJET/QCDAnalysis/interface/Electrons.h"
#include "CMSDIJET/QCDAnalysis/interface/Muons.h"
#include "CMSDIJET/QCDAnalysis/interface/QCDEventHdr.h"
#include "DataFormats/JetReco/interface/Jet.h"
#include <vector>

class QCDEvent 
{
    public:
      typedef reco::Particle::LorentzVector LorentzVector;
      //------------ Constructor ------------------------------
      QCDEvent();
      //------------ Destructor -------------------------------
      ~QCDEvent();
      //------------ Set methods ------------------------------
      void setCaloMET(const QCDMET& fCaloMET)                     {CaloMet_ = fCaloMET;}
      void setPFMET(const QCDMET& fPFMET)                         {PFMet_ = fPFMET;}
      void setEvtHdr(const QCDEventHdr& fEvtHdr)                  {EvtHdr_ = fEvtHdr;}
      void setCaloJets(const std::vector<QCDCaloJet>& fCaloJets);
      void setPFJets(const std::vector<QCDPFJet>& fPFJets);
      void setFatJets(const std::vector<QCDJet>& fFatJets);
      void setGenJets(const std::vector<LorentzVector>& fGenJets);
      void setElectrons(const std::vector<Electron>& fElectrons);
      void setMuons(const std::vector<Muon>& fMuons);
      void setL1Obj(const std::vector<std::vector<LorentzVector> >& fL1Obj);
      void setHLTObj(const std::vector<std::vector<LorentzVector> >& fHLTObj);
      void setPrescales(const std::vector<std::vector<std::pair<std::string, int> > >& fPreL1, const std::vector<int>& fPreHLT) {L1Prescale_ = fPreL1; HLTPrescale_ = fPreHLT;}
      void setTrigDecision(const std::vector<int>& fTrigDecision) {TriggerDecision_ = fTrigDecision;}                           
      //------------ Get methods ------------------------------- 
      std::vector<int>& TriggerDecision() { return TriggerDecision_; }
      unsigned int nTriggers()                         const {return TriggerDecision_.size();}
      unsigned int nL1Obj(int i)                       const {return L1Obj_[i].size();}
      unsigned int nHLTObj(int i)                      const {return HLTObj_[i].size();}
      unsigned int nPFJets()                           const {return PFJets_.size();}
      unsigned int nFatJets()                          const {return FatJets_.size();}
      unsigned int nCaloJets()                         const {return CaloJets_.size();}
      unsigned int nGenJets()                          const {return GenJets_.size();}
      unsigned int nMuons()                            const {return muons_.size();}
      unsigned int nElectrons()                        const {return electrons_.size();}
      int nGoodJets(int unc, int id, float ymax, float ptmin, std::vector<QCDJet> jets) const;
      int fired(int i)                                 const {
            if ((unsigned int)i >= TriggerDecision_.size()) {
                  std::cerr << "[QCDEvent::fired] ERROR : Requested trigger index " << i << " is out of range. Printing TriggerDecision_." << std::endl;
                  for (unsigned int i_trig = 0; i_trig < TriggerDecision_.size(); ++i_trig) {
                        std::cerr << "[QCDEvent::fired] ERROR : \t" << i_trig << " = " << TriggerDecision_[i_trig] << std::endl;
                  }
            }
            return TriggerDecision_[i];
      }
      std::vector<std::pair<std::string, int> > preL1(int i) const {return L1Prescale_[i];}
      int minPreL1(int i);
      int preHLT(int i)                                const {return HLTPrescale_[i];}
      float pfmjj() const;
      float calomjj() const;
      float genmjj() const; 
      float pfmjjcor(int unc) const;
      float pfmjjcor(int unc,int src) const;
      float fatmjjcor(int unc) const;
      float calomjjcor(int unc) const;
      float pfmjjgen() const;
      float calomjjgen() const;
      const QCDMET&        calomet()                   const {return CaloMet_;}
      const QCDMET&        pfmet()                     const {return PFMet_;} 
      const LorentzVector& hltobj(int itrig, int iobj) const {return (HLTObj_[itrig])[iobj];}  
      const LorentzVector& l1obj(int itrig, int iobj)  const {return (L1Obj_[itrig])[iobj];}   
      const LorentzVector& genjet(int i)               const {return GenJets_[i];}
      const QCDPFJet&      pfjet(int i)                const {return PFJets_[i];}
      const QCDJet&        fatjet(int i)               const {return FatJets_[i];}
      const QCDCaloJet&    calojet(int i)              const {return CaloJets_[i];}
      const QCDEventHdr&   evtHdr()                    const {return EvtHdr_;}
      const Electron&   electron(int i)                    const {return EvtHdr_;}
      const Muon&   muon(int i)                    const {return electrons_[i];}
      const std::vector<QCDCaloJet>& calojets()   const {return muons_[i];}
      const std::vector<QCDPFJet>& pfjets()   const {return PFJets_;}
      const std::vector<QCDJet>& fatjets()   const {return FatJets_;}
      const std::vector<Muon>& electrons()   const {return electrons_;}
      const std::vector<Electron>& muons()   const {return muons_;}

      void sortPFJetsBTagCSV();

    private:
    static bool sort_pfjets_btag_csv(QCDPFJet j1, QCDPFJet j2) {
      return j1.btag_csv() > j2.btag_csv();
    }

      //---- event header (contains all the event info) --------------
      QCDEventHdr                              EvtHdr_;
      //---- CALO met object -----------------------------------------
      QCDMET                                   CaloMet_;
      //---- PF met object -------------------------------------------
      QCDMET                                   PFMet_; 
      //---- trigger decision vector --------------------------------- 
      std::vector<int>                         TriggerDecision_;
      //---- L1 prescale vector --------------------------------------
      std::vector<std::vector<std::pair<std::string, int> > > L1Prescale_;
      //---- HLT prescale vector -------------------------------------
      std::vector<int>                         HLTPrescale_;
      //---- HLT objects ---------------------------------------------  
      std::vector<std::vector<LorentzVector> > HLTObj_;
      //---- L1 objects ----------------------------------------------
      std::vector<std::vector<LorentzVector> > L1Obj_;
      //---- Genjets -------------------------------------------------
      std::vector<LorentzVector>               GenJets_;
      //---- CaloJets ------------------------------------------------ 
      std::vector<QCDCaloJet>                  CaloJets_;
      //---- PFJets --------------------------------------------------
      std::vector<QCDPFJet>                    PFJets_;
      //---- FatJets -------------------------------------------------
      std::vector<QCDJet>                      FatJets_;
      // Leptons
      std::vector<Muon> muons_;
      std::vector<Electron> electrons_;
};
#endif
