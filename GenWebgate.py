#!/usr/bin/env python

import sys,os
import pexpect

user = sys.argv[1]
password = sys.argv[2]
host = sys.argv[3]
rpath = sys.argv[4]
lpath = sys.argv[5]






def doScp(user, password, host, rpath, lpath):
        child = pexpect.spawn('scp -r %s@%s:%s %s' % (user,host,rpath,lpath))
        
        i = child.expect(['password:', r"yes/no",pexpect.EOF])
        if i == 0:
                child.sendline(password)
        elif i == 1:
                child.sendline("yes")
                child.expect("password:", timeout=30)
                child.sendline(password)
        data = child.read()
        print data
        child.close()
        
        
doScp(user, password, host, rpath, lpath)





