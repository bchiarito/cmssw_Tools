import sys
import os
import fnmatch

# this script will generate commands to copy an entire areas of cmslpc eos, and will create the local directory structure necesary as well

got_path = sys.argv[1]

# get initial list of files
files_to_copy = []
for root, dirnames, filenames in os.walk(got_path):
  print root
  for filename in fnmatch.filter(filenames, '*.root'):
    if not 'failed' in root:
      print "got a file", filename
      files_to_copy.append(os.path.join(root, filename))
      
# generate mkdir command
mkdir_commands = []
top_level_dirs = ['DY', 'BKG', 'DATA', 'QCD']
for fi in files_to_copy:
  command = "mkdir -p "
  parsed_path = fi.split('/')
  append = False
  for chunk in parsed_path:
    if chunk in top_level_dirs:
      append = True
    if append:
      command += '/' + chunk
  mkdir_commands.append(command)

for command in mkdir_commands:
  print command

