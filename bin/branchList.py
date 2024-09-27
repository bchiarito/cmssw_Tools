#!/usr/bin/env python3
from ROOT import *
import sys
import os
import glob
import argparse

parser = argparse.ArgumentParser(description="", usage="./%(prog)s INPUT")
parser.add_argument("input", metavar='INPUT',help="rootfile or directory with one or more rootfiles")
parser.add_argument("-s", "--string", default="", metavar='PATTERN',help="matching pattern")
parser.add_argument("-t", "--tree", default='Events', metavar='PATH',help="path to TTree in TFile")
args = parser.parse_args()

inputPath = args.input
if os.path.isfile(inputPath):
  fi = args.input
elif os.path.isdir(inputPath):
  owd = os.getcwd()
  fi = None
  os.chdir(inputPath)
  for f in glob.glob("*.root"):
    fi = inputPath+'/'+f
    break
  if fi==None: raise SystemExit("No rootfiles in directory!")
  os.chdir(owd)
else:
  raise SystemExit("Input is neither a file nor a directory!")

f = TFile(fi)
tree = f.Get(args.tree)
names = [b.GetName() for b in tree.GetListOfBranches()]
for name in names:
  if args.string in name: print(name)
