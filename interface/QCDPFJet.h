#ifndef QCDPFJet_h
#define QCDPFJet_h
#include "CMSDIJET/QCDAnalysis/interface/QCDJet.h"

class QCDPFJet : public QCDJet {
 public:
	//------------ Constructor ------------------------------
	QCDPFJet() {
		chargedHadronEnergy_ = 0;
		neutralHadronEnergy_ = 0;
		photonEnergy_ = 0;
		electronEnergy_ = 0;
		muonEnergy_ = 0;
		HFHadronEnergy_ = 0;
		HFEMEnergy_ = 0;
		chargedHadronMultiplicity_ = 0;
		neutralHadronMultiplicity_ = 0;
		photonMultiplicity_ = 0;
		electronMultiplicity_ = 0;
		muonMultiplicity_ = 0;
		HFHadronMultiplicity_ = 0;
		HFEMMultiplicity_ = 0;
		chargedEmEnergy_ = 0;
		chargedMuEnergy_ = 0;
		neutralEmEnergy_ = 0;
		chargedMultiplicity_ = 0;
		neutralMultiplicity_ = 0;
		beta_ = 0;
		betaStar_ = 0;
	}
	//------------ Destructor -------------------------------
	~QCDPFJet() {}
	//------------ Set methods ------------------------------
	//void setFrac(float fchf, float fnhf, float fphf, float felf, float fmuf)  {chf_ = fchf; nhf_ = fnhf; phf_ = fphf; elf_ = felf; muf_ = fmuf;}
	//void setMulti(int fncand, int fchm, int fnhm, int fphm, int felm, int fmum) {ncand_ = fncand; chm_ = fchm; nhm_ = fnhm; phm_ = fphm; elm_ = felm; mum_ = fmum;}
	//void setBeta(float fbeta) {beta_ = fbeta;}
	//void setBetaStar(float fbetaStar) {betaStar_ = fbetaStar;}
	//void setHFFrac(float fhf_hf, float fhf_phf) {hf_hf_ = fhf_hf; hf_phf_ = fhf_phf;}
	//void setHFMulti(int fhf_hm, int fhf_phm) {hf_hm_ = fhf_hm; hf_phm_ = fhf_phm;}
	//------------ Get methods ------------------------------ 
	//float beta()     const {return beta_;}                
	//float betaStar() const {return betaStar_;}
	//float chf()      const {return chf_;} 
	//float nhf()      const {return nhf_;}
	//float phf()      const {return phf_;} 
	//float elf()      const {return elf_;}
	//float muf()      const {return muf_;}
	//float hf_hf()    const {return hf_hf_;}
	//float hf_phf()   const {return hf_phf_;}
	//int chm()        const {return chm_;}
	//int nhm()        const {return nhm_;}
	//int phm()        const {return phm_;}
	//int elm()        const {return elm_;}
	//int mum()        const {return mum_;}
	//int hf_hm()      const {return hf_hm_;}
	//int hf_phm()     const {return hf_phm_;}
	//int ncand()      const {return ncand_;}
	
	// Setters
	inline void setChargedHadronEnergy(float p_chargedHadronEnergy) {chargedHadronEnergy_ = p_chargedHadronEnergy;}
	inline void setNeutralHadronEnergy(float p_neutralHadronEnergy) {neutralHadronEnergy_ = p_neutralHadronEnergy;}
	inline void setPhotonEnergy(float p_photonEnergy) {photonEnergy_ = p_photonEnergy;}
	inline void setElectronEnergy(float p_electronEnergy) {electronEnergy_ = p_electronEnergy;}
	inline void setMuonEnergy(float p_muonEnergy) {muonEnergy_ = p_muonEnergy;}
	inline void setHFHadronEnergy(float p_HFHadronEnergy) {HFHadronEnergy_ = p_HFHadronEnergy;}
	inline void setHFEMEnergy(float p_HFEMEnergy) {HFEMEnergy_ = p_HFEMEnergy;}
	inline void setChargedHadronMultiplicity(int p_chargedHadronMultiplicity) {chargedHadronMultiplicity_ = p_chargedHadronMultiplicity;}
	inline void setNeutralHadronMultiplicity(int p_neutralHadronMultiplicity) {neutralHadronMultiplicity_ = p_neutralHadronMultiplicity;}
	inline void setPhotonMultiplicity(int p_photonMultiplicity) {photonMultiplicity_ = p_photonMultiplicity;}
	inline void setElectronMultiplicity(int p_electronMultiplicity) {electronMultiplicity_ = p_electronMultiplicity;}
	inline void setMuonMultiplicity(int p_muonMultiplicity) {muonMultiplicity_ = p_muonMultiplicity;}
	inline void setHFHadronMultiplicity(int p_HFHadronMultiplicity) {HFHadronMultiplicity_ = p_HFHadronMultiplicity;}
	inline void setHFEMMultiplicity(int p_HFEMMultiplicity) {HFEMMultiplicity_ = p_HFEMMultiplicity;}
	inline void setChargedEmEnergy(float p_chargedEmEnergy) {chargedEmEnergy_ = p_chargedEmEnergy;}
	inline void setChargedMuEnergy(float p_chargedMuEnergy) {chargedMuEnergy_ = p_chargedMuEnergy;}
	inline void setNeutralEmEnergy(float p_neutralEmEnergy) {neutralEmEnergy_ = p_neutralEmEnergy;}
	inline void setChargedMultiplicity(int p_chargedMultiplicity) {chargedMultiplicity_ = p_chargedMultiplicity;}
	inline void setNeutralMultiplicity(int p_neutralMultiplicity) {neutralMultiplicity_ = p_neutralMultiplicity;}
	inline void setBeta(float p_beta) {beta_ = p_beta;}
	inline void setBetaStar(float p_betaStar) {betaStar_ = p_betaStar;}

	// Getters
	inline float chargedHadronEnergy() const {return chargedHadronEnergy_;}
	inline float neutralHadronEnergy() const {return neutralHadronEnergy_;}
	inline float photonEnergy() const {return photonEnergy_;}
	inline float electronEnergy() const {return electronEnergy_;}
	inline float muonEnergy() const {return muonEnergy_;}
	inline float HFHadronEnergy() const {return HFHadronEnergy_;}
	inline float HFEMEnergy() const {return HFEMEnergy_;}
	inline int chargedHadronMultiplicity() const {return chargedHadronMultiplicity_;}
	inline int neutralHadronMultiplicity() const {return neutralHadronMultiplicity_;}
	inline int photonMultiplicity() const {return photonMultiplicity_;}
	inline int electronMultiplicity() const {return electronMultiplicity_;}
	inline int muonMultiplicity() const {return muonMultiplicity_;}
	inline int HFHadronMultiplicity() const {return HFHadronMultiplicity_;}
	inline int HFEMMultiplicity() const {return HFEMMultiplicity_;}
	inline float chargedEmEnergy() const {return chargedEmEnergy_;}
	inline float chargedMuEnergy() const {return chargedMuEnergy_;}
	inline float neutralEmEnergy() const {return neutralEmEnergy_;}
	inline int chargedMultiplicity() const {return chargedMultiplicity_;}
	inline int neutralMultiplicity() const {return neutralMultiplicity_;}
	inline float beta()     const {return beta_;}                
	inline float betaStar() const {return betaStar_;}

	// Calculated variables
	inline float  chargedHadronEnergyFraction() const {return chargedHadronEnergy() / e();}
	inline float neutralHadronEnergyFraction() const {return neutralHadronEnergy() / e();}
	inline float photonEnergyFraction() const {return photonEnergy() / e();}
	inline float electronEnergyFraction() const {return electronEnergy() / e();}
	inline float muonEnergyFraction() const {return muonEnergy() / e();}
	inline float HFHadronEnergyFraction() const {return HFHadronEnergy() / e();}
	inline float HFEMEnergyFraction() const {return HFEMEnergy() / e();}
	inline float chargedEmEnergyFraction() const {return chargedEmEnergy() / e();}
	inline float chargedMuEnergyFraction() const {return chargedMuEnergy() / e();}
	inline float neutralEmEnergyFraction() const {return neutralEmEnergy() / e();}
	inline int nPFCandidates() const {return chargedMultiplicity() + neutralMultiplicity();}

	inline bool isLooseID() const {
		return (neutralHadronEnergyFraction()<0.99 && neutralEmEnergyFraction()<0.99 && (chargedMultiplicity() + neutralMultiplicity())>1 && muonEnergyFraction()<0.8) && ((abs(eta())<=2.4 && chargedHadronEnergyFraction()>0 && chargedMultiplicity()>0 && chargedEmEnergyFraction()<0.99) || abs(eta())>2.4);
	}
	inline bool isTightID() const {
		return (neutralHadronEnergyFraction()<0.90 && neutralEmEnergyFraction()<0.90 && (chargedMultiplicity() + neutralMultiplicity())>1 && muonEnergyFraction()<0.8) && ((abs(eta())<=2.4 && chargedHadronEnergyFraction()>0 && chargedMultiplicity()>0 && chargedEmEnergyFraction()<0.90) || abs(eta())>2.4);
	}

 private:
	float chargedHadronEnergy_;
	float neutralHadronEnergy_;
	float photonEnergy_;
	float electronEnergy_;
	float muonEnergy_;
	float HFHadronEnergy_;
	float HFEMEnergy_;
	int chargedHadronMultiplicity_;
	int neutralHadronMultiplicity_;
	int photonMultiplicity_;
	int electronMultiplicity_;
	int muonMultiplicity_;
	int HFHadronMultiplicity_;
	int HFEMMultiplicity_;
	float chargedEmEnergy_;
	float chargedMuEnergy_;
	float neutralEmEnergy_;
	int chargedMultiplicity_;
	int neutralMultiplicity_;
	float beta_;
	float betaStar_;
};
#endif    
