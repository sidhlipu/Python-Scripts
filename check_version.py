#!/usr/bin/python
#Description: This script is used to check the version of different Micro Services
#Input:
#       1. Filename
#               format: IP Comma separated Service Names

import sys
import os
import json
from prettytable import PrettyTable

if len(sys.argv) < 3:
        print ("Insufficient arguments provided!!")
        print ("Help:")
        print ("  "+ sys.argv[0]+" inputFile jsonFileToCompare")
        print ("Input File Format:")
        print ("IP1 Service1,Serice2,Service3")
        print ("IP2 Service1,Serice2,Service3")
        sys.exit(-1)

vListcurr=[]
vListcheck=[]
serviceCurr={'service':vListcurr}
serviceCheck={'service':vListcheck}
separator=","

#Environments to compare with
if sys.argv[2] == 'stage1':
        urlToCheck="https://qa-ma.staging1.informaticacloud.com"
elif sys.argv[2] == 'prod':
        urlToCheck="https://qa-ma.staging1.informaticacloud.com"
elif sys.argv[2] == 'stage2':
        urlToCheck="https://qa-ma.staging1.informaticacloud.com"



def check_version(h,s):
        fh=open("ver_to_check",'a')
        if s == "identity-service":
                host='.'.join(os.popen("host "+h).read().split()[-1].split(".")[:-1])
                cmdToCheck1="curl -s --connect-timeout 2  --cacert /etc/ssl/infaca/ca-bundle.pem --cert /etc/ssl/infaca/host-key-bundle.pem -s https://"+host+":16014/identity-service/mgmtapi/version"
                cmdToCheck2="curl -s "+urlToCheck+"/identity-service/mgmtapi/version"
                data1=os.popen(cmdToCheck1).read();
                data2=os.popen(cmdToCheck2).read();
                fh.write("name:"+s+"\n")
                fh.write(data2)
                fh.close()

        elif s == "ma":
                host='.'.join(os.popen("host "+h).read().split()[-1].split(".")[:-1])
                cmdToCheck1="curl -s --connect-timeout 2  --cacert /etc/ssl/infaca/ca-bundle.pem --cert /etc/ssl/infaca/host-key-bundle.pem -s https://"+host+":16016/ma/mgmtapi/version"
                cmdToCheck2="curl -s "+urlToCheck+"/ma/mgmtapi/version"
                data1=os.popen(cmdToCheck1).read()
                data2=os.popen(cmdToCheck2).read();
                fh.write("name:"+s+"\n")
                fh.write(data2)
                fh.close()
        elif s  == "content-repo":
                host='.'.join(os.popen("host "+h).read().split()[-1].split(".")[:-1])
                cmdToCheck1="curl -s --connect-timeout 2  --cacert /etc/ssl/infaca/ca-bundle.pem --cert /etc/ssl/infaca/host-key-bundle.pem -s https://"+host+":16029/content-repo/mgmtapi/version"

                cmdToCheck2="curl -s "+urlToCheck+"/content-repo/mgmtapi/version"
                data1=os.popen(cmdToCheck1).read()
                data2=os.popen(cmdToCheck2).read();
                fh.write("name:"+s+"\n")
                fh.write(data2)
                fh.close()
        elif s  == "saas":
                host='.'.join(os.popen("host "+h).read().split()[-1].split(".")[:-1])
                cmdToCheck1="curl -s --connect-timeout 2 --connect-timeout 2 --cacert /etc/ssl/infaca/ca-bundle.pem --cert /etc/ssl/infaca/host-key-bundle.pem -s  https://"+host+":16006/saas/build.txt"

                cmdToCheck2="curl -s "+urlToCheck+"/saas/build.txt"
                data1=os.popen(cmdToCheck1).read()
                data2=os.popen(cmdToCheck2).read();
                fh.write("name:"+s+"\n")
                fh.write(data2)
                fh.close()
        elif s  == "ca-service":
                host='.'.join(os.popen("host "+h).read().split()[-1].split(".")[:-1])
                cmdToCheck1="curl -s --connect-timeout 2 --cacert /etc/ssl/infaca/ca-bundle.pem --cert /etc/ssl/infaca/host-key-bundle.pem -s https://"+host+":16027/ca-service/mgmtapi/version"

                cmdToCheck2="curl -s "+urlToCheck+"/ca-service/mgmtapi/version"
                data1=os.popen(cmdToCheck1).read()
                data2=os.popen(cmdToCheck2).read();
                fh.write("name:"+s+"\n")
                fh.write(data2)
                fh.close()
        elif s  == "migration":
                host='.'.join(os.popen("host "+h).read().split()[-1].split(".")[:-1])
                cmdToCheck1="curl -s --connect-timeout 2 --cacert /etc/ssl/infaca/ca-bundle.pem --cert /etc/ssl/infaca/host-key-bundle.pem -s https://"+host+":16028/migration/mgmtapi/version"

                cmdToCheck2="curl -s "+urlToCheck+"/migration/mgmtapi/version"
                data1=os.popen(cmdToCheck1).read()
                data2=os.popen(cmdToCheck2).read();
                fh.write("name:"+s+"\n")
                fh.write(data2)
                fh.close()
        elif s  == "license-service":
                host='.'.join(os.popen("host "+h).read().split()[-1].split(".")[:-1])
                cmdToCheck1="curl -s --connect-timeout 2 --cacert /etc/ssl/infaca/ca-bundle.pem --cert /etc/ssl/infaca/host-key-bundle.pem -s https://"+host+":16035/license-service/mgmtapi/version"

                cmdToCheck2="curl -s "+urlToCheck+"/license-service/mgmtapi/version"
                data1=os.popen(cmdToCheck1).read()
                data2=os.popen(cmdToCheck2).read();
                fh.write("name:"+s+"\n")
                fh.write(data2)
                fh.close()

        elif s  == "bundle-service":
                host='.'.join(os.popen("host "+h).read().split()[-1].split(".")[:-1])
                cmdToCheck1="curl -s --connect-timeout 2 --cacert /etc/ssl/infaca/ca-bundle.pem --cert /etc/ssl/infaca/host-key-bundle.pem -s https://"+host+":16050/bundle-service/mgmtapi/version"

                cmdToCheck2="curl -s "+urlToCheck+"/bundle-service/mgmtapi/version"
                data1=os.popen(cmdToCheck1).read()
                data2=os.popen(cmdToCheck2).read();
                fh.write("name:"+s+"\n")
                fh.write(data2)
                fh.close()

        elif s  == "auditlog-service":
                host='.'.join(os.popen("host "+h).read().split()[-1].split(".")[:-1])
                cmdToCheck1="curl -s --connect-timeout 2 --cacert /etc/ssl/infaca/ca-bundle.pem --cert /etc/ssl/infaca/host-key-bundle.pem -s https://"+host+":16529/auditlog-service/mgmtapi/version"

                cmdToCheck2="curl -s "+urlToCheck+"/auditlog-service/mgmtapi/version"
                data1=os.popen(cmdToCheck1).read()
                data2=os.popen(cmdToCheck2).read();
                fh.write("name:"+s+"\n")
                fh.write(data2)
                fh.close()

        elif s  == "jls-di":
                host='.'.join(os.popen("host "+h).read().split()[-1].split(".")[:-1])
                cmdToCheck1="curl -s --connect-timeout 2 --cacert /etc/ssl/infaca/ca-bundle.pem --cert /etc/ssl/infaca/host-key-bundle.pem -s https://"+host+":16026/jls-di/mgmtapi/version"

                cmdToCheck2="curl -s "+urlToCheck+"/jls-di/mgmtapi/version"
                data1=os.popen(cmdToCheck1).read()
                data2=os.popen(cmdToCheck2).read();
                fh.write("name:"+s+"\n")
                fh.write(data2)
                fh.close()

        elif s  == "preference-service":
                host='.'.join(os.popen("host "+h).read().split()[-1].split(".")[:-1])
                cmdToCheck1="curl -s --connect-timeout 2 --cacert /etc/ssl/infaca/ca-bundle.pem --cert /etc/ssl/infaca/host-key-bundle.pem -s https://"+host+":16022/preference-service/mgmtapi/version"
                cmdToCheck2="curl -s "+urlToCheck+"/preference-service/mgmtapi/version"
                data1=os.popen(cmdToCheck1).read()
                data2=os.popen(cmdToCheck2).read();
                fh.write("name:"+s+"\n")
                fh.write(data2)
                fh.close()

        elif s  == "cloudshell":
                host='.'.join(os.popen("host "+h).read().split()[-1].split(".")[:-1])
                cmdToCheck1="curl -s --connect-timeout 2 --cacert /etc/ssl/infaca/ca-bundle.pem --cert /etc/ssl/infaca/host-key-bundle.pem -s https://"+host+":16030/cloudshell/mgmtapi/version"

                cmdToCheck2="curl -s "+urlToCheck+"/cloudshell/mgmtapi/version"
                data1=os.popen(cmdToCheck1).read()
                data2=os.popen(cmdToCheck2).read();
                fh.write("name:"+s+"\n")
                fh.write(data2)
                fh.close()

        elif s  == "kms-service":
                host='.'.join(os.popen("host "+h).read().split()[-1].split(".")[:-1])
                cmdToCheck1="curl -s --connect-timeout 2 --cacert /etc/ssl/infaca/ca-bundle.pem --cert /etc/ssl/infaca/host-key-bundle.pem -s https://"+host+":16004/kms-service/mgmtapi/version"

                cmdToCheck2="curl -s "+urlToCheck+"/kms-service/mgmtapi/version"
                data1=os.popen(cmdToCheck1).read()
                data2=os.popen(cmdToCheck2).read();
                fh.write("name:"+s+"\n")
                fh.write(data2)
                fh.close()

        elif s  == "session-service":
                host='.'.join(os.popen("host "+h).read().split()[-1].split(".")[:-1])
                cmdToCheck1="curl -s --connect-timeout 2 --cacert /etc/ssl/infaca/ca-bundle.pem --cert /etc/ssl/infaca/host-key-bundle.pem -s  https://"+host+":16015/session-service/mgmtapi/version"

                cmdToCheck2="curl -s "+urlToCheck+"/session-service/mgmtapi/version"
                data1=os.popen(cmdToCheck1).read()
                data2=os.popen(cmdToCheck2).read();
                fh.write("name:"+s+"\n")
                fh.write(data2)
                fh.close()

        elif s  == "frs":
                host='.'.join(os.popen("host "+h).read().split()[-1].split(".")[:-1])
                cmdToCheck1="curl -s --connect-timeout 2 --cacert /etc/ssl/infaca/ca-bundle.pem --cert /etc/ssl/infaca/host-key-bundle.pem -s  https://"+host+":16018/frs/mgmtapi/version"

                cmdToCheck2="curl -s "+urlToCheck+"/frs/mgmtapi/version"
                data1=os.popen(cmdToCheck1).read()
                data2=os.popen(cmdToCheck2).read();
                fh.write("name:"+s+"\n")
                fh.write(data2)
                fh.close()

        elif s  == "notification-service":
                host='.'.join(os.popen("host "+h).read().split()[-1].split(".")[:-1])
                cmdToCheck1="curl -s --connect-timeout 2 --cacert /etc/ssl/infaca/ca-bundle.pem --cert /etc/ssl/infaca/host-key-bundle.pem -s  https://"+host+":16020/notification-service/mgmtapi/version"
                cmdToCheck2="curl -s "+urlToCheck+"/notification-service/mgmtapi/version"
                data1=os.popen(cmdToCheck1).read()
                data2=os.popen(cmdToCheck2).read();
                fh.write("name:"+s+"\n")
                fh.write(data2)
                fh.close()

        elif s  == "cloudUI":
                host='.'.join(os.popen("host "+h).read().split()[-1].split(".")[:-1])
                cmdToCheck1="curl -s --connect-timeout 2 --cacert /etc/ssl/infaca/ca-bundle.pem --cert /etc/ssl/infaca/host-key-bundle.pem -s https://"+host+":16007/cloudUI/mgmtapi/version"
                cmdToCheck2="curl -s "+urlToCheck+"/cloudUI/mgmtapi/version"
                data1=os.popen(cmdToCheck1).read()
                data2=os.popen(cmdToCheck2).read();
                fh.write("name:"+s+"\n")
                fh.write(data2)
                fh.close()

        elif s  == "scheduler-service":
                host='.'.join(os.popen("host "+h).read().split()[-1].split(".")[:-1])
                cmdToCheck1="curl -s --connect-timeout 2 --cacert /etc/ssl/infaca/ca-bundle.pem --cert /etc/ssl/infaca/host-key-bundle.pem -s  https://"+host+":16019/scheduler-service/mgmtapi/version"
                cmdToCheck2="curl -s "+urlToCheck+"/scheduler-service/mgmtapi/version"
                data1=os.popen(cmdToCheck1).read()
                data2=os.popen(cmdToCheck2).read();
                fh.write("name:"+s+"\n")
                fh.write(data2)
                fh.close()

        elif s  == "channel":
                host='.'.join(os.popen("host "+h).read().split()[-1].split(".")[:-1])
                cmdToCheck1="curl -s --connect-timeout 2 --cacert /etc/ssl/infaca/ca-bundle.pem --cert /etc/ssl/infaca/host-key-bundle.pem -s  https://"+host+":16010/channel/build.txt"
                cmdToCheck2="curl -s "+urlToCheck+"/channel/build.txt"
                data1=os.popen(cmdToCheck1).read()
                data2=os.popen(cmdToCheck2).read();
                fh.write("name:"+s+"\n")
                fh.write(data2)
                fh.close()

        elif s  == "ac":
                host='.'.join(os.popen("host "+h).read().split()[-1].split(".")[:-1])
                cmdToCheck1="curl -s --connect-timeout 2 --cacert /etc/ssl/infaca/ca-bundle.pem --cert /etc/ssl/infaca/host-key-bundle.pem -s  https://"+host+":16011/ac/build.txt"
                cmdToCheck2="curl -s "+urlToCheck+"/ac/build.txt"
                data1=os.popen(cmdToCheck1).read()
                data2=os.popen(cmdToCheck2).read();
                fh.write("name:"+s+"\n")
                fh.write(data2)
                fh.close()
        else:
                print s+":Servie Not defined"
                data1=''
        return data1,data2

def generateJson(retData,s,env,h,listN):
        data=retData.split("\n")
        count=1
        d='vList'+s
        d={}
        d.update({"name":s})
        #IP of the host. If required uncomment the below line
        d.update({"host":h})
        while count < len(data)-1:
                key=data[count].split("=")[0].strip()
                value=data[count].split("=")[1].lstrip()
                d.update({key:value})
                count=count+1
                listN.append(d)
                data.pop(count)

def call_vCheck(h,s):
        fh=open("version.txt",'wb')
        for s in serviceNames:
                retData1,retData2=check_version(h,s)
                if retData1 == '' or 'html' in retData2:
                        fh.write(s+":NA")
                else:
                        generateJson(retData1,s,'curr',h,vListcurr)
                        generateJson(retData2,s,'check',h,vListcheck)






with open(sys.argv[1],'r') as f:
        for line in f.readlines():
                inHostName=line.split()[0]
                ServiceName=line.split()[1]
                serviceNames=ServiceName.split(separator)
                if os.path.isfile("version_to_check.json"):
                        os.system("rm -rf version_to_check.json")
                call_vCheck(inHostName,serviceNames)


json_string=json.dumps(serviceCurr,ensure_ascii=True)
with open('version.json', 'w') as outfile:
    outfile.write(json_string)
    outfile.close()


json_string=json.dumps(serviceCheck,ensure_ascii=True)
with open('version_to_check.json', 'w') as outfile:
    outfile.write(json_string)
    outfile.close()

with open('version_to_check.json') as json_file:
        data1=json.load(json_file)

with open('version.json') as json_file:
        data2=json.load(json_file)


print ("Name:\tStatus:\tCurrVersion:\tExpectedVersion")
for i,j in zip(data1['service'],data2['service']):
	if i['version'] == j['version']:
	    data=[]
        data=[j["name"],"Pass",j["version"],i["version"]]
        col_width = max(len(word) for row in data for word in row) + 2  # padding
        for row in data:
                print "".join(word.ljust(col_width) for word in row)
    else:
    	data=[]
        data=[j["name"],"Fail",j["version"],i["version"]]
        col_width = max(len(word) for row in data for word in row) + 2  # padding
        for row in data:
                print "".join(word.ljust(col_width) for word in row)