#!/usr/bin/python
#Author: @Mohan K
#Description: This script is used to install the micro-services
#Input:
#       1. Filename
#               format: IP Comma separated Service Names

import sys
import os
import re
from time import sleep
from multiprocessing.dummy import Pool as ThreadPool


if len(sys.argv) < 3:
        print ("Insufficient arguments provided!!")
        print ("Help:")
        print ("  "+ sys.argv[0]+" inputFile parallel/sequential")
        print ("Input File Format:")
        print ("IP1 Service1,Serice2,Service3")
        print ("IP2 Service1,Serice2,Service3")
        sys.exit(-1)

inhostname=[]
conHosts={}
with open(sys.argv[1],'r') as f:
        for line in f.readlines():
                inhostname.append(line)

qastaging1_kafka_1="""
#!/bin/bash
##
##
##
## chkconfig:
## description:  Start up qastaging1_kafka_1

#. /etc/init.d/functions

#RETVAL=$?
#KAFKA_INFA_HOME=""
case "$1" in
 start)
        if [ -f /opt/kafka-qa-staging1/infa/bin/kafka_1_start.sh ];
          then
            echo "Starting qastaging1_kafka_1"
            /opt/kafka-qa-staging1/infa/bin/kafka_1_start.sh
        fi
;;
 stop)
        if [ -f /opt/kafka-qa-staging1/infa/bin/kafka_1_stop.sh ];
          then
             echo "Stopping "
                        /opt/kafka-qa-staging1/infa/bin/kafka_1_stop.sh
        fi
  ;;
 *)
  echo "Usage: $0 {start|stop}"
exit 1
;;
esac
#exit $RETVAL

"""

qastaging1_zookeeper_1="""
#!/bin/bash
##
##
##
## chkconfig:
## description:  Start up qastaging1_zookeeper_1

#. /etc/init.d/functions

#RETVAL=$?
#KAFKA_INFA_HOME=""
case "$1" in
 start)
        if [ -f /opt/kafka-qa-staging1/infa/bin/zookeeper_1_start.sh ];
          then
            echo "Starting qastaging1_zookeeper_1"
            /opt/kafka-qa-staging1/infa/bin/zookeeper_1_start.sh
        fi
;;
 stop)
        if [ -f /opt/kafka-qa-staging1/infa/bin/zookeeper_1_stop.sh ];
          then
             echo "Stopping "
                        /opt/kafka-qa-staging1/infa/bin/zookeeper_1_stop.sh
        fi
  ;;
 *)
  echo "Usage: $0 {start|stop}"
exit 1
;;
esac
#exit $RETVAL
"""



serviceDict={'session-service':'recipe[session-service::db],recipe[session-service::app],recipe[session-service::consulConfig],recipe[session-service::consulRegister]','frs':'recipe[frs::db],recipe[frs::app],recipe[frs::consulConfig],recipe[frs::consulRegister]','license-service':'recipe[license-service::db],recipe[license-service::app],recipe[license-service::consulConfig],recipe[license-service::consulRegister],recipe[license-service::post-deploy]','auditlog-service':'recipe[auditlog-service::app],recipe[auditlog-service::consulConfig],recipe[auditlog-service::consulRegister]','migration-service':'recipe[migration-service::app],recipe[migration-service::consulConfig],recipe[migration-service::consulRegister]','bundle-service':'recipe[bundle-service::app],recipe[bundle-service::consulConfig],recipe[bundle-service::consulRegister]','scheduler-service':'recipe[scheduler-service::db],recipe[scheduler-service::app],recipe[scheduler-service::consulConfig],recipe[scheduler-service::consulRegister]','kms-service':'recipe[kms-service::db],recipe[kms-service::app],recipe[kms-service::consulConfig],recipe[kms-service::consulRegister]','cloudUI':'recipe[cloudUI::app],recipe[cloudUI::consulConfig],recipe[cloudUI::consulRegister]','cloudshell':'recipe[cloudshell::app],recipe[cloudshell::consulConfig],recipe[cloudshell::consulRegister]','preference-service':'recipe[preference-service::db],recipe[preference-service::app],recipe[preference-service::consulConfig],recipe[preference-service::consulRegister]','jlsdi':'recipe[jls-di::db],recipe[jls-di::app],recipe[jls-di::consulConfig],recipe[jls-di::consulRegister];','ca-service':'recipe[ca-service::db],recipe[ca-service::app],recipe[ca-service::consulConfig],recipe[ca-service::consulRegister]','notification-service':'recipe[notification-service::db],recipe[notification-service::app],recipe[notification-service::consulConfig],recipe[notification-service::consulRegister]','pkgr':'recipe[pkgr::app],recipe[pkgr::consulConfig],recipe[pkgr::consulRegister]','v3api':'recipe[v3api::app],recipe[v3api::consulConfig],recipe[v3api::consulRegister]','autoscaler-service':'recipe[autoscaler-service::db],recipe[autoscaler-service::app],recipe[autoscaler-service::consulConfig],recipe[autoscaler-service::consulRegister]','pc2cloud':'recipe[pc2cloud-service::db],recipe[pc2cloud-service::app],recipe[pc2cloud-service::consulConfig],recipe[pc2cloud-service::consulRegister],recipe[pc2cloudUI::app],recipe[pc2cloudUI::consulConfig],recipe[pc2cloudUI::consulRegister],recipe[sensu-config::config]','saas-ac':'recipe[saas-ac::consulConfig],recipe[saas-ac::consulRegister]','saas-da':'recipe[saas-da::consulConfig],recipe[saas-da::consulRegister]','saas-channel':'recipe[saas-channel::consulConfig],recipe[saas-channel::consulRegister]','saas-validator':'recipe[saas-validator::consulConfig],recipe[saas-validator::consulRegister]','saas':'recipe[saas::consulConfig],recipe[saas::consulRegister]','autoscaler-service':'recipe[autoscaler-service::db],recipe[autoscaler-service::app],recipe[autoscaler-service::consulConfig],recipe[autoscaler-service::consulRegister]','pc2cloud-service':'recipe[pc2cloud-service::db],recipe[pc2cloud-service::app],recipe[pc2cloud-service::consulConfig],recipe[pc2cloud-service::consulRegister],recipe[pc2cloudUI::app],recipe[pc2cloudUI::consulConfig],recipe[pc2cloudUI::consulRegister],recipe[sensu-config::config]'}

def sshHost(host,command):
        print "ssh  -i /home/ec2-user/.ssh/elb.pem  ec2-user@"+host+" '"+command+"'"
        result=os.system("ssh -q -i /home/ec2-user/.ssh/elb.pem  ec2-user@"+host+" '"+command+"'")
        return result

def runPCommand(host,comp):
        if os.system("ssh -q -i /home/ec2-user/.ssh/elb.pem  ec2-user@"+host+" "+comp) != 0:
                print "Chef Setup Failed on "+host+" for "+comp
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
                        runPCommand(host,comp)
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

def listFetch(host):
        regex=re.compile(".*("+host+").*")
        services=[m.group(0) for l in inhostname for m in [regex.search(l)] if m][0].split()[2].split(',')
        return services

def composeServices(host):
        serviceList=listFetch(host)
        recipeToRun=[]
        for i in serviceList:
                if i in serviceDict.keys():
                        addRecipe=serviceDict[i]
                        recipeToRun.append(addRecipe)
                else:
                        print "Service not defined !!"
                        sys.exit(-1)

        if sys.argv[2]=='parallel':
                cmdToRun="sudo chef-client -o "+",".join(str(x) for x in recipeToRun)
                conHosts.update({host:cmdToRun})
     
        else:
                cmdToRun="sudo chef-client -o "+",".join(str(x) for x in recipeToRun)
                print cmdToRun
                #sshHost(host,cmdToRun)      




def sequenceSteps(step):
        if step == "maids":
                cmd1="sudo chef-client -o recipe[haproxy-consul::createIdsConfig];echo $?"
                print "Running: "+cmd1
                result=sshHost(idsHost,cmd1)
                print result
                if result != 0:
                        print cmd1+"Failed, please check manually"
                        sys.exit(-1)

                cmd2="sudo systemctl start haproxy;echo $?"
                print "Running: "+cmd2
                result=sshHost(idsHost,cmd2)
                if result != 0:
                        print cmd2+"Failed, please check manually"
                        sys.exit(-1)
                cmd3='sh -c "(sudo /usr/local/bin/consul-template -template "/etc/haproxy/haproxy_consul_config.ctmpl:/etc/haproxy/haproxy.cfg:chown haproxy.haproxy /etc/haproxy/haproxy.cfg && systemctl reload haproxy")" > /dev/null &'
                print "Running: "+cmd3
                result=sshHost(idsHost,cmd3)
                if result != 0:
                        print cmd3+"Failed, please check manually"
                        sys.exit(-1)
                cmd4="echo "+qastaging1_kafka_1+" > /etc/init.d/qastaging1_kafka_1"
                result=sshHost(cmsHost,cmd6)
                if result != 0:
                        print cmd4+"Failed, please check manually"
                        sys.exit(-1)
                
                cmd5="echo "+qastaging1_zookeeper_1+" > /etc/init.d/qastaging1_zookeeper_1"
                result=sshHost(cmsHost,cmd5)
                if result != 0:
                        print cmd5+"Failed, please check manually"
                        sys.exit(-1)
                
                cmd6="sudo chef-client -o recipe[kafka::zookeeper],recipe[kafka::kafka] -E qa-stage1-test-pod1-kafka;sudo chown -R kafka:kafka /opt/kafka-qa-int1;sudo chown kafka:kafka /etc/init.d/qaint1_*;sudo service qaint1_zookeeper_1 start;sudo service qaint1_kafka_1 start"
                print "Running: "+cmd6
                result=sshHost(cmsHost,cmd6)
                if result != 0:
                        print cmd4+"Failed, please check manually"
                        sys.exit(-1)
                cmd6='sudo chef-client -o recipe[identity-service::db],recipe[ma-service::db];sudo chef-client -o recipe[identity-service::app],recipe[identity-service::consulConfig],recipe[identity-service::consulRegister],recipe[identity-service::post-deploy];sudo chef-client -o recipe[ma-service::app],recipe[ma-service::consulConfig],recipe[ma-service::consulRegister];sudo chef-client -o recipe[content-repository-service::db];sudo chef-client -o recipe[content-repository-service::app],recipe[content-repository-service::consulConfig],recipe[content-repository-service::consulRegister];sudo chef-client -o recipe[v3api::app],recipe[v3api::consulConfig],recipe[v3api::consulRegister];echo $?'
                print "Running: "+cmd5
                result=sshHost(idsHost,cmd5)
                if result != 0:
                        print cmd5+"Failed, please check manually"
                        sys.exit(-1)
        

if( __name__ == "__main__"):
        

        regex=re.compile(".*(maids).*")
        idsHost=[m.group(0) for l in inhostname for m in [regex.search(l)] if m][0].split()[0]
        regex=re.compile(".*(cms).*")
        cmsHost=[m.group(0) for l in inhostname for m in [regex.search(l)] if m][0].split()[0]
        regex=re.compile(".*(ics).*")
        icsHost=[m.group(0) for l in inhostname for m in [regex.search(l)] if m][0].split()[0]
        sequenceSteps('maids')
        composeServices(cmsHost)
        composeServices(idsHost)
        composeServices(icsHost)
        #print conHosts
        if sys.argv[2]=='parallel':
                startThread()
        

        

        