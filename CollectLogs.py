#!/usr/bin/python
#DT: 18.01.2016
#@Siddharth.Mohapatra
#Log collection script for Nimbula Based Setup

import os,sys,time
import pexpect,re



podname=sys.argv[1]
type=sys.argv[2]
user='paasusr'
password='v2>Z6pHmq4E6Fp'
daasuser='daas'
daaspasswd='v2>Z6pHmq4E6Fq'
NFSloc='/net/slcn09sn02/export/dtelogs/'
#NFSloc='/home/oracle/scripts/logcollector/'
autowork=os.getenv('AUTO_WORK')
if type == 'base':
        dtelogs=os.popen("find "+autowork+" -name Createpod_Base -type d|rev|cut -d'/' -f2-|rev").read().rstrip()
else:
        dtelogs=os.popen("find "+autowork+" -name copyfiles_patch -type d|rev|cut -d'/' -f2-|rev").read().rstrip()

#Fetch DTE JobID
dteProp=os.popen("find "+autowork+"/oracle/work/ -name DTEjob.properties").read().rstrip()
if not dteProp:
        print "Unable to find DTEjob.properties"
else:
        dteJobID=os.popen("cat "+dteProp+"|grep JobReqID|awk -F= '{print $2}'").read().rstrip()
dataloc=NFSloc+"DTEJob-"+dteJobID+"/"+type
dataloc1=dataloc+"/DTElogs"
dataloc2=dataloc+"/ServerLogs"

os.system("mkdir -p "+dataloc1)
os.system("mkdir -p "+dataloc2)

result1 = r'\(yes\/no\)\? '
result2 = r'.*password:'
result3 = r'.*[$#] '
result5 = r'[sudo] password for paasusr '
result4 = r'.*~]#*.'

def login(user,podname,password):
        child = pexpect.spawn("ssh -l %s %s" %(user,podname),timeout=300)
        try:
                ret1 = child.expect([result1,result2,pexpect.EOF])
                if(ret1 == 0):
                        child.sendline("yes")
                        ret2 = child.expect([result2,result3,pexpect.EOF])
                        if(ret2 == 0):
                                child.sendline(password)
                                ret3 = child.expect([result3,pexpect.EOF])
                                if(ret3 == 0):
                                        return(SSHRunCommand(child,user,podname,password))
                elif(ret1 == 1):
                        child.sendline(password)
                        ret3 = child.expect([result3,pexpect.EOF])
                        if(ret3 == 0):
                                (SSHRunCommand(child,user,podname,password))

        except Exception as e:
                print e
                print "\n1.Unable to login got timeout"

def ScpCommands(file,podname,password,user,dataloc):
        child = pexpect.spawn('scp -q -r %s@%s:%s %s ' % (user,podname,file,dataloc),timeout=None)
        i = child.expect(['password:', r'\(yes\/no\)', r"yes/no",r'.*password for paasusr: ',r'.*[$#] '])
        if i == 0:
               child.sendline(password)
        elif i == 1:
                child.sendline("yes")
                child.expect("password:")
                child.sendline(password)
        data = child.read()



def SSHRunCommand(child,user,podname,password):
        child.sendline("sudo su -")
        child.sendline(password)
        child.expect([result4,pexpect.EOF])
        child.sendline("rm -rf /u01/data/chef.log")
        child.expect([result4,pexpect.EOF])
        child.sendline("cp /var/log/chef.log /u01/data")
        child.expect([result4,pexpect.EOF])
        child.sendline("chown paasusr:devops /u01/data/chef.log ")
        child.expect([result4,pexpect.EOF])

def CollectDaaSLogs():
        print "Copying logs from "+podname+"\n"
        response = login(user,podname,password)
        file='/u01/data/chef.log'
        loc=dataloc2+'/ChefLog'
        ScpCommands(file,podname,password,user,loc)
        print "chef.log                         copied"
        file='/u01/app/daasprovwlsadmin/domains/prov_domain/servers/AdminServer/logs/'
        loc=dataloc2+'/daasprovadmin/'
        ScpCommands(file,podname,daaspasswd,daasuser,loc)
        print "daasprovwlsadmin logs            copied"
        file='/u01/app/daasprovwlsmanaged/domains/prov_domain/servers/provclusterm01/logs/'
        dataloc=dataloc2+'/daasprovmanaged/'
        ScpCommands(file,podname,daaspasswd,daasuser,loc)
        print "daasprovwlsmanaged logs  copied"
        file='/u01/app/daaswlsadmin/domains/daas_domain/servers/AdminServer/logs/'
        loc=dataloc2+'/daaswlsadmin/'
        ScpCommands(file,podname,daaspasswd,daasuser,loc)
        print "daaswlsadmin logs                copied"
        file='/u01/app/edq73batchwlsmanaged/domains/base_domain/servers/batchclusterm01/logs/'
        loc=dataloc2+'/batchclusterm01/'
        ScpCommands(file,podname,daaspasswd,daasuser,loc)
        print "batchclusterm01 logs             copied"
        file='/u01/app/edq73rtwlsmanaged/domains/base_domain/servers/realtimeclusterm01/logs/'
        loc=dataloc2+'/realtimeclusterm01/'
        ScpCommands(file,podname,daaspasswd,daasuser,loc)
        print "realtimeclusterm01 logs  copied"
        file='/u01/app/edq73wlsadmin/domains/base_domain/servers/AdminServer/logs/'
        loc=dataloc2+'/edq73wlsadmin/'
        ScpCommands(file,podname,daaspasswd,daasuser,loc)
        print "edq73wlsadmin logs               copied"
        file='/u01/app/edq79wls/domains/edq_domain/servers/avclusterm01/logs/'
        loc=dataloc2+'/avclusterm01/'
        ScpCommands(file,podname,daaspasswd,daasuser,loc)
        print "avclusterm01 logs                copied"
        file='/u01/app/solrbootstrapnode/logs/'
        loc=dataloc2+'/solrbootstrapnode/'
        ScpCommands(file,podname,daaspasswd,daasuser,loc)
        print "solrbootstrapnode logs           copied"
        file='/u01/app/solrnode/logs/'
        loc=dataloc2+'/solrnode/'
        ScpCommands(file,podname,daaspasswd,daasuser,loc)
        print "solrnode logs                    copied"
        file='/u01/app/solrzookeeper/logs/'
        dataloc=dataloc2+'/solrzookeeper/'
        ScpCommands(file,podname,daaspasswd,daasuser,loc)
        print "solrzookeeper logs               copied"


if( __name__ == '__main__'):
  if(len(sys.argv) != 3):
    print "\nSome argument missing or extra. Found "+str(len(sys.argv))+" arguments"
    print "\nUsage: python hostname type[base/patch]"
  else:
        try:
                response = os.system("ping -c2 "+podname+" > /dev/null 2>&1")
                if response != 0:
                        print "\nDaaS Pod not reachable !!"
                        print "Collecting DTE logs only"
                        os.system("cp -r "+dtelogs+"/* "+dataloc1)
                        print "DTE logs                 copied"
                        print "\nAll logs copied under "+dataloc
                else:
                        CollectDaaSLogs()
                        os.system("cp -r "+dtelogs+"/* "+dataloc1)
                        print "DTE logs"
                        print "\nAll logs copied under "+dataloc
        except Exception as e:
                print e
                print "Failed to copy some logs"
