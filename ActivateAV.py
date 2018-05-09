#!/usr/bin/python

import os,sys
import fileinput,re


avdumpfile=sys.argv[1]
daasbox=sys.argv[2]
daasinsdir=sys.argv[3]

if len(sys.argv) < 4 :
        sys.exit(-1)

os.system("cp "+avdumpfile+" "+avdumpfile+".backup")
dumpfile=avdumpfile+".backup"

for line in fileinput.input(dumpfile, inplace=True):
        line = re.sub('DAASBOX',daasbox, line.rstrip())
        print(line)
os.system("cp "+dumpfile+" "+daasinsdir+"/instances/instance1/config/OHS/ohs1/mod_wl_ohs.conf")
os.system("cp "+dumpfile+" "+daasinsdir+"/mod_wl_ohs.conf")
