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
                                print "\n--> WARNING::Command Completed Status: WARN("+str(retcode)+")"
                                if retcode in ['-1','127','255','128','130']:
                                        sys.exit(-1)
                        else:
                                print "\n--> INFO::Command Completed Status: SUCCESS("+str(retcode)+")"
        except OSError as e:
                print >>sys.stderr, "!!! Running: `"+thiscommand+"` Failed with ", e


def GetSuite():
        runThis("unzip -o "+TestBed+"/systemtests-"+version+".zip -d "+TestBed+"/")
        runThis("unzip -o "+TestBed+"/docker_dependency.zip -d "+TestBed+"/")
        if os.path.isfile("/usr/bin/java"):
                runThis("unlink /usr/bin/java;rm -rf /usr/bin/java")
        runThis("ln -s "+TestBed+"/java/bin/java /usr/bin/java")
        if os.path.isfile("/usr/local/bin/firefox"):
                runThis("unlink /usr/bin/firefox;rm -rf /usr/bin/firefox")
        runThis("rm -rf  /opt/firefox* && cp -rvf "+TestBed+"/firefox /opt/firefox && ln -s /opt/firefox/firefox /usr/bin/firefox")
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
        f = open(TestBed+"/cert_override.txt","w")
        f.write(OverrideText)
        runThis("cp -f "+TestBed+"/cert_override.txt " +firefoxProfile)

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
        runThis("echo -n | openssl s_client -connect slc08apw.us.oracle.com:4443 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > "+TestBed+"/sslCertificate.cert ")
        runThis(TestBed+"/java/bin/keytool -import -noprompt -trustcacerts -alias myCert272 -file "+TestBed+"//sslCertificate.cert -keystore "+TestBed+"/java/jre/lib/security/cacerts -storepass changeit")
        runThis("certutil -A -n myCert272 -t 'TCu,Cuw,Tuw' -i "+TestBed+"/sslCertificate.cert -keystore -d "+firefoxProfile)





def StandardSubscription():
        runThis("cp "+TestBed+"/daas_ui/InstanceInfo.xml "+TestBed+"/daas_ui/InstanceInfo.xml.orig")
        tree = ET.parse(TestBed+"/daas_ui/InstanceInfo.xml")
        root = tree.getroot()
        def UpdateXML(name,value):
                for child in root:
                        if child.attrib["name"] in name:
                                child.attrib["value"] = value

        UpdateXML("TESTSUITE","execution\daas_Cloud_UI_MATS.xml")
        UpdateXML("BUILD","Test_Standard_company")
        UpdateXML("daas.service.subscription","Standard_company")
        UpdateXML("daas.service.daasuiUrl",PropDict["DAAS_UI_URL_1"].strip())
        UpdateXML("daas.service.daasuiUserPass",PropDict["DAAS_PWD_1"].strip())
        UpdateXML("daas.service.daasuiUser",PropDict["DAAS_USER_1"])
        UpdateXML("daas.service.SSOTenantName",PropDict["DAAS_IDM_TENANT_1"].strip())
        UpdateXML("daas.service.ServiceName",PropDict["DAAS_IDM_SERVICE_1"].strip())
        UpdateXML("daas.service.EnrichmentTimeout","1000")
        tree.write(TestBed+"/output.xml")
        with open(TestBed+"/output.xml","r") as f:
                    data="".join(line for line in f if not line.isspace())
        with open(TestBed+"/daas_ui/InstanceInfo.xml","w") as f:
                f.write(data)
                f.close
        runThis("rm -rf  "+TestBed+"/output.xml")

def EnterpriseSubscription():
        runThis("cp -f "+TestBed+"/daas_ui/InstanceInfo.xml.orig "+TestBed+"/daas_ui/InstanceInfo.xml")
        tree = ET.parse(TestBed+"/daas_ui/InstanceInfo.xml")
        root = tree.getroot()
        def UpdateXML(name,value):
                for child in root:
                        if child.attrib["name"] in name:
                                child.attrib["value"] = value

        UpdateXML("TESTSUITE","execution\daas_Cloud_UI_MATS.xml")
        UpdateXML("BUILD","Test_Enterprise_company")
        UpdateXML("daas.service.subscription","Enterprise_company")
        UpdateXML("daas.service.daasuiUrl",PropDict["DAAS_UI_URL_2"].strip())
        UpdateXML("daas.service.daasuiUserPass",PropDict["DAAS_PWD_2"].strip())
        UpdateXML("daas.service.daasuiUser",PropDict["DAAS_USER_2"])
        UpdateXML("daas.service.SSOTenantName",PropDict["DAAS_IDM_TENANT_2"].strip())
        UpdateXML("daas.service.ServiceName",PropDict["DAAS_IDM_SERVICE_2"].strip())
        UpdateXML("daas.service.EnrichmentTimeout","1000")
        tree.write(TestBed+"/output.xml")
        with open(TestBed+"/output.xml","r") as f:
                    data="".join(line for line in f if not line.isspace())
        with open(TestBed+"/daas_ui/InstanceInfo.xml","w") as f:
                f.write(data)
                f.close
        runThis("rm -rf  "+TestBed+"/output.xml")



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
if [ $OS = "Linux" ]; then
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
        runThis("cp "+TestBed+"/daas_ui/common/lib/runner.conf.bkp "+TestBed+"/daas_ui/common/lib/runner.conf")



def InstallANT():
        runThis("wget -P "+TestBed+"/InstallAnt https://artifactory-slc.oraclecorp.com/artifactory/simple/odc-release-local/apache-ant/apache-ant/1.9.6/apache-ant-1.9.6-bin.tar.gz")
        runThis("tar -xvzf "+TestBed+"/InstallAnt/apache-ant-1.9.6-bin.tar.gz -C  "+TestBed)
        runThis("wget -P "+TestBed+"/InstallAnt https://artifactory-slc.oraclecorp.com/artifactory/simple/repo1-cache/org/apache/ivy/ivy/2.4.0/ivy-2.4.0.jar")
        runThis(TestBed+"/apache-ant-1.9.6/bin/ant -version")


def RunUITest():
        print "Running Standard Subscription......"
        InstallANT()
        StandardSubscription()
        runThis("export DISPLAY=:9 && export ANT_HOME="+TestBed+"/apache-ant-1.9.6 && export JAVA_HOME="+TestBed+"/java && export PATH=$PATH:"+TestBed+"/apache-ant-1.9.6/:"+TestBed+"/java && cd "+TestBed+"/daas_ui && ./run.sh",True)
        print "\n\nStandard Subscription MATS completed !!!"
        print "Pheew !!.. Let me take some rest and then run Enterprise Subscription !!"
        sleep(10)
        print "\nNow running Enterprise Subscription"
        EnterpriseSubscription()
        runThis("export DISPLAY=:9 && export ANT_HOME="+TestBed+"/apache-ant-1.9.6 && export JAVA_HOME="+TestBed+"/java && export PATH=$PATH:"+TestBed+"/apache-ant-1.9.6/:"+TestBed+"/java && cd "+TestBed+"/daas_ui && ./run.sh",True)


def updateConfigPropsAPI(value,user,password,tenant,service):
        runThis("cp "+TestBed+"/daas_api/src/main/resources/config.properties "+TestBed+"/daas_api/src/main/resources/config.properties.orig")
        ApiProp = {}
        runThis("sed '/^$/d' "+TestBed+"/daas_api/src/main/resources/config.properties.orig|grep -v '#' > "+TestBed+"/daas_api/src/main/resources/api.props")
        with open(TestBed+"/daas_api/src/main/resources/api.props","r") as f :
                for line in f:
                        (key, val) = line.split("=")
                        ApiProp[(key)] = val
                f.close()

        hostName=os.popen("echo "+value.split("/")[2]+"|cut -d: -f1|sed 's/.*data.'//").read().strip()
        Url=value.split("/")[0]+"//"+value.split("/")[2]
        proxyPort = value.split("/")[2].split(":")[1]
        for keys,value in ApiProp.items():
                ApiProp["DAAS_URI"]= Url
                ApiProp["DAAS_USERNAME"]= user
                ApiProp["DAAS_PASSWORD"]= password
                ApiProp["DAAS_TENANT_ID"]= tenant
                ApiProp["DAAS_SERVICE_NAME"]= service
                ApiProp["AV_URI"]= Url
                ApiProp["DAAS_PROXY_FLAG"]= "Yes"
                ApiProp["DAAS_PROXY_HOST"]= hostName
                ApiProp["DAAS_PROXY_PORT"]= proxyPort
                ApiProp["HTTP_PROXY"]= hostName+":"+proxyPort

        g = open(TestBed+"/daas_api/src/main/resources/config.out","w")
        for key,val in ApiProp.items():
                g.write(key+"="+val+"\n")
        g.close()

def downloadMaven():
        runThis("tar -xvzf "+TestBed+"/apache-maven-3.1.0-bin.tar.gz -C "+TestBed+"/")
        if not os.path.isdir(TestBed+"/maven"):
                runThis("mkdir "+TestBed+"/maven")
        mavenConfig="""<?xml version="1.0" encoding="UTF-8"?>
        <settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd">
          <localRepository>"+TestBed+"maven/repo</localRepository>
        </settings>
        """
        with open(TestBed+"/maven/settings.xml","w") as f:
                f.write(mavenConfig)
        f.close()

def RunAPITest():
        runThis("unzip -o "+TestBed+"/daas_api.zip -d "+TestBed+"/daas_api")
        downloadMaven()
        print "\n\n\nRunning API MATS for Standard Subscription \n\n\n"
        updateConfigPropsAPI(PropDict["DAAS_UI_URL_1"].strip(),PropDict["DAAS_USER_1"].strip(),PropDict["DAAS_PWD_1"].strip(),PropDict["DAAS_IDM_TENANT_1"].strip(),PropDict["DAAS_IDM_SERVICE_1"].strip())
        shutil.move(TestBed+"/daas_api/src/main/resources/config.out",""+TestBed+"/daas_api/src/main/resources/config.properties")
        os.remove(TestBed+"/daas_api/src/main/resources/api.props")
        runThis("export JAVA_HOME="+TestBed+"/java && export M2_HOME="+TestBed+"/apache-maven-3.1.0 && export M2="+TestBed+"/apache-maven-3.1.0/bin && export PATH=$PATH:"+TestBed+"/apache-maven-3.1.0:"+TestBed+"/apache-maven-3.1.0/bin:"+TestBed+"/java && cd "+TestBed+"/daas_api/&& ./cprun",True)

        shutil.move(TestBed+"/daas_api/src/main/resources/config.properties.orig",""+TestBed+"/daas_api/src/main/resources/config.properties")

        print "Standard Subscription API MATS completed !!Pheew.."
        sleep(10)
        print "\n\n\nRunning API MATS for Enterprise Subscription \n\n\n"
        updateConfigPropsAPI(PropDict["DAAS_UI_URL_2"].strip(),PropDict["DAAS_USER_2"].strip(),PropDict["DAAS_PWD_2"].strip(),PropDict["DAAS_IDM_TENANT_2"].strip(),PropDict["DAAS_IDM_SERVICE_2"].strip())
        shutil.move(TestBed+"/daas_api/src/main/resources/config.out",""+TestBed+"/daas_api/src/main/resources/config.properties")
        os.remove(TestBed+"/daas_api/src/main/resources/api.props")
        runThis("export JAVA_HOME="+TestBed+"/java && export M2_HOME="+TestBed+"/apache-maven-3.1.0 && export M2="+TestBed+"/apache-maven-3.1.0/bin && export PATH=$PATH:"+TestBed+"/apache-maven-3.1.0:"+TestBed+"/apache-maven-3.1.0/bin:"+TestBed+"/java && cd "+TestBed+"/daas_api/&& ./cprun",True)

def CreateResults():
        runThis("mkdir "+TestBed+"/mats_results")
        runThis("cp -rv "+TestBed+"/daas_api/target/custom_reports "+TestBed+"/mats_results")
        runThis("cp -rv "+TestBed+"/daas_ui/results "+TestBed+"/mats_results")
        print "\n\nResults store in "+TestBed+"/mats_results"




if( __name__ == "__main__"):
        try:
                counter=0
                TestBed="/u01/work/tmp/systemtests"
                PropDict = {}
                with open(TestBed+"/daas_test.properties") as f:
                        for line in f:
                                (key, val) = line.split("=")
                                PropDict[(key)] = val
                suitefile=glob.glob(TestBed+"/systemtests-*")
                version=os.path.splitext(suitefile[0])[0].split("systemtests-")[1]
                GetSuite()
                ImportSSL()
                runThis("unzip -o "+TestBed+"/daas_ui.zip -d "+TestBed+"/daas_ui")
                addHosts(PropDict["DAAS_UI_URL_1"])
                addHosts(PropDict["DAAS_UI_URL_2"])
                runThis("chmod 644 /etc/hosts")
                ConfigVNC()
                runThis("cp "+TestBed+"/daas_ui/common/lib/runner.conf "+TestBed+"/daas_ui/common/lib/runner.conf.bkp")
                config=open(TestBed+"/daas_ui/common/lib/runner.conf","r")
                outfile=open(TestBed+"/daas_ui/common/lib/runner.conf.bkp","w")
                UpdateRunner("firefox_binary","firefox_binary=/usr/local/bin/firefox\n")
                config=open(TestBed+"/daas_ui/common/lib/runner.conf","r")
                outfile=open(TestBed+"/daas_ui/common/lib/runner.conf.bkp","w")
                UpdateRunner("classpath=","classpath="+TestBed+"/.ivy2/cache/:"+TestBed+"/daas_ui/common/lib/V2:"+TestBed+"/daas_ui/common/lib/general:"+TestBed+"/daas_ui/results/compiled:"+TestBed+"/java/lib/tools.jar\n")
                config=open(TestBed+"/daas_ui/common/lib/runner.conf","r")
                outfile=open(TestBed+"/daas_ui/common/lib/runner.conf.bkp","w")
                UpdateRunner("sourcepath=","sourcepath="+TestBed+"/daas_ui/common/lib_app/:"+TestBed+"/daas_ui/testscript/\n")
                config=open(TestBed+"/daas_ui/common/lib/runner.conf","r")
                outfile=open(TestBed+"/daas_ui/common/lib/runner.conf.bkp","w")
                UpdateRunner("firefoxTemplate","firefoxTemplate="+os.environ.get("firefoxprofile")+"\n")
                RunUITest()
                downloadMaven()
                RunAPITest()
                runThis("ps -ef | grep '[ ]:9'|awk '{print $2}'|xargs  kill")
        except:
                        print "MATS failed with below error: \n\n"
                        print(traceback.format_exc())
