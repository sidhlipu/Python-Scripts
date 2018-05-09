from fabric.api import *
import pexpect
env.user='daas'
env.password= r'v2>Z6pHmq4E6Fq'
env.timeout = 30 
#env.user='oracle'
#env.password="welcome1"
env.disable_known_hosts = True
env.skip_bad_hosts = True
env.warn_only = True






def EditCur(srvr,dnbuser):
   #srvr = "slcn09vmf0235.us.oracle.com"
   cmd = "sed -i  s/server/%s/ common.properties  && sed -i s/port/7005/ common.properties  && sed -i s/username/%s/ common.properties"%(srvr,dnbuser) 
   #print cmd
   with cd("/u01/app/install_wls/Oracle/Middleware/daashome/curator-console/resources"):
         #sudo(cmd,user="daas",shell=True,pty=True)
         run(cmd)







def Execdataload(srvr,dnbuser,dnbpasswd):
   #srvr = "slcn09vmf0235.us.oracle.com"
   cmd = 'java -jar DaaSCuratorConsole.jar -o create -w DbmrdDnBCompCont -s %s -p 7005 -u %s -pwd %s  -st "2013-11-11 12:00:00" -et "2013-11-11 12:00:00" -c "now" -d "Every Friday at 9.00pm starting 2013 ending 2014" -wfId 11 ' % (srvr,dnbuser,dnbpasswd)
   #cmd = 'java -jar DaaSCuratorConsole.jar -o create -w DbmrdDnBCompCont -s %s -p 7005 -u %s -pwd %s  -st "2013-11-11 12:00:00" -et "2013-11-11 12:00:00" -c "now" -d "Every Friday at 9.00pm starting 2013 ending 2014" -wfId 11 -t dtetenant01' % (srvr,dnbuser,dnbpasswd)
#print cmd

   with cd("/u01/app/install_wls/Oracle/Middleware/daashome/curator-console"):
     #sudo(cmd,user="daas",shell=True,pty=True)
     run(cmd)





def checkdataload(dnbpasswd):
   #srvr = "slcn09vmf0235.us.oracle.com"
   cmd = 'java -jar DaaSCuratorConsole.jar -o list  -pwd %s  -status RUNNING' %(dnbpasswd) 

   with cd("/u01/app/install_wls/Oracle/Middleware/daashome/curator-console"):
     #sudo(cmd,user="daas",shell=True,pty=True)
     run(cmd)




def checkcompletetasks():
   srvr = "slcn09vmf0235.us.oracle.com"
   cmd = 'java -jar DaaSCuratorConsole.jar -o list  -pwd Tzhgauwn4y_5di  -status COMPLETED' 

   with cd("/u01/oracle/work/app/install_wls/Oracle/Middleware/daashome/curator-console"):
     run(cmd)



