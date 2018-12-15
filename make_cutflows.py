import os
import glob
import fnmatch
import sys
import time

# help message
from optparse import OptionParser
usage = "python %prog <path_to_run> -n [N] -f [string]\n\n<path_to_run> should be the absolute path to the highest level of the run, on the local machine, whose contents will be directories: BKG, DY, DATA, and QCD.\nThe program will find the .tar.gz log files, extract them, and search the output for a printed cutflow, and it will aggregate the results accorss a whole dataset. The results are dumped to stdout."
parser = OptionParser(usage=usage)
parser.add_option('-n', '--num', type='int', action='store', default=18, dest='num', help='the number of lines in the cutflow')
parser.add_option('-f', '--flag', type='string', action='store', default='ran filter', dest='flag', help='the string in the output signifying that the cutflow is being printed next')
parser.add_option('--check', action='store_true', default=False, dest='check', help='instead of a full run, just print one example cutflow found in the logs')
parser.add_option('--debug', action='store_true', default=False, dest='debug', help='print messages while traversing the directory')
(options, args) = parser.parse_args()

class Dataset:
  pass

class CutflowCollection:

  def __init__(self, initial_path, num, flag): # external
    self.datasets = []
    self.num = num;
    self.flag = flag
    self.master_path = initial_path
    self.names = {}
  
  def add_dataset(self, name, locations): # external
    new_dataset = Dataset()
    new_dataset.name = name
    new_dataset.locations = locations
    new_dataset.logs = []
    self.datasets.append(new_dataset)

  def print_check(self): # external
    if len(self.datasets) == 0: print "[ERROR] Can't check cutflow because no datasets aded."
    for root, dirnames, filenames in os.walk(self.master_path):
      for dirname in dirnames:
        for location in self.datasets[0].locations:
          if dirname == location:
            tarfile,num = (self.get_logs(root + '/' + dirname))[0]
            cmd = "tar -xzf " + tarfile
            os.system(cmd)
            stdout_filename = "cmsRun-stdout-" + num + ".log"
            stderr_filename = "cmsRun-stderr-" + num + ".log"
            framwk_filename = "FrameworkJobReport-" + num + ".xml"
            stdout = open(stdout_filename,'r')
            record = False
            count = 0
            for line in stdout:
              if record:
                print line.strip()
                count = count + 1
              if count == self.num:
                record = False
              if line.strip()[0:len(self.flag)] == self.flag:
                record = True
            os.system("rm " + stdout_filename)
            os.system("rm " + stderr_filename)
            os.system("rm " + framwk_filename)
            return
            
  def traverse_for_logs(self, debug=False): # external
    for root, dirnames, filenames in os.walk(self.master_path):
      for dirname in dirnames:
        if debug: print root, dirname
        self.process(root, dirname)

  def process(self, root, dirname): # private
    for dataset in self.datasets:
      for location in dataset.locations:
        if dirname == location:
          dataset.logs = self.get_logs(root + '/' + dirname)

  def get_logs(self, path): # private
    tarfiles = []
    for root, dirnames, filenames in os.walk(path):
      for filename in fnmatch.filter(filenames, '*.tar.gz'):
        if not 'failed' in root:
          num = filename[filename.find('_')+1:filename.find('.')]
          tarfiles.append((os.path.join(root, filename),num))
    return tarfiles

  def get_names(self): # private
    if len(self.datasets) == 0: return
    dataset = self.datasets[0]
    if len(dataset.logs) == 0: return
    tarfile,num = dataset.logs[0]
    cmd = "tar -xzf " + tarfile
    os.system(cmd)
    stdout_filename = "cmsRun-stdout-" + num + ".log"
    stderr_filename = "cmsRun-stderr-" + num + ".log"
    framwk_filename = "FrameworkJobReport-" + num + ".xml"
    stdout = open(stdout_filename,'r')
    record = False
    count = 0
    for line in stdout:
      if record:
        l = line.split()
        self.names[count] = l[0]
        count = count + 1
      if count == self.num:
        record = False
      if line.strip()[0:len(self.flag)] == self.flag:
        record = True
    os.system("rm " + stdout_filename)
    os.system("rm " + stderr_filename)
    os.system("rm " + framwk_filename)

  def compute_cutflows(self, debug=False): # external
   self.get_names()
   for dataset in self.datasets:
      print "computing cutflow for", dataset.name
      dataset.cutflow = {}
      for i in range(self.num):
        dataset.cutflow[i] = 0
      for tarfile,num in dataset.logs:
        prefix = "root://cmsxrootd.fnal.gov/"
        rest_of_path = tarfile[11:len(tarfile)]
        parse = tarfile.split('/')
        tarball_filename = parse[len(parse)-1]
        print copy_cmd
        copy_cmd = "xrdcp --nopbar " + prefix + rest_of_path + "./" + tarball_filename
        cmd = "tar -xzf " + tarball_filename
        os.system(cmd)
        stdout_filename = "cmsRun-stdout-" + num + ".log"
        stderr_filename = "cmsRun-stderr-" + num + ".log"
        framwk_filename = "FrameworkJobReport-" + num + ".xml"
        if debug: print stdout_filename
        stdout = open(stdout_filename,'r')
        record = False
        count = 0
        for line in stdout:
          if record:
            l = line.split()
            dataset.cutflow[count] = dataset.cutflow[count] + int(l[1])
            count = count + 1
          if count == self.num:
            record = False
          if line.strip()[0:len(self.flag)] == self.flag:
            record = True
        os.system("rm " + stdout_filename)
        os.system("rm " + stderr_filename)
        os.system("rm " + framwk_filename)
        os.system("rm " + tarball_filename)

  def print_datasets(self): # external
    for dataset in self.datasets:
      print dataset.name, dataset.locations, len(dataset.logs), 'logs'

  def print_cutflows(self): # external
    for dataset in self.datasets:
      print dataset.name
      # this block specific to my cutflows #
      total = dataset.cutflow[0]
      total_pass = dataset.cutflow[9]
      total_reco_trigger = dataset.cutflow[3]
      ###
      for index in dataset.cutflow:
        eff = 0
        if index == 0: eff = 0
        if index >= 1 and index <= 9 and not total == 0: eff = dataset.cutflow[index]/float(total)
        if index >= 10 and index <= 16 and not dataset.cutflow[index] == 0: eff = float(total_pass)/dataset.cutflow[index]
        if index == 17 and not total_reco_trigger == 0: eff = dataset.cutflow[index]/float(total_reco_trigger)
        print "{0:<30} {1:<20,.0f} {2:<10.2%}".format(self.names[index], dataset.cutflow[index], eff)
      print ""

# main
time_start = time.time()
mycutflows = CutflowCollection(args[0], options.num, options.flag)
mycutflows.add_dataset('ttbar', ['TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'])
mycutflows.add_dataset('antitop', ['ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1'])
mycutflows.add_dataset('top', ['ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1'])
mycutflows.add_dataset('tWtop', ['ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1'])
mycutflows.add_dataset('tWantitop', ['ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1'])
mycutflows.add_dataset('wjets', ['WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'])
mycutflows.add_dataset('w1jets', ['W1JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'])
mycutflows.add_dataset('w2jets', ['W2JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'])
mycutflows.add_dataset('w3jets', ['W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'])
mycutflows.add_dataset('w4jets', ['W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'])
mycutflows.add_dataset('ww', ['WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8'])
mycutflows.add_dataset('wz1l', ['WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8'])
mycutflows.add_dataset('wz3nu', ['WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8'])
mycutflows.add_dataset('dysig', ['DY_50_ext1_signal', 'DY_50_ext2_signal'])
mycutflows.add_dataset('dybkg', ['DY_50_ext1_bkg', 'DY_50_ext2_bkg'])
mycutflows.add_dataset('dy10sig', ['DY_10to50_signal'])
mycutflows.add_dataset('dy10bkg', ['DY_10to50_bkg'])
mycutflows.add_dataset('qcd15to30', ['QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8'])
mycutflows.add_dataset('qcd30to50', ['QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8'])
mycutflows.add_dataset('qcd50to80', ['QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8'])
mycutflows.add_dataset('qcd80to120', ['QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8'])
mycutflows.add_dataset('qcd120to170', ['QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8'])
mycutflows.add_dataset('qcd170to300', ['QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8'])
mycutflows.add_dataset('qcd300to470', ['QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8'])
mycutflows.add_dataset('qcd470to600', ['QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8'])
mycutflows.add_dataset('qcd600to800', ['QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8'])
mycutflows.add_dataset('qcd800to1000', ['QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8'])
mycutflows.add_dataset('qcd1000to1400', ['QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8'])
mycutflows.add_dataset('qcd1400to1800', ['QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8'])
mycutflows.add_dataset('qcd1800to2400', ['QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8'])
mycutflows.add_dataset('qcd2400to3200', ['QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8'])
mycutflows.add_dataset('data', ['SingleMuon'])

if options.check:
  mycutflows.print_check()
  sys.exit()
mycutflows.traverse_for_logs(options.debug)
time_middle = time.time()
print "getting logs took {:.0f}".format(time_middle - time_start)
mycutflows.print_datasets()
mycutflows.compute_cutflows(options.debug)
mycutflows.print_cutflows()
time_end = time.time()
print "computing cutflows took {:.0f}".format(time_end - time_middle)
print "overall took {:.0f}".format(time_end - time_start)
