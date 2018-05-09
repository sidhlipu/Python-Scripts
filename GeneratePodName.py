import random
import re
import subprocess
import os
import ldap
import sys

def findaword():
  fp = open("/usr/share/dict/words", "r")
  words = fp.readlines()
  #print len(words)

  wordtoselect = random.randrange(1,len(words),3)
  return words[wordtoselect]






def doespodexist(ldapserver,pod):

    ldapcon = ldap.initialize("%s" % (ldapserver))
    #print ldapcon
    ldapbind = ldapcon.simple_bind_s("cn=OrclAdmin", "Fusionapps1")
    base_dn = "dc=us,dc=oracle,dc=com"
    attrs = ['orclmtserviceinstancename']
    filter = '(orclmtserviceinstancename=*)'
    podnames = []
    #print ldapbind

    search_results = ldapcon.search_s(base_dn, ldap.SCOPE_SUBTREE, filter, attrs )
    print len(search_results)
    for I in range(0,len(search_results)):
        podnames.append(search_results[I][1]['orclmtserviceinstancename'][0])

    if( pod in podnames):
       return 0

    else:
       return 1





while True:
    podname = findaword()
    tmpgpod = podname.lower()
    tmpgpod = tmpgpod.rstrip()
    tmppod = tmpgpod + 'pod01'
    pat = re.compile(r'[a-z]+')
    pat2 = re.compile(r'[-,_$@#]') 
    m = pat.search(podname)
    m1 = pat2.search(podname)
    if(len(podname) <=7 and m and len(podname)>4 and doespodexist(sys.argv[1],tmppod) and (not m1)):
      break;

srvctempl = sys.argv[3]
autodir = sys.argv[4]
gpod = podname.lower()
gpod = gpod.rstrip()
print gpod
tenant = gpod + 'tenant01'
tenantadm = tenant + 'admin'
pod = gpod + 'pod01'
podadm = pod + 'admin'
print "tenant = %s" % (tenant)
print "pod = %s" % (pod)
podsrvcparam = pod + 'srvc.param'
### Changes
podsrvcparam = autodir + '/' + podsrvcparam 

os.system("cp %s %s" % (srvctempl,podsrvcparam))

idmreg = re.match("ldap://(.*):3060", sys.argv[1])
idmhost = idmreg.group(1)

replacecmd = r"sed -ri -e 's#idmhost#%s#' -e 's#idmtenant#%s#' -e 's#idmtenantadmin#%s#' -e 's#idmpod#%s#' -e 's#idmpodadmin#%s#' -e 's#policyhost#%s#' -e 's#wlsnode#%s#' %s" %(idmhost,tenant,tenantadm,pod,podadm,idmhost,sys.argv[2],podsrvcparam)

print replacecmd
os.system(replacecmd)
os.system("rm -f /net/%s/%s/%s" % (sys.argv[2],sys.argv[5],'tmpsrvcparam'))
os.system("cp -f %s /net/%s/%s" % (podsrvcparam,sys.argv[2],sys.argv[5]))
os.system("cp -f %s /net/%s/%s/tmpsrvcparam" % (podsrvcparam,sys.argv[2],sys.argv[5]))

