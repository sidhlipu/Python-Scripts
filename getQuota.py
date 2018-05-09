#!/usr/bin/python
#Checks Nimbula Quota
#Sidharth.Mohapatra@oracle.com

import os,sys
import re
import smtplib
from email.mime.text import MIMEText

value=sys.argv[1]
submitter=sys.argv[2]
auto_work=os.getenv("AUTO_WORK")
NimbPassword='Orclization'
NimbFile = open(auto_work+'/password.file','w')
NimbFile.write(NimbPassword)
NimbFile.close()


os.chmod(auto_work+'/password.file',0400)
os.system('wget -q --output-document='+auto_work+'/quota.txt http://slc05vpf.us.oracle.com:8080/job/opc.psr-compute-service-quotamanager-ucf2c/lastSuccessfulBuild/artifact/mail.account.usage.totals.txt')
QuotaFile = open(auto_work+'/quota.txt','r')

for line in QuotaFile:
        if 'opcdaas' in line:
                if '.com' not in line:
                        Qtotal = int(line.split('|')[1])
QusedDQA = int(os.popen("nimbula-api -a https://api.oracleinternalucf2c.oraclecorp.com/ -u /opcdaas/dqa  -fcsv -Fname,status  list instance /opcdaas/dqa -p "+auto_work+"/password.file|grep -v name|wc -l").read())
QusedDir=int(os.popen("nimbula-api -a https://api.oracleinternalucf2c.oraclecorp.com/ -u /opcdaas/dqa  -fcsv -Fname,status  list instance /opcdaas/dir -p "+auto_work+"/password.file|grep -v name|wc -l").read())
Qused = int(QusedDQA + QusedDir)
os.remove(auto_work+'/password.file')

#Send failure mail
def SendMail(message):
        Subject = 'DaaS Installation Failed !!'
        fromaddr = 'daas.DTE@oracle.com'
        recipients = submitter.split(',')
        MESSAGE_FORMAT = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s"
        text = MESSAGE_FORMAT%('', ', '.join(recipients) , Subject, message)
        s = smtplib.SMTP('localhost')
        #s.set_debuglevel(1)
        s.sendmail(fromaddr, recipients,text)
        s.quit()

#Check if the file is present or not
def checkQuota():
        if os.path.isfile(auto_work+"/quota.txt"):
                Qavailable = Qtotal - Qused
                if Qavailable <= int(value):
                        print "Nimbula Quota not enough to start DaaS Patching!!"
                        print "Available: " + str(Qavailable) + " Required: ",value
                        message = """Nimbula Quota not enough to start DaaS Installation!!
Available: """+ str(Qavailable) + """ Required: """+value
                        SendMail(message)
                        sys.exit(-1)
                else:
                        print "Total quota available is :", Qavailable," Continuing .."
        else:
                print "Unable to retrive quota"
                sys.exit(-1)

checkQuota()
