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

#include <DataFormats/Common/interface/TriggerResults.h>
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
  const edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> triggerObjects_;
  const edm::EDGetTokenT< edm::TriggerResults > triggerResultsToken_;
  int sampleType;
  int setup;
  const StringCutObjectSelector<pat::Electron, true> cut;
  const CutSet<pat::Electron> flags;
  edm::EDGetTokenT<double> rhoToken;
  edm::EDGetTokenT<vector<Vertex> > vtxToken;
  TRandom3 rgen_;

  vector<string> eleHLTPaths1_;
//  vector<string> eleHLTPaths2_;
  vector<string> eleHLTFilters1_;
//  vector<string> eleHLTFilters2_;

};


EleFiller::EleFiller(const edm::ParameterSet& iConfig) :
  electronToken(consumes<pat::ElectronRefVector>(iConfig.getParameter<edm::InputTag>("src"))),
  triggerObjects_(consumes<pat::TriggerObjectStandAloneCollection> (iConfig.getParameter<edm::InputTag>("TriggerSet"))),
  triggerResultsToken_( consumes< edm::TriggerResults >( iConfig.getParameter< edm::InputTag >( "TriggerResults" ) ) ),
  sampleType(iConfig.getParameter<int>("sampleType")),
  setup(iConfig.getParameter<int>("setup")),
  cut(iConfig.getParameter<std::string>("cut")),
  flags(iConfig.getParameter<ParameterSet>("flags")),
  rgen_(0)
{
  rhoToken = consumes<double>(LeptonIsoHelper::getEleRhoTag(sampleType, setup));
  vtxToken = consumes<vector<Vertex> >(edm::InputTag("goodPrimaryVertices"));
  produces<pat::ElectronCollection>();

  if (sampleType == 2016)
  {
//	eleHLTPaths2_ = 
//	{
//	"HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*",
//	"HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*",
//	"HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_v*",
//	};
	eleHLTPaths1_ = 
	{
	"HLT_Ele25_eta2p1_WPTight_Gsf_v*",
	"HLT_Ele27_WPTight_Gsf_v*",
	"HLT_Ele27_eta2p1_WPLoose_Gsf_v*",
	"HLT_Ele32_eta2p1_WPTight_Gsf_v*",
	};
//	eleHLTFilters2_ =
//	{
//	"hltEle17Ele12CaloIdLTrackIdLIsoVLDZFilter",
//	"hltEle23Ele12CaloIdLTrackIdLIsoVLDZFilter",
//	"hltDiEle33CaloIdLGsfTrkIdVLDPhiUnseededFilter",
//	};
	eleHLTFilters1_ =
	{
	"hltEle25erWPTightGsfTrackIsoFilter",
	"hltEle27WPTightGsfTrackIsoFilter",
	"hltEle27erWPLooseGsfTrackIsoFilter",
	"hltEle32WPTightGsfTrackIsoFilter",
	};
  }
  else if (sampleType == 2017)
  {
//	eleHLTPaths2_ = 
//	{
//	"HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v*",
//	"HLT_DoubleEle33_CaloIdL_MW_v*",
//	};
	eleHLTPaths1_ =
	{
	"HLT_Ele35_WPTight_Gsf_v*",
	"HLT_Ele38_WPTight_Gsf_v*",
	"HLT_Ele40_WPTight_Gsf_v*",
	};
//        eleHLTFilters2_ =
//        {
//	"hltEle23Ele12CaloIdLTrackIdLIsoVLTrackIsoLeg",//"hltEle23Ele12CaloIdLTrackIdLIsoVLTrackIsoLeg2Filter",
//	"hltDiEle33CaloIdLMWPMS2UnseededFilter",
//	};
	eleHLTFilters1_ =
	{
	"hltEle35noerWPTightGsfTrackIsoFilter",
	"hltEle38noerWPTightGsfTrackIsoFilter",
	"hltEle40noerWPTightGsfTrackIsoFilter",
        };
  }
  else if (sampleType == 2018)
  {
//	eleHLTPaths2_ = 
//	{
//	"HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v*",
//	"HLT_DoubleEle25_CaloIdL_MW_v*",
//	};
	eleHLTPaths1_ =
	{
	"HLT_Ele32_WPTight_Gsf_v*",
	};
//        eleHLTFilters2_ =
//        {
//	"hltEle23Ele12CaloIdLTrackIdLIsoVLTrackIsoLeg",//"hltEle23Ele12CaloIdLTrackIdLIsoVLTrackIsoLeg2Filter",
//	"hltDiEle25CaloIdLMWPMS2UnseededFilter",
//	};
	eleHLTFilters1_ =
	{
	"hltEle32WPTightGsfTrackIsoFilter",
	//"hltEle32noerWPTightGsfTrackIsoFilter",
        };
  }

}
EleFiller::~EleFiller(){
}


void
EleFiller::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{  

  // Get leptons and rho
  edm::Handle<pat::ElectronRefVector> electronHandle;
  iEvent.getByToken(electronToken, electronHandle);

  edm::Handle< edm::TriggerResults > triggerResults;
  iEvent.getByToken( triggerResultsToken_, triggerResults );

  edm::Handle<pat::TriggerObjectStandAloneCollection> triggerObjects;
  iEvent.getByToken(triggerObjects_, triggerObjects);


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
    float fSCeta = fabs(SCeta);

    float combRelIsoPF = LeptonIsoHelper::combRelIsoPF(sampleType, setup, rho, l);

    //--- SIP, dxy, dz
    float IP      = fabs(l.dB(pat::Electron::PV3D));
    float IPError = l.edB(pat::Electron::PV3D);
    float SIP     = IP/IPError;

    float dxy = 999.;
    float dz  = 999.;
    const Vertex* vertex = 0;
    if (vertices->size()>0) {
      vertex = &(vertices->front());
      dxy = fabs(l.gsfTrack()->dxy(vertex->position()));
      dz  = fabs(l.gsfTrack()->dz(vertex->position()));
    } 

	  
    // Load correct RunII BDT ID+iso
    float BDT = -99;
    if      ( setup == 2016 ) BDT = l.userFloat("ElectronMVAEstimatorRun2Summer16IdIsoValues");
    else if ( setup == 2017 ) BDT = l.userFloat("ElectronMVAEstimatorRun2Fall17IsoV2Values");
    else if ( setup == 2018 ) BDT = l.userFloat("ElectronMVAEstimatorRun2Autumn18IdIsoValues");
//    cout << "BDT = " << BDT << endl;
    
    float pt = l.pt();

	  
    bool isBDT = false;

    if ( setup==2016 )
    {
       //WP taken from https://github.com/mkovac/cmssw/blob/Electron_XGBoost_MVA_2016_CMSSW_10_3_1/RecoEgamma/ElectronIdentification/python/Identification/mvaElectronID_Summer16_ID_ISO_cff.py#L27-L34 and transfered with https://github.com/cms-sw/cmssw/blob/CMSSW_9_4_X/RecoEgamma/EgammaTools/interface/MVAValueMapProducer.h#L145 so that they are between -1 and 1
       isBDT         = (pt<=10 && ((fSCeta<0.8                  && BDT >  0.95034841889) ||
                                   (fSCeta>=0.8 && fSCeta<1.479 && BDT >  0.94606270058) ||
                                   (fSCeta>=1.479               && BDT >  0.93872558098)))
                    || (pt>10  && ((fSCeta<0.8                  && BDT >  0.3782357877) ||
                                   (fSCeta>=0.8 && fSCeta<1.479 && BDT >  0.35871320305) ||
                                   (fSCeta>=1.479               && BDT >  -0.57451499543)));
    }
	 else if (setup==2017)
	 {
	   //WP taken from https://github.com/cms-sw/cmssw/blob/master/RecoEgamma/ElectronIdentification/python/Identification/mvaElectronID_Fall17_iso_V2_cff.py#L21 and transfered with https://github.com/cms-sw/cmssw/blob/CMSSW_9_4_X/RecoEgamma/EgammaTools/interface/MVAValueMapProducer.h#L145 so that they are between -1 and 1
	 	 isBDT         = (pt<=10 && ((fSCeta<0.8                  && BDT >  0.85216885148) ||
                                   (fSCeta>=0.8 && fSCeta<1.479 && BDT >  0.82684550976) ||
                                   (fSCeta>=1.479               && BDT >  0.86937630022)))
                    || (pt>10  && ((fSCeta<0.8                  && BDT >  0.98248928759) ||
                                   (fSCeta>=0.8 && fSCeta<1.479 && BDT >  0.96919224579) ||
                                   (fSCeta>=1.479               && BDT >  0.79349796445)));
	 }
    else if ( setup==2018 )
    {
       //WP taken from https://github.com/mkovac/cmssw/blob/Electron_XGBoost_MVA_2018_CMSSW_10_3_1/RecoEgamma/ElectronIdentification/python/Identification/mvaElectronID_Autumn18_ID_ISO_cff.py#L27-L35 and transfered with https://github.com/cms-sw/cmssw/blob/CMSSW_9_4_X/RecoEgamma/EgammaTools/interface/MVAValueMapProducer.h#L145 so that they are between -1 and 1
       isBDT         = (pt<=10 && ((fSCeta<0.8                  && BDT >  0.8955937602) ||
                                   (fSCeta>=0.8 && fSCeta<1.479 && BDT >  0.91106464032) ||
                                   (fSCeta>=1.479               && BDT >  0.94067753025)))
                    || (pt>10  && ((fSCeta<0.8                  && BDT >  0.04240620843) ||
                                   (fSCeta>=0.8 && fSCeta<1.479 && BDT >  0.0047338429) ||
                                   (fSCeta>=1.479               && BDT >  -0.60423293572)));
     }
	 else
	 {
	  	 std::cerr << "[ERROR] EleFiller: no BDT setup for: " << setup << " year!" << std::endl;
	 }

    //-- Missing hit  
	 int missingHit;
	 missingHit = l.gsfTrack()->hitPattern().numberOfAllHits(HitPattern::MISSING_INNER_HITS);
	 
    //-- Flag for crack electrons (which use different efficiency SFs)
    bool isCrack = l.isGap();
     
    //--- Trigger matching
    bool HLTMatch1 = false;
//    bool HLTMatch2 = false;
    vector<bool> eachPath1;
//    vector<bool> eachPath2;
    for ( size_t j = 0; j < eleHLTPaths1_.size(); ++j) 
       eachPath1.push_back(false);
//    for ( size_t j = 0; j < eleHLTPaths2_.size(); ++j)
//       eachPath2.push_back(false);

    for (size_t idxto = 0; idxto < triggerObjects->size(); ++idxto) {

       pat::TriggerObjectStandAlone obj = triggerObjects->at(idxto);
       obj.unpackFilterLabels(iEvent,*triggerResults );

       if (deltaR(obj,l)>0.1) continue;
       if (!obj.hasTriggerObjectType(trigger::TriggerElectron) && !obj.hasTriggerObjectType(trigger::TriggerPhoton)) continue;
    //pat::TriggerObjectStandAloneCollection obj= l.triggerObjectMatches();
    //cout<<obj.size()<<endl;
    //for ( size_t iTrigObj = 0; iTrigObj < obj.size(); ++iTrigObj ) {
    //   obj.at( iTrigObj ).unpackFilterLabels(iEvent,*triggerResults );
    //   for (size_t test=0;test<obj.at( iTrigObj ).filterLabels().size();test++) {
    //	  cout<<obj.at( iTrigObj ).filterLabels()[test].c_str()<<", ";
    //   }
    //   cout<<endl;
    //}
    //for ( size_t i = 0; i < obj.size(); ++i ) {
       l.addUserInt("TrgObj"+std::to_string(idxto),idxto);

       for (size_t j = 0; j < eleHLTPaths1_.size(); ++j) {
         if (obj.hasFilterLabel( eleHLTFilters1_[j] )) {
            HLTMatch1=true;
	    eachPath1[j]=true;
	 }
       }
//         for (size_t j = 0; j < eleHLTPaths2_.size(); ++j ) {
//	    if (eleHLTPaths2_[j] == "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v*") {
//		if (obj.at( i ).hasFilterLabel( eleHLTFilters2_[j]+"1Filter" ) || obj.at( i ).hasFilterLabel( eleHLTFilters2_[j]+"2Filter" )) {
//		    HLTMatch2=true;
//		    eachPath2[j]=true;
//		}
//	    }
//	    else {
//                if (obj.at( i ).hasFilterLabel( eleHLTFilters2_[j] )) {
//                    HLTMatch2=true;
//                    eachPath2[j]=true;
//                }
//	    }
         }
//      }

    for ( size_t j = 0; j < eleHLTPaths1_.size(); ++j)
       l.addUserFloat(eleHLTPaths1_[j], eachPath1[j]);
//    for ( size_t j = 0; j < eleHLTPaths2_.size(); ++j)
//       l.addUserFloat(eleHLTPaths2_[j], eachPath2[j]);
	 
     
    //-- Scale and smearing corrections are now stored in the miniAOD https://twiki.cern.ch/twiki/bin/view/CMS/EgammaMiniAODV2#Energy_Scale_and_Smearing
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
    l.addUserFloat("BDT",BDT);    
    l.addUserFloat("isBDT",isBDT);
    l.addUserFloat("isCrack",isCrack);
    l.addUserFloat("HLTMatch1", HLTMatch1);
//    l.addUserFloat("HLTMatch2", HLTMatch2);
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
  cout<<result->size()<<" soft electrons"<<endl;
  iEvent.put(std::move(result));
}


#include <FWCore/Framework/interface/MakerMacros.h>
DEFINE_FWK_MODULE(EleFiller);

