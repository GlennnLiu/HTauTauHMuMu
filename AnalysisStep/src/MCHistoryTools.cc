/** \file
 *
 *  Retrieve information for boson decays to leptons from the genparticle collection, in the following way:
 *  genH is the generated H (if more than one is present, the last one with daughter = Z is taken)
 *  genZs are the Zs (required to have parent!=Z to avoid double counting)
 *  genLeps are the leptons, required to have either parent=Z or (for generators where the Z 
 * is not explicit in the MC history) status = 3. beware of how FSR is described in the MC history...
 *
 *
 *  \author N. Amapane - CERN
 *  \author G. Ortona - LLR
 */

#include <HTauTauHMuMu/AnalysisStep/interface/MCHistoryTools.h>

#include <DataFormats/HepMCCandidate/interface/GenParticle.h>
#include <SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h>
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h" //Atbbf

// AT Additional libraries for GenJet variables
#include <DataFormats/PatCandidates/interface/Jet.h>
#include <CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h>
#include <CondFormats/JetMETObjects/interface/JetCorrectorParameters.h>
#include <JetMETCorrections/Objects/interface/JetCorrectionsRecord.h>
#include <JetMETCorrections/Modules/interface/JetResolution.h>
#include "DataFormats/JetReco/interface/GenJet.h"
#include "PhysicsTools/JetMCUtils/interface/JetMCTag.h"
#include "PhysicsTools/JetMCUtils/interface/CandMCTag.h"

#include <HTauTauHMuMu/AnalysisStep/interface/FinalStates.h>

#include <boost/algorithm/string/predicate.hpp>

using namespace std;
using namespace reco;
using namespace edm;
// using namespace JetMCTagUtils; //ATjets
// using namespace CandMCTagUtils; //Atjets

namespace {
  bool dbg = false;
}


MCHistoryTools::MCHistoryTools(const edm::Event & event, std::string sampleName, edm::Handle<edm::View<reco::Candidate> > & genParticles, edm::Handle<GenEventInfoProduct> & gen, edm::Handle<edm::View<reco::GenJet> > & genJets, edm::Handle<edm::View<pat::PackedGenParticle> > packedgenParticles) :
  ismc(false),
  processID(0),
  hepMCweight(1),
  isInit(false),
  theGenH(0)
{
  jets = genJets; //ATjets
  packed = packedgenParticles; //ATbbf
  particles = genParticles;
  if(particles.isValid()){

    ismc=true;
    
    processID = gen->signalProcessID();

    if (processID == 100) {
      // FIXME: fix gg2ZZ samples
      if (boost::starts_with(sampleName,"ZHiggs")) processID=900024;
      if (boost::starts_with(sampleName,"WHiggs")) processID=900026; 
      if (boost::starts_with(sampleName,"ggTo"))   processID=900661; 
    }

    if (processID == 0) {
      if (boost::starts_with(sampleName,"ZZZJets")) processID=900101;      
    }

    if (processID == 3) {
      if (boost::starts_with(sampleName,"WWJets")) processID=900102;      
      if (boost::starts_with(sampleName,"TTZJets")) processID=900103;      
    }
    
    if (processID == 5 || processID == 6) {
      if (boost::starts_with(sampleName,"TTZJets")) processID=900103;      
    }
    // for TTZ (without jets sample)
    if (boost::starts_with(sampleName,"TTZ")) processID=900104;
    if (boost::starts_with(sampleName,"TTTo2L2Nu")) processID=900104;
    // for WWZ
    if (boost::starts_with(sampleName,"WWZ")) processID=900105;
    // for tHW
    if (boost::starts_with(sampleName,"THW") || boost::starts_with(sampleName,"tHW")) processID=900106;
    //for ttWW
    if (boost::starts_with(sampleName,"TTWW")) processID=900106;

    // take the MC weight
    GenEventInfoProduct  genInfo = *(gen.product());
    hepMCweight = genInfo.weight();
      
  }
}

MCHistoryTools::~MCHistoryTools(){}


// Find the actual lepton parent (first parent in MC history with a different pdgID)
const reco::GenParticle* MCHistoryTools::getParent(const reco::GenParticle* genLep) {
  if(genLep==0) return 0; 
  int flavor = genLep->pdgId();
  
  while (genLep->mother()!=0 && genLep->mother()->pdgId() == flavor) {
    // cout  << " getparent " << genLep->mother()->pdgId() << endl;
    genLep = (const GenParticle*) genLep->mother();
  }
  //cout  << " getparent:ret: " << genLep->mother()->pdgId() << endl;
  return (const GenParticle*) genLep->mother();
}

// Same as the above, but try recovery in case default PAT matching fails.
// (This happens rather often for electron due to brems/FSR, since the default matching handles this poorly).
// The recovery consists in matching between a selected list of genleptons, cf. getMatch().
const reco::GenParticle* MCHistoryTools::getParent(const pat::Electron* lep, const vector<const Candidate *>& gen4lep) {
  const reco::GenParticle* parent= getParent((lep->genParticleRef()).get());
  if (parent==0) {
    parent=getParent(getMatch(lep, gen4lep));
  }
  return parent;
}

// Manual matching with closest same-flavour gen lepton (of any status). 
// This was test to work great when the provided candidates are e.g. only the signal ones.
//FIXME: check and charge!
const reco::GenParticle* MCHistoryTools::getMatch(const pat::Electron* lep, const vector<const Candidate *>& gen4lep) {
  float mindeltaR=9999;
  const Candidate * genmatch = 0;
  int lcode = lep->pdgId();
  for (vector<const Candidate *>::const_iterator iglep = gen4lep.begin(); iglep!=gen4lep.end(); ++iglep) {
    if ((*iglep)->pdgId() == lcode) {
      float dR = deltaR(*lep,*(*iglep));
      if (dR<mindeltaR && dR < 0.1) {
	mindeltaR=dR;
	genmatch = *iglep;
      }
    }
  }
  if(dbg)  cout << "Recovery match: dR: " << mindeltaR << " " << lep->pt() << " " << ((genmatch!=0)?(genmatch->pt()):-1) << endl;
  return (const GenParticle*) genmatch;
}

//Return the code of the particle's parent: 25 for H->Z->l; 23 for Z->l; +-15 for tau->l if genlep is e,mu.
int MCHistoryTools::getParentCode(const reco::GenParticle* genLep) {
  int parentId = 0;
  
  const Candidate* particle = getParent(genLep);
  
  if (particle) {
    parentId = abs(particle->pdgId());
    if ((parentId == 23 || parentId == 24) && particle->mother()!=0) {
      if (getParent((reco::GenParticle*)particle)->pdgId() == 25) parentId = 25;
    }
  }
  //   cout <<  " getParentCode1: result " <<  parentId << endl;
  return parentId;
}

// Same as above, but if no match is found, search for a match within gen4lep
// Cf. getParent(lep, gen4lep) for details.
int MCHistoryTools::getParentCode(const pat::Electron* lep, const vector<const Candidate *>& gen4lep) {
  int parentId = getParentCode((lep->genParticleRef()).get());
  
  if (parentId==0) { // Recover for bad matching to status 1 electrons due to brems
    const Candidate * particle = getParent(lep, gen4lep);
    if (particle) {
      parentId = particle->pdgId();
      //       cout << "getParentCode2 : " << parentId;
      if ((parentId == 23 || abs(parentId == 24)) && particle->mother()!=0) {
	      if (getParent((reco::GenParticle*)particle)->pdgId() == 25) parentId = 25;
      }
    }
  }
  //   cout <<  " getParentCode2: result " <<  parentId << endl;
  return parentId;
}


void
MCHistoryTools::init() {
  if (isInit) return;
  if (!ismc) return;


  std::vector<const reco::Candidate *> theGenFSRParents;

  for( View<Candidate>::const_iterator p = particles->begin(); p != particles->end(); ++ p ) {
    int id = abs(p->pdgId());

     //--- H
    if (id==25) {
      if (theGenH==0) theGenH = &*p; // Consider only the first one in the chain
    }
  }
  std::vector<const reco::Candidate *> backupLepts;
  for( View<Candidate>::const_iterator p = particles->begin(); p != particles->end(); ++ p ) {
    int id = abs(p->pdgId());
    if (id==23 || id==24) {
      if (theGenH!=0) {
        if (getParentCode((const GenParticle*)&*p)==25) {
          theGenV.push_back(&*p);
        }
        else theAssociatedV.push_back(&*p);
      }
      else theGenV.push_back(&*p);
    }

    // // W/Z from associated production (ie not from H)
    // else if (id==24) {
    //   if (p->mother()!=0 && p->mother()->pdgId()!=id) {
	  //     int pid = getParentCode((const GenParticle*)&*p);
	  //     if (pid!=25) theAssociatedV.push_back(&*p);
    //   }
    // }
    
    // Prompt leptons
    else if ((id== 13 || id==11 || id==15) && (p->mother()!=0)) {
      int mid = abs(p->mother()->pdgId());
      int pid = abs(getParentCode((const GenParticle*)&*p));
      if (theGenH!=0) {
        if (mid == 25 || ((mid==23 || mid==24) && pid==25)) theGenLeps.push_back(&*p);
        else theAssociatedLeps.push_back(&*p);
      }
      else {
        // cout<<"mid: "<<mid<<"; pid: "<<id<<"."<<endl;
        if (mid == 23) theGenLeps.push_back(&*p);
        else if (mid == 1 || mid == 2 || mid == 3 || mid == 4 || mid == 5 || mid == 6 || mid == 7 || mid == 8 || mid == 9 || mid == 21 || mid == 24) {
          if (backupLepts.size()<2) backupLepts.push_back(&*p);
        }
        else theAssociatedLeps.push_back(&*p);
      }
    }

    //FSR
    if (id==22) {
      const reco::GenParticle* fp = getParent((const GenParticle*)&*p);
      int pcode = fp->pdgId();
      if (abs(pcode) == 11 || abs(pcode) == 13) {
	//Search for the first ancestor of same ID of the photon's parent
	      while (fp->mother()!=0 && fp->mother()->pdgId() == pcode) {
	        fp = (const GenParticle*) fp->mother();
        }
	//Check that the lepton mother is a Z, W or H (for samples where intermediate bosons are not listed in the history). May not work correctly in some samples!
	      int origin = abs(fp->mother()->pdgId());
	      if (origin==23 || origin == 24 || origin == 25) {
	        theGenFSR.push_back(&*p);
	        theGenFSRParents.push_back(&*fp);
	      } else {
	  // the lepton that makes FSR is coming from elsewhere
	        if (dbg) cout << "WARNING: FSR with parent ID: " << pcode << " origin ID: " << origin << endl;
	      }
      }
      //assert(pcode!=23); // just an xcheck that we don't get FSR listed with Z as a parent... // commented out to make Zgamma samples work
    }
    
      
    if (dbg){
      if (id==13 || id==11 || id ==23 || id==24) {
	cout << "Genpart: id " << id << " pt " << p->pt() << " eta " << p->eta() << " phi " << p->phi()
	     << " status " << p->status()
	     << " parent id " << (p->mother()!=0?p->mother()->pdgId():0)
	  // << " vertex " << p->vertex()
	     << endl;
      }
    }
  } // end loop on particles
  if (theGenLeps.size()==0) theGenLeps=backupLepts;

  //FIXME just check consistency of FSR
  for (unsigned j=0; j<theGenFSRParents.size(); ++j) {
    bool found=false;
    for (unsigned i=0; i<theGenLeps.size(); ++i) {
      if (theGenLeps[i]==theGenFSRParents[j]) {
        found=true;
        break;
      }
    }
    if (!found) {
      for (unsigned i=0; i<theAssociatedLeps.size(); ++i) {
	      if (theAssociatedLeps[i]==theGenFSRParents[j]) {
	        found=true;
	        break;
	      }
      }
    }
    if (!found) cout << "ERROR: mismatch in FSR photon " << theGenFSR[j]->pt() << " " << theGenFSRParents[j]->pt() << " " << theGenFSRParents[j] << endl;
  }
  
  // Sort leptons, as done for the signal, for cases where we have 4.
  if (theGenLeps.size()==4) {
    const float ZmassValue = 91.1876;  
    float minDZMass=1E36;
    float iZ11=-1, iZ12=-1, iZ21=-1, iZ22=-1;
    
    // Find Z1 as closest-to-mZ l+l- combination
    for (int i=0; i<4; ++i) {
      for (int j=i+1; j<4; ++j) {
        if (theGenLeps[i]->pdgId()+theGenLeps[j]->pdgId()==0) { // Same flavour, opposite sign
          float dZMass = std::abs((theGenLeps[i]->p4()+theGenLeps[j]->p4()).mass()-ZmassValue);
          if (dZMass<minDZMass){
            minDZMass=dZMass;
            iZ11=i;
            iZ12=j;
          }
        }
      }
    }

    // Z2 is from remaining 2 leptons
    if (iZ11!=-1 && iZ12!=-1){
      for (int i=0; i<4; ++i) {
        if (i!=iZ11 && i!=iZ12) {
          if (iZ21==-1) iZ21=i;
          else iZ22=i;
        }
      }
    }

    bool do_SF_OS_check = true;
    
    if (processID == 900104 || processID == 900105 || processID == 900106) do_SF_OS_check = false;
    // if ( do_SF_OS_check && (iZ22==-1 || theGenLeps[iZ21]->pdgId()+theGenLeps[iZ22]->pdgId()!=0) ) {  //Test remaining conditions: Z2 is found and SF, OS
    //   cout << "MCHistoryTools: Cannot sort leptons ";
    //   for (int i=0; i<4; ++i) cout << theGenLeps[i]->pdgId() << " ";
    //   cout << iZ11 << " " << iZ12 << " " << iZ21 << " " << iZ22 << endl;
    //   abort();
    // }    
    if( (iZ11 != iZ12 && iZ21 != iZ22) || do_SF_OS_check) {// if do_SF_OS_check and same indexes something has gone bad, let's crash and check
       // Sort leptons by sign
       if (theGenLeps[iZ11]->pdgId() < 0 ) {
         swap(iZ11,iZ12);
       }
       if (theGenLeps[iZ21]->pdgId() < 0 ) {
         swap(iZ21,iZ22);
       }
    }
    
    if(iZ11>=0) theSortedGenLepts.push_back(theGenLeps[iZ11]);
    if(iZ12>=0) theSortedGenLepts.push_back(theGenLeps[iZ12]);
    if(iZ21>=0) theSortedGenLepts.push_back(theGenLeps[iZ21]);
    if(iZ22>=0) theSortedGenLepts.push_back(theGenLeps[iZ22]);

  } else if (theGenLeps.size()==2) {
    float L1=0,L2=1;
    if (theGenLeps[L1]->pdgId() < 0) swap(L1,L2);
    theSortedGenLepts.push_back(theGenLeps[L1]);
    theSortedGenLepts.push_back(theGenLeps[L2]);
  }
  else theSortedGenLepts = theGenLeps;

  // cout<<theSortedGenLepts.size()<<" leptons: "<<endl;
  // for (size_t i=0;i<theSortedGenLepts.size();i++) cout<<theSortedGenLepts[i]->pdgId()<<", ";
  // cout<<endl;
  // cout<<theGenZ.size()<<" Z bosons:"<<endl<<"MID: ";
  // for (size_t i=0;i<theGenZ.size();i++) cout<<theGenZ[i]->mother()->pdgId()<<", ";
  // cout<<endl<<endl;
  
  //AT Isolation
  for (unsigned int j=0; j<theSortedGenLepts.size(); ++j) {
    float iso = 0; //AT Supporting varibale to sum the different components in the isolation (ISO) variable
    std::vector<int> id;
    std::vector<float> pt;
    for( View<Candidate>::const_iterator p_iso = particles->begin(); p_iso != particles->end(); ++ p_iso) {
      if(theSortedGenLepts[j] != &*p_iso){ //The lepton for which I am calculating the isolation is not included in the isolation itself
        // cout << "Work in progress: isolation" << endl; //AT Uncomment just to check if the you actually enter in the loop
        if(p_iso->status() != 1) continue; //Stable particles only (To check!)
        if((abs(p_iso->pdgId()) == 12) || (abs(p_iso->pdgId()) == 14) || (abs(p_iso->pdgId()) == 16)) continue; //Exclude neutrinos
        if((abs(p_iso->pdgId()) == 11) || (abs(p_iso->pdgId()) == 13)) continue; //Exclude leptons
        if(std::find(theGenFSR.begin(), theGenFSR.end(), &*p_iso) != theGenFSR.end()) continue; //Exclude FSR photons
        // if(std::find(theSortedGenLepts.begin(), theSortedGenLepts.end(), &*p_iso) != theSortedGenLepts.end()) continue; //Exclude prompt leptons
        float dR = deltaR(*theSortedGenLepts[j], *p_iso);
        if(dR < 0.3){ //AT Isolation cut for DR<0.3
          iso += p_iso->pt();
          id.push_back(p_iso->pdgId());
          pt.push_back(p_iso->pt());
        }
      }
    }
    iso = iso / theSortedGenLepts[j]->pt();
    isolation.push_back(iso);
  }
  // cout<<"ATjets"<<endl;
  for(View<reco::GenJet>::const_iterator genjet = jets->begin(); genjet != jets->end(); genjet++){
    theGenJets.push_back(&* genjet);
    std::vector<bool> dR_clean;
    for(unsigned i = 0; i < theSortedGenLepts.size(); ++i){
      float dR = deltaR(*theSortedGenLepts[i], *genjet);
      if(dR<0.4) dR_clean.push_back(false);
      else dR_clean.push_back(true);
    }
    if (!(std::find(dR_clean.begin(), dR_clean.end(), false)!=dR_clean.end())){
      theCleanedGenJets.push_back(&* genjet);
    }
  } //ATjets

  // cout<<"visible leptons: "<<theSortedGenLepts.size()<<endl;
  //Visible leptons and tau neutrinos
  for (size_t ilep = 0;ilep<theSortedGenLepts.size();++ilep) {
    int id = abs(theSortedGenLepts[ilep]->pdgId());
    // cout<<"id:"<<id<<endl;
    if (id==11 || id==13) {
      theSortedVisGenLeps.push_back(theSortedGenLepts[ilep]);
      theGenTauNus.push_back(0);//theSortedGenLepts[ilep]);
    } else if (id==15) {
      bool isFinalTau=false;
      const Candidate *finalTau=theSortedGenLepts[ilep];
      while (!isFinalTau) {
	      bool noTauDau=true;
	      for (size_t iDau=0;iDau<finalTau->numberOfDaughters();iDau++) {
	        if (abs(finalTau->daughter(iDau)->pdgId())==15) {
	          noTauDau=false;
	          finalTau=finalTau->daughter(iDau);
	          break;
	        }
      	}
	      if (noTauDau)
	        isFinalTau=true;
      }
      int nDau=finalTau->numberOfDaughters();
      // cout<<"nDau:"<<nDau<<endl;
      //bool lepDecay=false;
      vector<int> TauNuIdx,LepIdx;
      for (int iDau=0;iDau<nDau;++iDau) {
        const Candidate *Dau = finalTau->daughter(iDau);
        if (abs(Dau->pdgId())==11 || abs(Dau->pdgId())==13) {
          LepIdx.push_back(iDau);
        } else if (abs(Dau->pdgId())==16) {//} || abs(Dau->pdgId())==14 || abs(Dau->pdgId())==12) {
          TauNuIdx.push_back(iDau);
        }
      }
      // cout<<"Nlep:"<<LepIdx.size()<<". Nnu:"<<TauNuIdx.size()<<endl;
      if (LepIdx.size()==1 && TauNuIdx.size()==1) {//For leptonically decaying taus, we save the lepton decay products, instead of 
        //lepDecay=true;
        theSortedVisGenLeps.push_back(finalTau->daughter(LepIdx[0]));
        theGenTauNus.push_back(0);//theSortedGenLepts[ilep]->daughter(TauNuIdx[0]));
      } else if (TauNuIdx.size()==1) {//For hadronically decaying taus, we still save the gen tau lepton
        theSortedVisGenLeps.push_back(theSortedGenLepts[ilep]);
        theGenTauNus.push_back(finalTau->daughter(TauNuIdx[0]));
      } else {
        cout<<"Warning: number of tau neutrinos not equal to one, must be something wrong: nDau="<<nDau<<",nLep="<<LepIdx.size()<<",nTauNu="<<TauNuIdx.size()<<". ";
        //for (int iDau=0;iDau<nDau;++iDau)
        cout<<endl;
        theSortedVisGenLeps.push_back(theSortedGenLepts[ilep]);
        theGenTauNus.push_back(0);//theSortedGenLepts[ilep]->daughter(TauNuIdx[0]));
      }
    }
  }

  isInit = true;

  if (dbg) {
    cout << "MCHistoryTools: "  << processID << " " << genFinalState() << " " << (theGenH==0) << " " << theGenLeps.size() // << " " << nMu << " " << nEle << " " << nTau 
	 << endl;
  }

}

void
MCHistoryTools::genAcceptance(bool& InEtaAcceptance, bool& InEtaPtAcceptance){
  if (!ismc) return;  
  init();

//   float gen_mZ1 = -1.;
//   float gen_mZ2 = -1.;
//   int gen_Z1_flavour =0;
//   int gen_Z2_flavour =0;

  InEtaAcceptance = false;
  InEtaPtAcceptance = false;

  if (theGenLeps.size()==4 || theGenLeps.size()==2) {
//     gen_mZ1 = (theSortedGenLepts[0]->p4()+theSortedGenLepts[1]->p4()).mass();
//     gen_mZ2 = (theSortedGenLepts[2]->p4()+theSortedGenLepts[3]->p4()).mass();
//     gen_Z1_flavour = abs(theSortedGenLepts[0]->pdgId());
//     gen_Z2_flavour = abs(theSortedGenLepts[1]->pdgId());

    size_t nlInEtaAcceptance = 0;
    size_t nlInEtaPtAcceptance = 0;

    for (unsigned int i=0; i<theGenLeps.size(); ++i){
      float abseta =  fabs(theGenLeps[i]->eta());
      int id = abs(theGenLeps[i]->pdgId());
      //FIXME should take the 2 gen l with status 1
      if ((id == 11 && theGenLeps[i]->pt() > 7. && abseta < 2.5) || (id == 13 && theGenLeps[i]->pt() > 5. && abseta < 2.4) || (id == 15 && theGenLeps[i]->pt() > 20 && abseta < 2.3)) {
	      ++nlInEtaPtAcceptance;
      }
      if ((id == 11 && abseta < 2.5) || (id == 13 && abseta < 2.4) || (id == 15 && abseta < 2.3)) { 
	      ++nlInEtaAcceptance;
      }
    }
    if (nlInEtaPtAcceptance>=theGenLeps.size()) InEtaPtAcceptance = true;
    if (nlInEtaAcceptance>=theGenLeps.size()) InEtaAcceptance = true;
  }
}


int
MCHistoryTools::genFinalState(){
  if (!ismc) return -1;  
  init();
  // cout<<"end initiate"<<endl;
  int gen_finalState = NONE;  
  int ifs=1;
  if (theSortedVisGenLeps.size()==2){
    for (int i=0; i<2; ++i) {
      ifs*=theSortedVisGenLeps[i]->pdgId();
    }

    // FIXME this does not make much sense now that we re-pair Zs in the MC history.
    if (ifs==-169) {
      gen_finalState = mumu;
    } else if (ifs==-165) {
      gen_finalState = etau;
    } else if (ifs==-195) {
      gen_finalState = mutau;
    } else if (ifs==-225) {
      gen_finalState = tautau;
    } else if (ifs==-143) {
      gen_finalState = emu;
    } else if (ifs==-121) {
      gen_finalState = ee;
    } else {
      gen_finalState = BUGGY;
    }
  }
  // cout<<gen_finalState<<endl;
  // if (gen_finalState==BUGGY || gen_finalState==NONE) {
  //   cout<<"Wrong gen_finalState"<<endl;
  //   for( View<Candidate>::const_iterator p = particles->begin(); p != particles->end(); ++ p ) {
  //     int id = abs(p->pdgId());
  //     if ((id== 13 || id==11 || id==15) && (p->mother()!=0)) {
  //       int mid = abs(p->mother()->pdgId());
  //       int pid = abs(getParentCode((const GenParticle*)&*p));
  //       // if (theGenH==0) {
  //         cout<<"id: "<<id<<"; mid: "<<mid<<"; final mid: "<<pid<<"."<<endl;
  //       // }
  //     }
  //   }
  // }
  return gen_finalState;
}

int
MCHistoryTools::genAssociatedFS(){
  if (!ismc) return -1;  
  init();

  if (theGenH==0) return -1;


  int id=-1;
  if (theAssociatedV.size()>0) {
    // FIXME should check that nothing is wrong
    //    if (theAssociatedV.size()>1) cout << "ERROR: associatedV = " << theAssociatedV.size() << endl;

    const reco::Candidate* genV = theAssociatedV.front();
    const reco::Candidate* dau = genV->daughter(0);
    while (dau!=0 && dau->pdgId() == genV->pdgId()) { // Find the boson's flavour
      genV=dau;
      dau=genV->daughter(0);
    }
    id = abs(dau->pdgId());
  
  }
  
  return id;
}

// Find gen FSR matching (closest) to recoFSR.
int MCHistoryTools::fsrMatch(const reco::Candidate* recoFSR, 
		       const vector<const reco::Candidate*>& genFSRs) {

  //FIXME: cuts should be tuned; is pT matching also necessary?
  const double dRMatchingCut = 0.3; // FIXME!!! 
  const double ptMinCut = 2.;

  double minDR = 99999;
  int matchIdx=-1;

  for (unsigned j=0; j<genFSRs.size(); ++j) {
    const reco::Candidate* gg = genFSRs[j];
    if (gg->pt()>ptMinCut) {
      double dR = reco::deltaR2(*gg,*recoFSR);
      if (dR<dRMatchingCut && dR<minDR) {
	minDR=dR;
	matchIdx=j;
      }
    }
  }

  return matchIdx;
}

Float_t MCHistoryTools::getHTAll() {
  Float_t HT=0.;
  for( View<pat::PackedGenParticle>::const_iterator p = packed->begin(); p != packed->end(); ++ p ) {
    HT+=p->pt();
  }
  return HT;
}

Float_t MCHistoryTools::getHTJet() {
  Float_t HT=0.;
  for( View<GenJet>::const_iterator p = jets->begin(); p != jets->end(); ++ p ) {
    HT+=p->pt();
  }
  return HT;
}
