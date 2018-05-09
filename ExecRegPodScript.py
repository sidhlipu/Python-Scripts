import pexpect
import os
import sys
import time
import re

prompt1 = r'\(yes\/no\)\? '
prompt2 = r'[Pp]assword: '
prompt3 = r'.*[$#] '
prompt4 = r'.*password for aime: '
prompt5 = r'.*New password: '
prompt6 = r'.*Retype new password: '

#hosts = open("qahosts.txt", "r").readlines()
#hosts.sort()

def readsrvcparam(filename):
   sep = r":"
   logfiles = list()
   data = {}
   fp = open(filename, "r")
   line = fp.readline()
   while(line):
      line = line.rstrip()
      print line
      data[re.sub(r'\s','',line.rstrip().split(sep,1)[0])] = re.sub(r'\s','',line.rstrip().split(sep,1)[1])
      line = fp.readline()
   podname = data['IDSTORE_SERVICE_NAME']
   podlogfile  = data['IDSTORE_SERVICE_NAME'] + '_' + 'logfile.out'
   tenantlogfile = data['IDSTORE_TENANT_NAME'] + '_' + 'logfile.out'
   poddumpfile = data['IDSTORE_SERVICE_NAME']  + '.dmp'
   logfiles.append(podname)
   logfiles.append(podlogfile)
   logfiles.append(tenantlogfile)
   logfiles.append(poddumpfile)
   return logfiles




wheretolog = readsrvcparam('/net/%s/%s/tmpsrvcparam' % (sys.argv[1],sys.argv[2]))
print wheretolog
#sys.exit(0)





try:
 hostname = sys.argv[1]
 homedir = sys.argv[2]
 mode = sys.argv[3]
 user = sys.argv[4]
 syspassword = sys.argv[5]
 orcltenantmgrloc = sys.argv[6]
 syspassword = syspassword.rstrip()
 syspassword = syspassword.lstrip()
 hosts = list()
 hosts.append(hostname)
except IndexError:
   print "Aborting this Execution... ,Please Pass hostname as an Arg\n";
   sys.exit(1)


for hst in hosts:
 child = pexpect.spawn("ssh -l %s  %s" %(user,hst))
 child.logfile = sys.stdout
 ret1 = child.expect([prompt1,prompt2,pexpect.EOF])
#print ret1
 if(ret1 == 0):
   child.sendline("yes")
   ret2 = child.expect([prompt2,pexpect.EOF])
   print ret2
   if(ret2 == 0):
    child.sendline(syspassword)
    ret8 = child.expect([prompt3,pexpect.EOF])
    if(ret8 == 0):
      child.sendline("python %s/RegisterPod.py %s %s %s %s %s %s" % (homedir,mode,wheretolog[0],wheretolog[1],wheretolog[2],wheretolog[3],orcltenantmgrloc))
      ret9 = child.expect([prompt3,pexpect.EOF])
      if(ret9 == 0):
            print child.before
      
 elif(ret1 == 1):
  child.sendline(syspassword)
  ret3 = child.expect([prompt3,pexpect.EOF])
  #print ret3
  if(ret3 == 0):
    child.maxsize = 500
    child.sendline("python %s/RegisterPod.py %s %s %s %s %s %s" % (homedir,mode,wheretolog[0],wheretolog[1],wheretolog[2],wheretolog[3],orcltenantmgrloc))
    ret4 = child.expect([prompt3,pexpect.EOF])
    #print ret4
    if(ret4 == 0):
          print child.before

