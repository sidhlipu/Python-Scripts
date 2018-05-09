#!/usr/bin/python

'''
 Oracle Corp Jul 10, 2017
'''

import subprocess, os, socket, sys, datetime, time, threading
from random import shuffle



#********************** Properties to edit - Start ********************

genNumber = '66'
targetHostnames = [
 'us2z11-daas-datasvc07-p27snode011.data.z11.usdc2.oraclecloud.com',
 'us2z11-daas-datasvc07-p27snode021.data.z11.usdc2.oraclecloud.com',
 'us2z11-daas-datasvc07-p27snode031.data.z11.usdc2.oraclecloud.com',
 'us2z11-daas-datasvc07-p27snode041.data.z11.usdc2.oraclecloud.com', 
 'us2z11-daas-datasvc07-p27snode051.data.z11.usdc2.oraclecloud.com',
 'us2z11-daas-datasvc07-p27snode061.data.z11.usdc2.oraclecloud.com',
 'us2z11-daas-datasvc07-p27snode071.data.z11.usdc2.oraclecloud.com',
 'us2z11-daas-datasvc07-p27snode081.data.z11.usdc2.oraclecloud.com'


]

#********************** Properties to edit - End  *********************



def runCurl(ip, cmd, logfile):
  errFile = open(logfile,'a+')
  start = time.time()

  cmd = 'curl --silent --fail -X GET "http://'+ip+ cmd
  print cmd
  returnValue = subprocess.call(cmd, shell=True, stderr=errFile)

  if returnValue ==  0:
    errFile.write("CURL STATUS OK FOR :: "+ip)
  else:
    errFile.write("CURL STATUS FAILED FOR :: "+ip)
  errFile.write("\nTIME TAKEN : "+str(round(time.time() - start,3))+" Secs \n\n")
  errFile.write("**********************************************************************************************\n")
  errFile.close()



emailrecipients = "keerthy.jayaraj@oracle.com, kirti.b.das@oracle.com, tom.enderes@oracle.com, venkatasubramanian.jayaraman@oracle.com, raju.borkakoty@oracle.com, surya.kavuluri@oracle.com, harisha.shankaramurthy@oracle.com, siddharth.mohapatra@oracle.com, suneelkumar.nalagala@oracle.com"
companycmd = ':7575/solr/dnb_company_us_'+ genNumber +'_shard1_replica1/select?q=*:*&collection=dnb_company_us_'+ genNumber +',dnb_company_others_'+ genNumber + '"'
contactcmd = ':7575/solr/dnb_contact_others_'+ genNumber +'_shard1_replica1/select?q=*:*&collection=dnb_contact_others_' + genNumber + '"'
outfile = '/tmp/curlOut.txt'

#emailrecipients = 'keerthy.jayaraj@oracle.com'


###### Triggering contact collection checks
with open(outfile,'a+') as f:
 f.write('                             CONTACT RESULTS         \n\n')
shuffle(targetHostnames)
[runCurl(host,contactcmd,outfile) for host in targetHostnames]


###### Triggering company collection checks
with open(outfile,'a+') as f:
 f.write('\n\n\n\n\n')
 f.write('                             COMPANY RESULTS          \n\n')
shuffle(targetHostnames)
[runCurl(host,companycmd, outfile) for host in targetHostnames]


###### Sending email
emailcmd = "mail -r cdc-z12-solr-monitor@oracle.com -s \"Solr CURL Query Status from CDC Z12 @ $(date)\" keerthy.jayaraj@oracle.com " + emailrecipients + "  < " + outfile
ret = subprocess.call(emailcmd, shell=True)
os.remove(outfile)


