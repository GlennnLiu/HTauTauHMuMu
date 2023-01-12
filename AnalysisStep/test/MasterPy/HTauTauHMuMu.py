import FWCore.ParameterSet.Config as cms
from HTauTauHMuMu.AnalysisStep.defaults import *
import os, sys

process = cms.Process("ZZ")

### ----------------------------------------------------------------------
### Flags that need to be set
### ----------------------------------------------------------------------

#Set defaults for variables used in this file (in case they are not defined by a caller script)
declareDefault("IsMC", True, globals())

# Set of effective areas, rho corrections, etc. (can be 2011, 2012, 2015 or 2016)
declareDefault("LEPTON_SETUP", 2016, globals())

declareDefault("OLDPATTRIGGER", False, globals())
# Flag that reflects the actual sqrts of the sample (can be 2011, 2012, 2015 or 2016)
# Can differ from SAMPLE_TYPE for samples that are rescaled to a different sqrts.
declareDefault("SAMPLE_TYPE", LEPTON_SETUP, globals())

declareDefault("YEAR", LEPTON_SETUP, globals())

# Control global tag to be used for 2018 data to distinguish between ReReco (period A, B, C) and PromptReco (period D)
declareDefault("DATA_TAG", "ReReco", globals())

#Optional name of the sample/dataset being analyzed
declareDefault("SAMPLENAME", "", globals())

#Apply muon scale correction
declareDefault("APPLYMUCORR", True, globals())

#Reapply JEC
declareDefault("APPLYJEC", True, globals())

#Apply JER
declareDefault("APPLYJER", True, globals())

#Recorrect MET
declareDefault("RECORRECTMET", True, globals())

#FSR mode
declareDefault("FSRMODE", "RunII", globals())

#Bunch spacing (can be 25 or 50)
declareDefault("BUNCH_SPACING", 25, globals())

#Selection flow strategy
declareDefault("SELSETUP", "allCutsAtOncePlusSmart", globals())

#Best candidate comparator (see interface/Comparators.h)
declareDefault("BESTCANDCOMPARATOR", "byBestZ1bestZ2", globals())

# Set to True to make candidates with the full combinatorial of loose leptons (for debug; much slower)
declareDefault("KEEPLOOSECOMB", False, globals())

# Activate the Z kinematic refit (very slow)
declareDefault("KINFITOLD", False, globals())

# ZZ kinematic fit
declareDefault("KINFIT", True, globals())

# Activate paths for loose electron categories
declareDefault("ADDLOOSEELE", False, globals())

# Activate trigger paths in MC; note that for 2016, only reHLT samples have the correct triggers!!!
declareDefault("APPLYTRIG", True, globals())

# CMSSW version 8X or 9X
CMSSW_VERSION = os.environ['CMSSW_VERSION']
CMSSWVERSION = int(CMSSW_VERSION.split("_")[1])

if SELSETUP=="Legacy" and not BESTCANDCOMPARATOR=="byBestZ1bestZ2":
    print "WARNING: In ZZ4lAnalysis.py the SELSETUP=\"Legacy\" flag is meant to reproduce the Legacy results, ignoring the setting of the BESTCANDCOMPARATOR: ",BESTCANDCOMPARATOR
    BESTCANDCOMPARATOR = "byBestZ1bestZ2"

# The isolation cuts for electrons and muons. FIXME: there is an hardcoded instance of these values in src/LeptonIsoHelper.cc !!
ELEISOCUT = 99999. # [FIXME] Remove isolation cuts from the code completely
MUISOCUT  = 0.35 # [FIXME] Remove isolation cuts from the code completely

### ----------------------------------------------------------------------
### Set the GT
### ----------------------------------------------------------------------
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag

if (SAMPLE_TYPE == 2016):
    if IsMC:
	#process.GlobalTag = GlobalTag(process.GlobalTag, '80X_mcRun2_asymptotic_2016_TrancheIV_v8','')
        process.GlobalTag = GlobalTag(process.GlobalTag, '94X_mcRun2_asymptotic_v3', '')
    else:
        process.GlobalTag = GlobalTag(process.GlobalTag, '94X_dataRun2_v10', '')

elif (SAMPLE_TYPE == 2017):
    if IsMC:
        process.GlobalTag = GlobalTag(process.GlobalTag, '94X_mc2017_realistic_v17', '')
    else:
        process.GlobalTag = GlobalTag(process.GlobalTag, '94X_dataRun2_v11', '')

elif (SAMPLE_TYPE == 2018):
    if IsMC:
        process.GlobalTag = GlobalTag(process.GlobalTag, '102X_upgrade2018_realistic_v21', '')
    else:
        if (DATA_TAG == "PromptReco"):
            process.GlobalTag = GlobalTag(process.GlobalTag, '102X_dataRun2_Prompt_v16', '')
        else:
            process.GlobalTag = GlobalTag(process.GlobalTag, '102X_dataRun2_v13', '')

print '\t',process.GlobalTag.globaltag


### ----------------------------------------------------------------------
### Standard stuff
### ----------------------------------------------------------------------
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )


### ----------------------------------------------------------------------
### Source
### ----------------------------------------------------------------------
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
      '/store/cmst3/user/cmgtools/CMG/GluGluToHToZZTo4L_M-130_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM/V5/PAT_CMG_V5_2_0/patTuple_1.root'
    )
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)


### ----------------------------------------------------------------------
### Trigger bit Requests
### ----------------------------------------------------------------------
import HLTrigger.HLTfilters.hltHighLevel_cfi

process.hltFilterDiMu  = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltFilterDiEle = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
#process.hltFilterMuEle = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
#process.hltFilterMuEle2 = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
#process.hltFilterMuEle3 = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
#process.hltFilterTriEle = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
#process.hltFilterTriMu  = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltFilterSingleEle = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltFilterSingleMu  = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()

process.hltFilterDiMu.TriggerResultsTag  = cms.InputTag("TriggerResults","","HLT")
process.hltFilterDiEle.TriggerResultsTag = cms.InputTag("TriggerResults","","HLT")
#process.hltFilterMuEle.TriggerResultsTag = cms.InputTag("TriggerResults","","HLT")
#process.hltFilterMuEle2.TriggerResultsTag = cms.InputTag("TriggerResults","","HLT")
#process.hltFilterMuEle3.TriggerResultsTag = cms.InputTag("TriggerResults","","HLT")
#process.hltFilterTriEle.TriggerResultsTag = cms.InputTag("TriggerResults","","HLT")
#process.hltFilterTriMu.TriggerResultsTag  = cms.InputTag("TriggerResults","","HLT")
process.hltFilterSingleEle.TriggerResultsTag = cms.InputTag("TriggerResults","","HLT")
process.hltFilterSingleMu.TriggerResultsTag = cms.InputTag("TriggerResults","","HLT")

process.hltFilterDiMu.throw  = cms.bool(False) #FIXME: beware of this!
process.hltFilterDiEle.throw = cms.bool(False) #FIXME: beware of this!
#process.hltFilterMuEle.throw = cms.bool(False) #FIXME: beware of this!
#process.hltFilterMuEle2.throw = cms.bool(False) #FIXME: beware of this!
#process.hltFilterMuEle3.throw = cms.bool(False) #FIXME: beware of this!
#process.hltFilterTriEle.throw = cms.bool(False) #FIXME: beware of this!
#process.hltFilterTriMu.throw  = cms.bool(False) #FIXME: beware of this!
process.hltFilterSingleEle.throw = cms.bool(False) #FIXME: beware of this!
process.hltFilterSingleMu.throw  = cms.bool(False) #FIXME: beware of this!

### 2016 triggers - final
if (LEPTON_SETUP == 2016):
   process.hltFilterDiEle.HLTPaths = ["HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*","HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*","HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_v*"]
   process.hltFilterDiMu.HLTPaths = ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v*","HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v*","HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v*","HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v*"]
   #process.hltFilterMuEle.HLTPaths = ["HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v*","HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v*","HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v*","HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*","HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*","HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*","HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_v*","HLT_Mu8_DiEle12_CaloIdL_TrackIdL_v*","HLT_DiMu9_Ele9_CaloIdL_TrackIdL_v*"]
   #process.hltFilterTriEle.HLTPaths = ["HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL_v*"]
   #process.hltFilterTriMu.HLTPaths = ["HLT_TripleMu_12_10_5_v*"]
   process.hltFilterSingleEle.HLTPaths = ["HLT_Ele25_eta2p1_WPTight_Gsf_v*","HLT_Ele27_WPTight_Gsf_v*","HLT_Ele27_eta2p1_WPLoose_Gsf_v*", "HLT_Ele32_eta2p1_WPTight_Gsf_v*"]
   process.hltFilterSingleMu.HLTPaths = ["HLT_IsoMu20_v*","HLT_IsoTkMu20_v*","HLT_IsoMu22_v*","HLT_IsoTkMu22_v*","HLT_IsoMu24_v*","HLT_IsoTkMu24_v*"]

   #process.triggerTriEle = cms.Path(process.hltFilterTriEle)
   #process.triggerTriMu  = cms.Path(process.hltFilterTriMu )
   process.triggerSingleEle = cms.Path(process.hltFilterSingleEle)
   process.triggerSingleMu  = cms.Path(process.hltFilterSingleMu )

### 2017 triggers - final
elif (LEPTON_SETUP == 2017):
   process.hltFilterDiEle.HLTPaths = ["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v*","HLT_DoubleEle33_CaloIdL_MW_v*"]
   process.hltFilterDiMu.HLTPaths = ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v*","HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_v*"]
   #process.hltFilterMuEle.HLTPaths = ["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*","HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v*","HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v*","HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*","HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ_v*","HLT_Mu8_DiEle12_CaloIdL_TrackIdL_v*","HLT_Mu8_DiEle12_CaloIdL_TrackIdL_DZ_v*"]
   #process.hltFilterTriEle.HLTPaths = ["HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL_v*"]
   #process.hltFilterTriMu.HLTPaths = ["HLT_TripleMu_10_5_5_DZ_v*","HLT_TripleMu_12_10_5_v*"]
   process.hltFilterSingleEle.HLTPaths = ["HLT_Ele35_WPTight_Gsf_v*","HLT_Ele38_WPTight_Gsf_v*","HLT_Ele40_WPTight_Gsf_v*"]
   process.hltFilterSingleMu.HLTPaths = ["HLT_IsoMu27_v*"]

   #process.triggerTriEle = cms.Path(process.hltFilterTriEle)
   #process.triggerTriMu  = cms.Path(process.hltFilterTriMu )
   process.triggerSingleEle = cms.Path(process.hltFilterSingleEle)
   process.triggerSingleMu  = cms.Path(process.hltFilterSingleMu )

### 2018 triggers - FIXME: to be updated (26/6/18)
elif (LEPTON_SETUP == 2018):
   process.hltFilterDiEle.HLTPaths = ["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v*","HLT_DoubleEle25_CaloIdL_MW_v*"]
   process.hltFilterDiMu.HLTPaths = ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v*"]
   #process.hltFilterMuEle.HLTPaths = ["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*","HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v*","HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v*","HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*","HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ_v*","HLT_Mu8_DiEle12_CaloIdL_TrackIdL_DZ_v*"]
   #process.hltFilterTriEle.HLTPaths = [""]
   #process.hltFilterTriMu.HLTPaths = ["HLT_TripleMu_10_5_5_DZ_v*","HLT_TripleMu_12_10_5_v*"]
   process.hltFilterSingleEle.HLTPaths = ["HLT_Ele32_WPTight_Gsf_v*"]
   process.hltFilterSingleMu.HLTPaths = ["HLT_IsoMu24_v*"]

   #process.triggerTriEle = cms.Path(process.hltFilterTriEle)
   #process.triggerTriMu  = cms.Path(process.hltFilterTriMu )
   process.triggerSingleEle = cms.Path(process.hltFilterSingleEle)
   process.triggerSingleMu  = cms.Path(process.hltFilterSingleMu )



process.triggerDiMu   = cms.Path(process.hltFilterDiMu)
process.triggerDiEle  = cms.Path(process.hltFilterDiEle)
#process.triggerMuEle  = cms.Path(process.hltFilterMuEle)

if OLDPATTRIGGER:
   TRIGGERSET="selectedPatTrigger"
else:
   TRIGGERSET="slimmedPatTrigger"

### ----------------------------------------------------------------------
### MET FILTERS
### ----------------------------------------------------------------------
#process.METFilters  = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
#process.METFilters.TriggerResultsTag  = cms.InputTag("TriggerResults","","RECO")
#if (IsMC):
#   process.METFilters.TriggerResultsTag  = cms.InputTag("TriggerResults","","PAT")
#
#if (LEPTON_SETUP == 2017):#MET Filters available in miniAOD as described here https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2
#   if (IsMC):
#      process.METFilters.HLTPaths = ["Flag_goodVertices","Flag_globalSuperTightHalo2016Filter","Flag_HBHENoiseFilter","Flag_HBHENoiseIsoFilter","Flag_EcalDeadCellTriggerPrimitiveFilter","Flag_BadPFMuonFilter","Flag_BadChargedCandidateFilter"]
#   else:
#      process.METFilters.HLTPaths = ["Flag_goodVertices","Flag_globalSuperTightHalo2016Filter","Flag_HBHENoiseFilter","Flag_HBHENoiseIsoFilter","Flag_EcalDeadCellTriggerPrimitiveFilter","Flag_BadPFMuonFilter","Flag_BadChargedCandidateFilter","Flag_eeBadScFilter"]
#
#process.triggerMETFilters = cms.Path(process.METFilters)

### ----------------------------------------------------------------------
### MC Filters and tools
### ----------------------------------------------------------------------

process.heavyflavorfilter = cms.EDFilter('HeavyFlavorFilter2',
#                                 src= cms.InputTag("genParticles"), # genParticles available only in PAT
                                 src= cms.InputTag("prunedGenParticles"),
                                 status2 = cms.bool(True),
                                 status3 = cms.bool(False),
                                 hDaughterVeto = cms.bool(False),
                                 zDaughterVeto = cms.bool(True),
                                 ptcut=cms.double(0)
                                 )


process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.drawTree = cms.EDAnalyzer("ParticleTreeDrawer",
                                   src = cms.InputTag("prunedGenParticles"),
                                   printP4 = cms.untracked.bool(False),
                                   printPtEtaPhi = cms.untracked.bool(False),
                                   printVertex = cms.untracked.bool(False),
                                   printStatus = cms.untracked.bool(True),
                                   printIndex = cms.untracked.bool(False) )


process.printTree = cms.EDAnalyzer("ParticleListDrawer",
                                   maxEventsToPrint = cms.untracked.int32(-1),
                                   printVertex = cms.untracked.bool(False),
                                   src = cms.InputTag("prunedGenParticles")
                                   )


process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
                                                   calibratedPatElectrons = cms.PSet(
                                                       initialSeed = cms.untracked.uint32(1),
                                                       engineName = cms.untracked.string('TRandom3')
                                                       ),
                                                   )

# FIXME Add total kinematics filter for MC

process.goodPrimaryVertices = cms.EDFilter("VertexSelector",
  src = cms.InputTag("offlineSlimmedPrimaryVertices"),
  cut = cms.string("!isFake && ndof > 4 && abs(z) <= 24 && position.Rho <= 2"),
  filter = cms.bool(True),
)


### ----------------------------------------------------------------------
### HTXS categorisation
### ----------------------------------------------------------------------
if(IsMC):
   process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
   process.mergedGenParticles = cms.EDProducer("MergedGenParticleProducer",
															  inputPruned = cms.InputTag("prunedGenParticles"),
															  inputPacked = cms.InputTag("packedGenParticles"),
															  )
   process.myGenerator = cms.EDProducer("GenParticles2HepMCConverter",
													 genParticles = cms.InputTag("mergedGenParticles"),
													 genEventInfo = cms.InputTag("generator"),
													 signalParticlePdgIds = cms.vint32(25), ## for the Higgs analysis
													 )
   process.rivetProducerHTXS = cms.EDProducer('HTXSRivetProducer',
															 HepMCCollection = cms.InputTag('myGenerator','unsmeared'),
															 LHERunInfo = cms.InputTag('externalLHEProducer'),
															 ProductionMode = cms.string('AUTO'),
															 )
   process.htxs = cms.Path(process.mergedGenParticles*process.myGenerator*process.rivetProducerHTXS)

### ----------------------------------------------------------------------
### ----------------------------------------------------------------------
### Loose lepton selection + cleaning + embedding of user data
### ----------------------------------------------------------------------
### ----------------------------------------------------------------------

SIP =  "userFloat('SIP') < 4"
#GOODMUON = "(userFloat('ID') || (userFloat('isTrackerHighPtMuon') && pt>200)) && " + SIP //used when MVA is applied
GOODELECTRON = "userFloat('ID') && " + SIP
GOODMUON     = "userFloat('ID') && " + SIP
TIGHTMUON    = "userFloat('isPFMuon') || (userFloat('isTrackerHighPtMuon') && pt>200)"


APPLYTESCORRECTION = True

#------- MUONS -------

#--- Set correct identifier for muon corrections
if LEPTON_SETUP == 2016: # Rochester corrections for 2016 data
      process.calibratedMuons = cms.EDProducer("RochesterPATMuonCorrector",
                                            src = cms.InputTag("slimmedMuons"),
                                            identifier = cms.string("RoccoR2016"),
                                            isMC = cms.bool(IsMC),
                                            isSynchronization = cms.bool(False),
                                            )
elif LEPTON_SETUP == 2017:# Rochester corrections for 2017 data
     process.calibratedMuons = cms.EDProducer("RochesterPATMuonCorrector",
                                         src = cms.InputTag("slimmedMuons"),
                                         identifier = cms.string("RoccoR2017"),
                                         isMC = cms.bool(IsMC),
                                         isSynchronization = cms.bool(False),
                                         )
elif LEPTON_SETUP == 2018:# Rochester corrections for 2018 data
     process.calibratedMuons = cms.EDProducer("RochesterPATMuonCorrector",
                                         src = cms.InputTag("slimmedMuons"),
                                         identifier = cms.string("RoccoR2018"),
                                         isMC = cms.bool(IsMC),
                                         isSynchronization = cms.bool(False),
                                         )

else:
    if APPLYMUCORR:
        print "APPLYMUCORR not configured for LEPTON_SETUP =", LEPTON_SETUP
        sys.exit()

#--- Mu Ghost cleaning
process.cleanedMu = cms.EDProducer("PATMuonCleanerBySegments",
                                   src = cms.InputTag("calibratedMuons"),
                                   preselection = cms.string("track.isNonnull"),
                                   passthrough = cms.string("isGlobalMuon && numberOfMatches >= 2"),
                                   fractionOfSharedSegments = cms.double(0.499))


process.bareSoftMuons = cms.EDFilter("PATMuonRefSelector",
    src = cms.InputTag("cleanedMu"),
    cut = cms.string("pt>5 && abs(eta)<2.4 && (isGlobalMuon || (isTrackerMuon && numberOfMatches>0)) && muonBestTrackType!=2")
#    Lowering pT cuts
#    cut = cms.string("(isGlobalMuon || (isTrackerMuon && numberOfMatches>0)) &&" +
#                     "pt>3 && p>3.5 && abs(eta)<2.4")
)


# MC matching. As the genParticles are no more available in cmg, we re-match with genParticlesPruned.
process.muonMatch = cms.EDProducer("MCMatcher", # cut on deltaR, deltaPt/Pt; pick best by deltaR
                                   src     = cms.InputTag("softMuons"), # RECO objects to match
                                   matched = cms.InputTag("prunedGenParticles"),   # mc-truth particle collection
                                   mcPdgId     = cms.vint32(13), # one or more PDG ID (13 = muon); absolute values (see below)
                                   checkCharge = cms.bool(True), # True = require RECO and MC objects to have the same charge
                                   mcStatus = cms.vint32(1),     # PYTHIA status code (1 = stable, 2 = shower, 3 = hard scattering)
                                   maxDeltaR = cms.double(0.5),  # Minimum deltaR for the match
                                   maxDPtRel = cms.double(0.5),  # Minimum deltaPt/Pt for the match
                                   resolveAmbiguities = cms.bool(True),     # Forbid two RECO objects to match to the same GEN object
                                   resolveByMatchQuality = cms.bool(False), # False = just match input in order; True = pick lowest deltaR pair first
                                   )

process.softMuons = cms.EDProducer("MuFiller",
    src = cms.InputTag("bareSoftMuons"),
    sampleType = cms.int32(SAMPLE_TYPE),
    setup = cms.int32(LEPTON_SETUP), # define the set of effective areas, rho corrections, etc.
    cut = cms.string("userFloat('dxy')<0.5 && userFloat('dz')<1."),
    TriggerResults = cms.InputTag('TriggerResults','','HLT'),
    TriggerSet = cms.InputTag(TRIGGERSET),
    flags = cms.PSet(
        ID = cms.string(TIGHTMUON), #"userFloat('isBDT')"), # muonMVA ID
        isSIP = cms.string(SIP),
        isGood = cms.string(GOODMUON),
        isIsoFSRUncorr  = cms.string("userFloat('combRelIsoPF')<" + str(MUISOCUT)),
#       Note: passCombRelIsoPFFSRCorr is currently set in LeptonPhotonMatcher for new FSR strategy; in ZZCandidateFiller for the old one
    )
)


if APPLYMUCORR :
    process.muons =  cms.Sequence(process.calibratedMuons + process.cleanedMu + process.bareSoftMuons + process.softMuons)
else:
    process.cleanedMu.src = cms.InputTag("slimmedMuons")
    process.muons =  cms.Sequence(process.cleanedMu + process.bareSoftMuons + process.softMuons)




#------- ELECTRONS -------

#--- Run2 electron momentum scale and resolution corrections

process.selectedSlimmedElectrons = cms.EDFilter("PATElectronSelector",
    src = cms.InputTag("slimmedElectrons"),
    cut = cms.string("pt>5 && abs(eta)<2.5")
)

if (LEPTON_SETUP == 2016):
   from RecoEgamma.EgammaTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
   setupEgammaPostRecoSeq(process,
                          runEnergyCorrections=True,
                          runVID=True,
                          eleIDModules=['RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Summer16_ID_ISO_cff','RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV70_cff'],
                          phoIDModules=['RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_Fall17_94X_V2_cff'],
                          era='2016-Legacy')

if (LEPTON_SETUP == 2017):
   from RecoEgamma.EgammaTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
   setupEgammaPostRecoSeq(process,
                          runEnergyCorrections=True,
                          runVID=True,
                          phoIDModules=['RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_Fall17_94X_V2_cff'],
                          era='2017-Nov17ReReco')

if (LEPTON_SETUP == 2018):
   from RecoEgamma.EgammaTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
   setupEgammaPostRecoSeq(process,
                          runEnergyCorrections=True,
                          runVID=True,
                          eleIDModules=['RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Autumn18_ID_ISO_cff','RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV70_cff'],
                             phoIDModules=['RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_Fall17_94X_V2_cff'],
                          era='2018-Prompt')


process.bareSoftElectrons = cms.EDFilter("PATElectronRefSelector",
   src = cms.InputTag("selectedSlimmedElectrons"),
   cut = cms.string("") #move pt>7 && abs(eta)<2.5 cut to softElectrons so that smear/scale corrections are done before the pT cut
   )

process.softElectrons = cms.EDProducer("EleFiller",
   src    = cms.InputTag("bareSoftElectrons"),
   TriggerResults = cms.InputTag('TriggerResults','','HLT'),
   TriggerSet = cms.InputTag(TRIGGERSET),
   sampleType = cms.int32(SAMPLE_TYPE),
   setup = cms.int32(LEPTON_SETUP), # define the set of effective areas, rho corrections, etc.
   cut = cms.string("pt>7 && abs(eta) < 2.5 && userFloat('dxy')<0.5 && userFloat('dz')<1"),
   flags = cms.PSet(
        ID = cms.string("userFloat('isBDT')"),
        isSIP = cms.string(SIP),
        isGood = cms.string(GOODELECTRON),
        isIsoFSRUncorr  = cms.string("userFloat('combRelIsoPF')<"+str(ELEISOCUT))
#       Note: passCombRelIsoPFFSRCorr is currently set in LeptonPhotonMatcher for new FSR strategy; in ZZCandidateFiller for the old one
        ),
   )


process.electrons = cms.Sequence(process.egammaPostRecoSeq + process.selectedSlimmedElectrons + process.bareSoftElectrons + process.softElectrons)



#--- TrackLess Electrons
process.bareSoftPhotons = cms.EDFilter("PATPhotonRefSelector",
   src = cms.InputTag("slimmedPhotons"),
   cut = cms.string("pt>7 && abs(eta)<2.5")
   )

process.softPhotons = cms.EDProducer("Philler",
   src    = cms.InputTag("bareSoftPhotons"),
   srcElectron = cms.InputTag("softElectrons"),
   mvaValuesMap = cms.InputTag("photonMVAValueMapProducer:TLEMVAEstimatorRun2Fall15V1Values"),
   mvaValuesMap2 = cms.InputTag("photonMVAValueMapProducer:PhotonMVAEstimatorRun2Spring15NonTrig25nsV2Values"),
   sampleType = cms.int32(SAMPLE_TYPE),
   setup = cms.int32(LEPTON_SETUP), # define the set of effective areas, rho corrections, etc.
   cut = cms.string("1"), # dxy, dz not applied
   flags = cms.PSet(
        ID = cms.string("userFloat('isBDT')"),
        isSIP = cms.string(SIP),
        isGood = cms.string(GOODELECTRON),
        pass_lepton_ID = cms.string("userFloat('isBDT')"),
        pass_lepton_SIP = cms.string(SIP),
#        isIsoFSRUncorr  = cms.string("userFloat('combRelIsoPF')<"+ELEISOCUT), #TLE isolation is not corrected for FSR gammas.
        ),
   )


process.electronMatch = cms.EDProducer("MCMatcher",       # cut on deltaR, deltaPt/Pt; pick best by deltaR
                                       src         = cms.InputTag("bareSoftElectrons"), # RECO objects to match
                                       matched     = cms.InputTag("prunedGenParticles"), # mc-truth particle collection
                                       mcPdgId     = cms.vint32(11),               # one or more PDG ID (11 = electron); absolute values (see below)
                                       checkCharge = cms.bool(True),               # True = require RECO and MC objects to have the same charge
                                       mcStatus    = cms.vint32(1),                # PYTHIA status code (1 = stable, 2 = shower, 3 = hard scattering)
                                       maxDeltaR   = cms.double(0.5),              # Minimum deltaR for the match
                                       maxDPtRel   = cms.double(0.5),              # Minimum deltaPt/Pt for the match
                                       resolveAmbiguities    = cms.bool(True),     # Forbid two RECO objects to match to the same GEN object
                                       resolveByMatchQuality = cms.bool(False),    # False = just match input in order; True = pick lowest deltaR pair first
                                       )


### ----------------------------------------------------------------------
### Lepton Cleaning (clean electrons collection from muons)
### ----------------------------------------------------------------------

process.cleanSoftElectrons = cms.EDProducer("PATElectronCleaner",
    # pat electron input source
    src = cms.InputTag("softElectrons"),
    # preselection (any string-based cut for pat::Electron)
    preselection = cms.string(''),
    # overlap checking configurables
    checkOverlaps = cms.PSet(
        muons = cms.PSet(
           src       = cms.InputTag("softMuons"), # Start from loose lepton def
           algorithm = cms.string("byDeltaR"),
           preselection        = cms.string("userFloat('isGood')"),
           deltaR              = cms.double(0.05),
           checkRecoComponents = cms.bool(False), # don't check if they share some AOD object ref
           pairCut             = cms.string(""),
           requireNoOverlaps   = cms.bool(True), # overlaps don't cause the electron to be discared
        )
    ),
    # finalCut (any string-based cut for pat::Electron)
    finalCut = cms.string(''),
)


#------- TAU LEPTONS -------

TAUCUT       = "pt>20 & abs(eta)<2.3"#"tauID('byCombinedIsolationDeltaBetaCorrRaw3Hits') < 1000.0 && pt>18"
SOSOTAU      = "decayMode()!=5 && decayMode()!=6 && tauID('decayModeFindingNewDMs') == 1 && userFloat('dz') < 1"
GOODTAU      = SOSOTAU# + " && tauID('byVVVLooseDeepTau2017v2p1VSjet') == 1 && tauID('byVVVLooseDeepTau2017v2p1VSe') == 1 && tauID('byVLooseDeepTau2017v2p1VSmu') == 1"
#GOODTAU_MU   = SOSOTAU# + " && tauID('byTightDeepTau2017v2p1VSmu') == 1 && tauID('byVLooseDeepTau2017v2p1VSe') == 1 && tauID('byMediumDeepTau2017v2p1VSjet') == 1"
#GOODTAU_ELE  = SOSOTAU# + " && tauID('byVLooseDeepTau2017v2p1VSmu') == 1 && tauID('byTightDeepTau2017v2p1VSe') == 1 && tauID('byMediumDeepTau2017v2p1VSjet') == 1"
#GOODTAU_TAU  = SOSOTAU# + " && tauID('byVLooseDeepTau2017v2p1VSmu') == 1 && tauID('byVLooseDeepTau2017v2p1VSe') == 1 && tauID('byMediumDeepTau2017v2p1VSjet') == 1"

GOODTAU_MU   = SOSOTAU + " && tauID('byTightDeepTau2017v2p1VSmu') == 1 && tauID('byVLooseDeepTau2017v2p1VSe') == 1 && tauID('byTightDeepTau2017v2p1VSjet') == 1"
GOODTAU_ELE  = SOSOTAU + " && tauID('byTightDeepTau2017v2p1VSmu') == 1 && tauID('byMediumDeepTau2017v2p1VSe') == 1 && tauID('byMediumDeepTau2017v2p1VSjet') == 1"
GOODTAU_TAU  = SOSOTAU + " && tauID('byTightDeepTau2017v2p1VSmu') == 1 && tauID('byVLooseDeepTau2017v2p1VSe') == 1 && tauID('byTightDeepTau2017v2p1VSjet') == 1"

import RecoTauTag.RecoTau.tools.runTauIdMVA as tauIdConfig

updatedTauName = "slimmedTausNewID" #name of pat::Tau collection with new tau-Ids


tauIdEmbedder = tauIdConfig.TauIDEmbedder(process, cms, debug = True,
                    updatedTauName = updatedTauName,
                    toKeep = ["deepTau2017v2p1", "2017v2"]  #["2017v1", "dR0p32017v2"]
)

tauIdEmbedder.runTauID()

process.bareTaus = cms.EDFilter("PATTauRefSelector",
    src = cms.InputTag("slimmedTausNewID"),
    cut = cms.string(TAUCUT)
    )


##NOT USED FOR NOW, TBD Later
process.cleanTaus = cms.EDProducer("PATTauCleaner",
    src = cms.InputTag("bareTaus"),
    # preselection (any string-based cut on pat::Tau)
    preselection = cms.string(
            'tauID("decayModeFinding") > 0.5 &'
            ' tauID("byLooseCombinedIsolationDeltaBetaCorr3Hits") > 0.5 &'
            ' tauID("againstMuonTight") > 0.5 &'
            ' tauID("againstElectronMedium") > 0.5'
        ),
 
   
   # overlap checking configurables
   checkOverlaps = cms.PSet(
      muons = cms.PSet(
          src       = cms.InputTag("cleanPatMuons"),
          algorithm = cms.string("byDeltaR"),
          preselection        = cms.string(""),
          deltaR              = cms.double(0.3),
          checkRecoComponents = cms.bool(False), # don't check if they share some AOD object ref
          pairCut             = cms.string(""),
          requireNoOverlaps   = cms.bool(False), # overlaps don't cause the electron to be discared
          ),
      electrons = cms.PSet(
          src       = cms.InputTag("cleanPatElectrons"),
          algorithm = cms.string("byDeltaR"),
          preselection        = cms.string(""),
          deltaR              = cms.double(0.3),
          checkRecoComponents = cms.bool(False), # don't check if they share some AOD object ref
          pairCut             = cms.string(""),
          requireNoOverlaps   = cms.bool(False), # overlaps don't cause the electron to be discared
          ),
      ),
        # finalCut (any string-based cut on pat::Tau)
        finalCut = cms.string(' '),
)


APPLYTESCORRECTION = APPLYTESCORRECTION if IsMC else False # always false if data


TESyear = "2016Legacy"

#if PERIOD=='postVFP':
#    TESyear = 'UL2016_postVFP'

if YEAR == 2017:
    TESyear = "2017ReReco"

if YEAR == 2018:
    TESyear = "2018ReReco"


process.softTaus = cms.EDProducer("TauFiller",
   src = cms.InputTag("bareTaus"),
   genCollection = cms.InputTag("prunedGenParticles"),
   vtxCollection = cms.InputTag("goodPrimaryVertices"),
   cut = cms.string(TAUCUT),
   discriminator = cms.string("byIsolationMVA3oldDMwoLTraw"),#TAUDISCRIMINATOR),

   ApplyTESCentralCorr = cms.bool(APPLYTESCORRECTION),
   flags = cms.PSet(
	ID = cms.string(GOODTAU),
        isGood = cms.string(GOODTAU),
	isGood_Mu  = cms.string(GOODTAU_MU),
        isGood_Ele = cms.string(GOODTAU_ELE),
        isGood_Tau = cms.string(GOODTAU_TAU)
        ),

   year = cms.string(TESyear)
   )


process.taus=cms.Sequence(process.rerunMvaIsolationSequence + process.slimmedTausNewID + process.bareTaus + process.softTaus)


### ----------------------------------------------------------------------
### L1 Prefiring issue for 2016 and 2017 data
### ----------------------------------------------------------------------

# Recipe taken from https://twiki.cern.ch/twiki/bin/viewauth/CMS/L1ECALPrefiringWeightRecipe#Recipe_details_10_2_X_X_10_or_9

if(IsMC and LEPTON_SETUP == 2016):
   from PhysicsTools.PatUtils.l1ECALPrefiringWeightProducer_cfi import l1ECALPrefiringWeightProducer
   process.prefiringweight = l1ECALPrefiringWeightProducer.clone(
                                                                 DataEra = cms.string("2016BtoH"),
                                                                 UseJetEMPt = cms.bool(False),
                                                                 PrefiringRateSystematicUncty = cms.double(0.2),
                                                                 SkipWarnings = False)

if(IsMC and LEPTON_SETUP == 2017):
   from PhysicsTools.PatUtils.l1ECALPrefiringWeightProducer_cfi import l1ECALPrefiringWeightProducer
   process.prefiringweight = l1ECALPrefiringWeightProducer.clone(
                                                                 DataEra = cms.string("2017BtoF"),
                                                                 UseJetEMPt = cms.bool(False),
                                                                 PrefiringRateSystematicUncty = cms.double(0.2),
                                                                 SkipWarnings = False)

if(IsMC and (LEPTON_SETUP == 2016 or LEPTON_SETUP == 2017)):
   process.Prefiring = cms.Path(process.prefiringweight)


### ----------------------------------------------------------------------
### Search for FSR candidates
### ----------------------------------------------------------------------

# Create a photon collection; cfg extracted from "UFHHTauTauHMuMuRun2.FSRPhotons.fsrPhotons_cff"
process.fsrPhotons = cms.EDProducer("PhotonFiller",
    electronSrc = cms.InputTag("cleanSoftElectrons"),
    sampleType = cms.int32(SAMPLE_TYPE),
    setup = cms.int32(LEPTON_SETUP), # define the set of effective areas, rho corrections, etc.
    photonSel = cms.string(FSRMODE)  # "skip", "passThrough", "Legacy", "RunII"
)

import PhysicsTools.PatAlgos.producersLayer1.pfParticleProducer_cfi
process.boostedFsrPhotons = PhysicsTools.PatAlgos.producersLayer1.pfParticleProducer_cfi.patPFParticles.clone(
    pfCandidateSource = 'fsrPhotons'
)

process.appendPhotons = cms.EDProducer("LeptonPhotonMatcher",
    muonSrc = cms.InputTag("softMuons"),
    electronSrc = cms.InputTag("cleanSoftElectrons"),
    photonSrc = cms.InputTag("boostedFsrPhotons"),
    sampleType = cms.int32(SAMPLE_TYPE),
    setup = cms.int32(LEPTON_SETUP), # define the set of effective areas, rho corrections, etc.
    photonSel = cms.string(FSRMODE),  # "skip", "passThrough", "Legacy", "RunII"
    muon_iso_cut = cms.double(MUISOCUT),
    electron_iso_cut = cms.double(ELEISOCUT),
    debug = cms.untracked.bool(False),
    )

if ADDLOOSEELE:
    process.appendPhotons.looseElectronSrc = cms.InputTag("cleanSoftLooseElectrons")
#    process.appendPhotons.tleSrc = cms.InputTag("softPhotons")
#    process.appendPhotons.TLEMinPt = cms.double(25.)

# All leptons, any F/C.
# CAVEAT: merging creates copies of the objects, so that CandViewShallowCloneCombiner is not able to find
# overlaps between merged collections and the original ones.
process.softLeptons = cms.EDProducer("CandViewMerger",
#    src = cms.VInputTag(cms.InputTag("softMuons"), cms.InputTag("cleanSoftElectrons"))
    src = cms.VInputTag(cms.InputTag("appendPhotons:muons"), cms.InputTag("appendPhotons:electrons"), cms.InputTag("softTaus"))
)



### ----------------------------------------------------------------------
### ----------------------------------------------------------------------
### BUILD CANDIDATES
### ----------------------------------------------------------------------
### ----------------------------------------------------------------------



### ----------------------------------------------------------------------
### Dileptons: combine/merge leptons into intermediate (bare) collections;
###            Embed additional user variables into final collections
### ----------------------------------------------------------------------
TWOGOODLEPTONS = "( userFloat('d0.isGood') && userFloat('d1.isGood'))"# && userFloat('isGoodTau') )" # Z made of 2 good leptons (ISO not yet applied)
TWOISOLEPTONS = "( userFloat('d0.passCombRelIsoPFFSRCorr') && userFloat('d1.passCombRelIsoPFFSRCorr') )"
TWOSFLEPTONS = "( ( abs(daughter(0).pdgId())!=15 && abs(daughter(1).pdgId())!=15 && abs(daughter(0).pdgId())==abs(daughter(1).pdgId()) ) || abs(daughter(0).pdgId())==15 || abs(daughter(1).pdgId())==15 )"
### NOTE: Isolation cut has been moved to ZZ candidates as we now correct for FSR of all four photons.
### Because if this, isBestZ flags are no longer correct; BESTZ_AMONG is set to "" for safety

# Cut to filter out unneeded ll combinations as upstream as possible
if KEEPLOOSECOMB:
    KEEPLOOSECOMB_CUT = 'mass > 0 && ' + TWOSFLEPTONS # Propagate also combinations of loose leptons (for debugging); just require same-flavour
else:
    if FSRMODE == "RunII" : # Just keep combinations of tight leptons (passing ID, SIP and ISO)
        KEEPLOOSECOMB_CUT = "mass > 0 && " + TWOSFLEPTONS + " && daughter(0).masterClone.userFloat('isGood') && daughter(1).masterClone.userFloat('isGood') && daughter(0).masterClone.userFloat('passCombRelIsoPFFSRCorr') &&  daughter(1).masterClone.userFloat('passCombRelIsoPFFSRCorr')"
    else :
        print "KEEPLOOSECOMB == False && FSRMODE =! RunII", FSRMODE, "is no longer supported"
        sys.exit()

### ----------------------------------------------------------------------
### Dileptons (Z->ee, Z->mm, Z->etau, Z->mutau, Z->tautau)
### ----------------------------------------------------------------------

# l+l- (SFOS, e and mu and tau)
process.bareZCand = cms.EDProducer("PATCandViewShallowCloneCombiner",
    decay = cms.string('softLeptons@+ softLeptons@-'),
    cut = cms.string(KEEPLOOSECOMB_CUT), # see below
    checkCharge = cms.bool(True)
)


#----------------- MET, also used for SVFit -------------------------

process.METSequence = cms.Sequence()

PFMetName = "slimmedMETs"
uncorrPFMetTag = cms.InputTag(PFMetName)

if YEAR == 2016:
    from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
    runMetCorAndUncFromMiniAOD(
            process,
            isData = (not IsMC)
    )

    process.METSequence += process.fullPatMetSequence
    PFMetName = "slimmedMETs"
    uncorrPFMetTag = cms.InputTag(PFMetName, "", "ZZ")

    #if not IsMC:
    #    process.patJetsReapplyJEC.userData.userFloats.src += ['pileupJetIdUpdated:fullDiscriminant']
    #    process.patJetsReapplyJEC.userData.userInts.src += ['pileupJetIdUpdated:fullId']

if YEAR == 2017:
    from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
    runMetCorAndUncFromMiniAOD(
            process,
            isData = (not IsMC),
            fixEE2017 = True,
            fixEE2017Params = {'userawPt': True, 'ptThreshold':50.0, 'minEtaThreshold':2.65, 'maxEtaThreshold': 3.139} ,
            postfix = "ModifiedMET"
    )

        # if running in schedule mode add this to your path
    process.METSequence += process.fullPatMetSequenceModifiedMET
    PFMetName = "slimmedMETsModifiedMET"
    uncorrPFMetTag = cms.InputTag(PFMetName, "", "ZZ")

    #process.patJetsReapplyJEC.userData.userFloats.src += ['pileupJetIdUpdated:fullDiscriminant']
    #process.patJetsReapplyJEC.userData.userInts.src += ['pileupJetIdUpdated:fullId']

if YEAR == 2018:
    from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
    runMetCorAndUncFromMiniAOD(process,
                               isData=(not IsMC),
                               )
    PFMetName = "slimmedMETs"
    uncorrPFMetTag = cms.InputTag(PFMetName, "", "ZZ")

    #process.patJetsReapplyJEC.userData.userFloats.src += ['pileupJetIdUpdated:fullDiscriminant']
    #process.patJetsReapplyJEC.userData.userInts.src += ['pileupJetIdUpdated:fullId']

    # Shift met due to central corrections of TES, EES, JER and JES
process.ShiftMETcentral = cms.EDProducer ("ShiftMETcentral",
					srcMET = uncorrPFMetTag,
					tauUncorrected = cms.InputTag("bareTaus"),
					tauCorrected = cms.InputTag("softTaus"),
                    jetCollection = cms.InputTag("dressedJets")
					)

srcMETTag = None
srcMETTag = cms.InputTag("ShiftMETcentral")

process.METSignificance = cms.EDProducer ("ExtractMETSignificance", 
					srcMET=uncorrPFMetTag 
					)

    # add variables with MET shifted for TES corrections
process.ShiftMETforTES = cms.EDProducer ("ShiftMETforTES", 
					srcMET  = srcMETTag, 
					tauCollection = cms.InputTag("softTaus")
					)

    # add variables with MET shifted for EES corrections (E->tau ES)
process.ShiftMETforEES = cms.EDProducer ("ShiftMETforEES",
					srcMET  = srcMETTag,
					tauCollection = cms.InputTag("softTaus")
					)

    # add variables with MET shifted for MES corrections (Mu->tau ES)
process.ShiftMETforMES = cms.EDProducer ("ShiftMETforMES",
					srcMET  = srcMETTag,
					tauCollection = cms.InputTag("softTaus")
					)

    # add variables with MET shifted for JES corrections
process.ShiftMETforJES = cms.EDProducer ("ShiftMETforJES", 
					srcMET  = srcMETTag, 
					jetCollection = cms.InputTag("dressedJets")
					)

    # add variables with MET shifted for EES corrections (E->tau ES)
process.ShiftMETforJER = cms.EDProducer ("ShiftMETforJER",
					srcMET  = srcMETTag,
					jetCollection = cms.InputTag("dressedJets")
					)

    # Get a standalone Puppi MET significance collection
#process.PuppiMETSignificance = cms.EDProducer ("ExtractMETSignificance",
#					srcMET=cms.InputTag("slimmedMETsPuppi")
#					)

    # Shift PUPPI met due to central corrections of TES and EES
#process.ShiftPuppiMETcentral = cms.EDProducer ("ShiftMETcentral",
#					srcMET = cms.InputTag("slimmedMETsPuppi"),
#					tauUncorrected = cms.InputTag("bareTaus"),
#					tauCorrected = cms.InputTag("softTaus")
#					)

process.METSequence += process.METSignificance
process.METSequence += process.ShiftMETcentral
process.METSequence += process.ShiftMETforTES
process.METSequence += process.ShiftMETforEES
process.METSequence += process.ShiftMETforMES
process.METSequence += process.ShiftMETforJES
process.METSequence += process.ShiftMETforJER
#process.METSequence += process.PuppiMETSignificance
#process.METSequence += process.ShiftPuppiMETcentral
metTag=uncorrPFMetTag

process.load('RecoMET.METFilters.ecalBadCalibFilter_cfi')

# In 2017 and 2018 some problematic crystals --> pass list of crystals
if YEAR == 2017 or YEAR == 2018:
    baddetEcallist = cms.vuint32(
            [872439604,872422825,872420274,872423218,
            872423215,872416066,872435036,872439336,
            872420273,872436907,872420147,872439731,
            872436657,872420397,872439732,872439339,
            872439603,872422436,872439861,872437051,
            872437052,872420649,872422436,872421950,
            872437185,872422564,872421566,872421695,
            872421955,872421567,872437184,872421951,
            872421694,872437056,872437057,872437313])

# In 2016 no problem --> pass empty list
if YEAR == 2016:
    baddetEcallist = cms.vuint32([])

process.ecalBadCalibReducedMINIAODFilter = cms.EDFilter(
        "EcalBadCalibFilter",
        EcalRecHitSource = cms.InputTag("reducedEgamma:reducedEERecHits"),
        ecalMinEt        = cms.double(50.),
        baddetEcal    = baddetEcallist,
        taggingMode = cms.bool(True),
        debug = cms.bool(False)
    )





ZLEPTONSEL     = TWOGOODLEPTONS # Note: this is without ISO

Z1PRESEL    = (ZLEPTONSEL + " && mass >= 81.1876 && mass <= 101.1876") # Note: this is without ISO

FLAVOUR	    = "((daughter(0).pdgId()*daughter(1).pdgId()==-121 && userFloat('eleHLTMatch')) ||  (daughter(0).pdgId()*daughter(1).pdgId()==-169 && userFloat('muHLTMatch')))"

BESTZ_AMONG = ( Z1PRESEL + "&&" + TWOISOLEPTONS + "&&" + FLAVOUR)

TWOGOODISOLEPTONS = ( TWOGOODLEPTONS + "&&" + TWOISOLEPTONS )


process.ZCand = cms.EDProducer("ZCandidateFiller",
    src	       = cms.InputTag("bareZCand"),
                               
    TriggerResults = cms.InputTag('TriggerResults','','HLT'),
    TriggerSet = cms.InputTag(TRIGGERSET),
                               
    sampleType = cms.int32(SAMPLE_TYPE),
    setup = cms.int32(LEPTON_SETUP), # define the set of effective areas, rho corrections, etc.
    bestZAmong = cms.string(BESTZ_AMONG),
    FSRMode = cms.string(FSRMODE), # "skip", "Legacy", "RunII"
    flags = cms.PSet(
        GoodLeptons = cms.string(ZLEPTONSEL),
        GoodIsoLeptons = cms.string(TWOGOODISOLEPTONS),
        Z1Presel = cms.string(Z1PRESEL),
    )
)


# ll, same flavour/any charge, for control regions only
process.bareLLCand = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string('softLeptons softLeptons'),
    #cut = cms.string('deltaR(daughter(0).eta, daughter(0).phi, daughter(1).eta, daughter(1).phi)>0.02'), # protect against ghosts
    cut = cms.string("deltaR(daughter(0).eta, daughter(0).phi, daughter(1).eta, daughter(1).phi)>0.02 && " + TWOSFLEPTONS), # protect against ghosts && same flavour
    checkCharge = cms.bool(False)
)

#process.SVLLCand = cms.EDProducer("ClassicSVfitInterface",
#                                  srcPairs   = cms.InputTag("bareLLCand"),
#                                  srcSig     = cms.InputTag("METSignificance", "METSignificance"),
#                                  srcCov     = cms.InputTag("METSignificance", "METCovariance"),
#                                  usePairMET = cms.bool(False),
#                                  srcMET     = srcMETTag,
#                                  computeForUpDownTES = cms.bool(True if IsMC else False),
#                                  computeForUpDownMET = cms.bool(True if IsMC else False),
#                                  METdxUP    = cms.InputTag("ShiftMETforTES", "METdxUP"),
#                                  METdyUP    = cms.InputTag("ShiftMETforTES", "METdyUP"),
#                                  METdxDOWN  = cms.InputTag("ShiftMETforTES", "METdxDOWN"),
#                                  METdyDOWN  = cms.InputTag("ShiftMETforTES", "METdyDOWN"),
#                                  METdxUP_EES   = cms.InputTag("ShiftMETforEES", "METdxUPEES"),
#                                  METdyUP_EES   = cms.InputTag("ShiftMETforEES", "METdyUPEES"),
#                                  METdxDOWN_EES = cms.InputTag("ShiftMETforEES", "METdxDOWNEES"),
#                                  METdyDOWN_EES = cms.InputTag("ShiftMETforEES", "METdyDOWNEES")
#)


process.LLCand = cms.EDProducer("ZCandidateFiller",
    src = cms.InputTag("bareLLCand"),
    sampleType = cms.int32(SAMPLE_TYPE),
    setup = cms.int32(LEPTON_SETUP), # define the set of effective areas, rho corrections, etc.
    bestZAmong = cms.string(BESTZ_AMONG),
    FSRMode = cms.string(FSRMODE), # "skip", "Legacy", "RunII"

    TriggerResults = cms.InputTag('TriggerResults','','HLT'),
    TriggerSet = cms.InputTag(TRIGGERSET),

    flags = cms.PSet(
        GoodLeptons = cms.string(ZLEPTONSEL),
        Z1Presel = cms.string(Z1PRESEL),
    )
)


### ----------------------------------------------------------------------
### TriLeptons (for fake rate)
### ----------------------------------------------------------------------
Z_PLUS_LEP_MIJ=("sqrt(pow(daughter(0).daughter({0}).energy+daughter(1).energy, 2) - " +
                "     pow(daughter(0).daughter({0}).px    +daughter(1).px, 2) -" +
                "     pow(daughter(0).daughter({0}).py    +daughter(1).py, 2) -" +
                "     pow(daughter(0).daughter({0}).pz    +daughter(1).pz, 2))")

process.ZlCand = cms.EDProducer("PATCandViewShallowCloneCombiner",
    decay = cms.string('ZCand softLeptons'),
    cut = cms.string("deltaR(daughter(0).daughter(0).eta, daughter(0).daughter(0).phi, daughter(1).eta, daughter(1).phi)>0.02 &&" + # Ghost suppression
                     "deltaR(daughter(0).daughter(1).eta, daughter(0).daughter(1).phi, daughter(1).eta, daughter(1).phi)>0.02 &&" +
                     ("(daughter(0).daughter(0).charge == daughter(1).charge || %s > 4) && " % ( Z_PLUS_LEP_MIJ.format(0))) +       # mLL>4 for the OS pair (Giovanni's impl)
                     ("(daughter(0).daughter(1).charge == daughter(1).charge || %s > 4) && " % ( Z_PLUS_LEP_MIJ.format(1))) +
                     "daughter(0).masterClone.userFloat('isBestZ') &&" + # This includes the Z1 isolation requirement
                     "daughter(0).masterClone.userFloat('Z1Presel')"
                     ),
    checkCharge = cms.bool(False)
)


### ----------------------------------------------------------------------
### Quadrileptons: combine/merge leptons into intermediate (bare) collections;
###                Embed additional user variables into final collections
### ----------------------------------------------------------------------

FOURGOODLEPTONS    =  ("( userFloat('d0.GoodLeptons') && userFloat('d1.GoodLeptons')" +
		       "&& userFloat('d0.isGoodTau') && userFloat('d1.isGoodTau')" +
                       "&& userFloat('d0.worstEleIso') <" + str(ELEISOCUT) +
                       "&& userFloat('d1.worstEleIso') <" + str(ELEISOCUT) +
                       "&& userFloat('d0.worstMuIso') <" + str(MUISOCUT) +
                       "&& userFloat('d1.worstMuIso') <" + str(MUISOCUT) + ")"
                       ) #ZZ made of 4 tight leptons passing SIP and ISO 

Z1MASS            = "( daughter('Z1').mass()>4 && daughter('Z1').mass()<200 )"
Z2MASS            = "( daughter('Z2').mass()>4 && daughter('Z2').mass()<140 )" # (was > 4 in Synch) to deal with m12 cut at gen level
#MLL3On4_12        = "userFloat('mZa')>12" # mll>12 on 3/4 pairs;
#MLLALLCOMB        = "userFloat('mLL6')>4" # mll>4 on 6/6 AF/AS pairs;
MLLALLCOMB        = "userFloat('mLL4')>4" # mll>4 on 4/4 AF/OS pairs;
SMARTMALLCOMB     = "userFloat('passSmartMLL')" # Require swapped-lepton Z2' to be >12 IF Z1' is SF/OS and closer to 91.1876 than mZ1
PT20_10           = "( userFloat('pt1')>20 && userFloat('pt2')>10 )" #20/10 on any of the 4 leptons
M4l100            = "mass>100"
OSSF		  = "( daughter('Z1').masterClone.userFloat('OSSF') && daughter('Z2').masterClone.userFloat('OSSF') )"
HLTMATCH	  = "( (daughter('Z1').daughter(0).pdgId()*daughter('Z1').daughter(1).pdgId()==-169 && daughter('Z1').masterClone().userFloat('muHLTMatch')) || (daughter('Z1').daughter(0).pdgId()*daughter('Z1').daughter(1).pdgId()==-121 && daughter('Z1').masterClone().userFloat('eleHLTMatch')) )"
BESTZ1		  = "daughter('Z1').masterClone().userFloat('isBestZ')"


if SELSETUP=="Legacy": # Default Configuration (Legacy paper): cut on selected best candidate
    print "SELSETUP=Legacy no longer supported after 8fb591a because we now set combRelIsoPFFSRCorr at the level of ZZ; will need to re-introduce it at  the Z level so that ZZCand.bestZAmong (ie isBestZ flag) works again as before"
    sys.exit()
    HASBESTZ          = "daughter('Z1').masterClone.userFloat('isBestZ')"
    BESTCAND_AMONG = (FOURGOODLEPTONS + "&&" +
                      HASBESTZ        + "&&" +
                      Z1MASS
                      )

    SR           = (FOURGOODLEPTONS + "&&" +
                           HASBESTZ        + "&&" +
                           Z1MASS          + "&&" +
                           Z2MASS          + "&&" +
                           MLLALLCOMB      + "&&" +
                           PT20_10         + "&&" +
                           "mass>70"        + "&&" +
                           "daughter('Z2').mass>12")


elif SELSETUP=="allCutsAtOnce": # Select best candidate among those passing all cuts

    BESTCAND_AMONG = (FOURGOODLEPTONS + "&&" +
                      Z1MASS          + "&&" +
                      Z2MASS          + "&&" +
                      MLLALLCOMB      + "&&" +
                      PT20_10         + "&&" +
                      "mass>70"       + "&&" +
                      "daughter('Z2').mass>12"
                      )

    SR = BESTCAND_AMONG



elif SELSETUP=="allCutsAtOnceButMZ2": # Select best candidate among those passing all cuts except mZ2, leave only mZ2 cut at the end

    BESTCAND_AMONG = (FOURGOODLEPTONS + "&&" +
                      Z1MASS          + "&&" +
                      Z2MASS          + "&&" +
                      MLLALLCOMB      + "&&" +
                      PT20_10         + "&&" +
                      "mass>70"
                      )

    SR           = (BESTCAND_AMONG + "&&" +
                           "daughter('Z2').mass>12")



elif SELSETUP=="allCutsAtOncePlusMZb": # Apply also cut on mZb, -> expected to reduce the background but also signal efficiency

    BESTCAND_AMONG = (FOURGOODLEPTONS + "&&" +
                      Z1MASS          + "&&" +
                      Z2MASS          + "&&" +
                      MLLALLCOMB      + "&&" +
                      PT20_10         + "&&" +
                      "mass>70"       + "&&" +
                      "userFloat('mZb')>12" + "&&" +
                      "daughter('Z2').mass>12"
                      )

    SR = BESTCAND_AMONG

elif SELSETUP=="allCutsAtOncePlusSmart": # Apply smarter mZb cut

    BESTCAND_AMONG = (FOURGOODLEPTONS + "&&" +
                      Z1MASS          + "&&" +
                      Z2MASS          + "&&" +
                      MLLALLCOMB      + "&&" +
                      PT20_10         + "&&" +
		      HLTMATCH	      + "&&" +
		      BESTZ1	      + "&&" +
		      #OSSF	      + "&&" +
                      "mass>70"       + "&&" +
                      SMARTMALLCOMB#   + "&&" +
              #        "daughter('Z2').masterClone.userFloat('goodMass')>12"
                      )

    SR = BESTCAND_AMONG


else:
    print "Please choose one of the following string for SELSETUP: 'Legacy', 'allCutsAtOnceButMZ2', 'allCutsAtOnce', 'allCutsAtOncePlusMZb', 'allCutsAtOncePlusSmart'"
    sys.exit()


FULLSEL            = (SR      + "&&" +
                      M4l100)


# Ghost Suppression cut
NOGHOST4l = ("deltaR(daughter(0).daughter(0).eta, daughter(0).daughter(0).phi, daughter(1).daughter(0).eta, daughter(1).daughter(0).phi)>0.02 &&"+
             "deltaR(daughter(0).daughter(0).eta, daughter(0).daughter(0).phi, daughter(1).daughter(1).eta, daughter(1).daughter(1).phi)>0.02 &&"+
             "deltaR(daughter(0).daughter(1).eta, daughter(0).daughter(1).phi, daughter(1).daughter(0).eta, daughter(1).daughter(0).phi)>0.02 &&"+
             "deltaR(daughter(0).daughter(1).eta, daughter(0).daughter(1).phi, daughter(1).daughter(1).eta, daughter(1).daughter(1).phi)>0.02") # protect against ghosts


# Preselection of 4l candidates
LLLLPRESEL = NOGHOST4l # Just suppress candidates with overlapping leptons

#LLLLPRESEL = (NOGHOST4l + "&&" +
#              FOURGOODLEPTONS) # Only retain candidates with 4 tight leptons (ID, iso, SIP)


# ZZ Candidates
if FSRMODE == "Legacy":
    print "\nERROR: FSRMODE=Legacy is no longer supported. Aborting...\n"
    exit(1)


process.bareZZCand= cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string('ZCand ZCand'),
    cut = cms.string(LLLLPRESEL),
    #checkOverlap = cms.bool(False),
    checkCharge = cms.bool(True)
)
process.ZZCand = cms.EDProducer("ZZCandidateFiller",
    src = cms.InputTag("bareZZCand"),
    srcMET     = srcMETTag,
    srcCov     = cms.InputTag("METSignificance", "METCovariance"),
    sampleType = cms.int32(SAMPLE_TYPE),
    setup = cms.int32(LEPTON_SETUP),
    #superMelaMass = cms.double(SUPERMELA_MASS),
    isMC = cms.bool(IsMC),
    bestCandAmong = cms.PSet(isBestCand = cms.string(BESTCAND_AMONG)),
    bestCandComparator = cms.string(BESTCANDCOMPARATOR),
    ZRolesByMass = cms.bool(True),
    doKinFitOld = cms.bool(KINFITOLD),
    debug = cms.bool(False),
    flags = cms.PSet(
        GoodLeptons =  cms.string(FOURGOODLEPTONS),
        Z2Mass  = cms.string(Z2MASS),
        MAllComb = cms.string(MLLALLCOMB),
        SR = cms.string(SR),
        FullSel70 = cms.string(SR), #Obsolete, use "SR"
        FullSel = cms.string(FULLSEL),
    ),
    recoProbabilities = cms.vstring(),
    #These are actually no longer needed after we dropped the Legacy FSR algorithm
    muon_iso_cut = cms.double(MUISOCUT),
    electron_iso_cut = cms.double(ELEISOCUT),
)



### ----------------------------------------------------------------------
### Z+LL Control regions.
### By constryction, daughter(0) is the Z, daughter(1) the LL pair.
### By setting ZRolesByMass = False, daugther('Z1') is set as daughter(0),
### so we can use the same cuts as for the SR.
### ----------------------------------------------------------------------

Z2MM = "abs(daughter(1).daughter(0).pdgId()*daughter(1).daughter(1).pdgId())==169" 		#Z2 = mumu
Z2EE = "abs(daughter(1).daughter(0).pdgId()*daughter(1).daughter(1).pdgId())==121" 		#Z2 = ee
Z2TT = "(abs(daughter(1).daughter(0).pdgId())==15 || abs(daughter(1).daughter(1).pdgId())==15)" #Z2 = tautau
Z2LL = "(" + Z2MM + "||" + Z2EE + "||" + Z2TT + ")"						#Z2 = mumu, ee, tautau
Z2LL_SS = Z2LL + " && daughter(1).daughter(0).pdgId()*daughter(1).daughter(1).pdgId()>0"	#Z2 = same-sign
Z2LL_OS = Z2LL + " && daughter(1).daughter(0).pdgId()*daughter(1).daughter(1).pdgId()<0"   	#Z2 = l+l-
Z2MM_OS = "daughter(1).daughter(0).pdgId()*daughter(1).daughter(1).pdgId()==-169" 		#Z2 = mu+mu-
Z2MM_SS = "daughter(1).daughter(0).pdgId()*daughter(1).daughter(1).pdgId()== 169" 		#Z2 = mu-mu-/mu+mu+
Z2EE_OS = "daughter(1).daughter(0).pdgId()*daughter(1).daughter(1).pdgId()==-121" 		#Z2 = e+e-
Z2EE_SS = "daughter(1).daughter(0).pdgId()*daughter(1).daughter(1).pdgId()== 121" 		#Z2 = e-e-/e+e+
Z2TT_OS = Z2TT + "&& daughter(1).daughter(0).pdgId()*daughter(1).daughter(1).pdgId()<0"		#Z2 = etau, mutau, tautau, OS
Z2TT_SS = Z2TT + "&& daughter(1).daughter(0).pdgId()*daughter(1).daughter(1).pdgId()>0"		#Z2 = etau, mutau, tautau, SS
Z2ID    = "userFloat('d1.d0.ID')     && userFloat('d1.d1.ID')"                    		#ID on LL leptons
Z2SIP   = "userFloat('d1.d0.SIP')< 4 && userFloat('d1.d1.SIP')< 4"                		#SIP on LL leptons, probably need to be modified because taus don't have SIP.
CR_Z2MASS = "daughter(1).mass()>4  && daughter(1).mass()<140"	#Mass on LL; cut at 4


# Define cuts for selection of the candidates among which the best one is chosen.
CR_BESTCANDBASE = ("userFloat('d0.Z1Presel') && userFloat('d0.worstEleIso') <" + str(ELEISOCUT) +
                   "&& userFloat('d0.worstMuIso') <" + str(MUISOCUT) ) # To be revised

CR_BESTCANDBASE_AA   = ("userFloat('d0.Z1Presel') && userFloat('d0.worstEleIso') <" + str(ELEISOCUT) +
                        "&& userFloat('d0.worstMuIso') <" + str(MUISOCUT) + "&&" +
                        Z2SIP) # base for AA CR: # Z1 with tight leptons passing SIP and ISO, mass cuts; SIP on Z2


CR_BESTZLLss = ""
if SELSETUP == "Legacy":
    # No longer supported; cf comment for "Legacy" in the SR.
    CR_BESTZLLss = CR_BESTCANDBASE_AA + "&&" + "userFloat('d0.isBestZ') &&"+ Z2LL_SS
elif SELSETUP == "allCutsAtOnceButMZ2":
    CR_BESTZLLss = CR_BESTCANDBASE_AA + "&&" + Z2LL_SS + "&&" +CR_Z2MASS + "&&" + MLLALLCOMB + "&&" + PT20_10 + "&& mass>70"
elif SELSETUP == "allCutsAtOnce":
    CR_BESTZLLss = CR_BESTCANDBASE_AA + "&&" + Z2LL_SS + "&&" +CR_Z2MASS + "&&" + MLLALLCOMB + "&&" + PT20_10 + "&&" + "mass>70" + "&&" + "daughter(1).mass>12"
elif SELSETUP == "allCutsAtOncePlusMZb":
    CR_BESTZLLss = CR_BESTCANDBASE_AA + "&&" + Z2LL_SS + "&&" +CR_Z2MASS + "&&" + MLLALLCOMB + "&&" + PT20_10 + "&&" + "mass>70" + "&&" + "daughter(1).mass>12" + "&&" + "userFloat('mZb')>12"
elif SELSETUP == "allCutsAtOncePlusSmart":
    CR_BESTZLLss = CR_BESTCANDBASE_AA + "&& (" + Z2LL_SS + ") && (" +CR_Z2MASS + ") && (" + MLLALLCOMB + ") && (" + PT20_10 + ") &&" + "mass()>70" + "&&" + "daughter(1).mass()>0" + "&&" + SMARTMALLCOMB + "&&" + HLTMATCH + "&&" + BESTZ1


# Base for the selection cut applied on the best candidate. This almost fully (except for M4l100) overlaps with the cuts defined above, except for startegies where the best candidate is chosen at the beginning (Legacy, allCutsAtOnceButMZ2).
CR_BASESEL = (CR_Z2MASS + "&&" +              # mass cuts on LL
              MLLALLCOMB + "&&" +             # mass cut on all lepton pairs
              PT20_10    + "&&" +             # pT> 20/10 over all 4 l
#              "daughter(1).mass()>12 &&" +      # mZ2 >12
              "mass()>70" )                     # m4l cut

##### CR based on Z+2 opposite sign leptons that pass the loose selection #####

# check weather the 2 leptons from Z2 pass the tight selection
PASSD0 = "(userFloat('d1.d0.isGood') && userFloat('d1.d0.isGoodTau') && userFloat('d1.d0.passCombRelIsoPFFSRCorr'))" # FIXME, passCombRelIsoPFFSRCorr result is hard coded
PASSD1 = "(userFloat('d1.d1.isGood') && userFloat('d1.d1.isGoodTau') && userFloat('d1.d1.passCombRelIsoPFFSRCorr'))" # FIXME, passCombRelIsoPFFSRCorr result is hard coded
# ... and fill some useful variable needed for the CR logic
FAILD0 = "!" + PASSD0
FAILD1 = "!" + PASSD1
BOTHFAIL = FAILD0 + "&&" + FAILD1
BOTHPASS = PASSD0 + "&&" + PASSD1
PASSD0_XOR_PASSD1 = "((" + PASSD0 + "&&" + FAILD1 + ") || (" + PASSD1 + "&&" + FAILD0 + "))"
PASSD0_OR_PASSD1  = "(" + PASSD0 + "||" + PASSD1 + ")"


CR_BESTZLLos = (CR_BESTCANDBASE_AA    + "&&" +
                CR_BASESEL            + "&&" +
                Z2LL_OS               + "&&" +
                SMARTMALLCOMB	      + "&&" +
		HLTMATCH	      + "&&" +
		BESTZ1         )

# CR 3P1F
CR_BESTZLLos_3P1F = (CR_BESTZLLos + "&&" + PASSD0_OR_PASSD1)
CR_ZLLosSEL_3P1F  = (CR_BESTZLLos + "&&" + PASSD0_XOR_PASSD1) # Is the CR_BESTZLLos request redundant?


# CR 2P2F
CR_BESTZLLos_2P2F   = (CR_BESTZLLos)
CR_ZLLosSEL_2P2F    = (CR_BESTZLLos + "&&" + BOTHFAIL)  # Is the CR_BESTZLLos request redundant?

################################################################################

#Prefix for Z2 daughters, to be used in the "cut" string
#D1D0 = "daughter(1).daughter(0).masterClone"
#D1D1 = "daughter(1).daughter(1).masterClone"


# Z (OSSF,both e/mu) + LL (any F/C, with no ID/iso); this is the starting point for control regions
process.bareZLLCand= cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string('ZCand LLCand'),
    cut = cms.string(NOGHOST4l),
#                     "&& !(" + Z2LL_OS + "&&" + D1D0+".userFloat('isGood')&&"+D1D1+".userFloat('isGood')&&"+D1D0+".userFloat('passCombRelIsoPFFSRCorr')&&"+D1D1+".userFloat('passCombRelIsoPFFSRCorr'))"), # Reject OS tight combinations. Note that BOTHFAIL cannot be used here ("d0.d1.xxx" is available only in and after ZZCandidateFiller.
    checkCharge = cms.bool(False)
)
process.ZLLCand = cms.EDProducer("ZZCandidateFiller",
    src = cms.InputTag("bareZLLCand"),
    srcMET     = srcMETTag,
    srcCov     = cms.InputTag("METSignificance", "METCovariance"),
    sampleType = cms.int32(SAMPLE_TYPE),
    setup = cms.int32(LEPTON_SETUP),
    #superMelaMass = cms.double(SUPERMELA_MASS),
    isMC = cms.bool(IsMC),
    bestCandComparator = cms.string(BESTCANDCOMPARATOR),
    bestCandAmong = cms.PSet(
      isBestCand    = cms.string("0"), #do not set SR best cand flag
      isBestCRZLLss = cms.string(CR_BESTZLLss),
      isBestCRZLLos_2P2F = cms.string(CR_BESTZLLos_2P2F),
      isBestCRZLLos_3P1F = cms.string(CR_BESTZLLos_3P1F)

    ),
    ZRolesByMass = cms.bool(False),  # daughter('Z1') = daughter(0)
    doKinFitOld = cms.bool(KINFITOLD),
    debug = cms.bool(False),
    flags = cms.PSet(
      SR = cms.string(SR),
      CRZLLss = cms.string(CR_BASESEL),             #combine with proper isBestCRZLLss for AA ss/os CRss
      CRZLLos_2P2F = cms.string(CR_ZLLosSEL_2P2F),
      CRZLLos_3P1F = cms.string(CR_ZLLosSEL_3P1F),
    ),
    recoProbabilities = cms.vstring(),
    #These are actually no longer needed after we dropped the Legacy FSR algorithm
    muon_iso_cut = cms.double(MUISOCUT),
    electron_iso_cut = cms.double(ELEISOCUT),
)


### ----------------------------------------------------------------------
### Jets
### ----------------------------------------------------------------------

# DEFAULT 2016 jet pileup ID training: _chsalgos_81x
# 2017-2018: jet pileup ID trainings to be updated
from RecoJets.JetProducers.PileupJetID_cfi import _chsalgos_94x, _chsalgos_102x
from RecoJets.JetProducers.PileupJetIDCutParams_cfi import full_81x_chs_wp
from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection

process.load("CondCore.CondDB.CondDB_cfi")

# Update jet collection in 2016 MC ntuples to include DeepCSV and DeepFlavour b tag algorithms                                                                                    
# NB: In 2016 Data we do not want to update jet collection to include DeepCSV info (it is already there!)

if (SAMPLE_TYPE == 2016 and IsMC):
    # JEC corrections
    jecLevels = [ 'L1FastJet', 'L2Relative', 'L3Absolute' ]
    
    btagVector = [
        'pfDeepFlavourJetTags:probb',
        'pfDeepFlavourJetTags:probbb',
        'pfDeepFlavourJetTags:problepb',
        'pfDeepFlavourJetTags:probc',
        'pfDeepFlavourJetTags:probuds',
        'pfDeepFlavourJetTags:probg',
        'pfDeepCSVJetTags:probudsg',
        'pfDeepCSVJetTags:probb',
        'pfDeepCSVJetTags:probc',
        'pfDeepCSVJetTags:probbb'
    ]

    updateJetCollection(
        process,
        jetSource = cms.InputTag('slimmedJets'),
        pvSource = cms.InputTag('offlineSlimmedPrimaryVertices'),
        svSource = cms.InputTag('slimmedSecondaryVertices'),
        jetCorrections = ('AK4PFchs', cms.vstring(jecLevels), 'None'),
        btagDiscriminators = btagVector,
        postfix = 'WithDeepInfo'
    )

    process.jetSequence = cms.Sequence(process.patJetCorrFactorsWithDeepInfo 
                                       *process.updatedPatJetsWithDeepInfo 
                                       *process.pfImpactParameterTagInfosWithDeepInfo 
                                       *process.pfInclusiveSecondaryVertexFinderTagInfosWithDeepInfo 
                                       *process.pfDeepCSVTagInfosWithDeepInfo
                                       *process.pfDeepCSVJetTagsWithDeepInfo 
                                       *process.pfDeepFlavourTagInfosWithDeepInfo
                                       *process.pfDeepFlavourJetTagsWithDeepInfo 
                                       *process.patJetCorrFactorsTransientCorrectedWithDeepInfo 
                                       *process.updatedPatJetsTransientCorrectedWithDeepInfo
    )
    
elif (SAMPLE_TYPE == 2017):
    process.load("RecoJets.JetProducers.PileupJetID_cfi")
    process.pileupJetIdUpdated = process.pileupJetId.clone(
        jets=cms.InputTag("slimmedJets"),
        inputIsCorrected=False,
        applyJec=True,
        vertexes=cms.InputTag("offlineSlimmedPrimaryVertices"),
        algos=cms.VPSet(_chsalgos_94x)
    )
elif (SAMPLE_TYPE == 2018):
    process.load("RecoJets.JetProducers.PileupJetID_cfi")
    process.pileupJetIdUpdated = process.pileupJetId.clone(
        jets=cms.InputTag("slimmedJets"),
        inputIsCorrected=False,
        applyJec=True,
        vertexes=cms.InputTag("offlineSlimmedPrimaryVertices"),
        algos=cms.VPSet(_chsalgos_102x)
    )
else:
    process.load("RecoJets.JetProducers.PileupJetID_cfi")
    process.pileupJetIdUpdated = process.pileupJetId.clone(
        jets=cms.InputTag("slimmedJets"),
        inputIsCorrected=False,
        applyJec=True,
        vertexes=cms.InputTag("offlineSlimmedPrimaryVertices"),
    )


theBTagger=""
theBTaggerThr=0
theBTagSFFile=""
theBTagMCEffFile=""
if (LEPTON_SETUP == 2016): #DeepCSV, from https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation2016Legacy
   theBTagger="pfDeepCSVJetTags:probb"
   theBTaggerThr=0.6321
   theBTagSFFile="HTauTauHMuMu/AnalysisStep/data/BTagging/DeepCSV_2016LegacySF_V1.csv"
   theBTagMCEffFile="HTauTauHMuMu/AnalysisStep/data/BTagging/bTagEfficiencies_2016_LegacyPaper.root"
elif (LEPTON_SETUP == 2017): #DeepCSV, from https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
   theBTagger="pfDeepCSVJetTags:probb"
   theBTaggerThr=0.4941
   theBTagSFFile="HTauTauHMuMu/AnalysisStep/data/BTagging/DeepCSV_94XSF_V4_B_F.csv"
   theBTagMCEffFile="HTauTauHMuMu/AnalysisStep/data/BTagging/bTagEfficiencies_2017_LegacyPaper.root"
elif (LEPTON_SETUP == 2018): #DeepCSV, from https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation102X
   theBTagger="pfDeepCSVJetTags:probb"
   theBTaggerThr=0.4184
   theBTagSFFile="HTauTauHMuMu/AnalysisStep/data/BTagging/DeepCSV_102XSF_V1.csv"
   theBTagMCEffFile="HTauTauHMuMu/AnalysisStep/data/BTagging/bTagEfficiencies_2018_LegacyPaper.root" 
else:
   sys.exit("ZZ4lAnalysis.py: Need to define the btagging for the new setup!")


### q/g likelihood
qgDatabaseVersion = 'cmssw8020_v2'
process.QGPoolDBESSource = cms.ESSource("PoolDBESSource",
      DBParameters = cms.PSet(messageLevel = cms.untracked.int32(1)),
      timetype = cms.string('runnumber'),
      toGet = cms.VPSet(
        cms.PSet(
            record = cms.string('QGLikelihoodRcd'),
            tag    = cms.string('QGLikelihoodObject_'+qgDatabaseVersion+'_AK4PFchs'),
            label  = cms.untracked.string('QGL_AK4PFchs')
        ),
      ),
      connect = cms.string('sqlite_fip:HTauTauHMuMu/AnalysisStep/data/QGTagging/QGL_'+qgDatabaseVersion+'.db')
)
process.es_prefer_qg = cms.ESPrefer('PoolDBESSource','QGPoolDBESSource')
process.load('RecoJets.JetProducers.QGTagger_cfi')
process.QGTagger.srcJets = cms.InputTag( 'slimmedJets' )
process.QGTagger.jetsLabel = cms.string('QGL_AK4PFchs')

### DRESSED JETS: b tag applied
process.dressedJets = cms.EDProducer("JetFiller",
    src = cms.InputTag("slimmedJets"),
    sampleType = cms.int32(SAMPLE_TYPE),
    setup = cms.int32(LEPTON_SETUP),
    cut = cms.string(""),#("pt>20 && abs(eta)<4.7 && userFloat('JetID') && (userFloat('PUjetID') || pt>50)"),
    isMC = cms.bool(IsMC),
    bTaggerName = cms.string(theBTagger),
    bTaggerThreshold = cms.double(theBTaggerThr),
    applyJEC = cms.bool(APPLYJEC),
    jecType = cms.string("AK4PFchs"),
    applyJER = cms.bool(APPLYJER),
    jerType = cms.string("AK4PFchs"),
    bTagSFFile = cms.string(theBTagSFFile),
    bTagMCEffFile = cms.string(theBTagMCEffFile),
    flags = cms.PSet()
    )


### Load JEC
#Taken from https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC#Recommended_for_MC

if (APPLYJEC and SAMPLE_TYPE == 2016):
    if IsMC:
        process.jec = cms.ESSource("PoolDBESSource",
            DBParameters = cms.PSet(
                messageLevel = cms.untracked.int32(1)
                ),
            timetype = cms.string('runnumber'),
            toGet = cms.VPSet(
                cms.PSet(
                    record = cms.string('JetCorrectionsRecord'),
                    tag    = cms.string('JetCorrectorParametersCollection_Summer16_07Aug2017_V11_MC_AK4PFchs'),
                    label  = cms.untracked.string('AK4PFchs')
                    ),
                ),
        connect = cms.string('sqlite_fip:HTauTauHMuMu/AnalysisStep/data/JEC/Summer16_07Aug2017_V11_MC.db'),             )
    else:
        process.jec = cms.ESSource("PoolDBESSource",
            DBParameters = cms.PSet(
                messageLevel = cms.untracked.int32(1)
                ),
            timetype = cms.string('runnumber'),
            toGet = cms.VPSet(
                cms.PSet(
                    record = cms.string('JetCorrectionsRecord'),
                    tag    = cms.string('JetCorrectorParametersCollection_Summer16_07Aug2017All_V11_DATA_AK4PFchs'),
                    label  = cms.untracked.string('AK4PFchs')
                    ),
                ),
            connect = cms.string('sqlite_fip:HTauTauHMuMu/AnalysisStep/data/JEC/Summer16_07Aug2017All_V11_DATA.db'),
            )

    ## Add an es_prefer statement to resolve a possible conflict from simultaneous connection to a global tag
    process.es_prefer_jec = cms.ESPrefer('PoolDBESSource','jec')

    ### REAPPLY JEC
    from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import updatedPatJetCorrFactors
    from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import updatedPatJets
    
    if IsMC:
        process.jetCorrFactors = updatedPatJetCorrFactors.clone(
            # JEC applied on jets including also DeepCSV and DeepFlavour tagger
            src = cms.InputTag("updatedPatJetsTransientCorrectedWithDeepInfo"),
            levels = ['L1FastJet','L2Relative','L3Absolute'],
            payload = 'AK4PFchs' )
            
        process.jetsWithJEC = updatedPatJets.clone(
            # JEC applied on jets including also DeepCSV and DeepFlavour tagger
            jetSource = cms.InputTag("updatedPatJetsTransientCorrectedWithDeepInfo"),
            jetCorrFactorsSource = cms.VInputTag(cms.InputTag("jetCorrFactors")),
            # b tag information
            addBTagInfo          = cms.bool(True),  ## master switch
            addDiscriminators    = cms.bool(True)   ## addition of btag discriminators
        )
        
        ### Replace inputs in QGTagger and dressedJets
        process.QGTagger.srcJets = cms.InputTag('jetsWithJEC')
        process.dressedJets.src = cms.InputTag('jetsWithJEC')

    # In 2016 Data we do not want to update jet collection to include DeepCSV info (it is already there!)
    else:    
        process.patJetCorrFactorsReapplyJEC = updatedPatJetCorrFactors.clone(
            src = cms.InputTag("slimmedJets"),
            levels = ['L1FastJet','L2Relative','L3Absolute','L2L3Residual'],
            payload = 'AK4PFchs' )

        process.patJetsReapplyJEC = updatedPatJets.clone(
            jetSource = cms.InputTag("slimmedJets"),
            jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJEC"))
        )

        ### Add pileup id and discriminant to patJetsReapplyJEC
        process.patJetsReapplyJEC.userData.userFloats.src += ['pileupJetIdUpdated:fullDiscriminant']
        process.patJetsReapplyJEC.userData.userInts.src += ['pileupJetIdUpdated:fullId']
        
        ### Replace inputs in QGTagger and dressedJets
        process.QGTagger.srcJets = cms.InputTag( 'patJetsReapplyJEC')
        process.dressedJets.src = cms.InputTag('patJetsReapplyJEC')


if (APPLYJEC and SAMPLE_TYPE == 2017):
    if IsMC:
        process.jec = cms.ESSource("PoolDBESSource",
            DBParameters = cms.PSet(
                messageLevel = cms.untracked.int32(1)
                ),
            timetype = cms.string('runnumber'),
            toGet = cms.VPSet(
                cms.PSet(
                    record = cms.string('JetCorrectionsRecord'),
                    tag    = cms.string('JetCorrectorParametersCollection_Fall17_17Nov2017_V32_94X_MC_AK4PFchs'),
                    label  = cms.untracked.string('AK4PFchs')
                    ),
                ),
              connect = cms.string('sqlite_fip:HTauTauHMuMu/AnalysisStep/data/JEC/Fall17_17Nov2017_V32_94X_MC.db'),
            )
    else:
        process.jec = cms.ESSource("PoolDBESSource",
            DBParameters = cms.PSet(
                messageLevel = cms.untracked.int32(1)
                ),
            timetype = cms.string('runnumber'),
            toGet = cms.VPSet(
                cms.PSet(
                    record = cms.string('JetCorrectionsRecord'),
                    tag    = cms.string('JetCorrectorParametersCollection_Fall17_17Nov2017_V32_94X_DATA_AK4PFchs'),
                    label  = cms.untracked.string('AK4PFchs')
                    ),
                ),
            connect = cms.string('sqlite_fip:HTauTauHMuMu/AnalysisStep/data/JEC/Fall17_17Nov2017_V32_94X_DATA.db'),
            )

    ## Add an es_prefer statement to resolve a possible conflict from simultaneous connection to a global tag
    process.es_prefer_jec = cms.ESPrefer('PoolDBESSource','jec')

    ### REAPPLY JEC
    from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import updatedPatJetCorrFactors
    process.patJetCorrFactorsReapplyJEC = updatedPatJetCorrFactors.clone(
        src = cms.InputTag("slimmedJets"),
        levels = ['L1FastJet','L2Relative','L3Absolute'],
        payload = 'AK4PFchs' )
    if not IsMC:
        process.patJetCorrFactorsReapplyJEC.levels = ['L1FastJet','L2Relative','L3Absolute','L2L3Residual']

    from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import updatedPatJets
    process.patJetsReapplyJEC = updatedPatJets.clone(
        jetSource = cms.InputTag("slimmedJets"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJEC"))
        )

    ### Add pileup id and discriminant to patJetsReapplyJEC
    process.patJetsReapplyJEC.userData.userFloats.src += ['pileupJetIdUpdated:fullDiscriminant']
    process.patJetsReapplyJEC.userData.userInts.src += ['pileupJetIdUpdated:fullId']

    ### Replace inputs in QGTagger and dressedJets
    process.QGTagger.srcJets = cms.InputTag( 'patJetsReapplyJEC')
    process.dressedJets.src = cms.InputTag('patJetsReapplyJEC')


if (APPLYJEC and SAMPLE_TYPE == 2018):
    if IsMC:
        process.jec = cms.ESSource("PoolDBESSource",
            DBParameters = cms.PSet(
                messageLevel = cms.untracked.int32(1)
                ),
            timetype = cms.string('runnumber'),
            toGet = cms.VPSet(
                cms.PSet(
                    record = cms.string('JetCorrectionsRecord'),
                    tag    = cms.string('JetCorrectorParametersCollection_Autumn18_V19_MC_AK4PFchs'), #for 10_2_X MC
                    label  = cms.untracked.string('AK4PFchs')
                    ),
                ),
              connect = cms.string('sqlite_fip:HTauTauHMuMu/AnalysisStep/data/JEC/Autumn18_V19_MC.db'), #for 10_2_X MC
            )
    else: # [FIXME] Preliminary recommendation is to use no JEC for data, change this once it is available
        process.jec = cms.ESSource("PoolDBESSource",
            DBParameters = cms.PSet(
                messageLevel = cms.untracked.int32(1)
                ),
            timetype = cms.string('runnumber'),
            toGet = cms.VPSet(
                cms.PSet(
                    record = cms.string('JetCorrectionsRecord'),
                    tag    = cms.string('JetCorrectorParametersCollection_Autumn18_RunABCD_V19_DATA_AK4PFchs'),
                    label  = cms.untracked.string('AK4PFchs')
                    ),
                ),
            connect = cms.string('sqlite_fip:HTauTauHMuMu/AnalysisStep/data/JEC/Autumn18_RunABCD_V19_DATA.db'),
            )

    ## Add an es_prefer statement to resolve a possible conflict from simultaneous connection to a global tag
    process.es_prefer_jec = cms.ESPrefer('PoolDBESSource','jec')

    ### REAPPLY JEC
    from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import updatedPatJetCorrFactors
    process.patJetCorrFactorsReapplyJEC = updatedPatJetCorrFactors.clone(
        src = cms.InputTag("slimmedJets"),
        levels = ['L1FastJet','L2Relative','L3Absolute'],
        payload = 'AK4PFchs' )
    if not IsMC:
        process.patJetCorrFactorsReapplyJEC.levels = ['L1FastJet','L2Relative','L3Absolute','L2L3Residual']

    from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import updatedPatJets
    process.patJetsReapplyJEC = updatedPatJets.clone(
        jetSource = cms.InputTag("slimmedJets"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJEC"))
        )

    ### Add pileup id and discriminant to patJetsReapplyJEC
    process.patJetsReapplyJEC.userData.userFloats.src += ['pileupJetIdUpdated:fullDiscriminant']
    process.patJetsReapplyJEC.userData.userInts.src += ['pileupJetIdUpdated:fullId']

    ### Replace inputs in QGTagger and dressedJets
    process.QGTagger.srcJets = cms.InputTag( 'patJetsReapplyJEC')
    process.dressedJets.src = cms.InputTag('patJetsReapplyJEC')


# JER from https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution#Smearing_procedures
if (APPLYJER and SAMPLE_TYPE == 2016):
   process.load('Configuration.StandardSequences.Services_cff')
   process.load("JetMETCorrections.Modules.JetResolutionESProducer_cfi")
   from CondCore.DBCommon.CondDBSetup_cfi import *
   process.jer = cms.ESSource("PoolDBESSource",
                                 CondDBSetup,
                                 connect = cms.string('sqlite_fip:HTauTauHMuMu/AnalysisStep/data/JER/Summer16_25nsV1_MC.db'),
                                 toGet = cms.VPSet(
                                                   cms.PSet(
                                                            record = cms.string('JetResolutionRcd'),
                                                            tag    = cms.string('JR_Summer16_25nsV1_MC_PtResolution_AK4PFchs'),
                                                            label  = cms.untracked.string('AK4PFchs_pt')
                                                            ),
                                                   cms.PSet(
                                                            record = cms.string('JetResolutionRcd'),
                                                            tag    = cms.string('JR_Summer16_25nsV1_MC_PhiResolution_AK4PFchs'),
                                                            label  = cms.untracked.string('AK4PFchs_phi')
                                                            ),
                                                   cms.PSet(
                                                            record = cms.string('JetResolutionScaleFactorRcd'),
                                                            tag    = cms.string('JR_Summer16_25nsV1_MC_SF_AK4PFchs'),
                                                            label  = cms.untracked.string('AK4PFchs')
                                                            )
                                                   )
                                 )
   process.es_prefer_jer = cms.ESPrefer('PoolDBESSource', 'jer')

if (APPLYJER and SAMPLE_TYPE == 2017):
   process.load('Configuration.StandardSequences.Services_cff')
   process.load("JetMETCorrections.Modules.JetResolutionESProducer_cfi")
   from CondCore.DBCommon.CondDBSetup_cfi import *
   process.jer = cms.ESSource("PoolDBESSource",
                                 CondDBSetup,
                                 connect = cms.string('sqlite_fip:HTauTauHMuMu/AnalysisStep/data/JER/Fall17_V3_94X_MC.db'),
                                 toGet = cms.VPSet(
                                                   cms.PSet(
                                                            record = cms.string('JetResolutionRcd'),
                                                            tag    = cms.string('JR_Fall17_V3_94X_MC_PtResolution_AK4PFchs'),
                                                            label  = cms.untracked.string('AK4PFchs_pt')
                                                            ),
                                                   cms.PSet(
                                                            record = cms.string('JetResolutionRcd'),
                                                            tag    = cms.string('JR_Fall17_V3_94X_MC_PhiResolution_AK4PFchs'),
                                                            label  = cms.untracked.string('AK4PFchs_phi')
                                                            ),
                                                   cms.PSet(
                                                            record = cms.string('JetResolutionScaleFactorRcd'),
                                                            tag    = cms.string('JR_Fall17_V3_94X_MC_SF_AK4PFchs'),
                                                            label  = cms.untracked.string('AK4PFchs')
                                                            )
                                                   )
                                 )
   process.es_prefer_jer = cms.ESPrefer('PoolDBESSource', 'jer')


if (APPLYJER and SAMPLE_TYPE == 2018):
    process.load('Configuration.StandardSequences.Services_cff')
    process.load("JetMETCorrections.Modules.JetResolutionESProducer_cfi")
    from CondCore.DBCommon.CondDBSetup_cfi import *
    process.jer = cms.ESSource("PoolDBESSource",
                               CondDBSetup,
                               #connect = cms.string('sqlite_fip:HTauTauHMuMu/AnalysisStep/data/JER/Autumn18_V1_MC.db'),
                               connect = cms.string('sqlite_fip:HTauTauHMuMu/AnalysisStep/data/JER/Autumn18_V7_MC.db'),
                               toGet = cms.VPSet(
                                                 cms.PSet(
                                                          record = cms.string('JetResolutionRcd'),
                                                          tag    = cms.string('JR_Autumn18_V7_MC_PtResolution_AK4PFchs'),
                                                          label  = cms.untracked.string('AK4PFchs_pt')
                                                          ),
                                                 cms.PSet(
                                                          record = cms.string('JetResolutionRcd'),
                                                          tag    = cms.string('JR_Autumn18_V7_MC_PhiResolution_AK4PFchs'),
                                                          label  = cms.untracked.string('AK4PFchs_phi')
                                                          ),
                                                 cms.PSet(
                                                          record = cms.string('JetResolutionScaleFactorRcd'),
                                                          tag    = cms.string('JR_Autumn18_V7_MC_SF_AK4PFchs'),
                                                          label  = cms.untracked.string('AK4PFchs')
                                                          )
                                                 )
                               )
    process.es_prefer_jer = cms.ESPrefer('PoolDBESSource', 'jer')

### Clean jets wrt. good (preFSR-)isolated leptons
# process.cleanJets = cms.EDProducer("JetsWithLeptonsRemover",
#                                    Jets      = cms.InputTag("dressedJets"),
#                                    Muons     = cms.InputTag("appendPhotons:muons"),
#                                    Electrons = cms.InputTag("appendPhotons:electrons"),
#                                    Taus	     = cms.InputTag("softTaus"),
#                                    Diboson   = cms.InputTag(""),
#                                    JetPreselection      = cms.string(""),
#                                    MuonPreselection = cms.string("userFloat('isGood') && userFloat('passCombRelIsoPFFSRCorr')"),
#                                    ElectronPreselection = cms.string("userFloat('isGood')"),
#                                    TauPreselection = cms.string("userFloat('isGood')"),
#                                    DiBosonPreselection  = cms.string(""),
#                                    MatchingType = cms.string("byDeltaR"),
#                                    cleanFSRFromLeptons = cms.bool(True),
#                                    DebugPlots = cms.untracked.bool(False),
#                                    DebugPrintOuts = cms.untracked.bool(False)
#                                    )

# if FSRMODE=="Legacy" :
#     process.cleanJets.cleanFSRFromLeptons = False


### ----------------------------------------------------------------------
### Missing ET
### ----------------------------------------------------------------------

#metTag = cms.InputTag("slimmedMETs")

# NB: b tag UPDATE DOES NOT WORK including this part related to MET => Updated info in jets get lost
if (RECORRECTMET and SAMPLE_TYPE == 2016):

#    from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
#    runMetCorAndUncFromMiniAOD(process,
#                               isData=(not IsMC),
#    )
#    metTag = cms.InputTag("slimmedMETs","","ZZ")

    # NB: removed to use properly update jet collection to include DeepCSV in 2016 ntuples
    ### somehow MET recorrection gets this lost again...                          
    if not IsMC:
        process.patJetsReapplyJEC.userData.userFloats.src += ['pileupJetIdUpdated:fullDiscriminant']
        process.patJetsReapplyJEC.userData.userInts.src += ['pileupJetIdUpdated:fullId']

#[FIXME] Does not work in CMSSW_10_3_1 currently                                                                                                                                      
### Recorrect MET, cf. https://indico.cern.ch/event/759372/contributions/3149378/attachments/1721436/2779341/metreport.pdf slide 10                                        
###                and https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETUncertaintyPrescription#Instructions_for_9_4_X_X_9_for_2 
if (RECORRECTMET and SAMPLE_TYPE == 2017):                                                                                                                   
#                                                                                                                                                                          
#    from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD                                                        
#                                                                                                                                                                         
#    runMetCorAndUncFromMiniAOD(process,                                                                                                                              
#                               isData=(not IsMC),                                                                                                                          
#                               fixEE2017 = True,                                                                                                                 
#                               fixEE2017Params = {'userawPt': True, 'ptThreshold':50.0, 'minEtaThreshold':2.65, 'maxEtaThreshold': 3.139} ,                          
#                               postfix = "ModifiedMET"                                                                                                            
#                               )                                                                                                                                            
#    metTag = cms.InputTag("slimmedMETsModifiedMET","","ZZ")                                                                                                                 
#                                                                                                                                                                      
#    ### somehow MET recorrection gets this lost again...                                                                                                                 
    process.patJetsReapplyJEC.userData.userFloats.src += ['pileupJetIdUpdated:fullDiscriminant']                                                                       
    process.patJetsReapplyJEC.userData.userInts.src += ['pileupJetIdUpdated:fullId']                                                                                

#if (RECORRECTMET and SAMPLE_TYPE == 2017):

#    from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
#    runMetCorAndUncFromMiniAOD(process,
#                               isData=(not IsMC),
#                               )
#    metTag = cms.InputTag("slimmedMETs","","ZZ")

    ### somehow MET recorrection gets this lost again...                                                                                          
#    process.patJetsReapplyJEC.userData.userFloats.src += ['pileupJetIdUpdated:fullDiscriminant']
#    process.patJetsReapplyJEC.userData.userInts.src += ['pileupJetIdUpdated:fullId']

if (RECORRECTMET and SAMPLE_TYPE == 2018):

#    from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
#    runMetCorAndUncFromMiniAOD(process,
#                               isData=(not IsMC),
#                               )
#    metTag = cms.InputTag("slimmedMETs","","ZZ")

    ### somehow MET recorrection gets this lost again...                                                                                                             
    process.patJetsReapplyJEC.userData.userFloats.src += ['pileupJetIdUpdated:fullDiscriminant']
    process.patJetsReapplyJEC.userData.userInts.src += ['pileupJetIdUpdated:fullId']



### ----------------------------------------------------------------------
### Paths
### ----------------------------------------------------------------------

process.preSkimCounter = cms.EDProducer("EventCountProducer")
process.PVfilter =  cms.Path(process.preSkimCounter+process.goodPrimaryVertices)

if APPLYJEC:
    if (SAMPLE_TYPE == 2016 and IsMC):
        # Removed pileupJetId update in order to use updateJetCollection
        process.Jets = cms.Path(process.jetSequence + process.jetCorrFactors + process.jetsWithJEC + process.QGTagger + process.dressedJets )
    elif (SAMPLE_TYPE == 2017 or SAMPLE_TYPE == 2018 or (SAMPLE_TYPE == 2016 and (not IsMC)) ):
        process.Jets = cms.Path(process.pileupJetIdUpdated + process.patJetCorrFactorsReapplyJEC + process.patJetsReapplyJEC + process.QGTagger + process.dressedJets )
else:
    process.Jets = cms.Path( process.QGTagger + process.dressedJets )


if (RECORRECTMET and SAMPLE_TYPE == 2016):
    if IsMC:
        process.MET = cms.Path(process.fullPatMetSequence)
    else:
        process.MET = cms.Path(process.fullPatMetSequence)

#[FIXME] Does not work in CMSSW_10_3_1 currently                                                                                                         
#if (RECORRECTMET and SAMPLE_TYPE == 2017):                                                                                                                       
#    if IsMC:                                                                                                                                                   
#        process.MET = cms.Path(process.fullPatMetSequenceModifiedMET)                                                                                              
#    else:                                                                                                                                                                  
#        process.MET = cms.Path(process.fullPatMetSequenceModifiedMET)                                                                                                     

if (RECORRECTMET and SAMPLE_TYPE == 2017):
    if IsMC:
        process.MET = cms.Path(process.fullPatMetSequenceModifiedMET)
    else:
        process.MET = cms.Path(process.fullPatMetSequenceModifiedMET)

if (RECORRECTMET and SAMPLE_TYPE == 2018):
    if IsMC:
        process.MET = cms.Path(process.fullPatMetSequence)
    else:
        process.MET = cms.Path(process.fullPatMetSequence)



### ----------------------------------------------------------------------
### Filters
### ----------------------------------------------------------------------
### Create filter for events with one candidate in the SR
process.ZZCandSR = cms.EDFilter("PATCompositeCandidateRefSelector",
    src = cms.InputTag("ZZCand"),
    cut = cms.string(SR) # That is, all candidates with m4l>70
 )

process.ZZCandFilter = cms.EDFilter("CandViewCountFilter",
                                src = cms.InputTag("ZZCandSR"),
                                minNumber = cms.uint32(1)
                            )

# Prepare lepton collections
process.Candidates = cms.Path(
       process.muons             +
       process.electrons         + process.cleanSoftElectrons +
       process.taus		 +
       process.fsrPhotons        + process.boostedFsrPhotons +
       process.appendPhotons     +
       process.softLeptons       +
       process.dressedJets       +#cleanJets         +
       process.METSequence	 +
# Build 4-lepton candidates
       process.bareZCand	 + process.ZCand	+
       #process.bareZCand         + process.SVZCand	 + process.ZCand     +
       process.bareZZCand        + process.ZZCand
    )

# Optional sequence to build control regions. To get it, add
#process.CRPath = cms.Path(process.CRZl) # only trilepton
#OR
#process.CRPath = cms.Path(process.CR)   # trilep+4lep CRs

process.CRZl = cms.Sequence(
       process.bareZCand	 + process.ZCand	+
       #process.bareZCand         + process.SVZCand       + process.ZCand     +
       process.ZlCand
   )

process.CR = cms.Sequence(
       process.bareZCand	 + process.ZCand	+
       #process.bareZCand         + process.SVZCand       + process.ZCand     +
       process.bareLLCand	 + process.LLCand	+
       #process.bareLLCand        + process.SVLLCand	 + process.LLCand    +
       process.bareZLLCand       + process.ZLLCand   +
       process.ZlCand
   )


### Skim, triggers and MC filters (Only store filter result, no filter is applied)

# 2012 skim, Reimplementation by Giovanni
#process.load("HTauTauHMuMu.AnalysisStep.Skim2012_cfg")
#process.SkimSequence = cms.Sequence(process.HZZSkim2012)
#process.Skim = cms.Path(process.SkimSequence)

#SkimPaths = cms.vstring('Skim')
SkimPaths = cms.vstring('PVfilter') #Do not apply skim, just require a good PV

# process.HF = cms.Path(process.heavyflavorfilter)

# FIXME total kin filter?


if (ADDLOOSEELE) :
    import os
    execfile(os.environ['CMSSW_BASE'] + "/src/HTauTauHMuMu/AnalysisStep/test/MasterPy/LooseEle.py")
#    execfile(os.environ['CMSSW_BASE'] + "/src/HTauTauHMuMu/AnalysisStep/test/MasterPy/TracklessEle.py")
