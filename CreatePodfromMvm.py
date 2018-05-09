#!/usr/bin/python
#Date:03/02/2015
#Author: Sidharth Mohapatra
#Description: This script is called inside DTE to login in to managementvm
#             to create DAAS POD.

import os,sys,time
import pexpect

if len(sys.argv) < 5 :
        print 'Insufficient number of arguments. Pass pod name and Nimbula User'
        print 'Ex: ./CreatePod.py <MvmPodName> <NimbulaUser> <DaasPodName>'
        sys.exit(-1)
MvmPodName=sys.argv[1]
NimbulaUser=sys.argv[2]
DaasPodName=sys.argv[3]
NimbPasswd=sys.argv[4]
Email=sys.argv[5]
MvmName=os.popen('knife node list |grep '+MvmPodName+'-mvm1').read().strip('\n')
MvmUser='paasusr'
MvmPasswd='v2>Z6pHmq4E6Fp'
auto_work=os.getenv("AUTO_WORK")+"/app"
Conf22=auto_work+'/pyconf/conf_22.py'
DaasOpsHome =  "/u01/data/daas-ops-home"
MediaDir = "/u01/data/media"
PodsetupDir = "/u01/data"
NpgInputDir= PodsetupDir+"/objectrepoclient/decrypted/npg-"+DaasPodName
NpgOutputDir=PodsetupDir+"/objectrepoclient/decrypted/output-"+DaasPodName

#Let's do SCP files from chef server
def doScp(user,password, host, path, files):
        try:
                child = pexpect.spawn('scp -r %s  %s@%s:%s' % (files,user,host,path),logfile=sys.stdout,timeout=None)
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
        except:
                print "Failed while copying"+files+" to "+host

def doSCP(user,password, host, path, files):
        try:
                child = pexpect.spawn('scp -r %s@%s:%s %s' % (user,host,files,path),logfile=sys.stdout,timeout=None)
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
        except:
                print "Failed while copying"+files+" to "+host
#Let's SSH to the management VM
def doSsh(user,password,host,command):
        child =  pexpect.spawn("ssh  -n %s@%s '%s'" % (user,host,command),logfile=sys.stdout,timeout=None)
        i = child.expect(['password:', r'\(yes\/no\)',r'.*password for paasusr: ',r'.*[$#] '])
        if i == 0:
                child.sendline(password)
        elif i == 1:
                child.sendline("yes")
                child.expect("password:")
                child.sendline(password)
        data = child.read()
        print data
        child.close()

#Creating mvminstall script
myfile1="mvminstall"
f = open(myfile1,'w')
f.write('cd '+PodsetupDir+'/daas-ops-home/daas-ops/highlevel\n')
f.write("python ../nodes/Msetupenv.py \'python mvm-installwls.py setup\'\n")
f.write('cd '+PodsetupDir+'/daas-ops-home/daas-ops/nodes\n')
f.write("python Msetupenv.py \'python main.py install_rcu install\'\n")
#f.write("python Msetupenv.py \'python main.py install_rcu74 install\'\n")
f.close()
os.system("mv mvminstall "+auto_work)

#Creating apply-patch script
myfile2="patch-apply"
f = open(myfile2,'w')
f.write("cd "+PodsetupDir+"/daas-ops-home/daas-ops/highlevel;")
f.write("python ../nodes/Msetupenv.py \'python daaspod.py apply-patch\'")
f.close()
os.system("mv patch-apply "+auto_work)

#Creating create-output script
myfile3="create-output"
f = open(myfile3,'w')
f.write("cd "+PodsetupDir+"/daas-ops-home/daas-ops/chef/generator-gen2;\n")
#f.write(".   ./setenv.sh && python  ../../nodes/Msetupenv.py 'python pod.py "+NpgInputDir+"/';\n")
f.write("python  ../../nodes/Msetupenv.py 'python pod.py "+NpgInputDir+"/';\n")
f.write("> output/nimbula-password;echo "+NimbPasswd+" > output/nimbula-password;\n")
f.write("cp -r output/* "+NpgOutputDir)
f.close()
os.system("mv create-output "+auto_work)

#Check if necessary files are present in auto_work or not !!
if os.path.isdir(auto_work+'/pyconf') is True and os.path.isfile(auto_work+'/pod.json') is True and os.path.isfile(auto_work+'/daasidm.json') is True and os.path.isfile(auto_work+'/override-key.key') is True:
        print "All the required files are present. Continuing !!"
        #SCP all the files to Management VM
        try:
                doSsh(MvmUser,MvmPasswd,MvmName,'mkdir '+NpgInputDir)
                doSsh(MvmUser,MvmPasswd,MvmName,'mkdir '+NpgOutputDir)
                doScp(MvmUser,MvmPasswd,MvmName,NpgInputDir,auto_work+'/pyconf')
                print 'Copied pyconf to '+MvmName
                #doScp(MvmUser,MvmPasswd,MvmName,PodsetupDir,auto_work+'/managementvm/opsserver_artifacts')
                print 'Copied opsserver artifacts to '+MvmName
                doScp(MvmUser,MvmPasswd,MvmName,NpgInputDir,auto_work+'/pod.json')
                print 'Copied  pod.json to '+MvmName
                doScp(MvmUser,MvmPasswd,MvmName,NpgInputDir,auto_work+'/daasidm.json')
                print 'Copied daasidm to '+MvmName
                doScp(MvmUser,MvmPasswd,MvmName,NpgInputDir,auto_work+'/override-key.key')
                print 'Copied override-key to '+MvmName
#                doScp(MvmUser,MvmPasswd,MvmName,auto_work+"/daas-ops-home/daas-ops/chef/generator-gen2/",NpgOutputDir)
                doScp(MvmUser,MvmPasswd,MvmName,PodsetupDir+"/daas-ops-home/daas-ops/nodes",auto_work+"/daas-ops-home/daas-ops/nodes/Msetupenv.py")
                #doSsh(MvmUser,MvmPasswd,MvmName,'cd '+NpgOutputDir+'/output;mv * ../;cd ../;rm -rf output')
                print "Copied output directory to "+MvmName
                doScp(MvmUser,MvmPasswd,MvmName,PodsetupDir,auto_work+'/mvminstall')
		print "Copied mvminstall script to "+MvmName
                doScp(MvmUser,MvmPasswd,MvmName,PodsetupDir,auto_work+'/patch-apply')
		print "Copied patch-apply script to "+MvmName
                doScp(MvmUser,MvmPasswd,MvmName,PodsetupDir,auto_work+'/create-output')
		print "Copied create-output script to "+MvmName
        except:
                print "Unable to copy somefiles, exiting !!"
                sys.exit(-1)

        try:
                #Taking a backup of .bashrc file
                doSsh(MvmUser,MvmPasswd,MvmName,'cp ~/.bashrc ~/.bashrc.orig')
                #Set environment variables in the management vm
                print "Setting up Nimbula Env Values"
                print "Setting daas_node_instance on management vm"
                doSsh(MvmUser,MvmPasswd,MvmName,"echo export daas_node_instance="+NpgInputDir+" >> ~/.bashrc")
                print "Setting NIMBULA_API on management vm"
                doSsh(MvmUser,MvmPasswd,MvmName,'echo export NIMBULA_API=https://api.oracleinternalucf2c.oraclecorp.com  >> ~/.bashrc')
                print "Setting NIMBULA_USER on management vm"
                doSsh(MvmUser,MvmPasswd,MvmName,'echo export NIMBULA_USER='+NimbulaUser+' >> ~/.bashrc')
                doSsh(MvmUser,MvmPasswd,MvmName,"echo export daas_email_recipients="+Email+" >> ~/.bashrc")
                #Run mvm-installwls.py on the managementvm
                try:
			doSsh(MvmUser,MvmPasswd,MvmName,'cd '+PodsetupDir+';bash create-output')
	                doSCP(MvmUser,MvmPasswd,MvmName,auto_work+"/daas-ops-home/daas-ops/chef/generator-gen2/",NpgOutputDir)
			os.system("mv "+auto_work+"/daas-ops-home/daas-ops/chef/generator-gen2/output-* "+auto_work+"/daas-ops-home/daas-ops/chef/generator-gen2/output")
		except:
			print "Failed to run create-output"
			sys.exit(-1)
		try:
                	doSsh(MvmUser,MvmPasswd,MvmName,'cd '+PodsetupDir+';bash mvminstall')
		except:
                	print "Failed to run mvminstall"
                	sys.exit(-1)
                try:
                       #Run pod-bringup.py setup on the managementvm
                	doSsh(MvmUser,MvmPasswd,MvmName,'cd '+NpgOutputDir+';python pod-bringup.py setup')
                except:
                	print "Failed to run pod-bringup.py setup"
                	sys.exit(-1)
                try:
                	#Run pod-bringup.py check on the managementvm
                	doSsh(MvmUser,MvmPasswd,MvmName,'cd '+NpgOutputDir+';python pod-bringup.py check')
                except:
                	print "Failed to run pod-bringup.py check"
                	sys.exit(-1)
                	print "Pod Setup Completed !!"

                #For patching DAAS Pod

                if os.system('cat '+auto_work+'/pyconf/conf_22.py|grep daas_patch_version') != 0:
                 	print "Fresh Install"

                elif int(os.popen('cat '+auto_work+'/pyconf/conf_22.py|grep daas_patch_version|cut -d= -f2').read().split("'")[1]) == 0:
                        print "Fresh Install"
                else:
                        try:
                                doSsh(MvmUser,MvmPasswd,MvmName,'cd '+PodsetupDir+';bash patch-apply')
                                print "DAAS Pod Patching completed !!\n"
				print "Checking Pod health stauts after patching\n\n"
				doSsh(MvmUser,MvmPasswd,MvmName,'cd '+NpgOutputDir+';scripts/check-pod-health.py |userscripts/verify-check-pod-health-output-for-patching.py')
                        except:
                                print "Apply patch on DAAS Pod Failed"
                                sys.exit(-1)
                doSsh(MvmUser,MvmPasswd,MvmName,'mv ~/.bashrc.orig ~/.bashrc')
	except:
		print 'Failed while running commands on Management VM'
		sys.exit(-1)
else:
        print "Some of the important files are missing. Please check in $auto_work, and re-run me!!"
        sys.exit(-1)

