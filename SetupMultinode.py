#!/usr/bin/python
#DT: 03-07-2016
#@Siddharth.Mohapatra@oracle.com
#Master Launcher Python Script for DaaS-Multi-Node Setup

import os,sys,glob
import urllib2
from time import sleep
import pexpect
import json
import base64
import socket
import smtplib
from email.mime.text import MIMEText
import traceback
from multiprocessing.dummy import Pool as ThreadPool
import glob




#GET DAAS
def getDaas():
        sleep(5)
        ArtifactURL = "http://artifactory-slc.oraclecorp.com/artifactory/daas-release-local/com/oracle/opc/definition/daas/"
        AdeUrl = glob.glob("/ade_autofs/gd11_cloud/DAAS_MAIN_GENERIC.rdd/"+Label.split("_")[3].strip()+"/daas/dist/artifactoryroot/com/oracle/opc/daas/deployments/daas-apps/*/*.zip")[0]
        url1 = AdeUrl.split("/")
        url1=url1[-1].split("-")[2:]
        url1='-'.join(url1).strip(".zip")
        print "Getting daas-"+url1+".zip from Artifactory"
        response=urllib2.urlopen(ArtifactURL+"/"+url1+"/daas-"+url1+".zip")
        fh = open(MultinodePath+"/daas-"+url1+".zip","wb")
        fh.write(response.read())
        fh.close()
        os.environ["DAASZIP"]=ArtifactURL+"/"+url1+"/daas-"+url1+".zip"
        os.environ["Daasversion"]=url1

#RUN ConfigurePOD
def CreatePod():
        try:
                os.system("cd "+MultinodePath+"/IDM/IDMScripts; perl ConfigurePod.pl")
                os.environ["IDMtenant01"]=os.popen("cat "+MultinodePath+"/IDM/IDMScripts/sid/propfromdmp.txt |grep daas_daas_pod_name|cut -d= -f2|sed s/pod01//").read().strip()+"tenant01"
                os.environ["IDMpod01"]=os.popen("cat "+MultinodePath+"/IDM/IDMScripts/sid/propfromdmp.txt |grep daas_daas_pod_name|cut -d= -f2").read().strip()
                fh = open(MultinodePath+"/IDM/IDMScripts/sid/daasprops","w")
                fh.write("#Host Properties\n")
                fh.write("default['daas_multinode']['primaryhost'] = \""+hosts['primary']+"\"\n")
                fh.write("default['daas_multinode']['edq73host'] = \""+hosts['edq73host']+"\"\n")
                fh.write("default['daas_multinode']['edq79host'] = \""+hosts['edq79host']+"\"\n")
                fh.write("default['daas_multinode']['daaswlshost'] = \""+hosts['daaswlshost']+"\"\n")
                fh.write("default['daas_multinode']['solrzoohost'] = \""+hosts['solrzookeeper']+"\"\n")
                fh.write("default['daas_multinode']['daas_daasdb_hostname'] = \""+hosts['primary']+"\"\n")
                fh.write("default['daas_multinode']['daasdaaswlsadmin_postdeploy_sdi_daasapp_baseuri'] = \""+ hosts['primary']+"\"\n")
                fh.write("default['daas_multinode']['omchost'] = \""+hosts['omchost']+"\"\n")
                fh.write("\n\n#DaaS IDM Properties\n")
                with open(MultinodePath+"/IDM/IDMScripts/sid/propfromdmp.txt",'r') as f:
                        for line in f:
                                line.strip()
                                fh.write("default['daas_multinode']['"+line.split("=",1)[0]+"'] = \""+line.split("=",1)[1].strip()+"\"\n")
                fh.close()

                fh = open(MultinodePath+"/IDM/IDMScripts/sid/daasprops","a")
                with open(MultinodePath+"/IDM/IDMScripts/sid/pwdsfromdmp.txt",'r') as f:
                        for line in f:
                                line.strip()
                                fh.write("default['daas_multinode']['"+line.split("=",1)[0]+"'] = \""+line.split("=",1)[1].strip()+"\"\n")

                os.system("cd "+MultinodePath+"/IDM/IDMScripts; perl ConfigurePod.pl")
                os.environ["IDMtenant02"]=os.popen("cat "+MultinodePath+"/IDM/IDMScripts/sid/propfromdmp.txt |grep daas_daas_pod_name|cut -d= -f2|sed s/pod01//").read().strip()+"tenant01"
                os.environ["IDMpod02"]=os.popen("cat "+MultinodePath+"/IDM/IDMScripts/sid/propfromdmp.txt |grep daas_daas_pod_name|cut -d= -f2").read().strip()
                fh.write("default['daas_multinode']['daas_daas_pod_name2'] = \""+os.environ.get('IDMpod02')+"\"\n")

                os.system("cd "+MultinodePath+"/IDM/IDMScripts; perl ConfigurePod.pl")
                os.environ["IDMtenant03"]=os.popen("cat "+MultinodePath+"/IDM/IDMScripts/sid/propfromdmp.txt |grep daas_daas_pod_name|cut -d= -f2|sed s/pod01//").read().strip()+"tenant01"
                os.environ["IDMpod03"]=os.popen("cat "+MultinodePath+"/IDM/IDMScripts/sid/propfromdmp.txt |grep daas_daas_pod_name|cut -d= -f2").read().strip()
                fh.write("default['daas_multinode']['daas_daas_pod_name3'] = \""+os.environ.get('IDMpod03')+"\"\n")
                os.system("cd "+MultinodePath+"/IDM/IDMScripts; perl ConfigurePod.pl")
                os.environ["IDMtenant04"]=os.popen("cat "+MultinodePath+"/IDM/IDMScripts/sid/propfromdmp.txt |grep daas_daas_pod_name|cut -d= -f2|sed s/pod01//").read().strip()+"tenant01"
                os.environ["IDMpod04"]=os.popen("cat "+MultinodePath+"/IDM/IDMScripts/sid/propfromdmp.txt |grep daas_daas_pod_name|cut -d= -f2").read().strip()
                fh.write("default['daas_multinode']['daas_daas_pod_name4'] = \""+os.environ.get('IDMpod04')+"\"\n")
                fh.write("default['daas_multinode']['daas_zip'] = \""+os.environ.get('DAASZIP')+"\"\n")
                fh.write("default['daas_multinode']['daas_ver'] = \""+os.environ.get('Daasversion')+"\"\n")
                fh.close()
        except:
                print Exception
                print "Unable to Create IDM Pod...exiting"
                sys.exit(-1)

#Download Cookbook and Populate IDM Attribute
def Populate():
        os.system("knife cookbook download -f daas-multinode-cookbook 16.3.3 -d "+MultinodePath+"/cookbooks")
        os.system("mv "+MultinodePath+"/cookbooks/daas-multinode-cookbook-16.3.3 "+MultinodePath+"/cookbooks/daas-multinode-cookbook")
        os.system("cat "+MultinodePath+"/IDM/IDMScripts/sid/daasprops >> "+MultinodePath+"/cookbooks/daas-multinode-cookbook/attributes/default.rb")
        os.system("rm -rf "+MultinodePath+"/IDM/IDMScripts/sid/*")

#Modify metadata and Upload
def Upload():
        f = open(MultinodePath+"/cookbooks/daas-multinode-cookbook/metadata.rb",'r')
        filedata = f.read()
        f.close()
        newdata = filedata.replace("16.3.3",CVersion)
        f = open(MultinodePath+"/cookbooks/daas-multinode-cookbook/metadata.rb.new",'w')
        f.write(newdata)
        f.close()
        os.system("mv -f "+MultinodePath+"/cookbooks/daas-multinode-cookbook/metadata.rb.new "+MultinodePath+"/cookbooks/daas-multinode-cookbook/metadata.rb")
        os.system("knife cookbook upload -o "+ MultinodePath+"/cookbooks daas-multinode-cookbook")

#Get Webgate artifacts

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
        os.system("mkdir -p "+MultinodePath+"/app/pyconf/webgate/daasohs-artifacts/config/simple")
        os.system("cp -f "+MultinodePath+"/tmp/Data_WG/{cwallet.sso,ObAccessClient.xml,password.xml} "+MultinodePath+"/app/pyconf/webgate/daasohs-artifacts/config/")
        os.system("cp -f "+MultinodePath+"/tmp/Data_WG/{aaa_cert.pem,aaa_key.pem} "+MultinodePath+"/app/pyconf/webgate/daasohs-artifacts/config/simple")
        os.system("chown -R oracle:oinstall "+MultinodePath+"/app/pyconf/")

#Run chef-client
def RunPChef(host):
        getWebgate('aime','2cool','slc08apv.us.oracle.com','/scratch/aime/work/u01/IDMTOP/products/app/iam/oam/server/rreg/output/Data_WG',MultinodePath+'/tmp')
        if os.system("ssh "+host+" 'chef-client '") != 0:
                print "chef-client failed on "+host
                sys.exit(-1)


def runCommand(host,comp):
        if os.system("ssh "+host+" 'chef-client'") != 0:
                print "chef-client failed on "+host+" for "+comp
                print "For more logs please check under "+host+":"+MultinodePath+"/log/"
                sys.exit(-1)


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

def CreateCuratorTXT():
        curator_body="""{
"cronInput": "now",
"isDeleted": "0",
"schedule": "never",
"startTime": "2013-03-18 00:00:00.0",
"endTime": "2014-04-01 09:00:00.0",
"workflowDefId": "111"
}"""
        os.system("touch "+MultinodePath+"/tmp/curator.txt")
        with open(MultinodePath+"/tmp/curator.txt","w") as f:
                f.write(curator_body)
        f.close()


#Register Service
def RegisterService(RegisterService,internalinstance,internaldomain):
        f = open(MultinodePath+RegisterService,'r')
        filedata = f.read()
        f.close()

        newdata = filedata.replace("DTEPOD01",internalinstance)
        newdata = newdata.replace("DTETENANT01",internaldomain)

        f = open(MultinodePath+"/tmp"+RegisterService,'w')
        f.write(newdata)
        f.close()
        os.system("curl -v -X POST -T "+MultinodePath+"/tmp"+RegisterService+" -H \"Content-Type:application/vnd.com.oracle.oracloud.provisioning.Service+json\" -H \"Accept:application/vnd.com.oracle.oracloud.provisioning.Service+json\" -u OCLOUD9_SDI_APPID:Qazygkl1b7w.fp -H \"X-ID-TENANT-NAME:CloudInfra\" http://"+hosts['primary']+":8571/data/admin/provisioning")


#Load Data
def LoadData(dataPath,internaldomain,internalinstance,LoadType):
        curator="onboarder"
        curatorpasswd="Welcome2"
        os.system("cp "+dataPath+" "+MultinodePath+"/app/ftp")
        os.system("curl -v -X POST -T "+MultinodePath+"/tmp/curator.txt -H'Content-Type:application/json' -H'Accept:application/json' -u "+curator+":"+curatorpasswd+" -H'X-ID-TENANT-NAME:"+internaldomain+"'  -H'X-USER-IDENTITY-DOMAIN-NAME:"+internaldomain+"'  -H'X-ORACLE-DAAS-SERVICE-NAME:"+internalinstance+"'  http://"+hosts['daaswlshost']+":7005/data/admin/curator/workflowjob/submit/workflowJob")
        output=queryAPI(hosts['daaswlshost'],curator,curatorpasswd,'RUNNING',internaldomain,internalinstance)
        #print output
        counter=0
        print "\n\n"+LoadType+" Dataload started RUNNING !!\n"
        while "RUNNING".find(output) != 1:
                output=queryAPI(hosts['daaswlshost'],curator,curatorpasswd,'RUNNING',internaldomain,internalinstance)
                if "null".find(output) != 0:
                        print LoadType+" Dataload is RUNNING will wait for 30s"
                        sleep(30)
                        counter+=30
                else:
                        print "\n\n"+LoadType+" Dataload Completed in \n"+str(counter/60)+" minutes\n\n"
                        break

def PrepareReport():
        with open(MultinodePath+"/tmp/Report.txt",'w') as f:
                url1=os.environ.get('IDMpod01')+"-"+os.environ.get('IDMtenant01')+".data."+hosts['primary']
                url2=os.environ.get('IDMpod02')+"-"+os.environ.get('IDMtenant02')+".data."+hosts['primary']
                url3=os.environ.get('IDMpod03')+"-"+os.environ.get('IDMtenant03')+".data."+hosts['primary']
                f.write("****************** DAAS MULTINODE SETUP ENVIRONMENT DETAILS*******************\n\n\n")
                f.write("[Primary Host]="+hosts['primary']+" , ")
                f.write("[DaaS Host]="+hosts['daaswlshost']+" , ")
                f.write("[EDQ73 Host]="+hosts['edq73host']+" , ")
                f.write("[EDQ79 Host]="+hosts['edq79host']+" , ")
                f.write("[Solr-Zookeeper Host]="+hosts['solrzookeeper']+" , ")
                f.write("[OMC Host]="+hosts['omchost']+" , ")
                f.write("\n\nDAAS LABEL: "+Label+"\n")
                f.write("\n\n#Host File Entries:\n")
                f.write(socket.gethostbyname(socket.gethostname())+"   "+url1+"\n")
                f.write(socket.gethostbyname(socket.gethostname())+"   "+url2+"\n")
                f.write(socket.gethostbyname(socket.gethostname())+"   "+url3+"\n")
                f.write("\n\n#DB Details")
                f.write("\nDB Host: "+hosts['primary'])
                f.write("\nSID/port : orcl/1521")
                f.write("\nSchema/Password: daas_app/daas_app, daas_dbmrd/daas_dbmrd")
                f.write("\n\n----------- Standard Subscription ------------\n")
                f.write("\nDaaS URL: http://"+url1+":8471/data/ui\n")
                f.write("#Curator User Details:\n")
                f.write("Curator Console User: onboarder\n")
                f.write("Curator Console Password: Welcome2\n")
                f.write("\n#UI Access Details:\n")
                f.write("Internal Domain:"+os.environ.get('IDMtenant01')+" \n")
                f.write("User Name: "+os.environ.get('IDMtenant01')+"admin\n")
                f.write("Password : Fusionapps1\n")
                f.write("#AV User Details:\n")
                f.write("User Name: avuser\n")
                f.write("Password : welcome1\n")
                f.write("\n------ Enterprise Subscription with AV --------\n")
                f.write("\nDaaS URL: http://"+url2+":8471/data/ui\n")
                f.write("#Curator User Details:\n")
                f.write("Curator Console User: onboarder\n")
                f.write("Curator Console Password: Welcome2\n")
                f.write("\n#UI Access Details:\n")
                f.write("Internal Domain:"+os.environ.get('IDMtenant02')+" \n")
                f.write("User Name: "+os.environ.get('IDMtenant02')+"admin\n")
                f.write("Password : Fusionapps1\n")
                f.write("#AV User Details:\n")
                f.write("User Name: avuser\n")
                f.write("Password : welcome1\n")
                f.write("\n--------- Contact Only  Subscription ---------\n")
                f.write("\nDaaS URL: http://"+url3+":8471/data/ui\n")
                f.write("#Curator User Details:\n")
                f.write("Curator Console User: onboarder\n")
                f.write("Curator Console Password: Welcome2\n")
                f.write("\n#UI Access Details:\n")
                f.write("Internal Domain:"+os.environ.get('IDMtenant03')+" \n")
                f.write("User Name: "+os.environ.get('IDMtenant03')+"admin\n")
                f.write("Password : Fusionapps1\n")
                f.write("#AV User Details:\n")
                f.write("User Name: avuser\n")
                f.write("Password : welcome1\n")
        f.close()

def SendMail(file,Email,status):
        fp = open(file,'rb')
        msg = MIMEText(fp.read())
        fp.close()
        to=Email
        msg['Subject'] = 'DAAS MULTINODE SETUP :: '+status
        msg['From'] = 'multnode-setup@oracle.com'
        msg['to'] = to
        msg['cc'] = 'siddharth.mohapatra@oracle.com'
        toaddr=to.split(",")+['siddharth.mohapatra@oracle.com']
        s = smtplib.SMTP('localhost')
        s.sendmail('multnode-setup@oracle.com',toaddr ,msg.as_string())
        s.quit()


def doScp(user,password, host,files,path):
        try:
                print 'scp -r %s  %s@%s:%s' % (files,user,host,path)
                child = pexpect.spawn('scp -r %s  %s@%s:%s' % (files,user,host,path),logfile=sys.stdout,timeout=None)
                i = child.expect(['password:', r'\(yes\/no\)', r"yes/no",r'.*password for paasusr: ',r'.*[$#] '])
                if i == 0:
                        child.sendline(password)
                elif i == 1:
                        child.sendline("yes")
                        child.expect("password:")
                        child.sendline(password)
                data = child.read()
                print data
                child.close()
        except:
                print(traceback.format_exc())
                print "Failed while copying"+files+" to "+host
def getMultiProps(workloc):
        os.system("wget http://slcn09vmf0163.us.oracle.com/bigfiles/bluekai/techstacks/common_multinode.tar.gz -P "+workloc)
        os.system("tar -xvzf "+workloc+"/common_multinode.tar.gz -C "+workloc+" --strip-components=1")
        f = open(workloc+"/IDM/IDMScripts/ConfigurePod.pl",'r')
        filedata = f.read()
        f.close()
        newdata = filedata.replace("/u01/common_multinode",workloc)
        f = open(workloc+"/IDM/IDMScripts/ConfigurePod.pl.tmp",'w')
        f.write(newdata)
        f.close()
        os.system("mv "+workloc+"/IDM/IDMScripts/ConfigurePod.pl.tmp "+workloc+"/IDM/IDMScripts/ConfigurePod.pl")



def SRGReport():
        with open(MultinodePath+"/tmp/SRG.txt",'w') as f:
                SRGurl=os.environ.get('IDMpod04')+"-"+os.environ.get('IDMtenant04')+".data."+hosts['primary']
                f.write("****************** DAAS MULTINODE SETUP ENVIRONMENT DETAILS*******************\n\n\n")
                f.write("DAAS LABEL: "+Label+"\n\n")
                f.write("[Primary Host]="+hosts['primary']+" , \n")
                f.write("[DaaS Host]="+hosts['daaswlshost']+" , \n")
                f.write("[EDQ73 Host]="+hosts['edq73host']+" , \n")
                f.write("[EDQ79 Host]="+hosts['edq79host']+" , \n")
                f.write("[Solr-Zookeeper Host]="+hosts['solrzookeeper']+" , \n")
                f.write("[OMC Host]="+hosts['omchost']+" , \n")
                f.write("\n\n#Host File Entries:\n")
                f.write(socket.gethostbyname(socket.gethostname())+"   "+SRGurl+"\n")
                f.write("\n\n#DB Details")
                f.write("\nDB Host: "+hosts['primary'])
                f.write("\nSID/port : orcl/1521")
                f.write("\nSchema/Password: daas_app/daas_app, daas_dbmrd/daas_dbmrd")
                f.write("\n\n----------- Enterprise Subscription with AV ------------\n")
                f.write("\nDaaS URL: http://"+SRGurl+":8471/data/ui\n")
                f.write("#Curator User Details:\n")
                f.write("Curator Console User: onboarder\n")
                f.write("Curator Console Password: Welcome2\n")
                f.write("\n#UI Access Details:\n")
                f.write("Internal Domain:"+os.environ.get('IDMtenant04')+" \n")
                f.write("User Name: "+os.environ.get('IDMtenant04')+"admin\n")
                f.write("Password : Fusionapps1\n")
                f.write("#AV User Details:\n")
                f.write("User Name: avuser\n")
                f.write("Password : welcome1\n")

def runTCommand(host,comp):
        if os.system("ssh "+host+" 'chef-client'") != 0:
                print "Chef Setup Failed on "+host+" for "+comp
                os.system("echo \"Chef Setup Failed on "+host+" for "+comp+" \n\">> "+MultinodePath+"/tmp/failed")
                os.system("cp "+MultinodePath+"/tmp/failed "+MultinodePath+"/tmp/failedrun")
                sys.exit(-1)

def runMulti():
        children = []
        for comp,host in conHosts.iteritems():
                pid = os.fork()
                if pid:
                        children.append(pid)
                else:
                        sleep(10)
                        print "\n\nRunning chef-client on "+host+" for "+comp+"\n\n"
                        runTCommand(host,comp)
                        os._exit(0)

        for i, child in enumerate(children):
                os.waitpid(child, 0)

def startThread():
        pool = ThreadPool(len(conHosts) -1)
        try:
                pool.map(runMulti(), 'True')
                pool.close()
                pool.join()
        except:
                os.system("killall -q ssh")
                os.kill(os.getpid(),9)

def AssignRecipes(task):
        for host in hosts:
                if host in 'primary':
                        os.system("knife node run_list "+task+" multi-node1 'recipe[cookbook-daasenv-setup::setupenv],recipe[daas-multinode-cookbook::installdb],recipe[daas-multinode-cookbook::createschema],recipe[daas-multinode-cookbook::setupohs]'")
                elif host in 'edq73host':
                        os.system("knife node run_list "+task+" multi-node2 'recipe[cookbook-daasenv-setup::setupenv],recipe[daas-multinode-cookbook::edq73wls]'")
                elif host in 'edq79host':
                        os.system("knife node run_list "+task+" multi-node3 'recipe[cookbook-daasenv-setup::setupenv],recipe[daas-multinode-cookbook::edq79wls]'")
                elif host in 'daaswlshost':
                        os.system("knife node run_list "+task+" multi-node4 'recipe[cookbook-daasenv-setup::setupenv],recipe[daas-multinode-cookbook::daaslwls]'")
                elif host in 'solrzookeeper':
                        os.system("knife node run_list "+task+" multi-node5 'recipe[cookbook-daasenv-setup::setupenv],recipe[daas-multinode-cookbook::solr-zookeeper]'")
                elif host in 'omchost':
                        os.system("knife node run_list "+task+" multi-node6 'recipe[cookbook-daasenv-setup::setupenv],recipe[daas-multinode-cookbook::omcsetup]'")
                else:
                        print "Unable to add recipes to nodes..Exiting"
                        sys.exit(-1)

def PrepEnv(task):
        for host in hosts:
                if host in 'primary':
                        os.system("knife node run_list "+task+" multi-node1 'recipe[daas-multinode-cookbook::makeconf]'")
                elif host in 'edq73host':
                        os.system("knife node run_list "+task+" multi-node2 'recipe[daas-multinode-cookbook::makeconf]'")
                elif host in 'edq79host':
                        os.system("knife node run_list "+task+" multi-node3 'recipe[daas-multinode-cookbook::makeconf]'")
                elif host in 'daaswlshost':
                        os.system("knife node run_list "+task+" multi-node4 'recipe[daas-multinode-cookbook::makeconf]'")
                elif host in 'solrzookeeper':
                        os.system("knife node run_list "+task+" multi-node5 'recipe[daas-multinode-cookbook::makeconf]'")
                elif host in 'omchost':
                        os.system("knife node run_list "+task+" multi-node6 'recipe[daas-multinode-cookbook::makeconf]'")
                else:
                        print "Unable to add recipes to nodes..Exiting"
                        sys.exit(-1)

def PrepPropsforMats():
        f=open(MultinodePath+"/tmp/systemtests/daas_test.properties",'a')
        Standard=os.environ.get('IDMpod01')+"-"+os.environ.get('IDMtenant01')+".data."+hosts['primary']
        Enterprise=os.environ.get('IDMpod02')+"-"+os.environ.get('IDMtenant02')+".data."+hosts['primary']
        ContactOnly=os.environ.get('IDMpod03')+"-"+os.environ.get('IDMtenant03')+".data."+hosts['primary']
        f.write("SUBSCRIPTION_1=Standard_company\n")
        f.write("SUBSCRIPTION_2=Enterprise_company\n")
        f.write("SUBSCRIPTION_3=AVSERVICE\n")
        f.write("CERTIFICATE_URL=https://slc08apw.us.oracle.com:4443\n")
        f.write("FIREFOX_PROXY=http://wpad/wpad.dat\n")
        f.write("daasbox="+hosts['primary']+"\n")
        f.write("DAAS_PROV_URL=\n")
        f.write("DAAS_UI_URL_1=http://"+Standard+":8471/data/ui\n")
        f.write("DAAS_IDM_SERVICE_1="+os.environ.get('IDMpod01')+"\n")
        f.write("DAAS_USER_1="+os.environ.get('IDMtenant01')+"admin\n")
        f.write("DAAS_PWD_1=Fusionapps1\n")
        f.write("DAAS_IDM_TENANT_1="+os.environ.get('IDMtenant01')+"\n")
        f.write("DAAS_UI_URL_2=http://"+Enterprise+":8471/data/ui\n")
        f.write("DAAS_IDM_SERVICE_2="+os.environ.get('IDMpod02')+"\n")
        f.write("DAAS_USER_2="+os.environ.get('IDMtenant02')+"admin\n")
        f.write("DAAS_PWD_2=Fusionapps1\n")
        f.write("DAAS_IDM_TENANT_2="+os.environ.get('IDMtenant02')+"\n")
        f.write("DAAS_IDM_SERVICE_3="+os.environ.get('IDMpod03')+"\n")
        f.write("DAAS_USER_3="+os.environ.get('IDMtenant03')+"admin\n")
        f.write("DAAS_PWD_3=Welcome2\n")
        f.write("DAAS_IDM_TENANT_3="+os.environ.get('IDMtenant03')+"\n")
        f.write("DAAS_API_URL_3=http://"+ContactOnly+":8471\n")
        f.write("DAAS_AV_URL_3=http://"+ContactOnly+":8471/av/api/v2/addressclean\n")
        f.write("DAAS_MANAGED_PORT=7005\n")
        f.write("PROV_MANAGED_PORT=8005\n")
        f.write("EDQ73RT_MANAGED_HOST_PORT=9993\n")
        f.write("EDQ73BATCH_MANAGED_HOST_PORT=9995\n")

def runMats():
        try:
                daasversion=glob.glob(MultinodePath+"/app/daas-ops-home-*")
                daasversion="-".join(daasversion[0].split("/")[-1].split("-")[-2:])
                defFile="http://artifactory-slc.oraclecorp.com/artifactory/daas-release-local/com/oracle/opc/definition/daas/"+daasversion+"/daas-"+daasversion+"-definition.json"
                os.system("wget -P "+MultinodePath+"/tmp/ "+defFile)
                systemtestzip=os.popen("cat "+MultinodePath+"/tmp/daas-"+daasversion+"-definition.json|grep -A1 systemtests|grep version|cut -d: -f2|cut -d, -f1").read().strip()
                os.system("wget -P "+MultinodePath+"/tmp/systemtests http://artifactory-slc.oraclecorp.com/artifactory/daas-release-local/com/oracle/opc/daas/testing/systemtests/"+systemtestzip+"/systemtests-"+systemtestzip+".zip")
                if os.path.isfile(MultinodePath+"/tmp/systemtests/daas_test.properties"):
                        os.system("python /u01/runMats.py")
                os.system("rm -rf /net/slcn09vmf0220.us.oracle.com/u01/srgresults/multinode-setup/ui/*")
                os.system("cp -r "+MultinodePath+"/tmp/systemtests/daas_ui/results/Test_Standard_company /net/slcn09vmf0220.us.oracle.com/u01/srgresults/multinode-setup/ui/")
                os.system("cp -r "+MultinodePath+"/tmp/systemtests/daas_ui/results/Test_Enterprise_company /net/slcn09vmf0220.us.oracle.com/u01/srgresults/multinode-setup/ui/")
                SUMMARY_FILE=os.popen('find . -name "Summary.xml"').read().strip().split('\n')
                SucDiffUI1=os.popen("cat "+SUMMARY_FILE[0]+"|grep 'test name'|cut -d' ' -f2,3|cut -d= -f2,3").read()
                SucDiffUI2=os.popen("cat "+SUMMARY_FILE[1]+"|grep 'test name'|cut -d' ' -f2,3|cut -d= -f2,3").read()
                API_SUMMARYFILE=os.popen('find . -name "daas_report.xml"').read().strip().split('\n')
                SucDiffAPI=os.popen("cat "+API_SUMMARYFILE[0]+"|grep 'test name'|cut -d' ' -f2,3|cut -d= -f2,3").read()
                f=open(MultinodePath+"/tmp/Report.txt",'a')
                f.write("\n\nStandard UI MATS Result\n")
                f.write("****************************\n")
                f.write("Result URL: http://slcn09vmf0220.us.oracle.com/SRG/multinode-setup/ui/Test_Standard_company/DaaS_MATS/DaaS/DaaS.html \n")
                f.write(SucDiffUI1)
                f.write("\n\nEnterPrise UI MATS Result\n")
                f.write("******************************\n")
                f.write("Result URL: http://slcn09vmf0220.us.oracle.com/SRG/multinode-setup/ui/Test_Enterprise_company/DaaS_MATS/DaaS/DaaS.html\n")
                f.write(SucDiffUI2)
                f.write("\n\nAPI MATS Result\n")
                f.write("******************************\n")
                f.write(SucDiffAPI)
                f.close()
        except:
                print "MATS was not run due to below error, please run it manually!!"
                print(traceback.format_exc())

if( __name__ == '__main__'):
        if(len(sys.argv) != 3):
                print "Are you kidding? I need 2 arguments & found only "+str(len(sys.argv))+" arguments"
                print "\nUsage: python SetupMultinode.py [DaaS Label] [E-MAIL]"
        else:
                try:
                        Label=sys.argv[1]
                        Email=sys.argv[2]
                        MultinodePath='/u01/work/'
                        CVersion="16.3.5"
                        getMultiProps(MultinodePath)
                        hosts={}
                        with open(MultinodePath+'/hosts','r') as f:
                                for line in f:
                                        hosts[line.strip().split('=')[0]]=line.strip().split('=')[1]
                        with open(MultinodePath+"/tmp/Start.txt",'w') as f:
                                f.write("Multi-node Setup Started\n\n")
                                f.write("DAAS LABEL: "+Label+"\n\n")
                                f.write("[Primary Host]="+hosts['primary']+" , ")
                                f.write("[DaaS Host]="+hosts['daaswlshost']+" , ")
                                f.write("[EDQ73 Host]="+hosts['edq73host']+" , ")
                                f.write("[EDQ79 Host]="+hosts['edq79host']+" , ")
                                f.write("[Solr-Zookeeper Host]="+hosts['solrzookeeper']+" , ")
                                f.write("[OMC Host]="+hosts['omchost']+" , ")
                                f.write("\n\n\n\nPlease note it may take a longer time to setup,please wait as we will notify you the Success/Failure Status")
                        f.close()
                        PrepEnv('remove')
                        AssignRecipes('remove')
                        SendMail(MultinodePath+"/tmp/Start.txt",Email,'Started')
                        print "Getting DaaS Zip File\n"
                        getDaas()
                        print "Creating IDM POD[s]...Please wait\n"
                        CreatePod()
                        Populate()
                        Upload()
                        PrepEnv('add')
                        conHosts={}
                        conHosts.update(hosts)
                        print conHosts
                        startThread()
                        if not os.path.isfile(MultinodePath+'/tmp/failed'):
                                pass
                        else:
                                print "EXITING !! Due to chef Failure\n\n"
                                SendMail(MultinodePath+"/tmp/failedrun",Mail,'Failed !!')
                                os.remove(MultinodePath+'/tmp/failed')
                                sys.exit()
                        PrepEnv('remove')
                        print "Adding rest of the recipes\n\n"
                        AssignRecipes('add')
                        print "\n\nInstalling DB,creating Daas schemas & Creating pyconf\n\n"
                        RunPChef(hosts['primary'])
                        daaspath=glob.glob(MultinodePath+'/app/daas-ops-home-*')
                        daasops="daas"+daaspath[0].split("daas")[1]
                        conHosts.pop("primary")
                        print conHosts
                        startThread()
                        if not os.path.isfile(MultinodePath+'/tmp/failed'):
                                pass
                        else:
                                print "EXITING !! Due to chef Failure\n\n"
                                SendMail(MultinodePath+"/tmp/failed",Mail,'Failed !!')
                                os.remove(MultinodePath+'/tmp/failed')
                                sys.exit(-1)
                        CreateCuratorTXT()
                        #Remove all recipes except appdeploy
                        AssignRecipes('remove')
                        os.system("knife node run_list add multi-node1 'recipe[daas-multinode-cookbook::deployapp]'")
                        print "\n\nDeploying DAAS Application now...\n\n"
                        runCommand(hosts['primary'],'Deploy App')
                        os.system("knife node run_list add multi-node1 'recipe[daas-multinode-cookbook::deployapp]'")
                        #Register Standard Subscription
                        RegisterService("/RegisterService.txt",os.environ.get('IDMpod01'),os.environ.get('IDMtenant01'))
                        #Initial Data Load
                        LoadData("/usr/local/packages/aime/dte/DTE/scripts/DaaS/c9/data/init/*.zip",os.environ.get('IDMtenant01'),os.environ.get('IDMpod01'),"Init")
                        #Incremental Data Load-1
                        LoadData("/usr/local/packages/aime/dte/DTE/scripts/DaaS/c9/data/incr1/*.zip",os.environ.get('IDMtenant01'),os.environ.get('IDMpod01'),"Incremental-1")
                        #Register Enterprise Subscription with AV
                        RegisterService("/RegisterService_ent.txt",os.environ.get('IDMpod02'),os.environ.get('IDMtenant02'))
                        #For SRG RUN
                        RegisterService("/RegisterService_ent.txt",os.environ.get('IDMpod04'),os.environ.get('IDMtenant04'))
                        #Register Contact-Only Subscrition
                        RegisterService("/RegisterService_cnt.txt",os.environ.get('IDMpod03'),os.environ.get('IDMtenant03'))
                        print "\n\n***************Multi-Node Setup Completed*******************\n"
                        PrepareReport()
                        SRGReport()
                        os.system("mkdir "+MultinodePath+"/tmp/systemtests/")
                        PrepPropsforMats()
                        runMats()
                        SendMail(MultinodePath+"/tmp/Report.txt",Email,'Execution Report')
                        SendMail(MultinodePath+"/tmp/SRG.txt",Email,'Execution Report for SRG')
                except:
                        print "Setup failed with below error: \n\n"
                        print(traceback.format_exc())
                        with open(MultinodePath+"/tmp/FiledReport.txt",'w') as f:
                                f.write("Setup failed with below error: \n\n")
                                f.write(traceback.format_exc())
                        f.close()
                        #Cleanup attributes and Run_List for next run
                        os.system("knife exec -E 'nodes.transform(:all) {|n| n.run_list([\"role[primary-role]\"])}'")
                        os.system("knife exec -E 'nodes.find(\"role:primary-role\") {|n| n.run_list.remove(\"role[primary-role]\"); n.save}'")
                        os.system("knife exec -E 'nodes.transform(:all) {|n| n.run_list([\"role[primary-role]\"])}'")
                        os.system("knife exec -E 'nodes.find(\"role:primary-role\") {|n| n.run_list.remove(\"role[primary-role]\"); n.save}'")
                        os.system("knife exec -E \"nodes.transform(:all) {|n| n.default_attrs[:daas_multinode].delete(:daas_ver) rescue nil }\"")
                        os.system("knife exec -E \"nodes.transform(:all) {|n| n.default_attrs[:daas_multinode].delete(:daas_zip) rescue nil }\"")
                        SendMail(MultinodePath+"/tmp/FiledReport.txt",Email,'Failed !!')
