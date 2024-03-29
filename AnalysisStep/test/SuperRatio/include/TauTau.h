#ifndef TauTau_h
#define TauTau_h

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
#include "TLegend.h"
#include "TGraphErrors.h"
#include "TMultiGraph.h"
#include "TROOT.h"
#include "TSystem.h"
#include "TLorentzVector.h"
#include "THStack.h"
#include "TF1.h"
#include "TMath.h"

#include <HTauTauHMuMu/AnalysisStep/test/SuperRatio/include/Settings.h>
#include <HTauTauHMuMu/AnalysisStep/interface/FinalStates.h>
#include <HTauTauHMuMu/AnalysisStep/interface/bitops.h>
#include <HTauTauHMuMu/AnalysisStep/test/SuperRatio/include/Plots.h>
// #include <HTauTauHMuMu/AnalysisStep/interface/TauIDSFTool.h>
#include <HTauTauHMuMu/AnalysisStep/test/SuperRatio/include/Tree.h>
#include <HTauTauHMuMu/AnalysisStep/test/SuperRatio/include/CMS_lumi.h>

using namespace std;

const int num_of_final_states      = 1;
const int num_of_categories        = 5;
const int num_of_fr_variations     = Settings::num_of_fr_variations;
const int num_of_njet_bins         = 3;
const int num_of_fake_bkg          = 1;

class TauTau: public Tree
{

public:
    TauTau();
    ~TauTau();
    
    void SetPaths(string,string,string);
    void SetFileList(string*,int,string*,int);
    
    void Set_taupt_bin(int, float*);
    void Set_lpt_bin(int, float*);
    void Set_Mvis_bin(int, float*,bool);
    void Set_MT_bin(int, float*);
    void Set_DR_bin(int, float*);

    void Step1_FakeRate_DeclareHistos();
    void Step1_FakeRate_FillHistos();
    void Step1_FakeRate_Compute();
    void Step1_FakeRate_SaveHistos();
    void Step1_FakeRate_GetHistos();

    void Step2_Closure_DeclareHistos();
    void Step2_Closure_FillHistos();
    void Step2_Closure_Compute();
    void Step2_Closure_SaveHistos();
    void Step2_Closure_GetHistos();

    void Step3_QCD_FakeRate_DeclareHistos();
    void Step3_QCD_FakeRate_FillHistos();
    void Step3_QCD_FakeRate_Compute();
    void Step3_QCD_FakeRate_SaveHistos();
    void Step3_QCD_FakeRate_GetHistos();

    void Step3_QCD_Closure_DeclareHistos();
    void Step3_QCD_Closure_FillHistos();
    void Step3_QCD_Closure_Compute();
    void Step3_QCD_Closure_SaveHistos();
    void Step3_QCD_Closure_GetHistos();

    void Step3_QCD_vsSR_DeclareHistos();
    void Step3_QCD_vsSR_FillHistos();
    void Step3_QCD_vsSR_Compute();
    void Step3_QCD_vsSR_SaveHistos();
    void Step3_QCD_vsSR_GetHistos();

private:
    int FindFinalState();
    int FindCategory();
    float calculate_K_factor(TString);
    void SetColor(TH1F*,int);
    TString ToFSName(string);
    TString ToProcessName(string);
    void DoDivision(TH1F*, TH1F*, TH1F*, bool);
    int NumberOfJets();

    string _path, _file_name, _savepath;
    vector<string> _dataFiles, _MCBkgFiles;
    vector<string> _s_process, _s_final_state, _s_categories, _s_fake_bkg, _s_variables;
    int _current_process, _current_final_state, _current_category, _current_njet_bin, _pass;
    float _lumi, _k_factor;
    double gen_sum_weights, _event_weight;

    float _taupt_bins[99], _lpt_bins[99], _Mvis_fine_bins[99], _Mvis_bins[99];
    int _n_taupt_bins, _n_lpt_bins, _n_Mvis_fine_bins, _n_Mvis_bins;
    
    TFile *input_file, *output_file;
    TTree *input_tree;
    TH1F *hCounters;

    TH1F *h_tmp;
    
    //step 1
    TH1F *h[num_of_fake_bkg][num_of_final_states][num_of_njet_bins][2];
    TH1F *h_FR[num_of_fake_bkg][num_of_final_states][num_of_njet_bins];
    TF1 *f_FR[num_of_fake_bkg][num_of_final_states][num_of_njet_bins];

    //step 2
    TH1F *hClosure[num_of_fake_bkg][num_of_final_states][2];
    TH1F *hClosure_FR[num_of_fake_bkg][num_of_final_states];
    TF1 *fClosure_FR[num_of_fake_bkg][num_of_final_states];

    //step 3
    TH1F *hQCD[num_of_final_states][num_of_njet_bins][2];
    TH1F *hQCD_FR[num_of_final_states][num_of_njet_bins];
    TF1 *fQCD_FR[num_of_final_states][num_of_njet_bins];

    TH1F *hQCDClosure[num_of_final_states][2];
    TH1F *hQCDClosure_FR[num_of_final_states];
    TF1 *fQCDClosure_FR[num_of_final_states];

    TH1F *hQCDvsSR[num_of_final_states][2];
    TH1F *hQCDvsSR_FR[num_of_final_states];
    TF1 *fQCDvsSR_FR[num_of_final_states];

    TString _histo_name, _histo_labels;
    
};
#endif