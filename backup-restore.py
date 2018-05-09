#!/usr/bin/python
#DT:13.01.2016
#Author: Sidharth Mohapatra
#This script uses index backup/restore utility of DaaS to perform index backup/restore


import sys,os
import pexpect


if len(sys.argv) < 5:
        print "Not all arguments provided !!"
        print "example: ./backup-restore.py backup/restore DaaSPodName MVMName InputDirectory"
        sys.exit(-1)

purpose=sys.argv[1]
podname=sys.argv[2]
mvmname=sys.argv[3]
inputdir=sys.argv[4]
password='v2>Z6pHmq4E6Fp'
user1='paasusr'
user2='daas'
daaspasswd='v2>Z6pHmq4E6Fq'
myfile1="backup-restore"

def RunCommands(podname,password,cmd,user):
        child = pexpect.spawn('ssh -n %s@%s "%s"' % (user,podname,cmd),logfile=sys.stdout,timeout=None)
        i = child.expect(['password:', r'\(yes\/no\)', r"yes/no",r'.*password for paasusr: ',r'.*[$#] '])
        if i == 0:
               child.sendline(password)
        elif i == 1:
                child.sendline("yes")
                child.expect("password:")
                child.sendline(password)
        data = child.read()
        print data
        child.close()

def ScpCommands(file,podname,password,user,dataloc):
        child = pexpect.spawn('scp -r %s %s@%s:%s ' % (file,user,podname,dataloc),logfile=sys.stdout,timeout=None)
        i = child.expect(['password:', r'\(yes\/no\)', r"yes/no",r'.*password for paasusr: ',r'.*[$#] '])
        if i == 0:
               child.sendline(password)
        elif i == 1:
                child.sendline("yes")
                child.expect("password:")
                child.sendline(password)
        data = child.read()
        print data

def CopyIndexFiles(user,podname,file,dataloc,password):
        child = pexpect.spawn('scp -r %s@%s:%s/* %s' % (user,podname,file,dataloc),logfile=sys.stdout,timeout=None)
        i = child.expect(['password:', r'\(yes\/no\)', r"yes/no",r'.*password for paasusr: ',r'.*[$#] '])
        if i == 0:
               child.sendline(password)
        elif i == 1:
                child.sendline("yes")
                child.expect("password:")
                child.sendline(password)
        data = child.read()
        print data

def CreateFile(purpose):
        f = open(myfile1,'w')
        f.write('cd /u01/data/daas-ops-home/daas-ops/utils/index-copy\n')
        f.write("export daas_node_instance="+inputdir+";/u01/data/daas-ops-home/daas-ops/nodes/Msetupenv.py \'python index-copy.py "+purpose+"\'\n")
        f.close()



def indexBackup(podname,password):
        try:
                print "I am backing up the index !!"
                os.system("python PwdChange.py "+podname)
                cmd="mkdir -p /u01/shared/indexbackup;chmod 777 /u01/shared/indexbackup"
                RunCommands(podname,daaspasswd,cmd,user2)
                dataloc='/u01/data'
                ScpCommands(myfile1,mvmname,password,user1,dataloc)
                cmd="sh /u01/data/"+myfile1
                RunCommands(mvmname,password,cmd,user1)
                file='/u01/shared/indexbackup'
                dataloc=os.getenv('AUTO_WORK')+"/indexbackup"
                os.system("mkdir -p "+dataloc)
                CopyIndexFiles(user2,podname,file,dataloc,daaspasswd)
                os.system("rm -rf "+myfile1)
                print "\nIndex Backup Success!!"
        except:
                print "Failed to run "+purpose+" scripts"


def indexRestore(podname,password):
        try:
                print "I am restoring the index !!"
                os.system("python PwdChange.py "+podname)
                cmd="mkdir -p /u01/shared/indexbackup;chmod 777 /u01/shared/indexbackup"
                RunCommands(podname,daaspasswd,cmd,user2)
                dataloc='/u01/data'
                ScpCommands(myfile1,mvmname,password,user1,dataloc)
                file=os.getenv('AUTO_WORK')+"/indexbackup/"
                dataloc='/u01/shared/indexrestore'
                ScpCommands(file,podname,daaspasswd,user2,dataloc)
                cmd='mv /u01/shared/indexbackup/indexbackup/* /u01/shared/indexbackup; rm -rf /u01/shared/indexbackup/indexbackup/'
                RunCommands(podname,daaspasswd,cmd,user2)
                cmd="sh /u01/data/"+myfile1
                RunCommands(mvmname,password,cmd,user1)
                os.system("rm -rf "+myfile1)
                print "\nIndex Restore Success!!"
        except:
                print "Failed to run "+purpose+" scripts"


if purpose == "backup":
        CreateFile(purpose)
        indexBackup(podname,password)
elif purpose == "restore":
        CreateFile(purpose)
        indexRestore(podname,password)