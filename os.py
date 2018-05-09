#!/usr/bin/env python
# OS upgrade script from OEL 6.x to OEL6.6 or OEL6.7
#Author(s): Naga Sai Vosetti <naga.sai.vosetti@oracle.com>
#version 6 added functionality for OL6.2

import os
import time
import sys
import commands
import re
import platform


def Backup():
    commands.getoutput('mkdir -p /etc/yum.repos.d/backup')
    commands.getoutput('mv /etc/yum.repos.d/* /etc/yum.repos.d/backup >/dev/null 2>&1')

def find_filer():
    nearest_fstatus, nearest_filer = commands.getstatusoutput("for filer in `cat /test1/writeable/nvosetti/filerlist|awk -F : '{print $1}'|sort|uniq`; do resp=$(ping $filer -c1 2>/dev/null |awk -F '[=, ]' '/ttl/ {print $(NF-1)}') ;[ -z $resp ] && resp=999999;echo $resp $filer;done |sort -n |head -n 1|awk '{print $2}'")
    if nearest_fstatus == 0:
        a=re.search('pd-yum',nearest_filer)
        if a:
            repo_file(nearest_filer)
        else:
            export=commands.getoutput("grep %s /test1/writeable/nvosetti/filerlist | awk -F : '{print $2}'"%(nearest_filer))
            commands.getoutput("mkdir -p /test/sai")
            commands.getoutput("mount %s:%s /test/sai"%(nearest_filer,export))
            #URL="file:///test/x86_64/redhat/%s/base/u%s/"%(urlVersion,Minor)
            OEL = open('/etc/yum.repos.d/OEL.repo', 'w')
            print  >> OEL, "[Repository]"
            print >> OEL, "name = Oracle Linux %su%s"%(Major,Minor)
            print  >> OEL, "baseurl= %s"%(URL1)
            print  >> OEL, "gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-oracle"
            print  >> OEL, "gpgcheck=0"
            print  >> OEL, "enabled=1"
            print  >> OEL
            print  >> OEL
            print  >> OEL, "[Kernel]"
            print >> OEL, "name = UEK3 Kernel"
            print  >> OEL, "baseurl= %sUEK3/"%(URL1)
            print  >> OEL, "gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-oracle"
            print  >> OEL, "gpgcheck=0"
            print  >> OEL, "enabled=1"
    else:
        print "Upgrade failed"
        sys.exit()

def repo_file(nearest_filer):
    URL = 'http://'+nearest_filer+'/yum/OracleLinux/'+MajorVersion+'/'+'U'+Minor+'/'+Arch+'/base'
    OEL = open('/etc/yum.repos.d/OEL.repo', 'w')
    print  >> OEL, "[Repository]"
    print >> OEL, "name = Oracle Linux %su%s"%(Major,Minor)
    print  >> OEL, "baseurl= %s"%(URL)
    print  >> OEL, "gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-oracle"
    print  >> OEL, "gpgcheck=0"
    print  >> OEL, "enabled=1"
    print  >> OEL
    print  >> OEL
    print  >> OEL, "[Kernel]"
    print >> OEL, "name = UEK3 Kernel"
    print  >> OEL, "baseurl= %s/UEK3/"%(URL)
    print  >> OEL, "gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-oracle"
    print  >> OEL, "gpgcheck=0"
    print  >> OEL, "enabled=1"

def check_yum_process():
    status = os.popen('ps -eaf |grep yum | grep -v grep')
    pid = status.readlines()
    if pid:
        return True
    else:
        return False

def mount_dir():
    commands.getstatusoutput('mkdir -p /test1/writeable')
    mt1, _ = commands.getstatusoutput('mount adcnas402.us.oracle.com:/export/writeable /test1/writeable')
    if mt1 != 0:
        print "Error mounting directory"
        sys.exit()
                
    
def upgrade():
    start_time=time.strftime("%d/%m/%Y %H:%M:%S")
    commands.getoutput('yum clean all')
    st, _ = commands.getstatusoutput('yum list all')
    if st == 0:
        o_st=os.system("yum upgrade -y --exclude=kernel* --exclude=sudo* --skip-broken >>/tmp/OS123 2>&1 &")
        if o_st == 0:
            sys.stdout.write('Upgrade inprogress....')
            while check_yum_process():
                sys.stdout.write('.....')
                sys.stdout.flush()
                time.sleep(60)
        else:
            print "Upgrade Error"
            sys.exit()
        end_time=time.strftime("%d/%m/%Y %H:%M:%S")
        output=commands.getoutput('tail -n 3 /tmp/OS123')
        stat=re.search('Complete!',output)
        if stat:
            print "Upgrade completed Successfully"
            upg_status = 'Completed Successfully'
        else:
            print "Upgrade Error"
            upg_status = 'Error'
    else:
        print "Upgrade Error"
        upg_status="Error"

    return start_time, upg_status


def kernel_upgrade(input):
    commands.getoutput('mv /etc/yum.repos.d/public-yum-ol6.repo /tmp')
    commands.getoutput('yum clean all')
    commands.getoutput('yum list all')
    if input == 'OL60u6':
        print "Kernel Upgrade in progress..."
        Ker_stat, Ker_out = commands.getstatusoutput('yum install -y kernel-uek-3.8.13-44.1.1.el6uek.x86_64')
        if Ker_stat == 0:
            print "Kernel Upgrade Completed Successfully"
            Ker_upg='Completed Successfully'
            u_release = "3.8.13-44.1.1.el6uek.x86_64"
        else:
            print "Kernel Upgrade Error"
            Ker_upg='Error'
            u_release = platform.release()
    elif input == 'OL60u7':
        print "Kernel Upgrade in progress..."
        Ker_stat, Ker_out = commands.getstatusoutput('yum install -y kernel-uek-3.8.13-68.3.4.el6uek.x86_64')
        if Ker_stat == 0:
            print "Kernel Upgrade Completed Successfully..."
            Ker_upg='Completed Successfully'
            u_release = "3.8.13-68.3.4.el6uek.x86_64"
        else:
            print "Kernel Upgrade Error"
            u_release = platform.release()
            Ker_upg='Error'
    else:
        print "Kernel Upgrade Error"
        u_release = platform.release()
        Ker_upg='Error'
        print Ker_upg, Host
    end_time=time.strftime("%d/%m/%Y %H:%M:%S")
    return end_time, Ker_upg, u_release

def copy_fun(Host):
    commands.getoutput('mkdir -p /root/backup_os')
    commands.getoutput('echo y | cp  /tmp/OS123 /root/backup_os/')
    commands.getoutput('echo y | cp /tmp/OS123 /test1/writeable/nvosetti/'+Host)

def clean_up():
    commands.getoutput('umount -l /test/sai')
    commands.getoutput('mv /tmp/public-yum-ol6.repo /etc/yum.repos.d/')
    commands.getoutput('rm -f /etc/yum.repos.d/OEL.repo')

def Reboot_force():
    commands.getoutput('reboot -n')

if __name__ == "__main__":
    OSTag = os.uname()[0]
    Host = os.uname()[1]
    Region = os.uname()[1][0:3]
    Arch = os.uname()[-1]
    OS_Version=platform.linux_distribution()[1][0]
    OS_Minor=platform.linux_distribution()[1]
    Owner_email=commands.getoutput("/usr/bin/curl -s -L http://devops.oraclecorp.com/host/api/%s/data |grep user_email|awk -F '=' '{print $2}'"%(Host))
    OS_Status=commands.getoutput('cat /etc/oracle-release | grep -i oracle')
    line="\n"
    if OSTag != "Linux":
        print "Server is not Linux"
        sys.exit()
    else:
        if os.getuid() != 0:
            print "Login as root user and retry"
            sys.exit()
        else:
            if OS_Status:
                if OS_Version == '6':
                    if OS_Minor == '6.6' or OS_Minor == '6.7':
                        print "Your System is already upto date"
                        sys.exit()
                    mount_dir()
                    if Arch != "x86_64":
                        print "Architecture not supported"
                        sys.exit()
                    print "Please take backup of your data before upgrade in the location: slcnas580.us.oracle.com:/export/cdc_kerberos_temp"
                    print "Supported Upgrade option is [OL60u6,OL60u7]"
                    print "What OS version you want to upgrade?"
                    input = raw_input()
                    if input != 'OL60u6' and input != 'OL60u7':
                            print "Unsupported Entry Option"
                            sys.exit()
                    Major = input.split('u')[0][2:]
                    MajorVersion = input.split('u')[0][0:3]
                    check_version = input.split('u')[0][2]
                    Minor = input.split('u')[1]
                    release = platform.release()
                    urlVersion = input.split('u')[0][2:]
                    URL1 = 'file:///test/sai/x86_64/redhat/%s/base/u%s/'%(urlVersion,Minor)
                    Backup()
                    #repo_file()
                    find_filer()
                    if OS_Version == check_version:
                        print "Upgrade is in progress it will take nearly 1 to 2 hours based on Network, please do not cancel the request as it will harm your system, raise SR if it is not completed in 2 hours from myhelp,"
                        if OS_Minor == '6.2':
                            commands.getoutput('rpm -e systemtap-runtime systemtap --nodeps')
                        start_time, upg_status = upgrade()
                        OS_UMinor=platform.linux_distribution()[1]
                        if upg_status == 'Error':
                            print "Skipping Kernel Upgrade"
                            u_release = platform.release()
                            end_time=time.strftime("%d/%m/%Y %H:%M:%S")
                            Ker_upg="Skipped"
                        else:
                            end_time, Ker_upg,u_release = kernel_upgrade(input)
                        copy_fun(Host)
                    else:
                        print "Trying to Upgrade to version which is not supported by your OS"
    print "Hostname,Owner email, OS version,updated OS version,Kernel,Upgraded kernel,Start time,End time,Upgrade Status,Kernel Status"
    print "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s"%(Host,Owner_email,OS_Minor,OS_UMinor,release,u_release,start_time,end_time,upg_status,Ker_upg)
    with open('/test1/writeable/nvosetti/OSupgrade.csv', 'a') as f:
        f.write(line)
        f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s"%(Host,Owner_email,OS_Minor,OS_UMinor,release,u_release,start_time,end_time,upg_status,Ker_upg))
    clean_up()
    commands.getstatusoutput('umount -l /test1/writeable')
    if upg_status == "Completed Successfully":
        print "Do you want to reboot the machine now as upgrade is Completed Successfully?(y/n)"
        status1 = raw_input()
        if status1 == 'y':
            print "Going for Reboot ......."
            time.sleep(20)
            Reboot_force()
        else:
            print "As you entered wrong option skipping reboot...."