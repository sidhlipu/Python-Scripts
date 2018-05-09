# Author : Kodath.Roshan@oracle.com
# Date of compilation: 17-03-2014

import re
import sys
import os



def ConvertToJson(Filename):
  sep = r':'
  global data
  data = dict()
  fp = open(Filename, "r")
  for line in  fp.readlines():
      data[re.sub(r'\s','',line.rstrip().split(sep,1)[0])] = re.sub(r'\s','',line.rstrip().split(sep,1)[1])



def FetchProps(OFilename):
    jsontodict = data 
    conf22jsonfile = open(OFilename, "w")

    idstoreservicetype = jsontodict['IDSTORE_SERVICE_TYPE']
    conf22jsonfile.write("daas_daas_pod_name=%s\n" % (jsontodict['IDSTORE_SERVICE_NAME']) )
    conf22jsonfile.write("daasdaaswlsadmin_oid_host=%s\n" % (jsontodict['IDSTORE_HOST']) )
    match = re.search('cn=(\w+)' , jsontodict['OCLOUD9_SERVICE_WLS_APPID'])
    conf22jsonfile.write("daas_daas_wlsadmin_username=%s\n" % (match.group(1)) )
    conf22jsonfile.write("daas_prov_wlsadmin_username=%s\n" % (match.group(1)) )
    conf22jsonfile.write("daas_edq73_wlsadmin_username=%s\n" % (match.group(1)) )
    conf22jsonfile.write("daas_daas_wlsnodemanager_username=%s\n" % (jsontodict['OCLOUD9_SERVICE_NM_APPID']) )
    conf22jsonfile.write("daas_prov_wlsnodemanager_username=%s\n" % (jsontodict['OCLOUD9_SERVICE_NM_APPID']) )
    conf22jsonfile.write("daas_edq73_wlsnodemanager_username=%s\n" % (jsontodict['OCLOUD9_SERVICE_NM_APPID']) )
    conf22jsonfile.write("daasdaaswlsadmin_oid_port=%s\n" % (jsontodict['IDSTORE_PORT']) )
    conf22jsonfile.write("daasdaaswlsadmin_oid_username=%s\n" % (jsontodict['DATASERVICE_IDROUSER']) )
    match = re.search('(cn=%s.*)'%(idstoreservicetype), jsontodict['OCLOUD9_SERVICE_NM_APPID'])
    conf22jsonfile.write("daasdaaswlsadmin_oid_base_dn=%s\n" % (match.group(1)) )
    conf22jsonfile.write("daasdaaswlsadmin_crosstenant_url=ldap://%s:%s\n" % (jsontodict['IDSTORE_HOST'],jsontodict['IDSTORE_PORT']) )
    conf22jsonfile.write("daasdaaswlsadmin_crosstenant_username=%s\n" % (jsontodict['DATASERVICE_IDROUSER']) )
    match = re.search('cn=(\w+)' , jsontodict['DATASERVICE_API_APPID'])
    conf22jsonfile.write("daasdaaswlsadmin_deploy_daasappid_username=%s\n" % (match.group(1)) )
    conf22jsonfile.write("daasedq73wlsadmin_owsm_role_name=%s\n" % (match.group(1) + '_ROLE') )
    match = re.search('cn=(\w+)' , jsontodict['DATASERVICE_API_APPID'])
    conf22jsonfile.write("daasdaaswlsadmin_deploy_daasedqws_username=%s\n" % (match.group(1)) )
    match = re.search('cn=(\w+)' , jsontodict['DATASERVICE_CCONSOLE_APPID'])
    conf22jsonfile.write("daasdaaswlsadmin_deploy_daascuratordnb_username=%s\n" % (match.group(1)) )
    conf22jsonfile.write("daasdaaswlsadmin_deploy_daascuratordnb_password=%s\n" % jsontodict['DATASERVICE_CCONSOLE_APPID_PASSWORD'])
    conf22jsonfile.write("daasdaaswlsadmin_reassociate_username=%s\n" % jsontodict['POLICYSTORE_READWRITEUSER'])
    conf22jsonfile.write("daasdaaswlsadmin_reassociate_jpsroot=%s\n" % jsontodict['POLICYSTORE_CONTAINER'])
    conf22jsonfile.write("daasdaaswlsadmin_reassociate_url=ldap://%s:%s\n" % (jsontodict['POLICYSTORE_HOST'],jsontodict['POLICYSTORE_PORT']) )
    conf22jsonfile.write("daasdaaswlsadmin_crosstenant_base_dn=%s\n" % jsontodict['CROSS_DOMAIN_GROUP_SEARCHBASE'])
    conf22jsonfile.close()


def FetchPasswords(OFilename):
    jsontodict = data 
    pwdsfiles = open(OFilename, "w")

    pwdsfiles.write("daas_daas_wlsadmin_password=%s\n" % (jsontodict['OCLOUD9_SERVICE_WLS_APPID_PASSWORD']) )
    pwdsfiles.write("daas_daas_wlsnodemanager_password=%s\n" % (jsontodict['OCLOUD9_SERVICE_NM_APPID_PASSWORD']) )
    pwdsfiles.write("daas_edq79_wlsadmin_password=%s\n" % (jsontodict['OCLOUD9_SERVICE_WLS_APPID_PASSWORD']) )
    pwdsfiles.write("daas_edq79_wlsnodemanager_password=%s\n" % (jsontodict['OCLOUD9_SERVICE_NM_APPID_PASSWORD']) )
    pwdsfiles.write("daas_prov_wlsadmin_password=%s\n" % (jsontodict['OCLOUD9_SERVICE_WLS_APPID_PASSWORD']) )
    pwdsfiles.write("daas_prov_wlsnodemanager_password=%s\n" % (jsontodict['OCLOUD9_SERVICE_NM_APPID_PASSWORD']) )
    pwdsfiles.write("daas_edq73_wlsadmin_password=%s\n" % (jsontodict['OCLOUD9_SERVICE_WLS_APPID_PASSWORD']) )
    pwdsfiles.write("daas_edq73_wlsnodemanager_password=%s\n" % (jsontodict['OCLOUD9_SERVICE_NM_APPID_PASSWORD']) )
    pwdsfiles.write("daasdaaswlsadmin_oid_password=%s\n" % (jsontodict['WLSPASSWD']) )
    pwdsfiles.write("daasdaaswlsadmin_crosstenant_password=%s\n" % (jsontodict['CROSS_DOMAIN_AUTH_PASSWORD']) )
    pwdsfiles.write("daasdaaswlsadmin_deploy_daasappid_password=%s\n" % (jsontodict['DATASERVICE_API_APPID_PASSWORD']) )
    pwdsfiles.write("daasdaaswlsadmin_deploy_daasedqws_password=%s\n" % (jsontodict['DATASERVICE_API_APPID_PASSWORD']) )
    pwdsfiles.write("daasdaaswlsadmin_reassociate_password=%s\n" % (jsontodict['POLICYSTORE_READWRITEUSER_PASSWD']) )
    pwdsfiles.close()
    



if( __name__ == '__main__'):

      dmpfile = sys.argv[1] 
      ConvertToJson(dmpfile)
      FetchProps(sys.argv[2])
      FetchPasswords(sys.argv[3])
