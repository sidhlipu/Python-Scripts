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
 hosts = list()
 hosts.append(hostname)
except IndexError:
   print "Aborting this Execution... ,Please Pass hostname as an Arg\n";
   sys.exit(1)


for hst in hosts:
 child = pexpect.spawn("ssh -l paasusr %s" %(hst))
 child.logfile = sys.stdout
 ret1 = child.expect([prompt1,prompt2,pexpect.EOF])
#print ret1
 if(ret1 == 0):
   child.sendline("yes")
   ret2 = child.expect([prompt2,pexpect.EOF])
   print ret2
   if(ret2 == 0):
    child.sendline("v2>Z6pHmq4E6Fp")
    ret8 = child.expect([prompt3,pexpect.EOF])
    if(ret8 == 0):
      child.sendline("sudo passwd daas")
      ret9 = child.expect([prompt4,pexpect.EOF])
      if(ret9 == 0):
        child.sendline("v2>Z6pHmq4E6Fp")
        ret10 = child.expect([prompt5,pexpect.EOF])
        if(ret10 == 0):
          child.sendline("v2>Z6pHmq4E6Fq")
          ret11 = child.expect([prompt6,pexpect.EOF])
          if(ret11 == 0):
            child.sendline("v2>Z6pHmq4E6Fq")
            ret12 = child.expect([prompt3,pexpect.EOF]) 
            print child.before
      
 elif(ret1 == 1):
  child.sendline("v2>Z6pHmq4E6Fp")
  ret3 = child.expect([prompt3,pexpect.EOF])
  #print ret3
  if(ret3 == 0):
    child.maxsize = 500
    child.sendline("sudo passwd daas")
    ret4 = child.expect([prompt4,pexpect.EOF])
    #print ret4
    if(ret4 == 0):
      #print child.before
      child.sendline("v2>Z6pHmq4E6Fp")
      ret5 = child.expect([prompt5,pexpect.EOF])
      #print ret5
      if(ret5 == 0):
        #print child.before
        child.sendline("v2>Z6pHmq4E6Fq")
        
        ret6 = child.expect([prompt6,pexpect.EOF])
        print ret6
        if(ret6 == 0):
          child.sendline("v2>Z6pHmq4E6Fq")
          ret7 = child.expect([prompt3,pexpect.EOF])
          #print ret7
          print child.before

