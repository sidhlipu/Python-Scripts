#!/usr/bin/python
#DT: 20.03.2017
#@Sidharth.Mohapatra@oracle.com
#e2e Setup
import sys,os
import subprocess
import pexpect
import traceback
import socket
import smtplib
from email.mime.text import MIMEText
import glob,urllib2
from optparse import OptionParser
from multiprocessing.dummy import Pool as ThreadPool
from time import sleep
import json
import base64



FNULL = open(os.devnull, 'w')
homeDir=os.environ.get("AUTO_WORK")

#Get user defined values
parser = OptionParser(usage='usage: %prog [options] arguments')
parser.add_option('-a',help="setup/cleanup [Mandatory]",action="store", dest="action")
parser.add_option('-e',help="email [Optional]",action="store", dest="email")
parser.add_option('--ld',help="DaaS label",action="store", dest="dlabel")
parser.add_option('--lb',help="B2Bx label",action="store", dest="blabel")
parser.add_option('--dbp',help="Dev DaaS build label",action="store", dest="daasbuild")
parser.add_option('--bbp',help="Dev B2Bx build label",action="store", dest="b2bxbuild")
parser.add_option('--m1',help="Offline B2Bx Machine [Mandatory]",action="store", dest="mach1")
parser.add_option('--m2',help="Online DaaS Machine [Mandatory]",action="store", dest="mach2")
parser.add_option('--m1user',help="Offline B2Bx Machine username [Mandatory]",action="store", dest="mach1user")
parser.add_option('--m2user',help="Online DaaS Machine username [Mandatory]",action="store", dest="mach2user")
parser.add_option('--m1pass',help="Offline B2Bx Machine password [Mandatory]",action="store", dest="mach1pass")
parser.add_option('--m2pass',help="Online DaaS Machine password [Mandatory]",action="store", dest="mach2pass")
(options, args) = parser.parse_args()


def sshHost(user,password,host,command):
        try:
                child =  pexpect.spawn("ssh -q -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -n %s@%s '%s'" % (user,host,command),logfile=sys.stdout,timeout=None)
                child.logfile = open("/tmp/mylog", "w")
                i = child.expect(['password:', r'\(yes\/no\)',r'.*password for paasusr: ',r'.*[$#] '])
                if i == 0:
                        child.sendline(password)
                elif i == 1:
                        child.sendline("yes")
                        child.expect("password:")
                        child.sendline(password)
                data = child.read()
                print data
                child.close()
                return True
        except:
                return False



def validateHosts(host,user,password,command):
        try:
                subprocess.check_call("ping -c1 " + host,shell=True,stdout=FNULL,stderr=FNULL)
                status=sshHost(user,password,host,command)
                return status
        except:
                traceback.format_exc()
                return False

def setNode(user,host,password):
        ip=os.popen("nslookup "+host+"|tail -2|grep Address|cut -d: -f2").read().strip()
        os.system('knife search "platform:*" -a ipaddress|grep -B1 '+ip+' > '+homeDir+'/node.name')
        nodeName=os.popen("cat "+homeDir+"/node.name|head -1|cut -d: -f1").read().strip()
        if not nodeName:
                sshHost(user,password,host,"rm -rf /etc/chef/*")
                sshHost(user,password,host,"rm -rf /root/.chef/*")
                sshHost(user,password,host,'wget  http://slcn09vmf0163.us.oracle.com/bigfiles/bluekai/techstacks/chef-keys.tar.gz -P /root/.chef')
                sshHost(user,password,host,'wget  http://slcn09vmf0163.us.oracle.com/bigfiles/bluekai/techstacks/validation.pem -P /etc/chef')
                sshHost(user,password,host,"tar -zxf /root/.chef/chef-keys.tar.gz --strip-components=1 -C /root/.chef")
                newNode=os.popen("knife node list|cut -d- -f2|sort -n|tail -1").read().strip()
                if len(newNode) == 0:
                        newNode='b2bx-1'
                        os.environ["nodeName"]=newNode
                        sshHost(user,password,host,"knife bootstrap -VV "+host+" --ssh-user root -P welcome1 -N "+newNode)
                        return newNode
                else:
                        newNode='b2bx-'+str(int(newNode)+1)
                        print newNode
                        sshHost(user,password,host,"knife bootstrap -VV "+host+" --ssh-user root -P welcome1 -N "+newNode)
                        return newNode
        else:
                print "Node already added as:"+nodeName
                return nodeName

def getDaas(Label,user,passw,mach):
        if 'PT' in Label:
                print "Running Setup for PT Label\n"
                ArtifactURL = "http://artifactory-slc.oraclecorp.com/artifactory/daas-release-local/pt"+Label.split('.')[2].split('_')[0]+"/com/oracle/opc/definition/daas/"
                AdeUrl = glob.glob("/ade_autofs/gd11_cloud/"+".".join(Label.split(".")[:2])+"."+"_".join(Label.split(".")[2].split("_")[:-1])+".rdd"+"/"+Label.split("_")[3].strip()+"/daas/dist/artifactoryroot/pt"+Label.split("_")[1].split('.')[2]+"/com/oracle/opc/daas/deployments/daas-apps/*/*.zip")[0]
                url1 = AdeUrl.split("/")
                url1=url1[-1].split("-")[2:]
                url1='-'.join(url1).strip(".zip")
                print "Getting daas-"+url1+".zip from Artifactory"
                sshHost(user,passw,mach,"wget "+url1+" -P "+homeDir)

        elif 'MAIN' in Label:
                print "Running Setup for MAIN Label\n"
                AdeUrl = glob.glob("/ade_autofs/gd11_cloud/DAAS_MAIN_GENERIC.rdd/"+Label.split("_")[3].strip()+"/daas/dist/artifactoryroot/com/oracle/opc/daas/deployments/daas-apps/*/*.zip")[0]
                url1 = AdeUrl.split("/")
                url1=url1[-1].split("-")[2:]
                url1='-'.join(url1).strip(".zip")
                print "Getting http://artifactory-slc.oraclecorp.com/artifactory/daas-release-local/com/oracle/opc/definition/daas/"+url1+"/daas-"+url1+".zip from Artifactory"
                sshHost(user,passw,mach,"wget http://artifactory-slc.oraclecorp.com/artifactory/daas-release-local/com/oracle/opc/definition/daas/"+url1+"/daas-"+url1+".zip -P "+homeDir)
        elif 'http' in Label:
                print "Getting label from Build Path"
                sshHost(user,passw,mach,"wget "+Label+" -P "+homeDir)
        else:
                print "Label not found!!"
                sys.exit(-1)


def CreateEnv(node):
      subprocess.call("knife node run_list add "+node+" 'recipe[daas-offline-cookbook::setupenv]'", shell=True,stdout=sys.stdout,stderr=sys.stdout)
      subprocess.call("knife node run_list add "+node+" 'recipe[daas-offline-cookbook::makeconf]'", shell=True,stdout=sys.stdout,stderr=sys.stdout)

def RestComponents(node,Recipe):
        subprocess.call("knife node run_list add "+node+" "+Recipe, shell=True,stdout=sys.stdout,stderr=sys.stdout)





def download():
        if options.dlabel is None:
                daasLabel=options.daasbuild
                getDaas(daasLabel,options.mach1user,options.mach1pass,options.mach1)
        elif options.daasbuild is None:
                daasLabel=options.dlabel
                getDaas(daasLabel,options.mach1user,options.mach1pass,options.mach1)
        else:
                print "Label for DAAS Online is not provided!!"
                sys.exit(-1)
        if options.blabel is None:
                daasLabel=options.b2bxbuild
                getDaas(daasLabel,options.mach2user,options.mach2pass,options.mach2)
        elif options.b2bxbuild is None:
                daasLabel=options.blabel
                getDaas(daasLabel,options.mach2user,options.mach2pass,options.mach2)
        else:
                print "Label for B2Bx Offline is not provided!!"
                sys.exit(-1)


def runTCommand(host):
        if host == options.mach1:
                user=options.mach1user
                password=options.mach1pass
                node=os.environ.get("node1")
        else:
                user=options.mach2user
                password=options.mach2pass
                node=os.environ.get("node2")
        sshHost(user,password,host,"export AUTO_WORK="+homeDir+" && chef-client > /var/log/chef.log 2>&1")


def runMulti():
        children = []
        for comp,host in conHosts.iteritems():
                pid = os.fork()
                if pid:
                        children.append(pid)
                else:
                        print "\n\nRunning chef-client on "+host
                        runTCommand(host)
                        os._exit(0)

        for i, child in enumerate(children):
                os.waitpid(child, 0)

def startThread():
        pool = ThreadPool(len(conHosts) -1)
        try:
                pool.map(runMulti(), 'True')
                pool.close()
                pool.join()
                return True
        except:
                os.system("killall -q ssh")
                os.kill(os.getpid(),9)
                return False

def CreatePod():
        try:
                os.system("cd "+homeDir+"/IDM/IDMScripts;perl ConfigurePod.pl")
                os.environ["IDMtenant01"]=os.popen("cat "+homeDir+"/IDM/IDMScripts/sid/propfromdmp.txt |grep daas_daas_pod_name|cut -d= -f2|sed s/pod01//").read().strip()+"tenant01"
                os.environ["IDMpod01"]=os.popen("cat "+homeDir+"/IDM/IDMScripts/sid/propfromdmp.txt |grep daas_daas_pod_name|cut -d= -f2").read().strip()
                os.system("cd "+homeDir+"/IDM/IDMScripts; perl ConfigurePod.pl")
                os.environ["IDMtenant02"]=os.popen("cat "+homeDir+"/IDM/IDMScripts/sid/propfromdmp.txt |grep daas_daas_pod_name|cut -d= -f2|sed s/pod01//").read().strip()+"tenant01"
                os.environ["IDMpod02"]=os.popen("cat "+homeDir+"/IDM/IDMScripts/sid/propfromdmp.txt |grep daas_daas_pod_name|cut -d= -f2").read().strip()
                os.system("cd "+homeDir+"/IDM/IDMScripts; perl ConfigurePod.pl")
                os.environ["IDMtenant03"]=os.popen("cat "+homeDir+"/IDM/IDMScripts/sid/propfromdmp.txt |grep daas_daas_pod_name|cut -d= -f2|sed s/pod01//").read().strip()+"tenant01"
                os.environ["IDMpod03"]=os.popen("cat "+homeDir+"/IDM/IDMScripts/sid/propfromdmp.txt |grep daas_daas_pod_name|cut -d= -f2").read().strip()
        except:
                print Exception
                print "Unable to Create IDM Pod...exiting"
                sys.exit(-1)


def getMultiProps(workloc):
        os.system("wget http://slcn09vmf0163.us.oracle.com/bigfiles/bluekai/techstacks/common_multinode.tar.gz -P "+workloc)
        os.system("tar -xvzf "+workloc+"/common_multinode.tar.gz -C "+workloc+" --strip-components=1")
        f = open(workloc+"/IDM/IDMScripts/ConfigurePod.pl",'r')
        filedata = f.read()
        f.close()
        newdata = filedata.replace("/u01/common_multinode",homeDir)
        f = open(workloc+"/IDM/IDMScripts/ConfigurePod.pl.tmp",'w')
        f.write(newdata)
        f.close()
        os.system("mv "+workloc+"/IDM/IDMScripts/ConfigurePod.pl.tmp "+workloc+"/IDM/IDMScripts/ConfigurePod.pl")

def queryAPI(srvr=None,user=None,pwd=None,status=None,domain=None,service=None):

    url=r'http://%s:7005/data/admin/curator/workflowjob/listJobsByStatus/%s' % (srvr,status)
    req=urllib2.Request(url)
    base64string = base64.encodestring('%s:%s' % (user, pwd))[:-1]
    req.add_header("Authorization", "Basic %s" % base64string)
    req.add_header("X-ID-TENANT-NAME", "%s" % domain)
    req.add_header("X-USER-IDENTITY-DOMAIN-NAME", "%s" % domain)
    req.add_header("X-ORACLE-DAAS-SERVICE-NAME", "%s" % service)

    content = urllib2.urlopen(req)
    jsonstring = content.read()
    return jsonstring


def RegisterService(RegisterService,internalinstance,internaldomain):
        f = open(homeDir+RegisterService,'r')
        filedata = f.read()
        f.close()

        newdata = filedata.replace("DTEPOD01",internalinstance)
        newdata = newdata.replace("DTETENANT01",internaldomain)

        f = open(homeDir+"/tmp"+RegisterService,'w')
        f.write(newdata)
        f.close()
        print "curl -v -X POST -T "+homeDir+"/tmp"+RegisterService+" -H \"Content-Type:application/vnd.com.oracle.oracloud.provisioning.Service+json\" -H \"Accept:application/vnd.com.oracle.oracloud.provisioning.Service+json\" -u OCLOUD9_SDI_APPID:zykhfPsgo2.u6d -H \"X-ID-TENANT-NAME:CloudInfra\" http://"+options.mach2+":8571/data/admin/provisioning"
        os.system("curl -v -X POST -T "+homeDir+"/tmp"+RegisterService+" -H \"Content-Type:application/vnd.com.oracle.oracloud.provisioning.Service+json\" -H \"Accept:application/vnd.com.oracle.oracloud.provisioning.Service+json\" -u OCLOUD9_SDI_APPID:zykhfPsgo2.u6d -H \"X-ID-TENANT-NAME:CloudInfra\" http://"+options.mach2+":8571/data/admin/provisioning")

#Load Data
def LoadData(dataPath,internaldomain,internalinstance,LoadType):
        curator="onboarder"
        curatorpasswd="Welcome2"
        sshHost(options.mach2user,options.mach2pass,options.mach2,"cp "+dataPath+" "+homeDir+"/app/ftp")
        sshHost(options.mach2user,options.mach2pass,options.mach2,"curl -v -X POST -T "+homeDir+"/tmp/curator.txt -H'Content-Type:application/json' -H'Accept:application/json' -u "+curator+":"+curatorpasswd+" -H'X-ID-TENANT-NAME:"+internaldomain+"'  -H'X-USER-IDENTITY-DOMAIN-NAME:"+internaldomain+"'  -H'X-ORACLE-DAAS-SERVICE-NAME:"+internalinstance+"'  http://"+options.mach2+":7005/data/admin/curator/workflowjob/submit/workflowJob")
        output=queryAPI(options.mach2,curator,curatorpasswd,'RUNNING',internaldomain,internalinstance)
        #print output
        counter=0
        print "\n\n"+LoadType+" Dataload started RUNNING !!\n"
        while "RUNNING".find(output) != 1:
                output=queryAPI(options.mach2,curator,curatorpasswd,'RUNNING',internaldomain,internalinstance)
                if "null".find(output) != 0:
                        print LoadType+" Dataload is RUNNING will wait for 30s"
                        sleep(30)
                        counter+=30
                else:
                        print "\n\n"+LoadType+" Dataload Completed in \n"+str(counter/60)+" minutes\n\n"
                        break

def getWebgate(user,password,host,rpath,lpath):
        child = pexpect.spawn('scp -r %s@%s:%s %s' % (user,host,rpath,lpath))
        i = child.expect(['password:', r"yes/no",pexpect.EOF])
        if i == 0:
                child.sendline(password)
        elif i == 1:
                child.sendline("yes")
                child.expect("password:", timeout=30)
                child.sendline(password)
        data = child.read()
        print data
        child.close()


def scpFiles(user,password,host,rpath,lpath):
        child = pexpect.spawn('scp -r %s %s@%s:%s ' % (lpath,user,host,rpath))
        i = child.expect(['password:', r"yes/no",pexpect.EOF])
        if i == 0:
                child.sendline(password)
        elif i == 1:
                child.sendline("yes")
                child.expect("password:", timeout=30)
                child.sendline(password)
        data = child.read()
        print data
        child.close()


def createWebgate():
        os.system("mkdir -p "+homeDir+"/tmp/webgate/daasohs-artifacts/config/simple")
        os.system("cp -f "+homeDir+"/tmp/Data_WG/{cwallet.sso,ObAccessClient.xml,password.xml} "+homeDir+"/tmp/webgate/daasohs-artifacts/config/")
        os.system("cp -f "+homeDir+"/tmp/Data_WG/{aaa_cert.pem,aaa_key.pem} "+homeDir+"/tmp/webgate/daasohs-artifacts/config/simple")
        os.system("chown -R oracle:oinstall "+homeDir+"/app/pyconf/")

def CreateCuratorTXT():
        curator_body="""{
"cronInput": "now",
"isDeleted": "0",
"schedule": "never",
"startTime": "2013-03-18 00:00:00.0",
"endTime": "2014-04-01 09:00:00.0",
"workflowDefId": "111"
}"""
        os.system("touch "+homeDir+"/tmp/curator.txt")
        with open(homeDir+"/tmp/curator.txt","w") as f:
                f.write(curator_body)
        f.close()

def setHostEntry():
        print "Setting host entries on "+options.mach2
        data1="10.240.185.53  cloudprimary.us.oracle.com cloudprimary"
        data2="10.240.185.54 oid.us.oracle.com       oid"
        data3="10.240.185.55 idm.us.oracle.com       idm"
        data4="10.240.185.56 ohs.us.oracle.com       ohs"
        data5="10.240.185.137 db.us.oracle.com        db"

        sshHost(options.mach2user,options.mach2pass,options.mach2," cat /u01/e2e-b2bx/test.idm|grep -q '10.240.185.53';stat=$?;if [ $stat  != 0 ];then echo '"+data1+"' >> /u01/e2e-b2bx/test.idm;fi")
        sshHost(options.mach2user,options.mach2pass,options.mach2," cat /u01/e2e-b2bx/test.idm|grep -q '10.240.185.54';stat=$?;if [ $stat  != 0 ];then echo '"+data2+"' >> /u01/e2e-b2bx/test.idm;fi")
        sshHost(options.mach2user,options.mach2pass,options.mach2," cat /u01/e2e-b2bx/test.idm|grep -q '10.240.185.55';stat=$?;if [ $stat  != 0 ];then echo '"+data3+"' >> /u01/e2e-b2bx/test.idm;fi")
        sshHost(options.mach2user,options.mach2pass,options.mach2," cat /u01/e2e-b2bx/test.idm|grep -q '10.240.185.56';stat=$?;if [ $stat  != 0 ];then echo '"+data4+"' >> /u01/e2e-b2bx/test.idm;fi")
        sshHost(options.mach2user,options.mach2pass,options.mach2," cat /u01/e2e-b2bx/test.idm|grep -q '10.240.185.137';stat=$?;if [ $stat  != 0 ];then echo '"+data5+"' >> /u01/e2e-b2bx/test.idm;fi")



def setup():
        try:
                #Offline
                node1=setNode(options.mach1user,options.mach1,options.mach1pass)
                os.environ["node1"]=node1
                #Online
                node2=setNode(options.mach2user,options.mach2,options.mach2pass)
                os.environ["node2"]=node2
                #Download DaaS Zip
                download()
                #Setup environment
                CreateEnv(node1)
                CreateEnv(node2)
                stat=startThread()
                if stat:
                        #Add Install DB Recipe to both nodes
                        RestComponents(node1,'recipe[daas-offline-cookbook::installdb]')
                        RestComponents(node2,'recipe[daas-offline-cookbook::installdb],recipe[daas-cookbook::makeconf]')
                        sshHost(options.mach2user,options.mach2pass,options.mach2,"chown -R oracle:oinstall "+homeDir+"/app/")
                        setHostEntry()
                        stat=startThread()
                        if stat:
                                sshHost(options.mach1user,options.mach1pass,options.mach1,"ls /u01/work/app/|grep daas-ops-home|tail -1|cut -d- -f4,5 >> "+homeDir+"/tmp/daas_version")
                                #Add Rest Components
                                RestComponents(node2,'recipe[daas-cookbook::createschema],recipe[daas-cookbook::edq73wls],recipe[daas-cookbook::edq79wls],recipe[daas-cookbook::daaslwls],recipe[daas-cookbook::solr-zookeeper],recipe[daas-cookbook::omcsetup],recipe[daas-cookbook::deployapp]')
                                RestComponents(node1,'recipe[daas-offline-cookbook::createschema],recipe[daas-offline-cookbook::daaslwls],recipe[daas-offline-cookbook::edq73wls],recipe[daas-offline-cookbook::odisetup],recipe[daas-offline-cookbook::offlinesolrzookeeper],recipe[daas-offline-cookbook::offlinesolrnode],recipe[daas-offline-cookbook::offlinewls12admin],recipe[daas-offline-cookbook::offlinewls12indexing],recipe[daas-offline-cookbook::offlinewlszookeeper],recipe[daas-offline-cookbook::offlinewls12deploy],recipe[daas-offline-cookbook::edq73batchdataloadwlsmanaged]')
                                stat=startThread()
                                if stat:
                                        getWebgate('aime','2cool','slc08apv.us.oracle.com','/scratch/aime/work/u01/IDMTOP/products/app/iam/oam/server/rreg/output/Data_WG',homeDir+'/tmp')
                                        createWebgate()
                                        scpFiles(options.mach2user,options.mach2pass,options.mach2,homeDir+'/app/pyconf/webgate',homeDir+'/tmp/webgate')
                                        sshHost(options.mach1user,options.mach1pass,options.mach1,"knife exec -E 'n=search(:node, \"name:"+nodename+"\").first; n.run_list = Chef::RunList.new(\"role[primary-role]\"); n.save'")
                                        RestComponents(node2,'recipe[daas-cookbook::setupohs]')
                                        sshHost(options.mach1user,options.mach1pass,options.mach1,"chef-client")
                                        RegisterService("/RegisterService.txt",os.environ.get('IDMpod01'),os.environ.get('IDMtenant01'))
                                        RegisterService("/RegisterService.txt",os.environ.get('IDMpod02'),os.environ.get('IDMtenant02'))
                                        RegisterService("/RegisterService.txt",os.environ.get('IDMpod03'),os.environ.get('IDMtenant03'))
                                        CreateCuratorTXT()
                                        scpFiles(options.mach2user,options.mach2pass,options.mach2,homeDir+'/tmp/curator.txt',homeDir+'/tmp/curator.txt')
                                        LoadData("/usr/local/packages/aime/dte/DTE/scripts/DaaS/c9/data/init/*.zip",os.environ.get('IDMtenant01'),os.environ.get('IDMpod01'),"Init")
                                        LoadData("/usr/local/packages/aime/dte/DTE/scripts/DaaS/c9/data/incr1/*.zip",os.environ.get('IDMtenant01'),os.environ.get('IDMpod01'),"Incremental-1")
                                        sshHost(options.mach1user,options.mach1pass,options.mach1,"mkdir -p "+homeDir+"/app/odi/load/rejectFiles")
                                        sshHost(options.mach1user,options.mach1pass,options.mach1,"mkdir -p "+homeDir+"/app/odi/load/archive")
                                        sshHost(options.mach1user,options.mach1pass,options.mach1,"mkdir -p "+homeDir+"/app/odi/load/exportCSVFiles")
        except:
                print "Setup Failed"
                traceback.format_exc()
                sys.exit(-1)

def cleanup(host,user,password,nodename):
        os.system("knife exec -E 'n=search(:node, \"name:"+nodename+"\").first; n.run_list = Chef::RunList.new(\"role[primary-role]\"); n.save'")
        #remove and reboot
        sshHost(user,password,host,"rm -rf "+homeDir+"/*;mv /var/log/chef.log /var/log/chef.log.lastrun")
        sshHost(user,password,host,"reboot")
        traceback.format_exc()

def SendMail(file,Email,status):
        fp = open(file,'rb')
        msg = MIMEText(fp.read())
        fp.close()
        to=Email
        msg['Subject'] = 'DAAS E2E OFFLINE/ONLINE SETUP :: '+status
        msg['From'] = 'odc-devops@oracle.com'
        msg['to'] = to
        msg['cc'] = 'siddharth.mohapatra@oracle.com'
        toaddr=to.split(",")+['siddharth.mohapatra@oracle.com']
        s = smtplib.SMTP('localhost')
        s.sendmail('odc-devops@oracle.com',toaddr ,msg.as_string())
        s.quit()


if options.mach1 is None or options.mach2 is None or  options.mach1user is None or options.mach2user is None or options.mach1pass is None or options.mach2pass is None:
        if options.dlabel is None and options.daasbuild is None or options.b2bxbuild is None and options.blabel is None:
                parser.error('Not all arguments passed:See -h or --help')
                sys.exit(-1)
else:
        try:
                if options.action is not None:
                        print options.action
                        if 'setup' in options.action:
                                if options.mach1user != 'root':
                                        print "root user is required to continue setup"
                                        sys.exit(-1)
                                if options.mach2user != 'root':
                                        print "root user is required to continue setup"
                                        sys.exit(-1)
                                if not homeDir:
                                        print "Home directory not set!!"
                                        print "Run export AUTO_WORK=/u01/work"
                                        sys.exit()

                                status1=validateHosts(options.mach1,options.mach1user,options.mach1pass,'w')
                                if status1:
                                        status2=validateHosts(options.mach2,options.mach2user,options.mach2pass,'w')
                                        if status2:
                                                print "\nPing and SSH sucess for "+options.mach1+" and "+options.mach2
                                                Email=options.email
                                                with open(homeDir+"/tmp/Start.txt",'w') as f:
                                                        f.write("Offline Hostname: "+options.mach1+"\n\n")
                                                        f.write("Online Hostname: "+options.mach2+"\n\n")
                                                        f.write("Please wait as we will notify you the Success/Failure Status")
                                                        f.write("\n\n\nRegards...")
                                                        f.write("\nDevOps Team")
                                                        f.close()
                                                SendMail(homeDir+"/tmp/Start.txt",Email,'Started')
                                                #Setup Offline and Online DaaS

                                                with open(homeDir+'/hosts','w') as f:
                                                        f.write("online="+options.mach1+"\n")
                                                        f.write("offline="+options.mach2)
                                                        f.close()
                                                hosts={}
                                                with open(homeDir+'/hosts','r') as f:
                                                        for line in f:
                                                                hosts[line.strip().split('=')[0]]=line.strip().split('=')[1]
                                                conHosts={}
                                                conHosts.update(hosts)
                                                getMultiProps(homeDir)
                                                CreatePod()
                                                sshHost(options.mach1user,options.mach2pass,options.mach2,"cp /net/slc08apv.us.oracle.com/scratch/aime/"+os.environ.get("IDMpod01")+".dmp "+homeDir+"/")
                                                setup()
                                                #Import ODI
                                                #sshHost(options.mach2user,options.mach2pass,options.mach2,"cd "+homeDir+"/app/install_odi/Oracle/oracle_common/common/bin;./wlst.sh createOdiDomainForStandaloneAgent.py")

                                                #Send Report
                                        else:
                                                "Unable to ping/ssh:"+options.mach2
                                else:
                                        print "Unable to ping/ssh machine:"+options.mach1
                        elif 'cleanup' in options.action:
                                node1=os.popen("knife search "+options.mach1+"|grep Node|cut -d: -f2").read().strip()
                                node2=os.popen("knife search "+options.mach2+"|grep Node|cut -d: -f2").read().strip()
                                currentHost=socket.gethostname()
                                if currentHost in options.mach1:
                                        cleanup(options.mach2,options.mach2user,options.mach2pass,node2)
                                        cleanup(options.mach1,options.mach1user,options.mach1pass,node1)
                                        print status
                                else:
                                        cleanup(options.mach1,options.mach1user,options.mach1pass,node1)
                                        cleanup(options.mach2,options.mach2user,options.mach2pass,node2)
                        else:
                                print "Action not supported, please refer help"
                                sys.exit(-1)
                else:
                        print "Choose a action[setup/cleanup] to perform"
                        sys.exit(-1)
        except:
                print "Setup failed with below error: \n\n"
                traceback.format_exc()
                with open(homeDir+"/tmp/FailedReport.txt",'w') as f:
                        f.write("Setup failed with below error: \n\n")
                        f.write(traceback.format_exc())
                        f.write("\n\n\n\nRegards...")
                        f.write("\nDevOps Team")
                        f.close()
                #SendMail(homeDir+"/tmp/FailedReport.txt",Email,'Failed !!')
                #Cleanup attributes and Run_List for next run
