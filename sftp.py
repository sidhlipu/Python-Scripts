#!/usr/bin/python

from pexpect import *
import sys
import os,time


def doSftp(user,host,remotepath,filename,command) :
        p = spawn('sftp %s@%s' %(user,host))
        #Uncomment the below line if you want to see the log in STDOUT[I didn't want to see]
        #p.logfile = sys.stdout
        p.expect('(?i)password:')
        x = p.sendline(passwd)
        x = p.expect(['Permission denied','sftp>'])
        if x == 0:
                print 'Permission denied for password:'
                print password
                p.kill(0)
        else:
                x = p.sendline('cd ' + remotepath)
                x = p.expect('sftp>')
                x = p.sendline(command +' '+ filename)
                x = p.expect('sftp>')
                x = p.isalive()
                x = p.close()
                retval = p.exitstatus

#Define details in the local host to copy to remote host here
host = 'slcn09vmf0262'
user = 'oracle'
passwd = 'welcome1'
remotepath = '/tmp'
filename = '/home/oracle/scripts/test/sid1'
command='put'

doSftp(user,host,remotepath,filename,command)
if os.path.isfile(filename) is True:
        print "Downloaded "+filename+" to "+remotepath
else:
        print "SFTP Failed...."
        print "File "+filename+" not found !!"
        sys.exit()

#Define details in the remote host to copy to local host here
host='slcn09vmf0262'
remotepath='/home/oracle/scripts/test'
filename='test1'
command='get'
archivedir="/tmp"
workdir=os.getcwd()

if os.path.isfile(workdir+'/'+filename) is False:
        i = 0
        while i < 3:
                #Change this value to 30. 3 attempts will be taken[3*30= 90 seconds]
                time.sleep(3)
                doSftp(user,host,remotepath,filename,command)
                i = i+1
                print filename+' file not found....... ['+str(i)+' Attempt]!!'
elif os.path.isfile(workdir+'/'+filename) is True:
        os.system('mv '+filename+' '+archivedir)
        print filename+" is copied to "+archivedir
else:
        print "Unable to find "+filename+" in the remote location "+remotepath
