#!/usr/bin/python
#DT:02.01.2016
#@Sidharth Mohapatra
#Creates property for C9 preflight

import os,sys,socket
import mmap,json

workdir=sys.argv[1]
type=sys.argv[2]
autowork=os.getenv("AUTO_WORK")
propFile=autowork+'/DaaSPropTemplate.txt'
prop=autowork+'/props.txt'
pwds=autowork+'/pwds.txt'

if workdir.endswith("/") is False:
        workdir=workdir+"/"

#Call CreateIDMPod.pl script here
os.system("./ConfigurePod.pl")

#Parse property file here
def searchValues(file,val):
        with open(file,'r') as f:
                for line in f:
                        if val in line:
                                (lvalue,rvalue)=line.split('=')
                                return rvalue.rstrip('\n')


val='daas_daas_pod_name'
podname=searchValues(propFile,val)
val="OAM-SERVER"
oidhost=searchValues("feeder.txt",val)

with open(prop,'a') as f:
        f.write("INSTALL_TYPE="+type+"\n")
        f.write("daas_daas_pod_name="+podname+"\n")
        f.write("PATCH_LOCATION="+workdir+"prop/patchzip"+"\n")
        f.write("daasdaaswlsadmin_deploy_daascuratordnb_username=onboarder"+"\n")
        f.write("daasdaaswlsadmin_deploy_daascuratordnb_password=Welcome2"+"\n")
        f.write("daas_test_identity_domain_name="+podname.split("pod01")[0]+"tenant01\n")
        f.write("daas_test_service_instance_name="+podname+"\n")
        f.write("daas_test_identity_domain_user_name="+podname.split("pod01")[0]+"tenant01admin\n")
        f.write("SDI_APPID_USER=OCLOUD9_SDI_APPID"+"\n")
        f.write("SDI_APPID_PASSWD=Qazygkl1b7w.fp"+"\n")
        f.write("DATALOC="+workdir+"ftp"+"\n")
        f.write("DATAFTPHOST="+socket.gethostname()+"\n")
        f.write("FTPUSER=oracle"+"\n")
        f.write("FTPPASS=welcome1"+"\n")
        f.write("OHSHOST="+socket.gethostname()+"\n")
        f.write("DAASOHS_LISTEN=8471"+"\n")
        f.write("EDQAVOHS_LISTEN=8471"+"\n")
        f.write("PROVOHS_LISTEN=8571"+"\n")
        f.write("EDQOHS_LISTEN=8671"+"\n")
        f.write("CHEFSERVICE=daas"+"\n")
        f.write("NIMBULA_PASSWORD=Orclization"+"\n")
        f.write("NIMBULA_USER=/opcdaas/dqa"+"\n")
        f.write("NIMBULA_API=https://api.oracleinternalucf2c.oraclecorp.com/"+"\n")
        f.write("CHEF_SERVER=grill.us.oracle.com"+"\n")
        f.write("CHEF_USER=daas"+"\n")
        f.write("CHEF_PASSWORD=orchestration"+"\n")
        f.write("BIGFILEREPO=http://"+socket.gethostname()+"/bigrepo/"+type+"/\n")
        f.write("NIMBULA_CUSTOMER=opcdaas"+"\n")
        f.write("NIMBULA_DOMAIN=oracleinternalucf2c.oraclecorp.com"+"\n")
        f.write("NIMBULA_ENV=ucf2c"+"\n")
        f.write("additional_data_bag_item="+workdir+"prop/emcc.json"+"\n")
        f.write("IDM_DUMP_FILE_PATH=/net/"+oidhost+"/scratch/aime/"+podname+".dmp\n")

f.close()

with open(pwds,'a') as f:
        f.write("daas_owsm_keystore_password=welcome1\n")
        f.write("daas_daasdb_sys_password=welcome1\n")
        f.write("daas_daasdb_user_password=daas_app\n")
        f.write("daas_edqdb_sys_password=welcome1\n")
        f.write("daas_edqdb_user_password=daas_edq\n")
        f.write("daas_dbmrddb_sys_password=welcome1\n")
        f.write("daas_dbmrddb_user_password=daas_dbmrd\n")
        f.write("daas_owsmdb_sys_password=welcome1\n")
        f.write("daas_owsmdb_schema_password=welcome1\n")
        f.write("daasedq73wlsadmin_owsmdb_schema_password=daas_owsm\n")
        f.write("daasedq79wlsadmin_owsmdb_schema_password=welcome1\n")
        f.write("daas_daaswlsadmin_opssdb_schema_password=welcome1\n")
        f.write("daas_edq79wlsadmin_opssdb_schema_password=welcome1\n")
        f.write("daas_daasprovwlsadmin_opssdb_schema_password=welcome1\n")
f.close()
if os.path.isdir(autowork+"/c9prop/"):
        os.system("rm -rf "+autowork+"/c9prop")

os.system("mkdir "+autowork+"/c9prop")
os.system("mkdir "+autowork+"/c9prop/patchzip")
os.system("mv "+prop+" "+autowork+"/c9prop")
os.system("mv "+pwds+" "+autowork+"/c9prop")
os.system("cp "+"/net/"+oidhost+"/scratch/aime/"+podname+".dmp"+" "+autowork+"/c9prop")

print "All properties created and stored under "+autowork+"/c9prop"
