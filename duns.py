#!/usr/bin/python

import os
import base64
import json
import shutil

csvfile=raw_input("Enter the CSV Filename :: ")
propfile=raw_input("Enter the property filename!!:: ")
dict= {}

with open(propfile,'r+') as f:
        for line in f:
                (key, val) = line.split('=')
                dict[(key)] = val.split('\n')[0]
daasuri = dict['DAAS_URI']+'/data/api/v2/search/companies/'
daasuser = dict['DAAS_USERNAME']
daaspasswd = dict['DAAS_PASSWORD']
daastenant = dict['DAAS_TENANT_ID']
daasservice = dict['DAAS_SERVICE_NAME']
encoded = base64.b64encode(daasuser+':'+daaspasswd)


tempFile= 'temp.csv'
with open(csvfile,'r') as f:
        head = f.readline().rstrip()
        header = head + ',Duns#\n'
        rest = ''.join(f.readlines())
        f.close
        p = open(tempFile,'w')
        p.write(header)
        p.write(rest)
        p.close()
os.remove(csvfile)
os.rename(tempFile,csvfile)

tempFile1='mytest.csv'
p = open(tempFile1,'w')

with open(csvfile,'r') as f:
        for line in f:
                listread=line.split(',')
                lastword=listread[-1].rstrip()
                if 'Duns#' in lastword:
                        #Do nothing
                        p.write(line)
                        p.close()
                else:
                        daasurl=daasuri+lastword
                        curlCommand = 'curl -s -X GET -H "X-ORACLE-DAAS-SERVICE-NAME: '+daasservice+'" -H "X-USER-IDENTITY-DOMAIN-NAME: '+daastenant+'" -H "X-ID-TENANT-NAME: '+daastenant+'" -H "Content-Type: application/json" -H "Accept: application/json" -H "Authorization: Basic '+encoded+'" -H "Cache-Control: no-cache" -H "Postman-Token: 255bf149-ada4-b6d9-1703-e79819a41c2f" \''+daasurl+'\''
                        test = os.popen(curlCommand)
                        with test as f:
                                data=json.load(f)
                        dunsnumber=data['dunsNumber']
                        newVal=line.rstrip()+','+str(dunsnumber)+'\n'
                        p = open(tempFile1,'a')
                        p.write(newVal)
                        p.close()

#os.remove(csvfile)
#shutil.copy(tempFile1,csvfile)
#os.remove(tempFile1)