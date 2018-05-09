#!/usr/bin/python
import os,glob

with open('duns') as f:
        list=f.read().splitlines()
os.system("ls *.txt|egrep -v 'results.txt|files.txt' > files.txt")

with open('files.txt') as f:
        files=f.read().splitlines()
        for f in files:
                file = open( f, 'r' )
                contents = file.read()
                for duns in list:
                        if duns in contents:
                                os.system("echo "+duns+" : "+file.name+" >> result.out")
                file.close()
