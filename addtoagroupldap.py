import ldap
import sys
import ldap.modlist as modlist

def getdn(ldapserver,commonname):

    ldapcon = ldap.initialize("%s" % (ldapserver))
    print ldapcon
    ldapbind = ldapcon.simple_bind_s("cn=OrclAdmin", "Fusionapps1")
    base_dn = "dc=us,dc=oracle,dc=com"
    attrs = ['dn']
    filter = '(cn=%s)' % (commonname)
    print ldapbind

    search_results = ldapcon.search_s(base_dn, ldap.SCOPE_SUBTREE, filter, attrs )
    print search_results
    if(len(search_results) > 0 ):
      dn = search_results[0][0]
      return dn
    ldapcon.unbind_s()


def mod_add(ldapserver,dn,attri,val):

    ldapcon = ldap.initialize("%s" % (ldapserver))
    print ldapcon
    ldapbind = ldapcon.simple_bind_s("cn=OrclAdmin", "Fusionapps1")
    mode_attrs = [(ldap.MOD_ADD, attri, val )]    
    ldapcon.modify_s(dn,mode_attrs)
    ldapcon.unbind_s()

def getpoddn(ldapserver,commonname,flter):

    ldapcon = ldap.initialize("%s" % (ldapserver))
    print ldapcon
    ldapbind = ldapcon.simple_bind_s("cn=OrclAdmin", "Fusionapps1")
    base_dn = "dc=us,dc=oracle,dc=com"
    attrs = ['dn']
    filter = '%s' % (flter)
    print ldapbind

    search_results = ldapcon.search_s(base_dn, ldap.SCOPE_SUBTREE, filter, attrs )
    print search_results
    if(len(search_results) > 0 ):
      dn = search_results[0][0]
      return dn
    ldapcon.unbind_s()


idm = sys.argv[1]
cmn1 = sys.argv[2]
cmn2 = sys.argv[3]
tenant = sys.argv[4]


consoledn =  getdn(idm, cmn1)     #get group dn

filt = r'(&(cn=%s)(orclmttenantuname=%s))' % (cmn2,tenant)
poddn = getpoddn(idm,cmn2,filt)   #get unique user dn
print consoledn
print poddn

mod_add(idm,consoledn,'uniquemember',poddn)

