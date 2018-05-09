#!/usr/bin/python
#Date: 26.12.2014
#Author: siddharth.mohapatra@oracle.com
#Description: This python script creates Management VM
#Takes 9 arguments from user input/command line:
#       1. ServiceName      2. Customer User  3. Pod Name    4. Type of Environment
#       5. Chef Server Name 6. Chef User name 7. Chef Passwd 8. Service User Passwd 9. NIMBULA API

import sys,os
import random,string,re
import pexpect,socket
from optparse import OptionParser

#Get user defined values
parser = OptionParser(usage='usage: %prog [options] arguments')

parser.add_option('-s',help="Service User",action="store", dest="servicename")
parser.add_option('-u',help="Customer User",action="store", dest="customeruser")
parser.add_option('-n',help="Pod Name",action="store", dest="podname")
parser.add_option('-t',help="Type of Environment",action="store", dest="type")
parser.add_option('-c',help="Chef Server name",action="store",dest="chefserver")
parser.add_option('-p',help="Service Password",action="store",dest="passwd")
parser.add_option('--cp',help="Chef Password",action="store",dest="chefpasswd")
parser.add_option('--cu',help="Chef User",action="store",dest="chefuser")
parser.add_option('--api',help="Nimbula API",action="store",dest="nimbulaapi")

(options, args) = parser.parse_args()

if options.servicename is None or options.customeruser is None or options.podname is None or options.type is None or  options.chefserver is None or options.passwd is None or options.chefpasswd is None or options.chefuser is None or options.nimbulaapi is None:
        parser.error('Not all arguments passed:See -h or --help')
elif options.type not in ['ucf6','ucf2c','ucf2b']:
        print "\nType of Environment provided is not correct: Select any in ucf6, ucf2c, ucf2b !!"
        sys.exit()

#Get Local systems IP Range
ip= socket.gethostbyname(socket.gethostname())
iprange=ip.split('.')[0]+'.'+ip.split('.')[1]+".0.0"

#Getting info about AUTO_WORK
if os.getenv('AUTO_WORK') is None:
        print "\nAUTO_WORK not set in env. Default setting it to  /scratch/aime/work !!"

#######SETTING AUTO_WORK=/u01/test/work for testing purpose, else it will be /scratch/aime/work when Live !!
        AUTO_WORK="/u01/test/work"
else:
        print "\nAUTO_WORK set to .."+os.getenv('AUTO_WORK')
        AUTO_WORK=os.getenv('AUTO_WORK')


#Default values
#AUTO_WORK='/u01/test'
MediaDir=AUTO_WORK+'/media'
word_file="/usr/share/dict/words"
DataBag=AUTO_WORK+"/app/managementvm/opsserver_artifacts/management_data_bag_item.json"
DirSecIpIntra = "10.250.0.0/16,10.240.0.0/16,"+iprange+"/16"
dirManagementVmServerDataSize = '40'


#Unzip daas-ops-home.zip
os.chdir(AUTO_WORK)
if os.path.isdir(AUTO_WORK+'/app/daas-ops-home') is True:
        print "\ndaas-ops-home is present under "+AUTO_WORK+"/app/daas-ops-home continuing !!"
else:
        os.system('mkdir '+AUTO_WORK+'/app')
#       os.system('cp '+MediaDir+'/daas-ops-home.zip '+AUTO_WORK+'/app')
        os.chdir(AUTO_WORK+'/app')
        os.system('unzip '+MediaDir+'/daas-ops-home.zip')
        os.chdir(AUTO_WORK+'/app/daas-ops-home/daas-ops/utils/management-vm/')


#Copy the management-vm.json Template
os.system('mkdir '+AUTO_WORK+'/app/managementvm')
os.system('cp '+ AUTO_WORK+'/app/daas-ops-home/daas-ops/utils/management-vm/management-vm.json.TEMPLATE '+AUTO_WORK+'/app/managementvm/management-vm.json')
ManagementJSON=AUTO_WORK+'/app/managementvm/management-vm.json'

#Create ops-server artifacts directory
os.system('mkdir '+AUTO_WORK+'/app/managementvm/opsserver_artifacts')

#Function to replace user-defined values in management-vm.json
def ReplaceUserInput(file,default,input):
        f1 = open(file).read()
        f2 = open(file,'w')
        r = f1.replace(default,input)
        f2.write(r)


#Function to generate 5 letter random word
words = open(word_file).read().splitlines()
def random_generator(size=5,words=words):
        return ''.join(random.choice(words) for x in range(size))+'1'


#Function to insert OG artifcats parameters in management-vm.json
def InsertValue(index,value):
        f = open(AUTO_WORK+'/app/managementvm/management-vm.json', "r")
        contents = f.readlines()
        f.close()

        contents.insert(index, value)

        f = open(AUTO_WORK+'/app/managementvm/management-vm.json', "w")
        contents = "".join(contents)
        f.write(contents)
        f.close()


#Generates random 5 Letter word
char=random_generator(1,words)
while len(char) != 6 :
        char=random_generator(1,words)
        char=re.sub('[-.,\']', '',char)

#Let's do SCP files from chef server
def doScp(user,password, host, path, files):
        child = pexpect.spawn('scp -r %s@%s:%s %s' % (user,host,path,files))
        i = child.expect(['assword:', r"yes/no"], timeout=30)
        if i == 0:
                child.sendline(password)
        elif i == 1:
                child.sendline("yes")
                child.expect("assword:", timeout=30)
                child.sendline(password)
        data = child.read()
        print data
        child.close()


#Replace user-defined values in management-vm.json
hostname =options.type + '-'+options.chefuser+'-'+options.podname+'-'+char.lower()+'.'+options.servicename+'.oracleinternal'+options.type+'.oraclecorp.com'
ReplaceUserInput(ManagementJSON,'PLACEHOLDER1',options.chefuser)
ReplaceUserInput(ManagementJSON,'PLACEHOLDER2',options.customeruser)
ReplaceUserInput(ManagementJSON,'PLACEHOLDER3',hostname)
ReplaceUserInput(ManagementJSON,'PLACEHOLDER4',options.podname)
ReplaceUserInput(ManagementJSON,'PLACEHOLDER5',dirManagementVmServerDataSize)
ReplaceUserInput(ManagementJSON,'PLACEHOLDER6',DataBag)
ReplaceUserInput(ManagementJSON,'PLACEHOLDER7',DirSecIpIntra)

Value1='"dirOpsServerArtifactsDir" : '+'"'+AUTO_WORK+'/app/managementvm/opsserver_artifacts",'
Value2='"dirOpsServerBinDir" : '+'"'+AUTO_WORK+'/app/managementvm/opsserver_artifacts/bin",'
Value3='"dirOpsServerOgDir" : '+'"'+AUTO_WORK+'/app/managementvm/opsserver_artifacts/og",'
InsertValue(20,Value1)
InsertValue(23,Value2)
InsertValue(28,Value3)

#Call doSCP function to copy files
if options.type in 'ucf2c' and options.chefserver in 'opsserver.opcops.oracleinternalucf6.oraclecorp.com':
        print "\nCopying /etc/ogucf2c from "+options.chefserver+" Server"
        doScp(options.chefuser,options.chefpasswd,options.chefserver,'/etc/ogucf2c',AUTO_WORK+'/app/managementvm/opsserver_artifacts/og')
        print "\nCopying /usr/local/devops/bin from "+options.chefserver+" Server"
        doScp(options.chefuser,options.chefpasswd,options.chefserver,'/usr/local/devops/bin',AUTO_WORK+'/app/managementvm/opsserver_artifacts')
        print "\nCopying management_data_bag_item.json from "+options.chefserver+" Server"
        doScp(options.chefuser,options.chefpasswd,options.chefserver,'/home/daas/management_data_bag_item.json',AUTO_WORK+'/app/managementvm/opsserver_artifacts')
else:
        print "\nCopying /etc/og from "+options.chefserver+" Server"
        doScp(options.chefuser,options.chefpasswd,options.chefserver,'/etc/og',AUTO_WORK+'/app/managementvm/opsserver_artifacts')
        print "\nCopying /usr/local/devops/bin from "+options.chefserver+" Server"
        doScp(options.chefuser,options.chefpasswd,options.chefserver,'/usr/local/devops/bin',AUTO_WORK+'/app/managementvm/opsserver_artifacts')
        print "\nCopying management_data_bag_item.json from "+options.chefserver+" Server"
        doScp(options.chefuser,options.chefpasswd,options.chefserver,'/home/daas/management_data_bag_item.json',AUTO_WORK+'/app/managementvm/opsserver_artifacts')


#Export Nimbula Environment Variables
os.environ['NIMBULA_API']="'"+options.nimbulaapi+"'"
os.environ['NIMBULA_USER']='/'+options.servicename+'/'+options.customeruser

#Running management-vm.py script
if os.system('python '+AUTO_WORK+'/app/daas-ops-home/daas-ops/utils/management-vm/management-vm.py '+AUTO_WORK+'/app/managementvm') != 0:
        print "\nFailure in running management-vm.py script !!"
        sys.exit(1)
else:
        print "\nSuccessfully ran management-vm.py script"

#Setting up nimbula password
os.system('echo '+options.passwd+' > '+AUTO_WORK+'/app/managementvm/output/nimbula-password')

os.chdir(AUTO_WORK+'/app/managementvm/output')

#Running service-security.py script
if os.system('python service-security.py setup') != 0:
        print "\nFailure in running service-security.py setup script!!"
        sys.exit(1)
else:
        print "\nSuccessfully ran service-security.py script"


#Running pod-bringup.py script
if os.system('python pod-bringup.py setup') != 0:
        print "\nFailure in running pod-bringup.py setup script !!"
        sys.exit(1)
else:
        print "\nSuccessfully ran pod-bringup.py setup script"


#Running pod-bringup.py check script
if os.system('python pod-bringup.py check') != 0:
        print "\nFailure in running pod-bringup.py check script !!"
        sys.exit(1)
else:
        print "\nSuccessfully ran pod-bringup.py check script"
