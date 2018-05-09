#!/usr/bin/python
#Date: 21/09/2014
#Author:Sidharth Mohapatra
#Description: This Script checks unattended patching status. It takes an input file with all the server names.
 
import os
import subprocess
import sys
 
 
class color:
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        RED = '\033[91m'
        DARKCYAN = '\033[36m'
        END = '\033[0m'
 
os.system('clear')
 
#Print Welcome Screen
print color.BLUE + '*'*28,' UNATTENDED PATCHING STATUS ','*'*28 + color.END
 
#Force user to give file name along with the command
if len(sys.argv) < 2:
        print '\nPlease provide the file name having all the server names along with the command,Please see below'
        print 'Example: ./unattended.py /var/tmp/server_names\n'
        sys.exit(0)
 
 
 
 
#Global Variables
vcommand1 = 'cat /var/log/fid-upgrade.log'
vcommand2 = "cat /etc/fidelity-release|awk '{print $5 " " $6 }'"
vhostnames = open(sys.argv[1])
verr_codes = ['3001','8001','9001']
vhost=vhostnames.readlines()
vhost= [str(value).strip() for value in vhost]
vhost_dead = []
vhost_alive = []
 
 
#Function to test ping for all the hosts
def ping_test(host):
        vping_test = os.system("ping -q -c 1 " + host + " > /dev/null 2>&1")
        if vping_test == 0:
                vhost_alive.append(host)
        else:
                vhost_dead.append(host)
 
 
 
#Function to ssh to all the hosts
def ssh_host(host,vcommand):
        ssh = subprocess.Popen(["ssh", "%s" % host, vcommand],
                                shell=False,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
 
        result = ssh.stdout.readlines()
        return result
 
#Get various statuses by calling ssh function
def get_status(host):
        vfid_log = ssh_host(host,vcommand1)
        vlog = [str(value).strip() for value in vfid_log]
        vpatch = ssh_host(host,vcommand2)
        vpatch_level = [str(value).strip() for value in vpatch]
        vexit_code = [s for s in vlog if "SessionInfo.session_status" in s]
        vexit_code = ''.join(vexit_code)
        vpatch_level = ''.join(vpatch_level)
        return vexit_code,vpatch_level
 
 
 
#Calling ping function here
i = 0
while i < len(vhost):
        ping_test(vhost[i])
        i += 1
#Find patching status of the alive hosts
k = 0
while k < len(vhost_alive):
        try:
                vexit_code,vpatch_level = get_status(vhost_alive[k])
                vexit_code = vexit_code.split('=')[1]
                if int(vexit_code) == 0:
                         print color.GREEN + '{message: <10}'.format(message=vhost_alive[k]),'  Status:Completed        Exit Code:',vexit_code,'                Fid Level:',vpatch_level + color.END
                elif vexit_code in verr_codes:
                        print color.RED + '{message: <10}'.format(message=vhost_alive[k]),'     Status:Aborted          Exit Code:',vexit_code,'        Fid Level:',vpatch_level + color.END
                elif vexit_code > 0:
                        print color.DARKCYAN + '{message: <10}'.format(message=vhost_alive[k]),'        Status:Completed        Exit Code:',vexit_code,'               Fid Level:',vpatch_level + color.END
        except IndexError:
                print color.RED + '{message: <10}'.format(message=vhost_alive[k]),'     Status:Unknown          Error:Investigate Manually' + color.END
        k += 1
j = 0
 
#Print all dead hosts
while j < len(vhost_dead):
        print color.RED + '{message: <10}'.format(message=vhost_dead[j]),'      Status:Unknown          Error: Host Dead        Fid Level: Unknown' + color.END
        j += 1
 
 
print '*'*86
