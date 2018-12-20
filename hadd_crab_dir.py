import sys
import os
from subprocess import call
from optparse import OptionParser
import time

time_begin = time.time()

parser = OptionParser()
parser.add_option('--onefile',action='store_true',default=False,dest='onefile')
parser.add_option('--yestoall',action='store_true',default=False,dest='yestoall')
parser.add_option('--weights',action='store',default="",dest='weightfile')
(options, args) = parser.parse_args()

# Usage
# arg 1 is a mutlicrab directory
# will dump merged rootfiles into one level up from crab directory
# if onefile option is supplied, those merged rootfiles will then also be merged
# if weights file is supplied, then mergeTFileServiceHistograms is used instead with the weights

if len(args) < 1:
  sys.exit()
path = args[0]
fullpath = os.path.abspath(path)

subdirs = []
for root, dirnames, filenames in os.walk(path):
  if root == path:
    for dirname in dirnames:
      subdirs.append(dirname)

# only seems to work from here, will have to move files afterwards if different directory desired
os.chdir(fullpath+"/../")

rootfiles = []
commands = []
for subdir in subdirs:
  fullsubdir = os.path.abspath(os.path.join(path,subdir))
  ls_command = "ls -1 "+fullsubdir+"/results/*"
  rootfile = subdir+".root"
  hadd_command = "hadd "+rootfile+" `"+ls_command+"`"
  commands.append(hadd_command)
  rootfiles.append(rootfile)

for command in commands:
  print command + "\n"
if not options.yestoall:
  response = raw_input("continue with these commands (y to continue)? ")
else:
  response = "y"
if response == "y":
  for command in commands:
    call(command, shell=True)

if options.onefile and options.weightfile == "":
  hadd_command = "hadd "+path[0:len(path)]+".root "
  for rootfile in rootfiles:
    hadd_command += rootfile+" "
  print "\n" + hadd_command
  if not options.yestoall:
    response = raw_input("\ncontinue with this command (y to continue)? ")
  else:
    response = "y"
  if response == "y":
    call(hadd_command, shell=True) 
    if not options.yestoall:
      cleanup = raw_input("clean up (y for yes)? ")
    else:
      cleanup = "y"
    if cleanup == "y":
      for rootfile in rootfiles:
        print "removed file", rootfile
        os.remove(rootfile)

if options.weightfile != "":
  merge_command = "mergeTFileServiceHistograms --output-file " + path[0:len(path)] + ".root --input-files "
  for rootfile in rootfiles:
    merge_command += rootfile+" "
  weights_file = open(options.weightfile)
  weights_string = ""
  for line in weights_file:
    weights_string += line.strip()+","
  weights_string = weights_string[0:len(weights_string)-1]
  merge_command += "--weights " + weights_string
  print "\n"+merge_command
  if not options.yestoall:
    response = raw_input("\ncontinue with this command (y to continue)? ")
  else:
    response = "y"
  if response == "y":
    call(merge_command, shell=True)
    if not options.yestoall:
      cleanup = raw_input("clean up (y for yes)? ")
    else:
      cleanup = "y"
    if cleanup == "y":
      for rootfile in rootfiles:
        print "removed file", rootfile
        os.remove(rootfile)

time_end = time.time()
print "Elapsed Time: ", (time_end - time_begin)
