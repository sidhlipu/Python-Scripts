import ldap
import sys
import ldap.modlist as modlist

def getdn(ldapserver,flter,attr):

    ldapcon = ldap.initialize("%s" % (ldapserver))
    #print ldapcon
    ldapbind = ldapcon.simple_bind_s("cn=OrclAdmin", "Fusionapps1")
    base_dn = "dc=us,dc=oracle,dc=com"
    attribute = '%s' % (attr)
    attrs = [attribute]
    filter = flter 
    #print ldapbind

    search_results = ldapcon.search_s(base_dn, ldap.SCOPE_SUBTREE, filter, attrs )
    if(len(search_results) > 0 ):
      return search_results
    ldapcon.unbind_s()



def mod_add(ldapserver,attributes,dn):

    ldapcon = ldap.initialize("%s" % (ldapserver))
    ldapbind = ldapcon.simple_bind_s("cn=OrclAdmin", "Fusionapps1")
    ldif = modlist.addModlist(attributes)
    print ldapcon.add_s(dn,ldif)
    ldapcon.unbind_s()


idm = sys.argv[1]
cmn1 = sys.argv[2]
attrtodisp = sys.argv[3]
tenant = sys.argv[4]
dloaduser = sys.argv[5]

uniqname = tenant + '.' + dloaduser

results  =  getdn(idm, cmn1,attrtodisp)
basedn = results[0][0]
tenantguid =  results[0][1]['orclmttenantguid'][0] 
newdn = 'cn=%s'%(dloaduser) + ',' + basedn

print "basedn = %s tenantguid = %s  newdn=%s" % (basedn,tenantguid,newdn)

attrs  = {}
attrs['objectclass'] = ['orclIDXPerson', 'orclUser','orclUserV2', 'oblixPersonPwdPolicy','oblixOrgPerson','OIMPersonPwdPolicy','inetorgperson','top','organizationalPerson','person']

userwriteprivilegeuc = r'cn=orclUserWritePrivilegeGroup,cn=SystemIDGroups,cn=Groups,orclMTTenantGuid=%s,dc=us,dc=oracle,dc=com' % (tenantguid)

tenantadmin = r'cn=TenantAdminGroup,cn=Groups,orclMTTenantGuid=%s,dc=us,dc=oracle,dc=com' % (tenantguid)

userwriteprefsprivilegeuc = r'cn=orclUserWritePrefsPrivilegeGroup,cn=SystemIDGroups,cn=Groups,orclMTTenantGuid=%s,dc=us,dc=oracle,dc=com' % (tenantguid)

userreadprivilegeuc = r'cn=orclUserReadPrivilegeGroup,cn=SystemIDGroups,cn=Groups,orclMTTenantGuid=%s,dc=us,dc=oracle,dc=com' % (tenantguid)


attrs['orclmtuid'] = uniqname
attrs['orclmttenantguid'] =  '%s' % (tenantguid)
#attrs['orclmttenantstate'] =  'ENABLED'
attrs['orclmttenantuname']= '%s' % (tenant)
attrs['orclsamaccountname'] = uniqname 
attrs['givenname'] = '%s' % (dloaduser)
attrs['obpasswordexpirydate'] = '2035-01-01T00:00:00Z'
attrs['sn'] = '%s' % (dloaduser)
attrs['displayname'] =  '%s' % (dloaduser)
attrs['mail'] = 'oracle@fake.com'
attrs['uid'] =  '%s' % (dloaduser)
attrs['obuseraccountcontrol'] = 'activated'
attrs['cn'] =  '%s' % (dloaduser)
attrs['description'] = 'Curator User' 

attrs['obpasswordchangeflag'] = 'false'
if (dloaduser == 'avuser'):
  attrs['userpassword'] = 'welcome1'
else:
  attrs['userpassword'] = 'Welcome2'

mod_add(idm,attrs,newdn)
