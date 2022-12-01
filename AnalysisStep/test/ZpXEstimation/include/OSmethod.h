#ifndef OSmethod_h
#define OSmethod_h

// C++
#include <iostream>
#include <fstream>
#include <iomanip> // For setprecision
#include <vector>
#include <map>

// ROOT
#include "TApplication.h"
#include "TStyle.h"
#include "TCanvas.h"
#include "TChain.h"
#include "TFile.h"
#include "TString.h"
#include "TStyle.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TH3F.h"
#include "TLegend.h"
#include "TGraphErrors.h"
#include "TGraph2DErrors.h"
#include "TMultiGraph.h"
#include "TROOT.h"
#include "TSystem.h"
#include "TLorentzVector.h"
#include "THStack.h"

// Include classes
#include <HTauTauHMuMu/AnalysisStep/test/ZpXEstimation/include/Tree.h>
#include <HTauTauHMuMu/AnalysisStep/test/ZpXEstimation/include/Settings.h>
#include <HTauTauHMuMu/AnalysisStep/test/ZpXEstimation/include/Plots.h>
//#include <HTauTauHMuMu/AnalysisStep/interface/Category.h>
#include <HTauTauHMuMu/AnalysisStep/interface/FinalStates.h>
#include <HTauTauHMuMu/AnalysisStep/test/ZpXEstimation/include/FakeRates.h>
#include <HTauTauHMuMu/AnalysisStep/interface/bitops.h>
#include <HTauTauHMuMu/AnalysisStep/test/ZpXEstimation/include/CMS_lumi.h>
#include <HTauTauHMuMu/AnalysisStep/interface/TauIDSFTool.h>

using namespace std;

const int num_of_processes         = Settings::num_of_processes;
const int num_of_flavours          = Settings::num_of_flavours;
const int num_of_final_states      = Settings::num_of_final_states;
//const int num_of_categories        = Settings::num_of_categories;
//const int num_of_categories_stxs   = Settings::num_of_categories_stxs;
const int num_of_regions_os        = Settings::num_of_regions_os;
const int num_of_eta_bins          = Settings::num_of_eta_bins;
const int num_of_fake_rates        = Settings::num_of_fake_rates;
const int num_of_fr_variations     = Settings::num_of_fr_variations;

class OSmethod: public Tree
{

public:
	
	OSmethod();
	~OSmethod();
   
   void FillFRHistos( TString );
   void FillDataMCPlots( TString );
   void MakeHistogramsZX( TString, TString );
   void MakeZXMCContribution( TString, TString );
   void SaveFRHistos( TString, bool, bool );
   void SaveDataMCHistos( TString );
   void SaveZXHistos( TString , bool );
   void GetFRHistos( TString );
   void GetDataMCHistos( TString );
   void GetZXHistos( TString );
   void PrintZXYields();
   void PlotDataMC_2P2F( TString, TString );
   void PlotDataMC_3P1F( TString, TString );
   void PlotDataMC( TString, TString );
   void PlotZXContributions( TString );
   void FitZX( TString );
   void ProduceFakeRates( TString );
   void Set_pT_binning( int, float* );
   void Set_MET_binning( int, float* );
   void SetLumi( float );
   
private:
   
   void DeclareFRHistos();
   void DeclareDataMCHistos();
   void DeclareZXHistos();
   void SubtractWZ( );
   void RemoveNegativeBins1D( TH1F* );
   void RemoveNegativeBins2D( TH2F* );
   void RemoveNegativeBins3D( TH3F* );
   void FillDataMCInclusive();
   void FillZXInclusive( bool );
   int find_current_process( TString );
   int FindFinalState();
   float calculate_K_factor( TString );
   int GENMatch(int, TString );
   float calculate_TauIDSF_OneLeg(short, float, float, int, int, bool);
   float calculate_TauIDSF(TString, bool);
   bool GetVarLogX( TString );
   bool GetVarLogY( TString );
   void SavePlots( TCanvas*, TString );
   void PlotFR();
   TLegend* CreateLegend_FR( string , TH1F*, TH1F*,TH1F*,TH1F* );
   TLegend* CreateLegend_FR_tau( string , TH2F*, TH2F*,TH2F*,TH2F* , TH2F*, TH2F*,TH2F*,TH2F* );
   TLegend* CreateLegend_ZXcontr( string , TH1F*, TH1F*,TH1F*,TH1F*,TH1F* );
   TLegend* CreateLegend_2P2F( string , TH1F*, TH1F*,TH1F*,TH1F*,TH1F* );
   TLegend* CreateLegend_3P1F( string , TH1F*, TH1F*,TH1F*,TH1F*,TH1F* ,TH1F*);

   TFile *input_file, *input_file_data;
   TFile *fOutHistos;
   TTree *input_tree, *input_tree_data;

   TH1F *hCounters;
   
   Long64_t n_gen_events;
   
   vector<string> _s_process, _s_flavour, _s_final_state, _s_category, _s_category_stxs, _s_region, _s_variation;
   TString _histo_name, _histo_labels;
   
   float jetPt[99];
   float jetEta[99];
   float jetPhi[99];
   float jetMass[99];
   float jetQGL[99];
   float jetPgOverPq[99];
   
   float _pT_bins[99], _MET_bins[99];
   
   int _current_process, _current_final_state, _current_category, _current_category_stxs, _n_pT_bins, _n_MET_bins;
   float _lumi, _yield_SR, _k_factor, _TauIDSF;
   double gen_sum_weights, _event_weight, _f3, _f4, _f3_Up, _f3_Dn, _f4_Up, _f4_Dn;
   vector< vector <float> > _expected_yield_SR, _number_of_events_CR;

   TH1F *histos_1D[num_of_regions_os][num_of_processes][num_of_final_states];//[num_of_categories_stxs];
   TH1F *histos_ZX[num_of_fr_variations][num_of_final_states];//[num_of_categories_stxs];
   TH1F *h_from2P2F_SR[num_of_fr_variations][num_of_final_states];//[num_of_categories_stxs];
   TH1F *h_from2P2F_3P1F[num_of_fr_variations][num_of_final_states];//[num_of_categories_stxs];
   TH1F *h_from3P1F_SR_final[num_of_fr_variations][num_of_final_states];//[num_of_categories_stxs];
   TH1F *h_from3P1F_SR[num_of_fr_variations][num_of_final_states];//[num_of_categories_stxs];
   TH1F *h_from3P1F_SR_ZZonly[num_of_fr_variations][num_of_final_states];//[num_of_categories_stxs];
   
   TH3F *passing[num_of_processes][num_of_flavours], *failing[num_of_processes][num_of_flavours];
   
   TH1F *FR_OS_electron_EB, *FR_OS_electron_EE, *FR_OS_muon_EB, *FR_OS_muon_EE;
   TH2F *FR_OS_tauE_Decay0, *FR_OS_tauE_Decay1, *FR_OS_tauE_Decay10, *FR_OS_tauE_Decay11, *FR_OS_tauMu_Decay0, *FR_OS_tauMu_Decay1, *FR_OS_tauMu_Decay10, *FR_OS_tauMu_Decay11, *FR_OS_tauTau_Decay0, *FR_OS_tauTau_Decay1, *FR_OS_tauTau_Decay10, *FR_OS_tauTau_Decay11;
   TH1F *FR_OS_electron_EB_unc, *FR_OS_electron_EE_unc, *FR_OS_muon_EB_unc, *FR_OS_muon_EE_unc;
   TH2F *FR_OS_tauE_Decay0_unc, *FR_OS_tauE_Decay1_unc, *FR_OS_tauE_Decay10_unc, *FR_OS_tauE_Decay11_unc, *FR_OS_tauMu_Decay0_unc, *FR_OS_tauMu_Decay1_unc, *FR_OS_tauMu_Decay10_unc, *FR_OS_tauMu_Decay11_unc, *FR_OS_tauTau_Decay0_unc, *FR_OS_tauTau_Decay1_unc, *FR_OS_tauTau_Decay10_unc, *FR_OS_tauTau_Decay11_unc;
//    TMultiGraph *mg_electrons, *mg_muons;//, *mg_tauE, *mg_tauMu, *mg_tauTau;
   
//    vector<Float_t> vector_X[num_of_fake_rates][num_of_eta_bins][num_of_flavours];
//    vector<Float_t> vector_Y[num_of_fake_rates][num_of_eta_bins][num_of_flavours];
//    vector<Float_t> vector_EX[num_of_fake_rates][num_of_eta_bins][num_of_flavours];
//    vector<Float_t> vector_EY[num_of_fake_rates][num_of_eta_bins][num_of_flavours];
  
   TauIDSFTool *DeepTauSF_VSe_ETau, *DeepTauSF_VSmu_ETau, *DeepTauSF_VSjet_ETau, *DeepTauSF_VSe_MuTau, *DeepTauSF_VSmu_MuTau, *DeepTauSF_VSjet_MuTau, *DeepTauSF_VSe_TauTau, *DeepTauSF_VSmu_TauTau, *DeepTauSF_VSjet_TauTau, *DeepTauSF_VSe_bare, *DeepTauSF_VSmu_bare, *DeepTauSF_VSjet_bare;
 
};
#endif
