import sys
import io
from optparse import OptionParser
parser = OptionParser()
parser.add_option('--l1', metavar='F', type='string', action='store',
                  dest='list1', default="",
                  help='')
parser.add_option('--l2', metavar='F', type='string', action='store',
                  dest='list2', default="",
                  help='')
parser.add_option('--l3', metavar='F', type='string', action='store',
                  dest='list3', default="",
                  help='')
(options, args) = parser.parse_args()

print "\nShared between list 1 and list 2, not list 3:\n"
file1 = open(options.list1)
for line1 in file1:
  file2 = open(options.list2)
  for line2 in file2:
    if line1.split()[0] == line2.split()[0]:
      skip = False
      file3 = open(options.list3)
      for line3 in file3:
        if line1.split()[0] == line3.split()[0]:
          skip = True
      if not skip:
        print line1.split()[0], line1.split()[1], line2.split()[1]
raw_input()

print "\nShared between list 1 and list 3, not list 2:\n"
file1 = open(options.list1)
for line1 in file1:
  file3 = open(options.list3)
  for line3 in file3:
    if line1.split()[0] == line3.split()[0]:
      skip = False
      file2 = open(options.list2)
      for line2 in file2:
        if line1.split()[0] == line2.split()[0]:
          skip = True
      if not skip:
        print line1.split()[0], line1.split()[1], line3.split()[1]
raw_input()

print "\nShared between list 2 and list 3, not list 1:\n"
file2 = open(options.list2)
for line2 in file2:
  file3 = open(options.list3)
  for line3 in file3:
    if line2.split()[0] == line3.split()[0]:
      skip = False
      file1 = open(options.list1)
      for line1 in file1:
        if line2.split()[0] == line1.split()[0]:
          skip = True
      if not skip:
        print line2.split()[0], line2.split()[1], line3.split()[1]
raw_input()

print "\nShared between all three:\n"
file1 = open(options.list1)
for line1 in file1:
  file2 = open(options.list2)
  for line2 in file2:
    file3 = open(options.list3)
    for line3 in file3:
      if line1.split()[0] == line2.split()[0] and line2.split()[0] == line3.split()[0]:
        print line1.split()[0], line1.split()[1], line2.split()[1], line3.split()[1]
raw_input()

print "\nExclusive to list 1:\n"
file1 = open(options.list1)
for line1 in file1:
  file2 = open(options.list2)
  infile2 = False
  infile3 = False
  for line2 in file2:
    file3 = open(options.list3)
    for line3 in file3:
      if line1.split()[0] == line2.split()[0]:
        infile2 = True
      if line1.split()[0] == line3.split()[0]:
        infile3 = True
  if not infile2 and not infile3:
    print line1.strip()
raw_input()

print "\nExclusive to list 2:\n"
file2 = open(options.list2)
for line2 in file2:
  file1 = open(options.list1)
  infile1 = False
  infile3 = False
  for line1 in file1:
    file3 = open(options.list3)
    for line3 in file3:
      if line2.split()[0] == line1.split()[0]:
        infile1 = True
      if line2.split()[0] == line3.split()[0]:
        infile3 = True
  if not infile1 and not infile3:
    print line2.strip()
raw_input()

print "\nExclusive to list 3:\n"
file3 = open(options.list3)
for line3 in file3:
  file1 = open(options.list1)
  infile1 = False
  infile2 = False
  for line1 in file1:
    file2 = open(options.list2)
    for line2 in file2:
      if line3.split()[0] == line1.split()[0]:
        infile1 = True
      if line3.split()[0] == line2.split()[0]:
        infile2 = True
  if not infile1 and not infile2:
    print line3.strip()
raw_input()
