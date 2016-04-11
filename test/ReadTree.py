import os
import sys
import ROOT
from ROOT import *
gSystem.Load("libFWCoreFWLite.so")
AutoLibraryLoader.enable()


def ReadTree():
	f_in  = TFile("ProcessedTree_data.root", "READ")
	f_out = TFile("DemoHistos.root","RECREATE")
	tree = f_in.Get("ak5/ProcessedTree")

	event = ROOT.QCDEvent()
	branch = tree.SetBranchAddress("events", event)

	NeventS = 10000
	HLT = "HLT_Jet300_v5"
	PTMIN = 100
	ETAMAX = 2.5

	histograms = Root.HistogramManager()
	histograms.AddPrefix("h_")
	histograms.AddTH1F("CorrectedJetPt","CorrectedJetPt",350,0,3500)
	histograms.AddTH1F("JetRapidity","JetRapidity",100,-5,5)
	histograms.AddTH1F("Beta","Beta",100,0,1.000001)
	histograms.AddTH1F("METoverSUMET","METoverSUMET",100,0,1.0001)
	histograms.AddTH1F("NumberOfVertices","NumberOfVertices",30,0,30)
	histograms.AddTH1F("PtDensityRho","PtDensityRho",50,0,50)
	#TProfile *pBetaVsNPV = new TProfile("BetaVsNPV","BetaVsNPV",20,0,20,0,1.000001)

	# Trigger
	h_trigger_names = f_in.Get("ak7/TriggerNames")
	ihlt = -1

	for ibin in xrange(1, h_trigger_names.GetNbinsX() + 1):
		name = TString(h_trigger_names.GetXaxis().GetBinLabel(ibin + 1))
		if (name.EqualTo(HLT)):
			ihlt = ibin
			continue
	if ihlt == -1:
		print "The requested trigger ({}) is not found ".format(HLT)
		sys.exit(1)
	else:
		print HLT + " -. " + ihlt

	#----------- counters -----------------------
	counter_hlt = 0
	counter_pv = 0
	counter_hcal = 0
	counter_jet = 0
	
	NEntries = tree.GetEntries()
	print "Tree has {} entries".format(NEntries)
	for i in xrange(min(NEntries, NeventS)):
		if i % (TMath.FloorNInt(min(NEntries, NeventS) / 10.)) == 0:
			print "On event {} / {}".format(i, min(NEntries, NeventS))

		tree.GetEntry(i)
		hlt_pass = False 
		prescale = 1
		if ihlt == -1:
			hlt_pass = True 
		else:
			if event.fired(ihlt) > 0:
				hlt_pass = True
				prescale = event.preL1(ihlt) * event.preHLT(ihlt)
		if hltPass:
			counter_hlt += 1
			#-------- check if the primary vertex is good ----
			if event.evtHdr().isPVgood() == 1:
				counter_pv += 1 
				#-------- check the loose HCAL noise filter ----------
				if event.evtHdr().looseHCALNoise():
					counter_hcal += 1
					#------- fill the MET/SumET control histo ----------
					hMET.Fill(event.pfmet().met_o_sumet())
					#------- fill the NPV histo ------------------------
					hNPV.Fill(event.evtHdr().nVtxGood())          
					#------- fill the Rho histo ------------------------
					hRho.Fill(event.evtHdr().pfRho())
					#------- loop over the PF jets ---------------------
					for j in xrange(event.nPFJets):
						#----- apply the pt and ID cuts ------------------
						if event.pfjet(j).ptCor() >= PTMIN and fabs(event.pfjet(j).eta()) < ETAMAX and event.pfjet(j).tightID():
							counter_jet += 1
							#------- fill some histograms ------------------
							histograms_.GetTH1F("hCorPt").Fill(event.pfjet(j).ptCor())
							histograms_.GetTH1F("hY").Fill(event.pfjet(j).y()) 
							histograms_.GetTH1F("hBeta").Fill(event.pfjet(j).beta())
							histograms_.GetTH1F("pBetaVsNPV").Fill(event.evtHdr().nVtxGood(),event.pfjet(j).beta())
					# jet loop
				# hcal noise filter    
			# pv cut
		# hlt
	# tree loop
	#----------------- print out some information ---------------
	print "events read:                      {}".format(NN)
	print "events after the trigger cut:     {}".format(counter_hlt)
	print "events after the PV cut:          {}".format(counter_pv)
	print "events after the HCAL filter cut: {}".format(counter_hcal)
	print "Number of jets:                   {}".format(counter_jet)
	#----------------- save the histos to the output file -------
	f_out.Write()

if __name__ == "__main__":
	ReadTree()

