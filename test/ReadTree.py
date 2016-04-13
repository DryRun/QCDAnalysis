import os
import sys
import ROOT
from ROOT import *
gSystem.Load("libFWCoreFWLite.so")
gSystem.Load("libMyToolsRootUtils.so")
AutoLibraryLoader.enable()


def ReadTree():
	f_in  = TFile("ProcessedTree_data.root", "READ")
	f_out = TFile("DemoHistos.root","RECREATE")
	tree = f_in.Get("ak5/ProcessedTree")

	event = ROOT.QCDEvent()
	branch = tree.SetBranchAddress("events", event)

	NeventS = 10000
	HLT = "HLT_PFJet320_v8"
	PTMIN = 100
	ETAMAX = 2.5

	histograms = Root.HistogramManager()
	histograms.AddPrefix("h_")

	histograms.AddTH1F("CorrectedJetPt", "CorrectedJetPt", "p_{T} [MeV]", 350, 0, 3500)
	histograms.AddTH1F("JetRapidity", "JetRapidity", "#eta", 100, -5, 5)
	histograms.AddTH1F("Beta", "Beta", "#beta", 100, 0, 1.000001)
	histograms.AddTH1F("METoverSUMET", "METoverSUMET", "MET/#Sigma E_{T}", 100, 0, 1.0001)
	histograms.AddTH1F("NumberOfVertices", "NumberOfVertices", "N_{vertex}", 30, 0, 30)
	histograms.AddTH1F("PtDensityRho", "PtDensityRho", "p_{T} density #rho", 50, 0, 50)
	#TProfile *pBetaVsNPV = new TProfile("BetaVsNPV","BetaVsNPV",20,0,20,0,1.000001)

	# Trigger
	h_trigger_names = f_in.Get("ak7/TriggerNames")
	ihlt = -1
	trigger_map = {}
	for ibin in xrange(1, h_trigger_names.GetNbinsX() + 1):
		name = TString(h_trigger_names.GetXaxis().GetBinLabel(ibin + 1))
		if (name.EqualTo(HLT)):
			ihlt = ibin
		if not name.EqualTo(""):
			trigger_map[name.Data()] = ibin
	if ihlt == -1:
		print "The requested trigger (" + HLT + ") is not found "
		sys.exit(1)
	else:
		print HLT + " -. " + str(ihlt)

	#----------- counters -----------------------
	counter_hlt = 0
	counter_pv = 0
	counter_hcal = 0
	counter_jet = 0
	
	trigger_counts_raw = {}
	trigger_counts_prescaled = {}
	for trigger_name, trigger_index in trigger_map.iteritems():
		trigger_counts_raw[trigger_name] = 0.
		trigger_counts_prescaled[trigger_name] = 0.

	NEntries = tree.GetEntries()
	print "Tree has " + str(NEntries) + " entries"
	for i in xrange(min(NEntries, NeventS)):
		if i % (TMath.FloorNint(min(NEntries, NeventS) / 10.)) == 0:
			print "On event " + str(i) + " / " + str(min(NEntries, NeventS))

		tree.GetEntry(i)

		# Record all passed triggers
		for trigger_name, trigger_index in trigger_map.iteritems():
			if event.fired(trigger_index) > 0:
				trigger_counts_raw[trigger_name] += 1
				trigger_counts_prescaled[trigger_name] += event.preL1(ihlt) * event.preHLT(ihlt)

		hlt_pass = False 
		prescale = 1
		if ihlt == -1:
			hlt_pass = True 
		else:
			if event.fired(ihlt) > 0:
				hlt_pass = True
				prescale = event.preL1(ihlt) * event.preHLT(ihlt)
		if hlt_pass:
			counter_hlt += 1
			#-------- check if the primary vertex is good ----
			if event.evtHdr().isPVgood() == 1:
				counter_pv += 1 
				#-------- check the loose HCAL noise filter ----------
				if event.evtHdr().hcalNoise():
					counter_hcal += 1
					#------- fill the MET/SumET control histo ----------
					histograms.GetTH1F("METoverSUMET").Fill(event.pfmet().met_o_sumet())
					#------- fill the NPV histo ------------------------
					histograms.GetTH1F("NumberOfVertices").Fill(event.evtHdr().nVtxGood())          
					#------- fill the Rho histo ------------------------
					histograms.GetTH1F("PtDensityRho").Fill(event.evtHdr().pfRho())
					#------- loop over the PF jets ---------------------
					for j in xrange(event.nPFJets()):
						#----- apply the pt and ID cuts ------------------
						if event.pfjet(j).ptCor() >= PTMIN and fabs(event.pfjet(j).eta()) < ETAMAX and event.pfjet(j).tightID():
							counter_jet += 1
							#------- fill some histograms ------------------
							histograms.GetTH1F("CorrectedJetPt").Fill(event.pfjet(j).ptCor(), prescale)
							histograms.GetTH1F("JetRapidity").Fill(event.pfjet(j).y()), prescale 
							histograms.GetTH1F("Beta").Fill(event.pfjet(j).beta(), prescale)
							#histograms.GetTH1F("pBetaVsNPV").Fill(event.evtHdr().nVtxGood(),event.pfjet(j).beta(), prescale)
					# jet loop
				# hcal noise filter    
			# pv cut
		# hlt
	# tree loop
	#----------------- print out some information ---------------
	print "events after the trigger cut:     " + str(counter_hlt)
	print "events after the PV cut:          " + str(counter_pv)
	print "events after the HCAL filter cut: " + str(counter_hcal)
	print "Number of jets:                   " + str(counter_jet)
	print "Trigger summary:"
	for trigger_name, trigger_index in trigger_map.iteritems():
		print "Trigger " + trigger_name + " = " + str(trigger_counts_raw[trigger_name]) + "(" + str(trigger_counts_prescaled[trigger_name]) + " with prescale)"

	#----------------- save the histos to the output file -------
	f_out.Write()

if __name__ == "__main__":
	ReadTree()

