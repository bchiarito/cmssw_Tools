#   The output can then be merged with:
#   $ cmsRun merge_cfg.py outputFile=merged.root inputFiles=file:file1.root,file:file2.root
#   Or, if many files are to be merged at once:
#   $ ls file*.root|sed 's/^/file:/'>list.txt
#   $ cmsRun merge_cfg.py outputFile=merged.root inputFiles_load=list.txt

import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing

options = VarParsing('analysis')
options.register('loginterval', 1000, mytype=VarParsing.varType.int)
options.parseArguments()

process = cms.Process("PickEvent")

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = options.loginterval

process.source = cms.Source ("PoolSource",
        fileNames = cms.untracked.vstring(options.inputFiles),
        duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
)

process.out = cms.OutputModule("PoolOutputModule",
        fileName = cms.untracked.string(options.outputFile)
)

process.end = cms.EndPath(process.out)


