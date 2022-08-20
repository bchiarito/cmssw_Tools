from ROOT import *
import sys

f = TFile(sys.argv[1])
tree = f.Get("diphotonAnalyzer/fTree2")
names = [b.GetName() for b in tree.GetListOfBranches()]
for name in names:
  print name
