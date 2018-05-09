#!/usr/bin/python
#@siddharth.mohapatra@oracle.com
#This script takes care of cleaning up multi-node environment setup

import os,sys
MultinodePath="/misc/common_multinode"
hosts={}
with open(MultinodePath+'/hosts','r') as f:
        for line in f:
                hosts[line.strip().split('=')[0]]=line.strip().split('=')[1]
print sorted(hosts.values(),reverse=True)
def child(host):
   os.system("ssh "+host+" 'chkconfig autofs on;service autofs stop;reboot'")
   os._exit(0) # else goes back to parent loop

def runClean():
    for host in sorted(hosts.values(),reverse=True):
        newpid = os.fork()
        if newpid == 0:
            child(host)
        else:
            print('Started cleaning on '+host+' with pid:',host,newpid)
            var1=os.wait()
            if var1[1] == 0:
                print "Success"
os.system("rm -rf "+MultinodePath+"/work/*")
os.system("rm -rf "+MultinodePath+"/tmp/*")
os.system("rm -rf "+MultinodePath+"/cookbook/*")
runClean()
