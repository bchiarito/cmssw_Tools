#! /bin/bash
# setup environment
export COIN_FULL_INDIRECT_RENDERING=1
export SCRAM_ARCH=slc6_amd64_gcc493
source /cvmfs/cms.cern.ch/cmsset_default.sh
# goto working directory
cd /cms/data24/chiarito/diphoton_gen/CMSSW_7_6_3/src
eval `scramv1 runtime -sh`
#Do whatever you want the script to do!
cmsRun MiniAODv2_cfg.py sample=$1 output=$2
