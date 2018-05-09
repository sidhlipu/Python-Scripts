#!/usr/bin/python
#Date: 14.4.2015
#Author: siddharth.mohapatra@oracle.com
#This is a parser script which populates data-dictionary.json as
#per DaaS Pod properties.
#Arguments #4
#1. InputDir Path 2. DaaS Pod Properties 3. DaaS Pod Passwd Properties
#4. daas-ops-home path
###########################################################################

import os,sys
import json


if len(sys.argv) < 5 :
        print 'Insufficient number of arguments !! See help below'
        print sys.argv[0]+' <InputDir> <daas-ops-home path> <DaaS Prop File> <Daas Passwd Prop file>'
        sys.exit(-1)

#########################
#Collect Prop files path#
#########################

InputDir=sys.argv[1]
OpsHomePath=sys.argv[2]
PodSetupProp=sys.argv[3]
PodPasswdProp=sys.argv[4]
PODJSON=InputDir+'/pod.json'
DictFile=OpsHomePath+'/daas-ops/utils/dd-tool/data-dictionary.json'

##################################
#Load the values in the dict file#
##################################

dict = json.load(open(DictFile))

#########################################
#Collect values from from the prop files#
#########################################
try:
	BFR=os.popen("cat "+PodSetupProp+"|grep -w BIGFILEREPO|awk -F= '{print $2}'").read()
	BFR=BFR.strip()

	FTPHOST=os.popen("cat "+PodSetupProp+"|grep -w DATAFTPHOST|awk -F= '{print $2}'").read()
	FTPHOST=FTPHOST.strip()

	CURATORPASWD = os.popen("cat "+PodSetupProp+"|grep -w FTPPASS|awk -F= '{print $2}'").read()
	CURATORPASWD = CURATORPASWD.strip()

	CURATORDNBUSERNAME = os.popen("cat "+PodSetupProp+"|grep -w FTPUSER|awk -F= '{print $2}'").read()
	CURATORDNBUSERNAME = CURATORDNBUSERNAME.strip()

	DAASDBPASSWD = os.popen("cat "+PodPasswdProp+"|grep -w daas_daasdb_user_password|awk -F= '{print $2}'").read()
	DAASDBPASSWD = DAASDBPASSWD.strip()

	DBMRDPASSWD = os.popen("cat "+PodPasswdProp+"|grep -w daas_dbmrddb_user_password|awk -F= '{print $2}'").read()
	DBMRDPASSWD = DBMRDPASSWD.strip()

	EDQ73DBPASSWD = os.popen("cat "+PodPasswdProp+"|grep -w daasedq73wlsadmin_owsmdb_schema_password|awk -F= '{print $2}'").read()
	EDQ73DBPASSWD = EDQ73DBPASSWD.strip()

	EDQ79DBPASSWD = os.popen("cat "+PodPasswdProp+"|grep -w daasedq79wlsadmin_owsmdb_schema_password|awk -F= '{print $2}'").read()
	EDQ79DBPASSWD = EDQ79DBPASSWD.strip()

	EDQUSERPASSWORD = os.popen("cat "+PodPasswdProp+"|grep -w daas_edqdb_user_password|awk -F= '{print $2}'").read()
	EDQUSERPASSWORD = EDQUSERPASSWORD.strip()

	DBHOSTNAME = os.popen('hostname -f').read()
	DBHOSTNAME = DBHOSTNAME.strip()

	OWSMDBSCHEMAPASSWORD = os.popen("cat "+PodPasswdProp+"|grep -w daas_owsmdb_schema_password|awk -F= '{print $2}'").read()
	OWSMDBSCHEMAPASSWORD = OWSMDBSCHEMAPASSWORD.strip()

	DBSYSPASSWORD = os.popen("cat "+PodPasswdProp+"|grep -w daas_daasdb_sys_password|awk -F= '{print $2}'").read()
	DBSYSPASSWORD = DBSYSPASSWORD.strip()

	EDQ73OHSHOST = os.popen("cat "+PodSetupProp+"|grep -w OHSHOST|awk -F= '{print $2}'").read()
	EDQ73OHSHOST = EDQ73OHSHOST.strip()

	EDQ73OHSLISTEN = os.popen("cat "+PodSetupProp+"|grep -w EDQOHS_LISTEN |awk -F= '{print $2}'").read()
	EDQ73OHSLISTEN = EDQ73OHSLISTEN.strip()

	IDENTITYDOMAINNAME = os.popen("cat "+PodSetupProp+"|grep -w daas_test_identity_domain_name|awk -F= '{print $2}'").read()
	IDENTITYDOMAINNAME = IDENTITYDOMAINNAME.strip()

	IDENTITYDOMAINUSERNAME = os.popen("cat "+PodSetupProp+"|grep -w daas_test_identity_domain_user_name|awk -F= '{print $2}'").read()
	IDENTITYDOMAINUSERNAME = IDENTITYDOMAINUSERNAME.strip()

	IDENTITYDOMAINUSERPASSWORD =  os.popen("cat "+PodPasswdProp+"|grep -w daas_test_identity_domain_user_password|awk -F= '{print $2}'").read()
	IDENTITYDOMAINUSERPASSWORD = IDENTITYDOMAINUSERPASSWORD.strip()
	
	NIMBULACUST = os.popen("cat "+PodSetupProp+"|grep -w NIMBULA_CUSTOMER|awk -F= '{print $2}'").read()
 	NIMBULACUST = NIMBULACUST.strip()

	NIMBULADOMAIN = os.popen("cat "+PodSetupProp+"|grep -w NIMBULA_DOMAIN |awk -F= '{print $2}'").read()
	NIMBULADOMAIN = NIMBULADOMAIN.strip()
	NIMBULADOMAIN = NIMBULACUST+"."+NIMBULADOMAIN

	NIMBULAENV = os.popen("cat "+PodSetupProp+"|grep -w NIMBULA_ENV|awk -F= '{print $2}'").read()
	NIMBULAENV = NIMBULAENV.strip()

	PATCH_VERSION = os.popen("cat "+PodSetupProp+"|grep -w DAAS_VERSION|awk -F= '{print $2}'").read()
	PATCH_VERSION = PATCH_VERSION.strip()

	PODNAME = os.popen("cat "+PodSetupProp+"|grep -w daas_daas_pod_name|awk -F= '{print $2}'").read()
	PODNAME = PODNAME.strip().lower()

	DAASOHSLISTEN = os.popen("cat "+PodSetupProp+"|grep -w DAASOHS_LISTEN|awk -F= '{print $2}'").read()
	DAASOHSLISTEN = DAASOHSLISTEN.strip()

	PROVOHSLISTEN = os.popen("cat "+PodSetupProp+"|grep -w PROVOHS_LISTEN|awk -F= '{print $2}'").read()
	PROVOHSLISTEN = PROVOHSLISTEN.strip()

	SDIDAASAPPBASEURI = "http://data."+os.popen("cat "+PodSetupProp+"|grep -w OHSHOST|awk -F= '{print $2}'").read().strip()+":"+DAASOHSLISTEN

	SDIPROVISIONINGBASEURI  = "http://"+os.popen("cat "+PodSetupProp+"|grep -w OHSHOST|awk -F= '{print $2}'").read().strip()+":"+PROVOHSLISTEN

	SERVICE = os.popen("cat "+PodSetupProp+"|grep -w CHEFSERVICE|awk -F= '{print $2}'").read()
	SERVICE = SERVICE.strip()

	SERVICEINSTANCENAME = os.popen("cat "+PodSetupProp+"|grep -w daas_test_service_instance_name|awk -F= '{print $2}'").read()
	SERVICEINSTANCENAME  = SERVICEINSTANCENAME.strip()

	USER = os.popen("cat "+PodSetupProp+"|grep -w NIMBULA_USER|cut -d'=' -f 2|cut -d'/' -f 3").read()
	USER = USER.strip()

	PATCHVERSION = os.popen("cat "+PodSetupProp+"|grep -w DAAS_VERSION|awk -F= '{print $2}'").read()
	PATCHVERSION = PATCHVERSION.strip()

	CURATORDNBREMOTELOCATION = os.popen("cat "+PodSetupProp+"|grep -w DATALOC|awk -F= '{print $2}'").read()
	CURATORDNBREMOTELOCATION = CURATORDNBREMOTELOCATION.strip()
except:
	print 'Failed while fetching values from Prop files'
	sys.exit(-1)

######################################################
#Replace the values collected in data-dictionary.json#
######################################################

dict['DD_IPLIST_INTRA'] = '0.0.0.0/0'
dict['DD_IPLIST_PUBLIC'] = '0.0.0.0/0'
dict['DD_BIGFILEREPO_URL'] = BFR
dict['DD_CURATORDNB_INPUTFILEURL'] = 'sftp://'+FTPHOST
dict['DD_CURATORDNB_REMOTELOCATION'] = CURATORDNBREMOTELOCATION
dict['DD_DB_RACONS'] = ''
dict['DD_CURATORDNB_PASSWORD'] = CURATORPASWD
dict['DD_DB_DAAS_USER_PASSWORD'] = DAASDBPASSWD
dict['DD_DB_DBMRD_USER_PASSWORD'] = DBMRDPASSWD
dict['DD_DB_EDQ73OWSMDB_SCHEMA_PASSWORD'] = EDQ73DBPASSWD
dict['DD_DB_EDQ79OWSMDB_SCHEMA_PASSWORD'] = EDQ79DBPASSWD
dict['DD_DB_EDQ_USER_PASSWORD'] = EDQUSERPASSWORD
dict['DD_DB_HOSTNAME'] = DBHOSTNAME
dict['DD_DB_OWSMDB_SCHEMA_PASSWORD'] = OWSMDBSCHEMAPASSWORD
dict['DD_DB_PORT'] = '1521'
dict['DD_DB_SERVICE'] = 'orcl.us.oracle.com'
dict['DD_DB_SYS_PASSWORD'] = DBSYSPASSWORD
dict['DD_DB_SYS_USERNAME'] = 'sys'
dict['DD_DEPLOYMENTNAME'] = 'daasmaster'
dict['DD_EDQ73_OHS_HOST'] = EDQ73OHSHOST
dict['DD_EDQ73_OHS_LISTEN'] = EDQ73OHSLISTEN
dict['DD_IDENTITY_DOMAIN_NAME'] = IDENTITYDOMAINNAME
dict['DD_IDENTITY_DOMAIN_USER_NAME'] = IDENTITYDOMAINUSERNAME
dict['DD_IDENTITY_DOMAIN_USER_PASSWORD'] = IDENTITYDOMAINUSERPASSWORD
dict['DD_NIMBULA_DOMAIN'] = NIMBULADOMAIN
dict['DD_NIMBULA_ENV'] = NIMBULAENV
dict['DD_PATCH_VERSION'] = PATCHVERSION
dict['DD_PODNAME'] = PODNAME
dict['DD_PROXYCLIENT'] = ''
dict['DD_SDI_DAASAPP_BASEURI'] = SDIDAASAPPBASEURI
dict['DD_SDI_PROVISIONING_BASEURI'] = SDIPROVISIONINGBASEURI
dict['DD_SERVICE'] = SERVICE
dict['DD_SERVICE_INSTANCE_NAME'] = SERVICEINSTANCENAME
dict['DD_USER'] = USER
dict['DD_CURATORDNB_USERNAME'] = CURATORDNBUSERNAME

##############################################
#Lets load the values in data-dictionary.json#
##############################################

json.dump(dict,open(InputDir+'/data-dictionary.json','w'),indent=0)

#####################################
#Running replace-dd.py parser script#
#####################################
try:
	os.system(OpsHomePath+'/daas-ops/utils/dd-tool/replace-dd.py '+InputDir)
	print "Successfully ran replace-dd.py"
	if os.system("ls -l "+PODJSON) == 0:
		os.system(" sed -i 's/somedir or somefile.json/%extradatabaggage%/g' "+PODJSON)
	else:
		print "pod.json doesn't exist"
		sys.exit(-1)
except:
	print "Failed while running replace-dd.py"
	sys.exit(-1)

