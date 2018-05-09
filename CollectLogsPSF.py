#!/usr/bin/python
#DT: 18.01.2016
#@Siddharth.Mohapatra
#Log collection script for PSF Based Setup

import os,sys,time

NFSloc='/net/slcn09sn02/export/dtelogs/'
autowork=os.getenv('AUTO_WORK')

#Fetch DTE JobID
dteProp=os.popen("find "+autowork+" -name DTEjob.properties").read().rstrip()
if not dteProp:
        print "Unable to find DTEjob.properties"
else:
        dteJobID=os.popen("cat "+dteProp+"|grep JobReqID|awk -F= '{print $2}'").read().rstrip()


dtelogs=os.popen("find "+autowork+" -name DTE.log -type f|rev|cut -d'/' -f2-|rev").read().rstrip()

logLocation=NFSloc+"DTEJob-"+dteJobID
dteLogs=logLocation+"/DTElogs"
wlsLogs=logLocation+"/ServerLogs"
os.system("mkdir "+logLocation)
os.system("mkdir "+dteLogs)
os.system("mkdir "+wlsLogs)

#Collect DTE Logs here
os.system("cp -rfp "+dtelogs+"/* "+dteLogs)
print "Logs             Status"
print "-----------------------"
print "DTELogs          Done"


def CopyFiles(file,loc):
        logName=os.popen("echo "+file+"|cut -d/ -f6").read().rstrip()
        os.system("mkdir "+wlsLogs+"/"+logName)
        log=autowork+file
        os.system("cp -rfp "+log+" "+wlsLogs+"/"+logName)

#Collect WLS Logs here
file='/app/daasops/instance/daas_in_a_box/daasprovwlsadmin/domains/prov_domain/servers/AdminServer/logs/'
CopyFiles(file,wlsLogs)
file='/app/daasops/instance/daas_in_a_box/daasprovwlsmanaged/domains/prov_domain/servers/provclusterm01/logs/'
CopyFiles(file,wlsLogs)
file='/app/daasops/instance/daas_in_a_box/daaswlsadmin/domains/daas_domain/servers/AdminServer/logs/'
CopyFiles(file,wlsLogs)
file='/app/daasops/instance/daas_in_a_box/edq73batchwlsmanaged/domains/base_domain/servers/batchclusterm01/logs/'
CopyFiles(file,wlsLogs)
file='/app/daasops/instance/daas_in_a_box/edq73rtwlsmanaged/domains/base_domain/servers/realtimeclusterm01/logs/'
CopyFiles(file,wlsLogs)
file='/app/daasops/instance/daas_in_a_box/edq73wlsadmin/domains/base_domain/servers/AdminServer/logs/'
CopyFiles(file,wlsLogs)
file='/app/daasops/instance/daas_in_a_box/edq79wls/domains/edq_domain/servers/avclusterm01/logs/'
CopyFiles(file,wlsLogs)
file='/app/daasops/instance/daas_in_a_box/solrnode/logs/'
CopyFiles(file,wlsLogs)
file='/app/daasops/instance/daas_in_a_box/solrzookeeper/logs/'
CopyFiles(file,wlsLogs)
print "WLSLogs          Done"
print "\nLogs Collected under "+logLocation
