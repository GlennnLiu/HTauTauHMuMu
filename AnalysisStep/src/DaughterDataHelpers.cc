#include <HTauTauHMuMu/AnalysisStep/interface/DaughterDataHelpers.h>

#include <DataFormats/PatCandidates/interface/CompositeCandidate.h>
#include <DataFormats/PatCandidates/interface/Muon.h>
#include <DataFormats/PatCandidates/interface/Electron.h>
#include <DataFormats/PatCandidates/interface/Photon.h>
#include <DataFormats/PatCandidates/interface/Tau.h>

using namespace std;
using namespace reco;

void userdatahelpers::embedDaughterData(pat::CompositeCandidate& cand) {

  for (unsigned i = 0; i<cand.numberOfDaughters(); ++i) {
    const reco::Candidate* d = cand.daughter(i);

    if(d->hasMasterClone()) d = d->masterClone().get();
    
    // We need the concrete object to access the method userFloat(). 
    // (A more general solution would be to creat a StringObjectFunction on the fly for each 
    // entry in userFloatNames(). That's maybe too time consuming (to be checked))
    if (const pat::CompositeCandidate* cc = dynamic_cast<const pat::CompositeCandidate*>(d)) {
      embedDaughterData(cand, i, cc);      
    } else if (const pat::Muon* mu = dynamic_cast<const pat::Muon*>(d)) {
      embedDaughterData(cand, i, mu);
    } else if (const pat::Electron* ele = dynamic_cast<const pat::Electron*>(d)) {
      embedDaughterData(cand, i, ele);
    } else if (const pat::Photon* ele = dynamic_cast<const pat::Photon*>(d)) {
      embedDaughterData(cand, i, ele);
    } else if (const pat::Tau* tau = dynamic_cast<const pat::Tau*>(d)) {
      embedDaughterData(cand, i ,tau);
    } else {
      edm::LogError("") << "DaughterDataEmbedder: Unsupported daughter type";
    }
  }
}


float userdatahelpers::getUserFloat(const reco::Candidate* c, const char* name){
  if(c->hasMasterClone()) c = c->masterClone().get();
  if (const pat::Muon* mu = dynamic_cast<const pat::Muon*>(c)) {
    return mu->userFloat(name);
  } else if (const pat::Electron* ele = dynamic_cast<const pat::Electron*>(c)) {
    return ele->userFloat(name);
  } else if (const pat::Photon* ele = dynamic_cast<const pat::Photon*>(c)) {
    return ele->userFloat(name);
  } else if (const pat::Tau* tau = dynamic_cast<const pat::Tau*>(c)) {
    return tau->userFloat(name);
  }  else if (const pat::CompositeCandidate* cc = dynamic_cast<const pat::CompositeCandidate*>(c)) {
    return cc->userFloat(name);
  }
  edm::LogError("") << "userdatahelpers::getUserFloat: Unsupported daughter type";

  return 0;
}

bool userdatahelpers::hasUserFloat(const reco::Candidate* c, const char* name){
  if(c->hasMasterClone()) c = c->masterClone().get();
  if (const pat::Muon* mu = dynamic_cast<const pat::Muon*>(c)) {
    return mu->hasUserFloat(name);
  } else if (const pat::Electron* ele = dynamic_cast<const pat::Electron*>(c)) {
    return ele->hasUserFloat(name);
  } else if (const pat::Photon* ele = dynamic_cast<const pat::Photon*>(c)) {
    return ele->hasUserFloat(name);
  } else if (const pat::Tau* tau = dynamic_cast<const pat::Tau*>(c)) {
    return tau->hasUserFloat(name);
  }  else if (const pat::CompositeCandidate* cc = dynamic_cast<const pat::CompositeCandidate*>(c)) {
    return cc->hasUserFloat(name);
  }
  edm::LogError("") << "userdatahelpers::hasUserFloat: Unsupported daughter type";

  return false;
}

int userdatahelpers::getUserInt(const reco::Candidate* c, const char* name){
  const reco::Candidate* d;
  if(c->hasMasterClone()) d = c->masterClone().get();
  else d = c;
  if (const pat::Muon* mu = dynamic_cast<const pat::Muon*>(d)) {
    return mu->userInt(name);
  } else if (const pat::Electron* ele = dynamic_cast<const pat::Electron*>(d)) {
    return ele->userInt(name);
  } else if (const pat::Photon* ele = dynamic_cast<const pat::Photon*>(d)) {
    return ele->userInt(name);
  } else if (const pat::Tau* tau = dynamic_cast<const pat::Tau*>(d)) {
    return tau->userInt(name);
  } else if (const pat::CompositeCandidate* cc = dynamic_cast<const pat::CompositeCandidate*>(d)) {
    return cc->userInt(name);
  }
  edm::LogError("") << "userdatahelpers::hasUserInt: Unsupported daughter type";
  return 0;
}

bool  userdatahelpers::hasUserInt(const reco::Candidate* c, const char* name)
{
  const reco::Candidate* d;
  if(c->hasMasterClone()) d = c->masterClone().get();
  else d = c;
  if (const pat::Muon* mu = dynamic_cast<const pat::Muon*>(d)) {
    return mu->hasUserInt(name);
  } else if (const pat::Electron* ele = dynamic_cast<const pat::Electron*>(d)) {
    return ele->hasUserInt(name);
  } else if (const pat::Photon* ele = dynamic_cast<const pat::Photon*>(d)) {
    return ele->hasUserInt(name);
  }  else if (const pat::Tau* tau = dynamic_cast<const pat::Tau*>(d)) {
    return tau->hasUserInt(name);
  } else if (const pat::CompositeCandidate* cc = dynamic_cast<const pat::CompositeCandidate*>(d)) {
    return cc->hasUserInt(name);
  }
  edm::LogError("") << "userdatahelpers::hasUserInt: Unsupported daughter type";
  return false;  
}

const PhotonPtrVector*  
userdatahelpers::getUserPhotons(const reco::Candidate* c){
  if(c->hasMasterClone())  c = c->masterClone().get();
  if (abs(c->pdgId())==13) {
    const pat::Muon* mu = static_cast<const pat::Muon*>(c);
    if (mu->hasUserData("FSRCandidates")){
      return mu->userData<PhotonPtrVector>("FSRCandidates");
    } else return 0;
  } else if (abs(c->pdgId())==11) {
    const pat::Electron* ele = static_cast<const pat::Electron*>(c);
    if (ele->hasUserData("FSRCandidates")){
      return ele->userData<PhotonPtrVector>("FSRCandidates");
    } else return 0;
  } else if (abs(c->pdgId())==22) {
    const pat::Photon* ele = static_cast<const pat::Photon*>(c);
    if (ele->hasUserData("FSRCandidates")){
      return ele->userData<PhotonPtrVector>("FSRCandidates");
    } else return 0;
  } else if (abs(c->pdgId())==15) {
    return 0;
  } else {
    cout << "ERROR: userdatahelpers::getUserPhotons" << endl;
    abort();
  }
}


void userdatahelpers::getSortedLeptons(const pat::CompositeCandidate& cand, vector<const Candidate*>& leptons, vector<string>& labels, vector<const Candidate*>& fsrPhotons, std::vector<short>& fsrIndex) {

  leptons = {cand.daughter(0), cand.daughter(1)};
  labels = {"d0.","d1."};
  vector<unsigned> lOrder = {0,1};

  // Sort leptons by charge
  bool need_swap = false;

  // if(abs(leptons[0]->pdgId()) == 22 || abs(leptons[1]->pdgId()) == 22) {
  //     int non_TLE_index = -1;
  //     if(abs(leptons[0]->pdgId()) != 22) non_TLE_index = 0;
  //     if(abs(leptons[1]->pdgId()) != 22) non_TLE_index = 1;
  //     if(non_TLE_index == -1) {
  //       edm::LogError("") << "Found a Z candidate made of two TLE, this should never happen!";
  //       abort();
  //     }
  //     if(leptons[non_TLE_index]->charge() < 0 && non_TLE_index == 0) need_swap = true; 
  // } else {
  //   if (leptons[0]->charge() < 0 && leptons[0]->charge()*leptons[1]->charge()<0) {
  //     need_swap = true;
  //   }
  // }
  if(need_swap) {
      swap(leptons[0],leptons[1]);
      swap(labels[0],labels[1]);
      swap(lOrder[0],lOrder[1]);
  }

  // Collect FSR
  for (unsigned ifsr=2; ifsr<cand.numberOfDaughters(); ++ifsr) {
    const pat::PFParticle* fsr = static_cast<const pat::PFParticle*>(cand.daughter(ifsr));
    int ilep = fsr->userFloat("leptIdx");
    fsrPhotons.push_back(fsr);
    fsrIndex.push_back(lOrder[ilep]);
  }
}


void 
userdatahelpers::getSortedZLeptons(const pat::CompositeCandidate& cand, vector<const Candidate*>& leptons, vector<string>& labels, vector<const Candidate*>& fsrPhotons, std::vector<short>& fsrIndex) {

  // Pointer to leptons, to be sorted by charge, in order Lp, Ln
  leptons = {cand.daughter(0), cand.daughter(1)};

  labels = {"d0.","d1."};
  vector<unsigned> lOrder = {0,1};

  if (leptons[0]->charge() < 0 && leptons[0]->charge()*leptons[1]->charge()<0) {
    swap(leptons[0],leptons[1]);
    swap(labels[0],labels[1]);
    swap(lOrder[0],lOrder[1]);
  }
     
  // Collect FSR
  for (unsigned ifsr=2; ifsr<cand.numberOfDaughters(); ++ifsr) {
    const pat::PFParticle* fsr = static_cast<const pat::PFParticle*>(cand.daughter(ifsr));
    int ilep = fsr->userFloat("leptIdx");
    fsrPhotons.push_back(fsr);
    fsrIndex.push_back(lOrder[ilep]);
  }

}

bool userdatahelpers::isAncestor(const reco::Candidate* ancestor, const reco::Candidate * particle)
{
//particle is already the ancestor
    if(ancestor == particle ) return true;

//otherwise loop on mothers, if any and return true if the ancestor is found
    for(size_t i=0;i< particle->numberOfMothers();i++)
    {
	if(isAncestor(ancestor,particle->mother(i))) return true;
    }
//if we did not return yet, then particle and ancestor are not relatives
    return false;
}
