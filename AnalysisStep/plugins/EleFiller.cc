/** \class EleFiller
 *
 *  No description available.
 *
 *  $Date: 2013/05/24 15:42:42 $
 *  $Revision: 1.28 $
 *  \author N. Amapane (Torino)
 *  \author S. Bolognesi (JHU)
 *  \author C. Botta (CERN)
 *  \author S. Casasso (Torino)
 */

#include <FWCore/Framework/interface/Frameworkfwd.h>
#include <FWCore/Framework/interface/EDProducer.h>
#include <FWCore/Framework/interface/Event.h>
#include <FWCore/ParameterSet/interface/ParameterSet.h>
#include <FWCore/Framework/interface/ESHandle.h>

// #include <DataFormats/Common/interface/TriggerResults.h>
#include "DataFormats/Math/interface/deltaR.h"

#include <HTauTauHMuMu/AnalysisStep/interface/CutSet.h>
#include <HTauTauHMuMu/AnalysisStep/interface/LeptonIsoHelper.h>

#include <vector>
#include <string>
#include "TRandom3.h"

using namespace edm;
using namespace std;
using namespace reco;



class EleFiller : public edm::EDProducer {
 public:
  /// Constructor
  explicit EleFiller(const edm::ParameterSet&);
    
  /// Destructor
  ~EleFiller();

 private:
  virtual void beginJob(){};  
  virtual void produce(edm::Event&, const edm::EventSetup&);
  virtual void endJob(){};

  edm::EDGetTokenT<pat::ElectronRefVector> electronToken;
  edm::EDGetTokenT<pat::ElectronRefVector> electronToken_bis;
    
  // const edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> triggerObjects_;
  // const edm::EDGetTokenT< edm::TriggerResults > triggerResultsToken_;
  int sampleType;
  int setup;
  const StringCutObjectSelector<pat::Electron, true> cut;
  const CutSet<pat::Electron> flags;
  edm::EDGetTokenT<double> rhoToken;
  edm::EDGetTokenT<vector<Vertex> > vtxToken;
  TRandom3 rgen_;

};


EleFiller::EleFiller(const edm::ParameterSet& iConfig) :
  electronToken(consumes<pat::ElectronRefVector>(iConfig.getParameter<edm::InputTag>("src"))),
  // triggerObjects_(consumes<pat::TriggerObjectStandAloneCollection> (iConfig.getParameter<edm::InputTag>("TriggerSet"))),
  // triggerResultsToken_( consumes< edm::TriggerResults >( iConfig.getParameter< edm::InputTag >( "TriggerResultsLabel" ) ) ),
  sampleType(iConfig.getParameter<int>("sampleType")),
  setup(iConfig.getParameter<int>("setup")),
  cut(iConfig.getParameter<std::string>("cut")),
  flags(iConfig.getParameter<ParameterSet>("flags")),
  rgen_(0)
{
  rhoToken = consumes<double>(LeptonIsoHelper::getEleRhoTag(sampleType, setup));
  vtxToken = consumes<vector<Vertex> >(edm::InputTag("goodPrimaryVertices"));
  produces<pat::ElectronCollection>();

}
EleFiller::~EleFiller(){
}


void
EleFiller::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{  

  // Get leptons and rho
  edm::Handle<pat::ElectronRefVector> electronHandle;
  iEvent.getByToken(electronToken, electronHandle);

  // edm::Handle< edm::TriggerResults > triggerResults;
  // iEvent.getByToken( triggerResultsToken_, triggerResults );

  // edm::Handle<pat::TriggerObjectStandAloneCollection> triggerObjects;
  // iEvent.getByToken(triggerObjects_, triggerObjects);


  edm::Handle<double> rhoHandle;
  iEvent.getByToken(rhoToken, rhoHandle);
  double rho = *rhoHandle;

  edm::Handle<vector<Vertex> > vertices;
  iEvent.getByToken(vtxToken,vertices);

  // Output collection
  auto result = std::make_unique<pat::ElectronCollection>();

  for (unsigned int i = 0; i< electronHandle->size(); ++i){

    //---Clone the pat::Electron
    pat::Electron l(*((*electronHandle)[i].get()));

    //--- PF ISO
    // for cone size R=0.3 :
    float PFChargedHadIso   = l.pfIsolationVariables().sumChargedHadronPt;
    float PFNeutralHadIso   = l.pfIsolationVariables().sumNeutralHadronEt;
    float PFPhotonIso       = l.pfIsolationVariables().sumPhotonEt;

    float SCeta = l.superCluster()->eta(); 
    // float fSCeta = fabs(SCeta);

    float combRelIsoPF = LeptonIsoHelper::combRelIsoPF(sampleType, setup, rho, l);

    //--- SIP, dxy, dz
    float IP      = fabs(l.dB(pat::Electron::PV3D));
    float IPError = l.edB(pat::Electron::PV3D);
    float SIP     = IP/IPError;
    float dxy = std::abs(l.dB(pat::Electron::PV2D));
    float dz  = std::abs(l.dB(pat::Electron::PVDZ));;      

	  
    // // Load correct RunII BDT ID+iso
    // float BDT = -99;
    // if      ( setup == 2016 ) BDT = l.userFloat("ElectronMVAEstimatorRun2Summer16ULIdIsoValues");
    // else if ( setup == 2017 ) BDT = l.userFloat("ElectronMVAEstimatorRun2Summer17ULIdIsoValues");
    // else if ( setup == 2018 ) BDT = l.userFloat("ElectronMVAEstimatorRun2Summer18ULIdIsoValues");
    
    float isEleID80         = l.electronID("mvaEleID_Fall17_iso_V2_wp80");
    float isEleNoIsoID80    = l.electronID("mvaEleID_Fall17_noIso_V2_wp80");
    float isEleID90         = l.electronID("mvaEleID_Fall17_iso_V2_wp90");
    float isEleNoIsoID90    = l.electronID("mvaEleID_Fall17_noIso_V2_wp90");
    float isEleIDLoose      = l.electronID("mvaEleID_Fall17_iso_V2_wpLoose");
    float isEleNoIsoIDLoose = l.electronID("mvaEleID_Fall17_noIso_V2_wpLoose");
    // float isEleID80         = l.electronID("mvaEleID-Fall17-iso-V2-wp80");
    // float isEleNoIsoID80    = l.electronID("mvaEleID-Fall17-noIso-V2-wp80");
    // float isEleID90         = l.electronID("mvaEleID-Fall17-iso-V2-wp90");
    // float isEleNoIsoID90    = l.electronID("mvaEleID-Fall17-noIso-V2-wp90");
    // float isEleIDLoose      = l.electronID("mvaEleID-Fall17-iso-V2-wpLoose");
    // float isEleNoIsoIDLoose = l.electronID("mvaEleID-Fall17-noIso-V2-wpLoose");
    
    // float pt = l.pt();

    l.addUserFloat("isEleID80",isEleID80);
    l.addUserFloat("isEleNoIsoID80",isEleNoIsoID80);
    l.addUserFloat("isEleID90",isEleID90);
    l.addUserFloat("isEleNoIsoID90",isEleNoIsoID90);
    l.addUserFloat("isEleIDLoose",isEleIDLoose);
    l.addUserFloat("isEleNoIsoIDLoose",isEleNoIsoIDLoose);

    //Addtional information
    l.addUserFloat("ConversionVeto",l.passConversionVeto());
    // l.addUserFloat("")

    //-- Missing hit  
	  int missingHit;
	  missingHit = l.gsfTrack()->hitPattern().numberOfAllHits(HitPattern::MISSING_INNER_HITS);
	 
    //-- Flag for crack electrons (which use different efficiency SFs)
    bool isCrack = l.isGap();
     
    //-- Scale and smearing corrections are now stored in the miniAOD https://twiki.cern.ch/twiki/bin/view/CMS/EgammaMiniAODV2#Energy_Scale_and_Smearing
    //-- Unchanged in UL implementation TWiki accessed on 27/04  
    float uncorrected_pt = l.pt();
    float corr_factor = l.userFloat("ecalTrkEnergyPostCorr") / l.energy();//get scale/smear correction factor directly from miniAOD
     
    //scale and smsear electron
    l.setP4(reco::Particle::PolarLorentzVector(l.pt()*corr_factor, l.eta(), l.phi(), l.mass()*corr_factor));
     
    //get all scale uncertainties and their breakdown
    float scale_total_up = l.userFloat("energyScaleUp") / l.energy();
    float scale_stat_up = l.userFloat("energyScaleStatUp") / l.energy();
    float scale_syst_up = l.userFloat("energyScaleSystUp") / l.energy();
    float scale_gain_up = l.userFloat("energyScaleGainUp") / l.energy();
    float scale_total_dn = l.userFloat("energyScaleDown") / l.energy();
    float scale_stat_dn = l.userFloat("energyScaleStatDown") / l.energy();
    float scale_syst_dn = l.userFloat("energyScaleSystDown") / l.energy();
    float scale_gain_dn = l.userFloat("energyScaleGainDown") / l.energy();
     
    //get all smearing uncertainties and their breakdown
    float sigma_total_up = l.userFloat("energySigmaUp") / l.energy();
    float sigma_rho_up = l.userFloat("energySigmaRhoUp") / l.energy();
    float sigma_phi_up = l.userFloat("energySigmaPhiUp") / l.energy();
    float sigma_total_dn = l.userFloat("energySigmaDown") / l.energy();
    float sigma_rho_dn = l.userFloat("energySigmaRhoDown") / l.energy();
    float sigma_phi_dn = l.userFloat("energySigmaPhiDown") / l.energy();

	  
    //--- Embed user variables
    l.addUserFloat("PFChargedHadIso",PFChargedHadIso);
    l.addUserFloat("PFNeutralHadIso",PFNeutralHadIso);
    l.addUserFloat("PFPhotonIso",PFPhotonIso);
    l.addUserFloat("combRelIsoPF",combRelIsoPF);
    l.addUserFloat("SCeta",SCeta);
    l.addUserFloat("rho",rho);
    l.addUserFloat("SIP",SIP);
    l.addUserFloat("dxy",dxy);
    l.addUserFloat("dz",dz);
    l.addUserFloat("isCrack",isCrack);
    l.addUserFloat("missingHit", missingHit);
    l.addUserFloat("uncorrected_pt",uncorrected_pt);
    l.addUserFloat("scale_total_up",scale_total_up);
    l.addUserFloat("scale_stat_up",scale_stat_up);
    l.addUserFloat("scale_syst_up",scale_syst_up);
    l.addUserFloat("scale_gain_up",scale_gain_up);
    l.addUserFloat("scale_total_dn",scale_total_dn);
    l.addUserFloat("scale_stat_dn",scale_stat_dn);
    l.addUserFloat("scale_syst_dn",scale_syst_dn);
    l.addUserFloat("scale_gain_dn",scale_gain_dn);
    l.addUserFloat("sigma_total_up",sigma_total_up);
    l.addUserFloat("sigma_total_dn",sigma_total_dn);
    l.addUserFloat("sigma_rho_up",sigma_rho_up);
    l.addUserFloat("sigma_rho_dn",sigma_rho_dn);
    l.addUserFloat("sigma_phi_up",sigma_phi_up);
    l.addUserFloat("sigma_phi_dn",sigma_phi_dn);

    //--- MC parent code 
//     MCHistoryTools mch(iEvent);
//     if (mch.isMC()) {
//       int MCParentCode = 0;
//       //      int MCParentCode = mch.getParentCode(&l); //FIXME: does not work on cmg
//       l.addUserFloat("MCParentCode",MCParentCode);
//     }

    //--- Check selection cut. Being done here, flags are not available; but this way we 
    //    avoid wasting time on rejected leptons.
    if (!cut(l)) continue;

    //--- Embed flags (ie flags specified in the "flags" pset)
    for(CutSet<pat::Electron>::const_iterator flag = flags.begin(); flag != flags.end(); ++flag) {
      l.addUserFloat(flag->first,int((*(flag->second))(l)));
    }

    result->push_back(l);
  }
  //cout<<result->size()<<" soft electrons"<<endl;
  iEvent.put(std::move(result));
}


#include <FWCore/Framework/interface/MakerMacros.h>
DEFINE_FWK_MODULE(EleFiller);

