import pexpect
import os
import sys
import time

prompt1 = r'\(yes\/no\)\? '
prompt2 = r'password: '
prompt3 = r'.*[$#] '
prompt4 = r'.*password for paasusr: '
prompt5 = r'.*New password: '
prompt6 = r'.*Retype new password: '


#hosts = open("qahosts.txt", "r").readlines()
#hosts.sort()

try:
 hostname = sys.argv[1];
 #hosts = list()
 #hosts.append(hostname)
 user = sys.argv[2];
 password = sys.argv[3];
 destdir = sys.argv[5];
 sourcedir = sys.argv[4];
 
 cmd = r'scp -r %s@%s:%s %s/' % (user,hostname,sourcedir,destdir)
except IndexError:
   print "Aborting this Execution... ,Please Pass hostname as an Arg\n";
   sys.exit(1)


#for hst in hosts:
child = pexpect.spawn(cmd)
child.logfile = sys.stdout
ret1 = child.expect([prompt1,prompt2,pexpect.EOF])
if(ret1 == 0):
   child.sendline("yes")
   ret2 = child.expect([prompt2,pexpect.EOF])
   print ret2
   if(ret2 == 0):
    child.sendline(password)
    ret8 = child.expect([prompt3,pexpect.EOF])
    if(ret8 == 0):
            print child.before
      
elif(ret1 == 1):
  child.sendline(password)
  ret3 = child.expect([prompt3,pexpect.EOF])
  #print ret3
  if(ret3 == 0):
    child.maxsize = 500
    print child.before

