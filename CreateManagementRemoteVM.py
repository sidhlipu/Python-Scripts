#!/usr/bin/python
#Date: 26.12.2014
#Author: siddharth.mohapatra@oracle.com
#Description: This python script creates Management VM


import sys,os
import random,string,re
import subprocess
from optparse import OptionParser

#Get user defined values for ServiceName,PodName,CustomerUser,Type of Environment
parser = OptionParser(usage='usage: %prog [options] arguments')

parser.add_option('-S',help="Service Name",action="store", dest="servicename")
parser.add_option('-C',help="Customer User",action="store", dest="customeruser")
parser.add_option('-P',help="Pod Name",action="store", dest="podname")
parser.add_option('-T',help="Type of Environment",action="store", dest="type")
parser.add_option('-W',help="Provide AUTO_WORK Dirctory Path",action="store",dest="auto_work")
(options, args) = parser.parse_args()

if options.servicename is None or options.customeruser is None or options.podname is None or options.type is None or options.auto_work is None:
        parser.error('Not all arguments passed:See help')
elif options.type not in ['ucf6','ucf2c','ucf2b']:
        print "Type of Environment provided is not correct: Select any in ucf6, ucf2c, ucf2b !!"
        sys.exit()

#Default values
AUTO_WORK=options.auto_work
MediaDir=AUTO_WORK+'/media'
word_file="/usr/share/dict/words"
DataBag="/home/daas/management_data_bag_item.json"
DirSecIpIntra = '10.250.0.0/16,10.240.0.0/16'


#Create media directory under AUTO_WORK and run flaten.py script in it
os.system('mkdir -p '+MediaDir)
Flaten='cd '+MediaDir+';/ade_autofs/gd11_cloud/DAAS_MAIN_GENERIC.rdd/LATEST/daas/daas-ops/utils/daas-flatten-label.py'
os.system(Flaten)


#Unzip daas-ops-home.zip
os.chdir(AUTO_WORK)
os.system('unzip '+MediaDir+'/daas-ops-home.zip')
os.chdir(AUTO_WORK+'/daas-ops-home/daas-ops/utils/management-vm/')


#Copy the management-vm.json Template
os.system('cp '+ AUTO_WORK+ "/daas-ops-home/daas-ops/utils/management-vm/management-vm.json.TEMPLATE management-vm.json ")
ManagementJSON=AUTO_WORK+'/daas-ops-home/daas-ops/utils/management-vm/management-vm.json'


#Function to replace user-defined values in management-vm.json
def ReplaceUserInput(file,default,input):
        f1 = open(file).read()
        f2 = open(file,'w')
        r = f1.replace(default,input)
        f2.write(r)


#Function to generate 5 letter random word
words = open(word_file).read().splitlines()
def random_generator(size=5,words=words):
        return ''.join(random.choice(words) for x in range(size))


#Function to insert OG artifcats parameters in management-vm.json
def InsertValue(index,value):
        f = open(AUTO_WORK+'/daas-ops-home/daas-ops/utils/management-vm/management-vm.json', "r")
        contents = f.readlines()
        f.close()

        contents.insert(index, value)

        f = open(AUTO_WORK+'/daas-ops-home/daas-ops/utils/management-vm/management-vm.json', "w")
        contents = "".join(contents)
        f.write(contents)
        f.close()


#Generates random 5 Letter word
char=random_generator(1,words)
while len(char) != 6 :
        char=random_generator(1,words)
        char=re.sub('[-.,\']', '',char)+'1'


#Replace user-defined values in management-vm.json
hostname =options.type + '-'+options.servicename+'-'+options.podname+'-'+char.lower()+'.opcdaas.oracleinternal'+options.type+'.oraclecorp.com'
ReplaceUserInput(ManagementJSON,'PLACEHOLDER1',options.servicename)
ReplaceUserInput(ManagementJSON,'PLACEHOLDER2',options.customeruser)
ReplaceUserInput(ManagementJSON,'PLACEHOLDER3',hostname)
ReplaceUserInput(ManagementJSON,'PLACEHOLDER4',options.podname)
ReplaceUserInput(ManagementJSON,'PLACEHOLDER5','20')
ReplaceUserInput(ManagementJSON,'PLACEHOLDER6',DataBag)
ReplaceUserInput(ManagementJSON,'PLACEHOLDER7',DirSecIpIntra)

Value1='"dirOpsServerArtifactsDir" : "/home/daas/opsserver-artifacts",'
Value2='"dirOpsServerBinDir" : "/home/daas/opsserver-artifacts/bin",'
InsertValue(20,Value1)
InsertValue(24,Value2)


#Insert value as per the environment type in management-vm.json
if options.type in 'ucf2c':
        Value3='"dirOpsServerOgDir" : "/home/daas/opsserver-artifacts/ogucf2c",'
        InsertValue(29,Value3)
elif options.type in 'ucf6':
        Value3='"dirOpsServerOgDir" : "/home/daas/opsserver-artifacts/ogucf6",'
        InsertValue(29,Value3)

os.chdir(AUTO_WORK)


#SCP daas-ops-home to opsserver
subprocess.Popen(["scp","-r",'daas-ops-home' ,'daas@opsserver.opcops.oracleinternalucf6.oraclecorp.com:/home/daas/']).wait()


#Commands to be run on opsserver
host="daas@opsserver.opcops.oracleinternalucf6.oraclecorp.com"
Command="cd /home/daas;rm -rf /home/daas/opsserver-artifacts ;mkdir /home/daas/opsserver-artifacts;cd /home/daas/opsserver-artifacts;"+"ln -s /etc/og"+options.type+";ln -s /usr/local/devops/bin;cd /home/daas/daas-ops-home/daas-ops/utils/management-vm;python management-vm.py  ~/daas-ops-home/daas-ops/utils/management-vm;> /home/daas/daas-ops-home/daas-ops/utils/management-vm/output/nimbula-password;echo 'Orclization' > /home/daas/daas-ops-home/daas-ops/utils/management-vm/output/nimbula-password;export NIMBULA_USER=/opcdaas/dqa;export NIMBULA_API=https://api.oracleinternalucf2c.oraclecorp.com;cd /home/daas/daas-ops-home/daas-ops/utils/management-vm/output"#;python service-security.py setup;python pod-bringup.py setup"


#Run the defined commands on opsserver
ssh = subprocess.Popen(["ssh", "%s" % host, Command],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
while True:
    out = ssh.stdout.read(1)
    if out == '' and ssh.poll() != None:
        break
    if out != '':
        sys.stdout.write(out)
        sys.stdout.flush()

##
