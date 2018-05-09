import ldap
import sys
import ldap.modlist as modlist

def mod_replace(ldapserver,commonname,attri):

  
    ldapcon = ldap.initialize("%s" % (ldapserver))
    print ldapcon
    ldapbind = ldapcon.simple_bind_s("cn=OrclAdmin", "Fusionapps1")
    base_dn = "dc=us,dc=oracle,dc=com"
    attrs = ['dn']
    filter = '(cn=%s)' % commonname
    print ldapbind

    search_results = ldapcon.search_s(base_dn, ldap.SCOPE_SUBTREE, filter, attrs )
    if(len(search_results) > 0):
      dn = search_results[0][0]
      print dn
      mod_attrs = [( ldap.MOD_REPLACE, '%s' %(attri), 'false' )]
      print ldapcon.modify_s(dn,mod_attrs)
      ldapcon.unbind_s()


mod_replace(sys.argv[1], sys.argv[2],sys.argv[3])
