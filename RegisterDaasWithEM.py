import pexpect
import subprocess
import os
import re
import sys
from os.path import expanduser

#Sample how to run
#python em.py paramfile


result1 = r'\(yes\/no\)\? '
result2 = re.compile('password:',re.I)
result3 = r'.*[$#] '
podId = None
failed = re.compile('failed',re.I)
err = re.compile('error',re.I)
success = re.compile('successful',re.I)
paramdict = {}
try:
	logfile = open("em.log","w")
except IOError:
	print "Can't create log file here....redirecting to /tmp/em.log"
	logfile = open("/tmp/em.log","w")

def execcommand(cmd=None):
	output = subprocess.Popen(cmd,stdout=logfile, stderr=logfile,shell=True)
	output.communicate()[0]
	print "\n return code  ------>"+str(output.returncode)
	return output.returncode

def error():
	logfile.close()
	sys.stdout = sys.__stdout__
	print "\nSome error ocurred please check em.log"
	sys.exit(127)

def login(user=None,host=None,password=None):
  child = pexpect.spawn("ssh -l %s  %s" %(user,host))
  child.logfile = logfile
  try:
    ret1 = child.expect([result1,result2,pexpect.EOF])
    if(ret1 == 0):
      child.sendline("yes")
      ret2 = child.expect([result2,pexpect.EOF])
      if(ret2 == 0):  
        child.sendline(password)
        ret3 = child.expect([result3,pexpect.EOF])
        if(ret3 == 0):
          print "\n logged in successfully"
          return child
    elif(ret1 == 1):
      child.sendline(password)
      ret3 = child.expect([result3,pexpect.EOF])
      if(ret3 == 0):
        print "\n logged in successfully"
        return child
  except:
    print "\nUnable to login got timeout"
    child.close()
    error()

def generateScripts(daas_ops_home=None, podId=None, podtenant=None, hostname=None, curatorUsr=None, curPass=None, emUsr=None, emPass=None, host=None, daasemagent_em_upload_port=None, emgcUIpass=None):
	os.chdir(daas_ops_home+"/daas-ops-home/daas-ops/nodes/emagent/template/discovery-scripts/")
	add = './addDaaSPod.sh -s "Oracle Social Data Service Pod Instance '+podId+'" -t "oracle_data_pod" -k "Oracle Social Data Service Search Cluster Instance '+podId+'" -u "oracle_data_search" -o "'+hostname+'" -a "3872" -m "'+host+'" -r "'+daasemagent_em_upload_port+'" -i "MachineName='+hostname+';Port=7001;protocol=t3;service=weblogic.management.mbeanservers.domainruntime;MetricSource=WebLogic;MonitoringURI=http://'+hostname+':7005/data;CloudInfraDomain='+podtenant+';CloudInfraService='+podId+'" -c "UserName:'+emUsr+';password:'+emPass+'" -d "Alias:'+curatorUsr+';Password:'+curPass+'" -p "em_client_password='+emgcUIpass+';em_client_user=sysman;EMGC_OMS_ACCESS_PROTOCOL=http;customer.name=;subscription.id=;csi.number=;department=;line.of.business=data;comment=;lifecycle.status=;location=" -w "weblogic_server_version=10;administration_server_host='+hostname+';port=7001;username='+emUsr+';password='+emPass+';external_parameters=;jmx_protocol=;jmx_server_url=;unique_domain_identifier=daas_farm'+podId+';agent_url=https://'+hostname+':3872/emd/main/;domain_name=daas_domain" -x "weblogic_server_version=10;administration_server_host='+hostname+';port=8001;username='+emUsr+';password='+emPass+';external_parameters=;jmx_protocol=;jmx_server_url=;unique_domain_identifier=prov_farm'+podId+';agent_url=https://'+hostname+':3872/emd/main/;domain_name=prov_domain" -q "weblogic_server_version=10;administration_server_host='+hostname+';port=9991;username='+emUsr+';password='+emPass+';external_parameters=;jmx_protocol=;jmx_server_url=;unique_domain_identifier=edq_farm'+podId+';agent_url=https://'+hostname+':3872/emd/main/;domain_name=base_domain" -n "weblogic_server_version=10;administration_server_host='+hostname+';port=9996;username='+emUsr+';password='+emPass+';external_parameters=;jmx_protocol=;jmx_server_url=;unique_domain_identifier=edq79_farm'+podId+';agent_url=https://'+hostname+':3872/emd/main/;domain_name=edq_domain"'
	delete = './deleteDaaSPod.sh -s "Oracle Social Data Service Pod Instance '+podId+'" -t "oracle_data_pod" -k "Oracle Social Data Service Search Cluster Instance '+podId+'" -u "oracle_data_search" -m "'+host+'" -r "'+daasemagent_em_upload_port+'" -p "em_client_password='+emgcUIpass+';em_client_user=sysman;EMGC_OMS_ACCESS_PROTOCOL=http" -w "unique_domain_identifier=daas_farm'+podId+';domain_name=daas_domain" -x "unique_domain_identifier=prov_farm'+podId+';domain_name=prov_domain" -q "unique_domain_identifier=edq_farm'+podId+';domain_name=base_domain" -n "unique_domain_identifier=edq79_farm'+podId+';domain_name=edq_domain"'
	addpod_fp = open("add","w")
	addpod_fp.truncate()
	addpod_fp.write(add)
	addpod_fp.close()
	deletepod_fp = open("delete","w")
	deletepod_fp.truncate()
	deletepod_fp.write(delete)
	deletepod_fp.close()
	os.system("chmod 777 *")
	os.system("mkdir -p ~/%s" % (podId))
	os.system("cp * ~/%s" % (podId))

def secureCopy(user=None,host=None,password=None):
  direc = expanduser("~")
  child = pexpect.spawn("scp -r %s/%s %s@%s:/tmp" %(direc,podId,user,host))
  child.logfile = logfile
  try:
    ret1 = child.expect([result1,result2,pexpect.EOF])
    if(ret1 == 0):
      child.sendline("yes")
      ret2 = child.expect([result2,pexpect.EOF])
      if(ret2 == 0):  
        child.sendline(password)
        ret3 = child.expect([result3,pexpect.EOF])
        if(ret3 == 0):
          print "\n copied successfully"
          child.close()
    elif(ret1 == 1):
      child.sendline(password)
      ret3 = child.expect([result3,pexpect.EOF])
      if(ret3 == 0):
        print "\n copied successfully"
        child.close()
  except:
    print "\nUnable to login got timeout"
    error()


def editConf(daas_node_instance=None, emhost=None, zipfile=None, daasemagent_em_upload_port=None):
	conf = daas_node_instance+"/pyconf/conf_22.py"
	fp_conf = open(conf,"r")
	conf_data = fp_conf.read()
	conf_data = conf_data.replace('daasemagent_oms_host', "daasemagent_oms_host = '%s'\n#" % emhost)
	conf_data = conf_data.replace('daasemagent_em_upload_port', "daasemagent_em_upload_port = %s\n#" % daasemagent_em_upload_port)
	conf_data = conf_data.replace('daasemagent_port ', "daasemagent_port = 3872\n#")
	conf_data = conf_data.replace('daasemagent_installer_filename', "daasemagent_installer_filename = '%s'\n#" % zipfile)
	fp_conf.close()
	os.rename(conf,conf+"_old")
	fp_conf = open(conf,"w")
	fp_conf.write(conf_data)
	fp_conf.close()

def editPsswd(daas_node_instance=None, emgcUIpass=None):
	passwd = daas_node_instance+"/pyconf/pwds_22.py"
	fp_passwd = open(passwd,"r")
	passwd_data = fp_passwd.read()
	passwd_data = passwd_data.replace('daasemagent_registration_password ', "daasemagent_registration_password = '%s'\n#" % emgcUIpass)
	fp_passwd.close()
	os.rename(passwd,passwd+"_old")
	fp_passwd = open(passwd,"w")
	fp_passwd.write(passwd_data)
	fp_passwd.close()

def preReq(URL=None,DaasMedia=None,zipfile=None):
	if(os.path.isfile(DaasMedia+zipfile) == False):
		os.chdir(DaasMedia)
		if(execcommand("wget %s" % URL) !=0 ):
			print "\ncommand wget "+URL+" failed."
	if(os.path.isdir("/u01/app")):
		direc = "/u01/app"
	else:
		direc = expanduser("~")
	if(execcommand('/usr/local/packages/aime/ias/run_as_root "rm -rf /etc/oraTab /etc/oraInst.loc /etc/oragchomelist %s/oraInventory"' % direc) != 0):
		print "\nUnable to delete dependencies"

def emAction(daas_ops_home=None,daas_node_instance=None,action=None):
	os.chdir(daas_ops_home+"daas-ops-home/daas-ops/nodes/")
	os.system("cp -f setupenv.py Msetupenv.py")
	os.system("sed -i 's|sys.exit.*|sys.exit(subprocess.call( sys.argv[1], shell=True ))|g' Msetupenv.py")
	os.chdir(daas_ops_home+"daas-ops-home/daas-ops/highlevel/")
	if(execcommand("export daas_node_instance=%s ; python ../nodes/Msetupenv.py 'python emagent.py %s';exit" % (daas_node_instance,action)) != 0):
		print "\n setup failed"
		error()
	#root scripts
	if(os.path.isdir("/u01/app")):
		direc = "/u01/app"
	else:
		direc = expanduser("~")
	if(action == "setup"):
		if(execcommand('/usr/local/packages/aime/ias/run_as_root "%s/oraInventory/orainstRoot.sh"' % direc) != 0):
			print "\n oraInventory/orainstRoot.sh  script failed"
			error()
		if(execcommand('/usr/local/packages/aime/ias/run_as_root "%s/emagent/core/12.1.0.4.0/root.sh"' % daas_node_instance) != 0):
			print "\n emagent/12.1.0.4.0/orainstRoot.sh script failed"
			error()


def podAction(child=None, emhost=None, action=None, envtype=None, emgcUIport=None, emgcUIpass=None, OMS_HOME=None):
	if(action == 'setup'):
		command = 'add'
	else:
		command = 'delete'
	child.sendline("chmod -R 777 /tmp/%s" % podId)
	if(envtype == 'pool'):
		child.sendline("sudo su -")
		child.sendline("su - emadm")
		child.sendline("export OMS_HOME=%s" % OMS_HOME)
		child.sendline("export PATH=${PATH}:${OMS_HOME}/bin")
	else:
		child.sendline("setenv OMS_HOME %s" % OMS_HOME)
		child.sendline("setenv PATH ${PATH}:${OMS_HOME}/bin")
	child.sendline("cd /tmp/%s" % podId)
	try:
		child.sendline("emcli setup -url=https://%s:%s/em -username=sysman -pass=%s" % (emhost,emgcUIport,emgcUIpass))	
		ret1 = child.expect([result1,success,pexpect.EOF])
		if(ret1 == 0):
			child.sendline("yes")
			ret2 = child.expect([success,pexpect.EOF])
			if(ret2 == 0):
				print "\n**************emcli setup completed***********"
			else:
				print "\nerror occurred"
		elif(ret1 == 1):
			print "\n**************emcli setup completed***********"
		else:
			print "\nerror occured"
			child.close()
			error()
		child.sendline("bash %s" % command)
		ret1 = child.expect([err,success,pexpect.EOF])
		if(ret1 == 0):
			error()
		elif(ret1 == 1):
			child.sendline("exit")
			print "\n"+child.before
		child.close()
	except:
		print "\n Exception occured please check logs"
		error()

if( __name__ == '__main__'):
  if(len(sys.argv) != 2 ):
    print "\nSome arguments missing or extra. Found "+str(len(sys.argv))+" arguments"
    print "\nUsage: python em.py paramfile"
    error()
  else:
	#all vars
	print "\n logs redirected to em.log"
	logfile.truncate()
	sys.stdout = logfile
	sys.stderr = logfile
	print sys.argv[1]
	param_fp = open(sys.argv[1],"r")
	paramNum = 0
	for line in param_fp:
		line = line.strip("\n")
                if line:
                   if not line.startswith("#"):
		      paramdict[line.split("=")[0].strip()] = line.split("=")[1].strip()
		      paramNum = paramNum + 1

	#if(paramNum != 20):
		#print "\nSome mandatory options missing or extra. Found "+str(paramNum)+" arguments"
		#error()

	print "\nall parameters\n"
	print paramdict
	podId = paramdict['podId']
	tmp = paramdict['bigrepoUrl']
	zipfile = tmp.split("/")[-1]

	#call methods
	if(paramdict['action'] == 'setup'):
		preReq(paramdict['bigrepoUrl'],paramdict['DaasMedia'],zipfile)
		print "\n ******************** pre-req completed***************************"

		editConf(paramdict['daas_node_instance'],paramdict['emhost'],zipfile,paramdict['daasemagent_em_upload_port'])
		print "\n ******************** editConf completed***************************"

		editPsswd(paramdict['daas_node_instance'],paramdict['emgcUIpass'])
		print "\n ******************** editPsswd completed***************************"

		emAction(paramdict['daas_ops_home'],paramdict['daas_node_instance'],paramdict['action'])
		print "\n ******************** installEM completed***************************"

	generateScripts(paramdict['daas_ops_home'],paramdict['podId'],paramdict['podtenant'],paramdict['podhost'],paramdict['curatorUsr'],paramdict['curPass'],paramdict['emUsr'],paramdict['emPass'],paramdict['emhost'],paramdict['daasemagent_em_upload_port'],paramdict['emgcUIpass'])
	print "\n ******************** generateScripts completed***************************"

	secureCopy(paramdict['emhostUsr'],paramdict['emhost'],paramdict['emhostPass'])
	print "\n ******************** secureCopy completed***************************"

	child = login(paramdict['emhostUsr'],paramdict['emhost'],paramdict['emhostPass'])
	print "\n ******************** login em host completed***************************"

	podAction(child,paramdict['emhost'],paramdict['action'],paramdict['envtype'],paramdict['emgcUIport'],paramdict['emgcUIpass'],paramdict['OMS_HOME'])
	print "\n ********************pod "+paramdict['action']+" completed in emcc***************************"

	if(paramdict['action'] == 'cleanup'):
		emAction(paramdict['daas_ops_home'],paramdict['daas_node_instance'],paramdict['action'])
		print "\n ******************** cleanup completed ********************"
	logfile.close()
	sys.stdout = sys.__stdout__
	print "\n************** successful ****************"
