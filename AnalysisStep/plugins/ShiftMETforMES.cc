#include <FWCore/Framework/interface/Frameworkfwd.h>
#include <FWCore/Framework/interface/EDProducer.h>
#include <FWCore/Framework/interface/Event.h>
#include <FWCore/Framework/interface/ESHandle.h>
#include <FWCore/MessageLogger/interface/MessageLogger.h>
#include <FWCore/ParameterSet/interface/ParameterSet.h>
#include <FWCore/Utilities/interface/InputTag.h>
#include <DataFormats/PatCandidates/interface/MET.h>
#include <DataFormats/METReco/interface/PFMET.h>
#include <DataFormats/METReco/interface/PFMETCollection.h>
#include <DataFormats/METReco/interface/CommonMETData.h>
#include <DataFormats/PatCandidates/interface/Tau.h>
#include "TLorentzVector.h"
#include <HTauTauHMuMu/AnalysisStep/interface/DaughterDataHelpers.h>
#include <DataFormats/Candidate/interface/Candidate.h>

#include <vector>
#include <string>

using namespace edm;
using namespace std;
using namespace reco;

using LorentzVectorE = ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiE4D<double>>;

class ShiftMETforMES : public edm::EDProducer {
    public: 
        /// Constructor
        explicit ShiftMETforMES(const edm::ParameterSet&);
        /// Destructor
        ShiftMETforMES(){};

    private:
        virtual void beginJob(){};  
        virtual void produce(edm::Event&, const edm::EventSetup&);
        virtual void endJob(){};

        edm::EDGetTokenT<View<pat::MET>> theMETTag;
        edm::EDGetTokenT<pat::TauCollection> theTauTag;
};

ShiftMETforMES::ShiftMETforMES(const edm::ParameterSet& iConfig) :
theMETTag(consumes<View<pat::MET>>(iConfig.getParameter<edm::InputTag>("srcMET"))),
theTauTag(consumes<pat::TauCollection>(iConfig.getParameter<edm::InputTag>("tauCollection")))
{
    produces<double>("METdxUPMES");
    produces<double>("METdyUPMES");
    produces<double>("METdxDOWNMES");
    produces<double>("METdyDOWNMES");
    
}

void ShiftMETforMES::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    // Declare ptrs to save MET variations
    std::unique_ptr<double> dx_UP_ptr   (new double);
    std::unique_ptr<double> dy_UP_ptr   (new double);
    std::unique_ptr<double> dx_DOWN_ptr (new double);
    std::unique_ptr<double> dy_DOWN_ptr (new double);

    // Get the MET
    Handle<View<pat::MET> > METHandle;
    iEvent.getByToken(theMETTag, METHandle);
    const pat::MET& patMET = (*METHandle)[0];
   
    // Get the Taus
    Handle<pat::TauCollection> tauHandle;
    iEvent.getByToken(theTauTag, tauHandle);
    
    // Define the correction of the met
    TLorentzVector deltaTaus_UP  ;
    TLorentzVector deltaTaus_DOWN;
    //cout << "-- DeltaUP  : " << deltaTaus_UP.Pt() << " / " << deltaTaus_UP.Eta() << endl;
    //cout << "-- DeltaDOWN: " << deltaTaus_DOWN.Pt() << " / " << deltaTaus_DOWN.Eta() << endl;
    //cout << "-- MET      : " << patMET.px() << " / " << patMET.py() << endl;
    
    //cout << "--------- *** SHIFTED BEGIN LOOP" << endl;
    
    // Loop on taus
    //for (unsigned int itau = 0; itau < tauHandle->size(); ++itau)
    int itau=0;
    for(pat::TauCollection::const_iterator inputTau = tauHandle->begin(); inputTau != tauHandle->end(); ++inputTau, ++itau)
    {
      //cout << "-----> iTau " << itau << endl;

      //---Clone the pat::Tau
      pat::Tau tau(*inputTau);
      
      // cast to reco::Candidate*
      const reco::Candidate* l = (const reco::Candidate*)&tau;
      //cout << "---> reco cand gotten: " << LorentzVectorE(l->p4()) << endl;
        
      // Unshifted tau
      TLorentzVector pfour;
      pfour.SetPxPyPzE (l->px(), l->py(), l->pz(), l->energy());
      
      // Shifted taus
      TLorentzVector pfourMuUp;
      TLorentzVector pfourMuDown;

      int hasMES = ( userdatahelpers::getUserFloat(l,"genmatch")==2 || userdatahelpers::getUserFloat(l,"genmatch")==4 ) ? true : false ;   // actual check of the value of the userfloat
      //cout << "---> exist/user/has: " << existUp << " / " << userdatahelpers::getUserInt(l,"TauUpExists") << " / " << hasUp << endl;
      if(hasMES)
      {
        pfourMuUp=pfour*1.01;
        deltaTaus_UP += ( pfourMuUp - pfour );

        pfourMuDown=pfour*0.99;
        deltaTaus_DOWN += ( pfourMuDown - pfour );

        //cout << "---> deltaTaus_MID: " << deltaTaus_UP.Px() << " / " << deltaTaus_UP.Py() << endl;
        //cout << "---> pfour       : " << pfour.Px() << " / " << pfour.Py() << endl;
        //cout << "---> pfourTauUp  : " << pfourTauUp.Px() << " / " << pfourTauUp.Py() << endl;
        //cout << "---> deltaTaus_UP: " << deltaTaus_UP.Px() << " / " << deltaTaus_UP.Py() << endl;
        //cout << "---> pfourTauDown  : " << pfourTauDown.Pt() << " / " << pfourTauDown.Eta() << endl;
        //cout << "---> deltaTaus_DOWN: " << deltaTaus_DOWN.Px() << " / " << deltaTaus_DOWN.Py() << endl;
      }
    
    } // end loop on taus
    //cout << "------- endl loop ------" << endl;
    //cout << "-- AFTER DeltaUP  : " << deltaTaus_UP.Pt() << " / " << deltaTaus_UP.Eta() << endl;
    //cout << "--                : " << deltaTaus_UP.Px() << " / " << deltaTaus_UP.Py() << endl;
    //cout << "-- AFTER DeltaDOWN: " << deltaTaus_DOWN.Pt() << " / " << deltaTaus_DOWN.Eta() << endl;
    //cout << "--                : " << deltaTaus_DOWN.Px() << " / " << deltaTaus_DOWN.Py() << endl;
    //cout << "-- AFTER MET      : " << patMET.px() << " / " << patMET.py() << endl;
    
    // Calculate the correction
    (*dx_UP_ptr) = patMET.px() - deltaTaus_UP.Px();
    (*dy_UP_ptr) = patMET.py() - deltaTaus_UP.Py();

    (*dx_DOWN_ptr) = patMET.px() - deltaTaus_DOWN.Px();
    (*dy_DOWN_ptr) = patMET.py() - deltaTaus_DOWN.Py();
    
    //cout << "SHIFTED UP  : " << *dx_UP_ptr << " / " << *dy_UP_ptr << endl;
    //cout << "SHIFTED DOWN: " << *dx_DOWN_ptr << " / " << *dy_DOWN_ptr << endl;

    iEvent.put( std::move(dx_UP_ptr)  , "METdxUPMES"   );
    iEvent.put( std::move(dy_UP_ptr)  , "METdyUPMES"   );
    iEvent.put( std::move(dx_DOWN_ptr), "METdxDOWNMES" );
    iEvent.put( std::move(dy_DOWN_ptr), "METdyDOWNMES" );
    
}

#include <FWCore/Framework/interface/MakerMacros.h>
DEFINE_FWK_MODULE(ShiftMETforMES);
