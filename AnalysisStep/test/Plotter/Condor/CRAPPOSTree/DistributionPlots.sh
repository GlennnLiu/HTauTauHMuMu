#!/bin/sh

export CMSSW_VERSION=CMSSW_10_6_26;
export SCRAM_ARCH=slc7_amd64_gcc700;
source /cvmfs/cms.cern.ch/cmsset_default.sh

cd /afs/cern.ch/user/g/geliu/LepUni_incl/CMSSW_10_6_26/src/
cmsenv
ulimit -s unlimited
mkdir /eos/home-g/geliu/LepUni/Histos/UL2016/DistributionPlots/CRAPPOSTree.Plots
DistributionPlots --region CRAPPOSTree --addData