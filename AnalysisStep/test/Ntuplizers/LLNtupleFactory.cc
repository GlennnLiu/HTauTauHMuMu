#include <cassert>
#include <iostream>

#include "LLNtupleFactory.h"

/*
bool addKinRefit = false;
bool addVtxFit = false;
bool writePhotons = false;  // Write photons in the tree. Must be set also in LLNtupleMaker.cc
*/
using namespace std;

LLNtupleFactory::LLNtupleFactory(TTree* outTree_input, TTree *failedTree_input)
{
  //---- create output tree ----
  _outTree = outTree_input;
  _failedTree = failedTree_input;
  /*
  cout<<"Factory!"<<endl;
  for(int i=0;i<99;i++){
     intVector[i]=0;
  shortVector[i]=0;
   boolVector[i]=0;
   longVector[i]=0;
   charVector[i]=0;
   floatVector[i]=0;
  //vectorVector[i]=0;
  }
  //std::vector<float> defaultVector[6];
  //std::vector<TString> nameVector[7];

  cout<<"end factory"<<endl;
  
  for(int i=0;i<7;i++)nBranches[i]=0;
*/
  //InitializeVariables();
  
  //_firstZStored = false;
  //_LeptonIndex = 1;
  //_LeptonIsoIndex = 1;

}

///--- Destructor ---
LLNtupleFactory::~LLNtupleFactory()
{
  // Delete me_branches branches
//  for (unsigned int ib=0; ib<recome_branches.size(); ib++) delete recome_branches.at(ib);
//  for (unsigned int ib=0; ib<lheme_branches.size(); ib++) delete lheme_branches.at(ib);
}

///---- Write an event to TTree ----
void LLNtupleFactory::FillCurrentTree(bool passed)
{
  if (passed)
    _outTree->Fill();
  else if (_failedTree)
    _failedTree->Fill();
}
void LLNtupleFactory::FillEvent(bool passed)
{
  FillCurrentTree(passed);
  InitializeVariables(); // Reset all values and clean vectors
}

///---- Write to a text file branches declaration ----
void LLNtupleFactory::DumpBranches(TString filename) const
{
  //----- symply use MakeClass
  _outTree->MakeClass(filename);
  return;
}

void LLNtupleFactory::Book(TString name, Float_t &variable, bool putinfailedtree){
  TString leafname=name.Data();
  leafname.Append("/F");
  defaultsFloat[&variable] = variable; // defaultT is a map<T*, value>
  _outTree->Branch(name.Data(), &variable, leafname.Data());
  if (putinfailedtree && _failedTree)
    _failedTree->Branch(name.Data(), &variable, leafname.Data());
}
void LLNtupleFactory::Book(TString name, Int_t &value, bool putinfailedtree){
  TString leafname=name.Data();
  leafname.Append("/I");
  defaultsInt[&value] = value; // defaultT is a map<T*, value>
  _outTree->Branch(name.Data(), &value, leafname.Data());
  if (putinfailedtree && _failedTree)
    _failedTree->Branch(name.Data(), &value, leafname.Data());
}
void LLNtupleFactory::Book(TString name, Bool_t &value, bool putinfailedtree){
  TString leafname=name.Data();
  leafname.Append("/O");
  defaultsBool[&value] = value; // defaultT is a map<T*, value>
  _outTree->Branch(name.Data(), &value, leafname.Data());
  if (putinfailedtree && _failedTree)
    _failedTree->Branch(name.Data(), &value, leafname.Data());
}
void LLNtupleFactory::Book(TString name, Short_t &value, bool putinfailedtree){
  TString leafname=name.Data();
  leafname.Append("/S");
  defaultsShort[&value] = value; // defaultT is a map<T*, value>
  _outTree->Branch(name.Data(), &value, leafname.Data());
  if (putinfailedtree && _failedTree)
    _failedTree->Branch(name.Data(), &value, leafname.Data());
}
void LLNtupleFactory::Book(TString name, Long64_t &value, bool putinfailedtree){
  TString leafname=name.Data();
  leafname.Append("/L");
  defaultsLong[&value] = value; // defaultT is a map<T*, value>
  _outTree->Branch(name.Data(), &value, leafname.Data());
  if (putinfailedtree && _failedTree)
    _failedTree->Branch(name.Data(), &value, leafname.Data());
}
void LLNtupleFactory::Book(TString name, Char_t &value, bool putinfailedtree){
  TString leafname=name.Data();
  leafname.Append("/B");
  defaultsChar[&value] = value; // defaultT is a map<T*, value>
  _outTree->Branch(name.Data(), &value, leafname.Data());
  if (putinfailedtree && _failedTree)
    _failedTree->Branch(name.Data(), &value, leafname.Data());
}
void LLNtupleFactory::Book(TString name, std::vector<float> &value, bool putinfailedtree){
  defaultsVectorFloat[&value] = value; // defaultT is a map<T*, value>
  _outTree->Branch(name.Data(), &value);
  if (putinfailedtree && _failedTree)
    _failedTree->Branch(name.Data(), &value);
}
void LLNtupleFactory::Book(TString name, std::vector<short> &value, bool putinfailedtree){
  defaultsVectorShort[&value] = value;
  _outTree->Branch(name.Data(), &value);
  if (putinfailedtree && _failedTree)
    _failedTree->Branch(name.Data(), &value);
}
void LLNtupleFactory::Book(TString name, std::vector<char> &value, bool putinfailedtree){
  defaultsVectorChar[&value] = value;
  _outTree->Branch(name.Data(), &value);
  if (putinfailedtree && _failedTree)
    _failedTree->Branch(name.Data(), &value);
}
void LLNtupleFactory::Book(TString name, std::vector<bool> &value, bool putinfailedtree){
  defaultsVectorBool[&value] = value;
  _outTree->Branch(name.Data(), &value);
  if (putinfailedtree && _failedTree)
    _failedTree->Branch(name.Data(), &value);
}


void LLNtupleFactory::InitializeVariables()
{
 for (auto it = defaultsFloat.begin(); it != defaultsFloat.end(); ++it ) *(it->first) = it->second;
 for (auto it = defaultsInt.begin(); it != defaultsInt.end(); ++it ) *(it->first) = it->second;
 for (auto it = defaultsBool.begin(); it != defaultsBool.end(); ++it ) *(it->first) = it->second;
 for (auto it = defaultsShort.begin(); it != defaultsShort.end(); ++it ) *(it->first) = it->second;
 for (auto it = defaultsLong.begin(); it != defaultsLong.end(); ++it ) *(it->first) = it->second;
 for (auto it = defaultsChar.begin(); it != defaultsChar.end(); ++it ) *(it->first) = it->second;
 for (auto it = defaultsVectorFloat.begin(); it != defaultsVectorFloat.end(); ++it ) it->first->clear();
 for (auto it = defaultsVectorShort.begin(); it != defaultsVectorShort.end(); ++it ) it->first->clear();
 for (auto it = defaultsVectorChar.begin(); it != defaultsVectorChar.end(); ++it ) it->first->clear();
 for (auto it = defaultsVectorBool.begin(); it != defaultsVectorBool.end(); ++it ) it->first->clear();

// for (unsigned int ib=0; ib<recome_branches.size(); ib++) recome_branches.at(ib)->reset();
// for (unsigned int ib=0; ib<lheme_branches.size(); ib++) lheme_branches.at(ib)->reset();

/*
  for(int i=0;i<nBranches[kBool];i++){boolVector[i]=defaultVector[kBool].at(i);}
  for(int i=0;i<nBranches[kShort];i++){shortVector[i]=defaultVector[kShort].at(i);}
  for(int i=0;i<nBranches[kInt];i++){intVector[i]=defaultVector[me_brancheskInt].at(i);}
  for(int i=0;i<nBranches[kChar];i++){charVector[i]=defaultVector[kChar].at(i);}
  for(int i=0;i<nBranches[kLong];i++){longVector[i]=defaultVector[kLong].at(i);}
  for(int i=0;i<nBranches[kFloat];i++){floatVector[i]=defaultVector[kFloat].at(i);}
  for(int i=0;i<nBranches[kVectorFloat];i++){vectorVector[i].clear();}
*/
}

/*
void LLNtupleFactory::createNewCandidate()
{
  _firstZStored = false;
  _LeptonIndex = 1;
  _LeptonIsoIndex = 1;

  return;
}
*/


