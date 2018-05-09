#This script automates configuration of DaaS POD against an SDI instance.
#Pre-requisite: python module 'pexpect' should be installed
#It takes 7 arguments in a file, arguments are:
#   - SDI user name to login
#   - SDI host machine name
#   - SDI user's password to login
#   - PodId to register
#   - Provisioning host machine name
#   - Provisioning server port
#   - Environment type like pool or c9
#It creates sdi.log file which contains all details.


import sys
import re
import pexpect

#pool = re.compile('slcn17vmf*',re.I)
result1 = r'\(yes\/no\)\? '
result2 = re.compile('password:',re.I)
result3 = r'.*[$#] '
result4 = re.compile(r'provisioning',re.I)
result5 = r'root*.'
result6 = r'appinfra*.'
failed = re.compile('failed',re.I)
success = re.compile('successfully',re.I)
paramdict = {}

def login(user=None,host=None,password=None,podId=None,provHost=None,provPort=None,logfile=None,envtype=None):
  child = pexpect.spawn("ssh -l %s  %s" %(user,host))
  child.logfile = logfile
  #child.logfile = open('SDI.log','w')
  try:
    ret1 = child.expect([result1,result2,pexpect.EOF])
    if(ret1 == 0):
      child.sendline("yes")
      ret2 = child.expect([result2,pexpect.EOF])
      if(ret2 == 0):  
        child.sendline(password)
        ret3 = child.expect([result3,pexpect.EOF])
        if(ret3 == 0):
          return(checkInSDI(child,host,podId,provHost,provPort,envtype))
    elif(ret1 == 1):
      child.sendline(password)
      ret3 = child.expect([result3,pexpect.EOF])
      if(ret3 == 0):
        return(checkInSDI(child,host,podId,provHost,provPort,envtype))
  except:
    print "\nUnable to login got timeout"

def checkInSDI(child=None,host=None,podId=None,provHost=None,provPort=None,envtype=None):
  if(envtype == 'pool'):
    path = '/u01/app/fmw/Oracle_SDI1/sdictl/'
    child.sendline("sudo su -")
    ret1 = child.expect([result5,pexpect.EOF])
    if(ret1 == 0):
      child.sendline("su - appinfra")
      ret2 = child.expect([result6,pexpect.EOF])
  else:
    child.sendline("setenv SDISERVER_URL http://localhost:7005")
    ret2 = child.expect([result3,pexpect.EOF])
    path = '/scratch/aime/work/CLOUDTOP/SDI/OracleHome/sdictl/'
  if(ret2 == 0):
    child.sendline("%ssdictl.sh listpod | grep -i %s" % (path,podId))
    try:
      ret1 = child.expect(result4,timeout=60)
      if(ret1 == 0):
        print "\n\nPod exists "
        print ret1
        return(deleteInSDI(child,podId,path,provHost,provPort))
    except:
      print "\n\n Exception occured pod not found"
      print child.before
      return(RegisterInSDI(child,podId,path,provHost,provPort))

def deleteInSDI(child=None,podId=None,path=None,provHost=None,provPort=None):
  child.sendline("%ssdictl.sh rmpod -PodId %s" % (path,podId))
  try:
    ret1 = child.expect([failed,success])
    if(ret1 == 1):
      print "\n\n **** will register again"
      return(RegisterInSDI(child,podId,path,provHost,provPort))
    elif(ret1 == 0):
      child.sendline("%ssdictl.sh updatepod -podId %s -addconstraint OPC_ORDER:+DO_NOT_MATCH" % (path,podId))
      ret2 = child.expect([failed,success])
      if(ret2 == 1):
        print "\n\n **** will register again"
        return(RegisterInSDI(child,podId,path,provHost,provPort))
      elif(ret2 == 0):
        print "\n\n Pod already exists with tenants\n"+child.before
        return 0
  except:
    print "\n\nException occured due to timeout or EOF issue"
    print child.before


def RegisterInSDI(child=None,podId=None,path=None,provHost=None,provPort=None):
  child.sendline('%ssdictl.sh addexternalpod -serviceType "Data" -provisioningURI http://%s:%s/data/admin/provisioning -PodID "%s"' % (path,provHost,provPort,podId))
  try:
    ret1 = child.expect([success,pexpect.EOF])
    if(ret1 == 0):
      child.close()
      print "\n\nRegistered successfully"
      return 1
  except:
    print "\n\nSome error occurred while registering pod or timeout\n"
    print child.before
    return 0
  
#login("aime","slc03ttc.us.oracle.com","2cool","dummy101") #c9
#output = login("aime","slcn17vmf0159.c9dev1.oraclecorp.com","2cool","dummy101",dummy,1001) #pool 3
#print "\nScript reslut "+str(output)
#login("aime","slcn17vmf0109.c9dev1.oraclecorp.com","2cool","dummy101") #pool 2



if( __name__ == '__main__'):
  if(len(sys.argv) != 2):
    print "\nSome argument missing or extra. Found "+str(len(sys.argv))+" arguments"
    print "\nUsage: python sdi.py sdi_config"
  else:
    print sys.argv[1]
    param_fp = open(sys.argv[1],"r")
    paramNum = 0
    for line in param_fp:
      line = line.strip("\n")
      if line:
         if not line.startswith("#"):  
            paramdict[line.split("=")[0].strip()] = line.split("=")[1].strip()
            paramNum = paramNum + 1
            print paramNum 
    #if(paramNum != 7):
     # print "\nSome mandatory options missing or extra. Found "+str(paramNum)+" arguments"
     # sys.exit(127)
    try:
      logfile = open("sdi.log","w")
    except IOError:
      print "\nCan't  create log file ....redirecting log to /tmp/sdi.log";
      logfile = open("/tmp/sdi.log","w")
    logfile.truncate()
    sys.stdout = logfile
    sys.stderr = logfile
    print paramdict
    # user=sys.argv[1]
    # SDIhost=sys.argv[2]
    # SDIpass=sys.argv[3]
    # podId=sys.argv[4]
    # provHost=sys.argv[5]
    # provPort=sys.argv[6]
    response = login(paramdict['user'],paramdict['SDIhost'],paramdict['SDIpass'],paramdict['podId'],paramdict['provHost'],paramdict['provPort'],logfile,paramdict['envtype'])
    logfile.close()
    sys.stdout = sys.__stdout__
    if(response == 1):
      print "\n****************    Registering Successful *****************\n"
    else:
      print "\n****************   Some error occured please check sdi.log *****************\n"
