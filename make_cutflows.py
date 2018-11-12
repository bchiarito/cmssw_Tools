import os
import glob
import fnmatch
import sys
import time

time_begin = time.time()

NUM_CUTFLOWS = 15

# usage:
# python <this_script>.py dir_of_sample
def print_usage():
  print "give directory as arg"
  sys.exit()
if len(sys.argv) < 2:
  print_usage()

# grab all the logs
path = sys.argv[1]
tarfiles = []
for root, dirnames, filenames in os.walk(path):
  for filename in fnmatch.filter(filenames, '*.tar.gz'):
    if not 'failed' in root:
      num = filename[filename.find('_')+1:filename.find('.')]
      tarfiles.append((os.path.join(root, filename),num))

# untar and get cutflow
o = open("cutflow.txt",'w')
cutflows = {}
for i in range(NUM_CUTFLOWS):
  cutflows[i] = 0
for tar,num in tarfiles:
  cmd = "tar -xzf " + tar
  os.system(cmd)
  stdout_filename = "cmsRun-stdout-" + num + ".log"
  stderr_filename = "cmsRun-stderr-" + num + ".log"
  framwk_filename = "FrameworkJobReport-" + num + ".xml"
  print stdout_filename
  stdout = open(stdout_filename,'r')

  record = False
  count = 0
  for line in stdout:
    #print line
    if record:
      l = line.split()
      #print count, l[1]
      if count <= 7:
        cutflows[count] = cutflows[count] + int(l[1])
      if count > 7:
        cutflows[count] = cutflows[count] + int(l[2])
      count = count + 1
    if count == NUM_CUTFLOWS:
      record = False
    if line.strip()[0:10] == "ran filter":
      record = True

  os.system("rm " + stdout_filename)
  os.system("rm " + stderr_filename)
  os.system("rm " + framwk_filename)

# print the cutflow we got
for entry in cutflows: 
  print cutflows[entry]

time_end = time.time()

print "Elapsed Time: ", "%.1f" % (time_end - time_begin), "sec"
