#!/usr/bin/python
#DT: 05.11.2018
#Usage Metrics of all Hosts.

import os,sys
import socket
import datetime


def checkUsage(host,command):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        res = sock.connect_ex((host,22))
        if res == 0:
                result=os.popen('ssh -q -o ConnectTimeout=10 '+host+' "'+command+'"').read().strip()
                return result
        else:
                return ''


#MEMORY
def checkMem(host):
        print host
        res=checkUsage(host,'free -m |grep Mem:')
        if res != '':
                memTotal=res.split()[1]
                memUsed=res.split()[2]
                memFree=res.split()[3]
                memAverage=[memTotal,memUsed,memFree]
                return memAverage

#LOAD
def checkLoad(host):
        dateList=[]
        for i in range(int(dateRange)):
                date = datetime.datetime.today() - datetime.timedelta(days=i)
                dateList.append(date.strftime("%y.%m.%d"))
        date1="|".join(str(x) for x in dateList)
        res=checkUsage(host,'cat /var/log/cpuload|egrep \''+date1+'\'')
        resList1=res.split('\n')
        resList2=" ".join(str(x) for x in resList1)
        load=0
        if res != '':
                for x in resList2.split()[1::2]:
                        load=float(load)+float(x)
                        loadAvg=load/float(100) * 100
                maxLoad = max(resList2.split()[1::2])
                return [loadAvg,maxLoad]

#CPU COUNT
def checkCPU(host):
        res=checkUsage(host,'cat /proc/cpuinfo |grep processor|wc -l')
        if res != '':
                return res


def checkDisk(host):
        res=checkUsage('slcn13vmf0209','vgs|grep -v VG')
        if res != '':
                vgs=map(None, *([iter(res.split())] * 7))
                count=0
                diskUsed=[]
                diskFree=[]
                while count < len(vgs):
                        diskUsed.append(vgs[count][5])
                        diskFree.append(vgs[count][6])
                        count=count+1
                return diskUsed,diskFree


if( __name__ == '__main__'):
        dateRange=sys.argv[1]
        with open('hosts.txt','r') as f:
                hosts=f.read().strip()
        hostList=hosts.split()
        count=0
        res={}
        while count <  len(hostList):
                res1=checkMem(hostList[count])
                res_2=checkLoad(hostList[count])
                res3=checkCPU(hostList[count])
                res4=checkDisk(hostList[count])
                if res_2 != None:
                        maxLoad=float(res_2[1])/float(100) * 100
                        print maxLoad
                        res2=res_2[0]
                if res1 == None or res2 == None or res3 == None or res4 == None:
                        pass
                else:
                        res.update({hostList[count]:[res1,res2,res3,res4,maxLoad]})
                count=count+1
        with open('usageReport.html','w') as f:
                f.write('<!DOCTYPE html>\n')
                f.write('<html>\n')
                f.write('<body>\n')
                f.write('<head>\n')
                f.write('<style>\n')
                f.write('table, th, td {\n')
                f.write('border: 1px solid black;\n')
                f.write('}\n')
                f.write('</style>\n')
                f.write('</head>\n')
                f.write('<body>\n')
                f.write('<h2>DAAS INFRA USAGE STATISTICS</h2>\n')
                f.write('')
                f.write('<table style="width:100%">\n')
                f.write('  <tr>\n')
                f.write('    <th>Hostname</th>\n')
                f.write('    <th>Total_Memory(MB)</th> \n')
                f.write('    <th>Memory_Used(MB)</th>\n')
                f.write('       <th>Memory_Free(MB)</th>\n')
                f.write('       <th>Memory_Free(MB) %</th>\n')
                f.write('       <th>Load_Average %</th>\n')
                f.write('       <th>Peak_CPU%('+dateRange+') day(s)</th>\n')
                f.write('       <th>No_Of_CPU</th>\n')
                for key,value in res.iteritems():
                        f.write('<tr>\n')
                        f.write("<td><a href='http://slcn13vmf0209.us.oracle.com/xymon-cgi/showgraph.sh?host="+key+".us.oracle.com&service=la&graph_width=576&graph_height=120&disp="+key+"%2eus%2eoracle%2ecom&nostale&color=green&graph_start=1542526554&graph_end=1542699354&action=menu'>"+key+"</a></td>\n")
                        f.write('<td>'+str(value[0][0])+'</td>\n')
                        f.write('<td>'+str(value[0][1])+'</td>\n')
                        f.write('<td>'+str(value[0][2])+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="http://slcn13vmf0209.us.oracle.com/xymon-cgi/svcstatus.sh?HOST='+key+'.us.oracle.com&SERVICE=memory">- - - </a></td>\n')
                        val=float(value[0][2])/float(value[0][0])*100
                        f.write('<td>'+str('%.2f'%val)+'</td>\n')
                        f.write('<td>'+str('%.2f'%float(value[1]))+'</td>\n')
                        f.write('<td>'+str(value[4])+'</td>\n')
                        f.write('<td>'+str(value[2])+'</td>\n')
                f.write('  </tr>\n')
                f.write('</table>\n')
                f.write('</body>\n')
                f.write('</html>\n')
                f.close()