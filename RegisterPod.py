import pexpect
import os
import sys
import time

prompt1 = r'\(yes\/no\)\? '
prompt2 = r'.*User Password.*'
prompt3 = r'.*[$#] '
prompt4 = r'.*password for paasusr: '
prompt5 = r'.*New password: '
prompt6 = r'.*Retype new password: '


modes = ['createMTService', 'createTenant' , 'createService']

mode = sys.argv[1];
source = sys.argv[2] + 'srvc.param'
source = source.rstrip()
inputfile = os.environ['HOME'] + '/' + source 
homedir = os.environ['HOME']
password = r'Fusionapps1' 
#logfile = sys.argv[2];
podlogfile = r'%s' % (sys.argv[3])
tenantlogfile = r'%s' % (sys.argv[4])
dumpfile = r'%s' % (sys.argv[5])
orcltenantmgrloc = sys.argv[6]
c1 = r'chmod 777 %s/%s' %(homedir,dumpfile)

 
if(mode == modes[1]):
   cmd = r'./orclTenantManager.sh mode=createTenant component=LDAP input_params=%s debug_level=ALL debug_file=%s/%s' % (inputfile, homedir,tenantlogfile)
elif(mode == modes[2]):
    cmd = r'./orclTenantManager.sh mode=createService component=LDAP input_params=%s debug_level=ALL debug_file=%s/%s' % (inputfile, homedir,podlogfile)
elif(mode == modes[0]):
    cmd = r'./orclTenantManager.sh  mode=createMTService component=LDAP input_params=%s  debug_level=ALL debug_file=%s/%s dump_file=%s/%s' % (inputfile, homedir,podlogfile,homedir,dumpfile) 
    


os.chdir("%s" % (orcltenantmgrloc))
child = pexpect.spawn(cmd)
child.logfile = sys.stdout
ret1 = child.expect([prompt2,prompt3,pexpect.EOF])
if(ret1 == 0):
   child.sendline(password)
   ret2 = child.expect([prompt2,pexpect.EOF])
   print ret2
   if(ret2 == 0):
    child.sendline(password)
    ret8 = child.expect([prompt2,pexpect.EOF])
    if(ret8 == 0):
     child.sendline(password)       
     ret9 = child.expect([prompt2,pexpect.EOF])
     if(ret9 == 0):
       child.sendline(password)
       ret10 = child.expect([prompt3,pexpect.EOF])
       if(ret10 == 0):
         print child.before
      
elif(ret1 == 1):
    print child.before

os.system(c1)
