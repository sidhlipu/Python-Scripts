#!/usr/bin/python
#DT: 15.06.2016
#@siddharth.mohapatra@oracle.com
#This is wrapper script for running DaaS Test Suite
#       1. Start Display
#       2. Setup Firefox profile
#       3. Import SSL Certificate
#       4. Set UI test Properties
#       5. Setup VNC
#       6. Install Ant
#       7. Get MATS suite from Artifactory [This has been depriciated]
#       8. Run MATS
#################################################################
import os,sys
import shutil
import xml.etree.ElementTree as ET
from time import sleep
import subprocess
import traceback
import glob




def runThis(thiscommand,stdFlag=False):
        global counter
        counter = counter + 1
        try:
                if stdFlag:
                        FNULL=sys.stdout
                else:
                        FNULL = open(os.devnull, 'w')
                sys.stdout.write("Step "+str(counter)+": RUN `"+thiscommand+"`")
                sys.stdout.flush()
                retcode = subprocess.call(thiscommand, shell=True,stdout=FNULL,stderr=FNULL)
                if retcode < 0:
                        print >>sys.stderr, "Child was terminated by signal", -retcode
                else:
                        if retcode != 0:
                                print "\n--> CRITICAL::Command Completed Status: FAILED("+str(retcode)+")"
                                if retcode in ['-1','127','255','128','130']:
                                        sys.exit(-1)
                        else:
                                print "\n--> INFO::Command Completed Status: SUCCESS("+str(retcode)+")"
        except OSError as e:
                print >>sys.stderr, "!!! Running: `"+thiscommand+"` Failed with ", e



def GetSuite():
        runThis("unzip -o /systemtests/systemtests-"+version+".zip -d /systemtests/")
        runThis("unzip -o /systemtests/docker_dependency.zip -d /systemtests/")
        if os.path.isfile("/usr/local/bin/java"):
                runThis("unlink /usr/local/bin/java;rm -rf /usr/local/bin/java")
        runThis("ln -s /systemtests/java/bin/java /usr/local/bin/java")
        if os.path.isfile("/usr/local/bin/firefox"):
                runThis("unlink /usr/local/bin/firefox;rm -rf /usr/local/bin/firefox")
        runThis("rm -rf  /opt/firefox* && cp -rvf /systemtests/firefox /opt/firefox && ln -s /opt/firefox/firefox /usr/local/bin/firefox")
        runThis("service messagebus start")


def SetEnvForMATS():
        runThis(" /usr/bin/Xvfb :9 -screen 0 1024x768x24 &")
        os.environ["DISPLAY"] = ":9"
        runThis("firefox -CreateProfile daasProfile &> /tmp/.firefox.out ")
        firefoxProfile=os.popen("cat /tmp/.firefox.out |grep firefox|sed 's/.*at//'|sed 's/prefs.js'//").read().strip().split("'")[1]
        os.environ["firefoxprofile"]=firefoxProfile
        runThis("rm -rf /tmp/.firefox.out")
        OverrideText="""
# PSM Certificate Override Settings file
# This is a generated file!  Do not edit.
slc08aqe.us.oracle.com:4443     OID.2.16.840.1.101.3.4.2.1      01:0E:2A:8A:D3:A9:3B:A4:AE:58:4F:AD:2C:E7:BD:45:B7:97:6F:A0:C4:FA:96:A5:29:DD:77:85:3A:05:B1:B7       U       AAAAAAAAAAAAAAABAAAAXQcwWzETMBEGCgmSJomT8ixkARkWA2NvbTEWMBQGCgmS  JomT8ixkARkWBm9yYWNsZTESMBAGCgmSJomT8ixkARkWAnVzMRgwFgYDVQQDDA8q  LnVzLm9yYWNsZS5jb20=
"""
        f = open("/systemtests/cert_override.txt",'w')
        f.write(OverrideText)
        runThis("cp -f /systemtests/cert_override.txt " +firefoxProfile)

        AddSettings="""
user_pref("network.proxy.autoconfig_url", "http://wpad/wpad.dat");
user_pref("network.proxy.type", 2);
user_pref("browser.download.dir", "/root/Downloads");
user_pref("browser.download.folderList", 2);
user_pref("browser.download.manager.showWhenStarting", false);
"""
        f = open(firefoxProfile+"prefs.js","w")
        f.write(AddSettings)

        mimiTypes="""<?xml version="1.0"?>
<RDF:RDF xmlns:NC="http://home.netscape.com/NC-rdf#"
         xmlns:RDF="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <RDF:Description RDF:about="urn:mimetypes">
    <NC:MIME-types RDF:resource="urn:mimetypes:root"/>
  </RDF:Description>
  <RDF:Description RDF:about="urn:schemes">
    <NC:Protocol-Schemes RDF:resource="urn:schemes:root"/>
  </RDF:Description>
  <RDF:Seq RDF:about="urn:mimetypes:root">
    <RDF:li RDF:resource="urn:mimetype:text/csv"/>
    <RDF:li RDF:resource="urn:mimetype:text/plain"/>
    <RDF:li RDF:resource="urn:mimetype:application/xml"/>
  </RDF:Seq>
  <RDF:Description RDF:about="urn:mimetype:text/csv"
                   NC:value="text/csv"
                   NC:editable="true"
                   NC:description="CSV document">
    <NC:handlerProp RDF:resource="urn:mimetype:handler:text/csv"/>
  </RDF:Description>
  <RDF:Description RDF:about="urn:mimetype:handler:text/csv"
                   NC:alwaysAsk="false"
                   NC:saveToDisk="true">
    <NC:externalApplication RDF:resource="urn:mimetype:externalApplication:text/csv"/>
  </RDF:Description>
  <RDF:Description RDF:about="urn:mimetype:text/plain"
                   NC:value="text/plain"
                   NC:editable="true"
                   NC:description="TXT document">
    <NC:handlerProp RDF:resource="urn:mimetype:handler:text/plain"/>
  </RDF:Description>
  <RDF:Description RDF:about="urn:mimetype:handler:text/plain"
                   NC:alwaysAsk="false"
                   NC:saveToDisk="true">
    <NC:externalApplication RDF:resource="urn:mimetype:externalApplication:text/plain"/>
  </RDF:Description>
  <RDF:Description RDF:about="urn:mimetype:application/xml"
                   NC:value="application/xml"
                   NC:editable="true"
                   NC:description="XML document">
    <NC:handlerProp RDF:resource="urn:mimetype:handler:application/xml"/>
  </RDF:Description>
  <RDF:Description RDF:about="urn:mimetype:handler:application/xml"
                   NC:alwaysAsk="false"
                   NC:saveToDisk="true">
    <NC:externalApplication RDF:resource="urn:mimetype:externalApplication:application/xml"/>
  </RDF:Description>
</RDF:RDF>
        """
        f = open(firefoxProfile+"mimeTypes.rdf","w")
        f.write(mimiTypes)
        os.environ["firefoxprofile"]=firefoxProfile

def ImportSSL():
        SetEnvForMATS()
        firefoxProfile=os.environ.get("firefoxprofile")
        runThis("echo -n | openssl s_client -connect slc08apw.us.oracle.com:4443 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > /systemtests/sslCertificate.cert ")
        runThis("/systemtests/java/bin/keytool -import -noprompt -trustcacerts -alias myCert272 -file /systemtests//sslCertificate.cert -keystore /systemtests/java/jre/lib/security/cacerts -storepass changeit")
        runThis("certutil -A -n myCert272 -t 'TCu,Cuw,Tuw' -i /systemtests/sslCertificate.cert -keystore -d "+firefoxProfile)





def StandardSubscription():
        runThis("cp /systemtests/daas_ui/InstanceInfo.xml /systemtests/daas_ui/InstanceInfo.xml.orig")
        tree = ET.parse('/systemtests/daas_ui/InstanceInfo.xml')
        root = tree.getroot()
        def UpdateXML(name,value):
                for child in root:
                        if child.attrib['name'] in name:
                                child.attrib['value'] = value

        UpdateXML("TESTSUITE","execution\daas_Cloud_UI_MATS.xml")
        UpdateXML("BUILD","Test_Standard_company")
        UpdateXML("daas.service.subscription","Standard_company")
        UpdateXML("daas.service.daasuiUrl",PropDict['DAAS_UI_URL_1'].strip())
        UpdateXML("daas.service.daasuiUserPass",PropDict['DAAS_PWD_1'].strip())
        UpdateXML("daas.service.daasuiUser",PropDict['DAAS_USER_1'])
        UpdateXML("daas.service.SSOTenantName",PropDict['DAAS_IDM_TENANT_1'].strip())
        UpdateXML("daas.service.ServiceName",PropDict['DAAS_IDM_SERVICE_1'].strip())
        UpdateXML("daas.service.EnrichmentTimeout","1000")
        tree.write('/systemtests/output.xml')
        with open("/systemtests/output.xml","r") as f:
                    data="".join(line for line in f if not line.isspace())
        with open("/systemtests/daas_ui/InstanceInfo.xml","w") as f:
                f.write(data)
                f.close
        runThis("rm -rf  /systemtests/output.xml")

def EnterpriseSubscription():
        runThis("cp -f /systemtests/daas_ui/InstanceInfo.xml.orig /systemtests/daas_ui/InstanceInfo.xml")
        tree = ET.parse('/systemtests/daas_ui/InstanceInfo.xml')
        root = tree.getroot()
        def UpdateXML(name,value):
                for child in root:
                        if child.attrib['name'] in name:
                                child.attrib['value'] = value

        UpdateXML("TESTSUITE","execution\daas_Cloud_UI_MATS.xml")
        UpdateXML("BUILD","Test_Enterprise_company")
        UpdateXML("daas.service.subscription","Enterprise_company")
        UpdateXML("daas.service.daasuiUrl",PropDict['DAAS_UI_URL_2'].strip())
        UpdateXML("daas.service.daasuiUserPass",PropDict['DAAS_PWD_2'].strip())
        UpdateXML("daas.service.daasuiUser",PropDict['DAAS_USER_2'])
        UpdateXML("daas.service.SSOTenantName",PropDict['DAAS_IDM_TENANT_2'].strip())
        UpdateXML("daas.service.ServiceName",PropDict['DAAS_IDM_SERVICE_2'].strip())
        UpdateXML("daas.service.EnrichmentTimeout","1000")
        tree.write('/systemtests/output.xml')
        with open("/systemtests/output.xml","r") as f:
                    data="".join(line for line in f if not line.isspace())
        with open("/systemtests/daas_ui/InstanceInfo.xml","w") as f:
                f.write(data)
                f.close
        runThis("rm -rf  /systemtests/output.xml")



def addHosts(value):
        runThis(" chmod 777 /etc/hosts")
        daasURL=os.popen("echo "+value.split("/")[2]+"|cut -d: -f1").read().strip()
        hostName=os.popen("echo "+value.split("/")[2]+"|cut -d: -f1|sed 's/.*data.'//").read().strip()
        hostIP=os.popen("host "+hostName).read().strip()
        runThis("echo "+hostIP.split()[3]+"  "+daasURL+" >> /etc/hosts")


def ConfigVNC():
        xstartup="""#!/bin/sh

[ -r /etc/sysconfig/i18n ] && . /etc/sysconfig/i18n
export LANG
export SYSFONT
vncconfig -iconic &
xhost +
gconftool-2 --set -t boolean /apps/gnome-screensaver/idle_activation_enabled false
gconftool-2 --set -t boolean /schemas/apps/gnome-screensaver/lock_enabled  false
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
OS=`uname -s`
if [ $OS = 'Linux' ]; then
  case "$WINDOWMANAGER" in
    *gnome*)
      if [ -e /etc/SuSE-release ]; then
        PATH=$PATH:/opt/gnome/bin
        export PATH
      fi
      ;;
  esac
fi
if [ -x /etc/X11/xinit/xinitrc ]; then
  exec /etc/X11/xinit/xinitrc
fi
if [ -f /etc/X11/xinit/xinitrc ]; then
  exec sh /etc/X11/xinit/xinitrc
fi
[ -r $HOME/.Xresources ] && xrdb $HOME/.Xresources
xsetroot -solid grey
xterm -geometry 80x24+10+10 -ls -title "$VNCDESKTOP Desktop" &

if [ -e /usr/bin/startkde ]
then
 /usr/bin/startkde &
elif [ -e /usr/bin/gnome-session ]
then
 /usr/bin/gnome-session &
fi"""
        runThis("touch /root/.vnc/xstartup")
        f = open("/root/.vnc/xstartup","w")
        f.write(xstartup)
        runThis("chmod 755 /root/.vnc/xstartup && vncserver -geometry 1600x1200")
        f.close()

def UpdateRunner(find,value):
        for line in config:
                if find in line:
                        line=value
                outfile.write(line)
        outfile.close()
        runThis("cp /systemtests/daas_ui/common/lib/runner.conf.bkp /systemtests/daas_ui/common/lib/runner.conf")



def InstallANT():
        runThis("wget -P /systemtests/InstallAnt https://artifactory-slc.oraclecorp.com/artifactory/simple/odc-release-local/apache-ant/apache-ant/1.9.6/apache-ant-1.9.6-bin.tar.gz")
        runThis("tar -xvzf /systemtests/InstallAnt/apache-ant-1.9.6-bin.tar.gz -C /systemtests")
        runThis("wget -P /systemtests/InstallAnt https://artifactory-slc.oraclecorp.com/artifactory/simple/repo1-cache/org/apache/ivy/ivy/2.4.0/ivy-2.4.0.jar")
        runThis("/systemtests/apache-ant-1.9.6/bin/ant -version")


def runUIStandard():
        print "Running Standard Subscription......"
        StandardSubscription()
        runThis("export DISPLAY=:9 && export ANT_HOME=/systemtests/apache-ant-1.9.6 && export JAVA_HOME=/systemtests/java && export PATH=$PATH:/systemtests/apache-ant-1.9.6/:/systemtests/java && cd /systemtests/daas_ui && ./run.sh",True)
        print "\n\nStandard Subscription MATS completed !!!"

def runUIEnterprise():
        print "\nNow running Enterprise Subscription"
        EnterpriseSubscription()
        runThis("export DISPLAY=:9 && export ANT_HOME=/systemtests/apache-ant-1.9.6 && export JAVA_HOME=/systemtests/java && export PATH=$PATH:/systemtests/apache-ant-1.9.6/:/systemtests/java && cd /systemtests/daas_ui && ./run.sh",True)


def updateConfigPropsAPI(value,user,password,tenant,service):
        runThis("cp /systemtests/daas_api/src/main/resources/config.properties /systemtests/daas_api/src/main/resources/config.properties.orig")
        ApiProp = {}
        runThis("sed '/^$/d' /systemtests/daas_api/src/main/resources/config.properties.orig|grep -v '#' > /systemtests/daas_api/src/main/resources/api.props")
        with open("/systemtests/daas_api/src/main/resources/api.props","r") as f :
                for line in f:
                        (key, val) = line.split("=")
                        ApiProp[(key)] = val
                f.close()

        hostName=os.popen("echo "+value.split("/")[2]+"|cut -d: -f1|sed 's/.*data.'//").read().strip()
        Url=value.split("/")[0]+"//"+value.split("/")[2]
        proxyPort = value.split("/")[2].split(":")[1]
        for keys,value in ApiProp.items():
                ApiProp['DAAS_URI']= Url
                ApiProp['DAAS_USERNAME']= user
                ApiProp['DAAS_PASSWORD']= password
                ApiProp['DAAS_TENANT_ID']= tenant
                ApiProp['DAAS_SERVICE_NAME']= service
                ApiProp['AV_URI']= Url
                ApiProp['DAAS_PROXY_FLAG']= "Yes"
                ApiProp['DAAS_PROXY_HOST']= hostName
                ApiProp['DAAS_PROXY_PORT']= proxyPort
                ApiProp['HTTP_PROXY']= hostName+":"+proxyPort

        g = open('/systemtests/daas_api/src/main/resources/config.out','w')
        for key,val in ApiProp.items():
                g.write(key+"="+val+"\n")
        g.close()

def downloadMaven():
        runThis("tar -xvzf /systemtests/apache-maven-3.1.0-bin.tar.gz -C /systemtests/")
        if not os.path.isdir("/systemtests/maven"):
                runThis("mkdir /systemtests/maven")
        mavenConfig="""<?xml version="1.0" encoding="UTF-8"?>
        <settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd">
          <localRepository>/systemtests/maven/repo</localRepository>
        </settings>
        """
        with open("/systemtests/maven/settings.xml",'w') as f:
                f.write(mavenConfig)
        f.close()

def runAPIStandard():
        print "\n\n\nRunning API MATS for Standard Subscription \n\n\n"
        updateConfigPropsAPI(PropDict['DAAS_UI_URL_1'].strip(),PropDict['DAAS_USER_1'].strip(),PropDict['DAAS_PWD_1'].strip(),PropDict['DAAS_IDM_TENANT_1'].strip(),PropDict['DAAS_IDM_SERVICE_1'].strip())
        shutil.move("/systemtests/daas_api/src/main/resources/config.out","/systemtests/daas_api/src/main/resources/config.properties")
        os.remove("/systemtests/daas_api/src/main/resources/api.props")
        runThis("export JAVA_HOME=/systemtests/java && export M2_HOME=/systemtests/apache-maven-3.1.0 && export M2=/systemtests/apache-maven-3.1.0/bin && export PATH=$PATH:/systemtests/apache-maven-3.1.0:/systemtests/apache-maven-3.1.0/bin:/systemtests/java && cd /systemtests/daas_api/&& ./cprun",True)
        shutil.move("/systemtests/daas_api/src/main/resources/config.properties.orig","/systemtests/daas_api/src/main/resources/config.properties")
        print "Standard Subscription API MATS completed !!Pheew.."

def runAPIEnterprise():
        print "\n\n\nRunning API MATS for Enterprise Subscription \n\n\n"
        updateConfigPropsAPI(PropDict['DAAS_UI_URL_2'].strip(),PropDict['DAAS_USER_2'].strip(),PropDict['DAAS_PWD_2'].strip(),PropDict['DAAS_IDM_TENANT_2'].strip(),PropDict['DAAS_IDM_SERVICE_2'].strip())
        shutil.move("/systemtests/daas_api/src/main/resources/config.out","/systemtests/daas_api/src/main/resources/config.properties")
        os.remove("/systemtests/daas_api/src/main/resources/api.props")
        runThis("export JAVA_HOME=/systemtests/java && export M2_HOME=/systemtests/apache-maven-3.1.0 && export M2=/systemtests/apache-maven-3.1.0/bin && export PATH=$PATH:/systemtests/apache-maven-3.1.0:/systemtests/apache-maven-3.1.0/bin:/systemtests/java && cd /systemtests/daas_api/&& ./cprun",True)





if( __name__ == '__main__'):
        try:
                counter=0
                PropDict = {}
                with open("/systemtests/daas_test.properties") as f:
                        for line in f:
                                (key, val) = line.split("=")
                                PropDict[(key)] = val
                suitefile=glob.glob("/systemtests/systemtests-*")
                version=os.path.splitext(suitefile[0])[0].split("systemtests-")[1]
                GetSuite()
                addHosts(PropDict['DAAS_UI_URL_1'])
                addHosts(PropDict['DAAS_UI_URL_2'])
                runThis("chmod 644 /etc/hosts")
                if 'ui' in PropDict['test.suite']:
                        runThis("unzip -o /systemtests/daas_ui.zip -d /systemtests/daas_ui")
                        ImportSSL()
                        ConfigVNC()
                        runThis("cp /systemtests/daas_ui/common/lib/runner.conf /systemtests/daas_ui/common/lib/runner.conf.bkp")
                        config=open("/systemtests/daas_ui/common/lib/runner.conf",'r')
                        outfile=open("/systemtests/daas_ui/common/lib/runner.conf.bkp",'w')
                        UpdateRunner("firefox_binary","firefox_binary=/usr/local/bin/firefox\n")
                        config=open("/systemtests/daas_ui/common/lib/runner.conf",'r')
                        outfile=open("/systemtests/daas_ui/common/lib/runner.conf.bkp",'w')
                        UpdateRunner("classpath=","classpath=/systemtests/.ivy2/cache/:/systemtests/daas_ui/common/lib/V2:/systemtests/daas_ui/common/lib/general:/systemtests/daas_ui/results/compiled:/systemtests/java/lib/tools.jar\n")
                        config=open("/systemtests/daas_ui/common/lib/runner.conf",'r')
                        outfile=open("/systemtests/daas_ui/common/lib/runner.conf.bkp",'w')
                        UpdateRunner("sourcepath=","sourcepath=/systemtests/daas_ui/common/lib_app/:/systemtests/daas_ui/testscript/\n")
                        config=open("/systemtests/daas_ui/common/lib/runner.conf",'r')
                        outfile=open("/systemtests/daas_ui/common/lib/runner.conf.bkp",'w')
                        UpdateRunner("firefoxTemplate","firefoxTemplate="+os.environ.get("firefoxprofile")+"\n")
                        runThis("mkdir /systemtests/mats_results")
                        InstallANT()
                        if 'UI_STANDARD' in PropDict['test_type']:
                                runUIStandard()
                        else:
                                runUIEnterprise()
                        runThis("cp -rv /systemtests/daas_ui/results /systemtests/mats_results")
                        runThis("ps -ef | grep '[ ]:9'|awk '{print $2}'|xargs  kill")
                else:
                        runThis("unzip -o /systemtests/daas_api.zip -d /systemtests/daas_api")
                        downloadMaven()
                        if 'API_STANDARD' in PropDict['test_type']:
                                runAPIStandard()
                        else:
                                runAPIEnterprise()
                        print "Completed"
                        runThis("cp -rv /systemtests/daas_api/target/custom_reports /systemtests/mats_results")
        except:
                        print "MATS failed with below error: \n\n"
                        print(traceback.format_exc())
