import os
import glob
import fnmatch
import sys

#returns string representations of the XS and uncertainty
def getXSAndUncert(filepath):
    f = open(filepath,'r')
    for line in f:
        s = line.split()
        if len(s) < 9:
            continue
        #elif s[0] == "Before" and s[1] == "matching:": #found the XS!
        #    xs = s[6]
        #    uncert = s[8]
        #    return (xs,uncert)
        elif s[0] == "After" and s[1] == "filter:": #found the XS!
            xs = s[6]
            uncert = s[8]
            return (xs,uncert)
    return (-1,-1)

# untar all the logs
if len(sys.argv) < 2:
  print "give directory as arg"
  sys.exit()
print 'working in', sys.argv[1]
path = sys.argv[1]
tarfiles = []
for root, dirnames, filenames in os.walk(path):
  for filename in fnmatch.filter(filenames, '*.tar.gz'):
    tarfiles.append(os.path.join(root, filename))

# make cross section txt file summary
o = open("Xsecs.txt",'w')
for tar in tarfiles:
  print tar
  cmd = "tar -xzf " + tar
  #print cmd
  os.system(cmd)
  sample = tar
  
  for f in glob.glob('./cmsRun-stdout-*.log'):
    xs,uncert = getXSAndUncert(f)
    line = "%s %s %s\n"%(sample,xs,uncert)
    o.write(line)  

  os.system('rm ./cmsRun-*')
  os.system('rm ./FrameworkJobReport*')
