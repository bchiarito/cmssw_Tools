import os
import glob
import fnmatch
import sys
import time

class Dataset:
  pass

class CutflowCollection:

  def __init__(self, initial_path, num, flag):
    self.datasets = []
    self.num = num;
    self.flag = flag
    self.master_path = initial_path
    self.names = {}
  
  def add_dataset(self, name, locations):
    new_dataset = Dataset()
    new_dataset.name = name
    new_dataset.locations = locations
    new_dataset.logs = []
    self.datasets.append(new_dataset)

  def traverse_for_logs(self, debug):
    for root, dirnames, filenames in os.walk(self.master_path):
      for dirname in dirnames:
        if debug: print root, dirname
        self.process(root, dirname)

  def process(self, root, dirname):
    for dataset in self.datasets:
      for location in dataset.locations:
        if dirname == location:
          dataset.logs = self.get_logs(root + '/' + dirname)

  def get_logs(self, path):
    tarfiles = []
    for root, dirnames, filenames in os.walk(path):
      for filename in fnmatch.filter(filenames, '*.tar.gz'):
        if not 'failed' in root:
          num = filename[filename.find('_')+1:filename.find('.')]
          tarfiles.append((os.path.join(root, filename),num))
    return tarfiles

  def get_names(self):
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

  def compute_cutflows(self):
   self.get_names()
   for dataset in self.datasets:
      print "computing cutflow for", dataset.name
      dataset.cutflow = {}
      for i in range(self.num):
        dataset.cutflow[i] = 0
      for tarfile,num in dataset.logs:
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
            dataset.cutflow[count] = dataset.cutflow[count] + int(l[1])
            count = count + 1
          if count == self.num:
            record = False
          if line.strip()[0:len(self.flag)] == self.flag:
            record = True
        os.system("rm " + stdout_filename)
        os.system("rm " + stderr_filename)
        os.system("rm " + framwk_filename)

  def print_datasets(self):
    for dataset in self.datasets:
      print dataset.name, dataset.locations, len(dataset.logs), 'logs'

  def print_cutflows(self):
    for dataset in self.datasets:
      print dataset.name
      # this block specific to my cutflows #
      total = dataset.cutflow[0]
      total_pass = dataset.cutflow[9]
      total_reco_trigger = dataset.cutflow[3]
      ###
      for index in dataset.cutflow:
        if index == 0: eff = 0
        if index >= 1 and index <= 9: eff = dataset.cutflow[index]/float(total)
        if index >= 10 and index <= 16: eff = float(total_pass)/dataset.cutflow[index]
        if index == 17: eff = dataset.cutflow[index]/float(total_reco_trigger)
        print "{0:<20} {1:<20,.0f} {2:<20.2%}".format(self.names[index], dataset.cutflow[index], eff)
      print ""

# main
mycutflows = CutflowCollection('/cms/chiarito/eos/twoprong/ztagandprobe/Nov17_trees/', 18, 'ran filter')

mycutflows.add_dataset('ttbar', ['TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'])
mycutflows.add_dataset('dysig', ['DY_50_ext1_signal_MuonHadronicFilter', 'DY_50_ext2_signal_MuonHadronicFilter'])

mycutflows.traverse_for_logs(True)

mycutflows.print_datasets()

mycutflows.compute_cutflows()

mycutflows.print_cutflows()
