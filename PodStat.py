#!/usr/bin/python


import os,sys
import pexpect

argn = len(sys.argv) - 1
if argn != 4:
	print "Invalid usage"
	print "Usage : python scriptname user pasword hostname command"
	sys.exit(-1)


user = sys.argv[1]
#user = 'paasusr'
password = sys.argv[2]
#password = 'v2>Z6pHmq4E6Fp'
host = sys.argv[3]
#host = 'ucf2c-daas-daasmgm6n0y01-mvm1.opcdaas.oracleinternalucf2c.oraclecorp.com'
command = sys.argv[4]
#command = 'hostname ; echo $?'


def dossh(user, password, host, command):
        child = pexpect.spawn('ssh %s@%s %s' % (user,host,command))
        i = child.expect(['password:', r"yes/no",pexpect.EOF])
        if i == 0:
                child.sendline(password)
        elif i == 1:
                child.sendline("yes")
                child.expect("password:", timeout=30)
                child.sendline(password)
        data = int(child.read())
        return data
        child.close()


print dossh(user, password, host, command)
#print retstatus

