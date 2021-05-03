#! /bin/sh
# source this.sh DIR_NAME
mkdir $1
cd $1
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_2_22
cd CMSSW_10_2_22/src
cmsenv
git cms-addpkg SimCalorimetry/HcalTrigPrimProducers
git cms-addpkg SimCalorimetry/HcalTrigPrimAlgos
git clone git@github.com:bchiarito/cmssw_dlphin_tpana.git MyAna
scram build
cd ../test/
git init
git remote add origin git@github.com:bchiarito/cmssw_dlphin_tptest.git
git pull origin master
ls -l
