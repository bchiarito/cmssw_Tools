import sys
import os
import glob
import fnmatch
import time

time_begin = time.time()

path = sys.argv[1]
if len(sys.argv) > 2:
  out = sys.argv[2]
else:
  out = ''

print path

tarfiles = []
for root, dirnames, filenames in os.walk(path):
  for filename in fnmatch.filter(filenames, '*.tar.gz'):
    tarfiles.append(os.path.join(root, filename))

for tar in tarfiles:
  print tar
  cmd = "tar -xzf " + tar
  os.system(cmd)

os.system('rm ./cmsRun-stderr-*.log')
os.system('rm ./cmsRun-stdout-*.log')

fjr2json_command = 'fjr2json.py --output=fjr2json_output_%s_json.txt ./FrameworkJobReport-*.xml' % out

os.system(fjr2json_command)

os.system('rm ./FrameworkJobReport-*.xml')

time_end = time.time()

print "Elapsed Time: ", "%.1f" % (time_end - time_begin), "sec"
