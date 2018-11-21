#!/usr/bin/python
import os
#res=os.popen("top -b -n1 -d1|grep 'Cpu(s)'|cut -d: -f2").read().strip()
fileList=os.popen("ls /var/log/oswatcher/archive/oswtop/|grep `date +'%y.%m.%d'`").read().strip()
for x in fileList.split('\n'):
        x1=os.popen('cat /var/log/oswatcher/archive/oswtop/'+x+'|grep "Cpu(s)"|cut -d, -f1|cut -d: -f2|cut -d% -f1').read().strip()
        x2=os.popen('cat /var/log/oswatcher/archive/oswtop/'+x+'|grep "Cpu(s)"|cut -d, -f2|cut -d% -f1').read().strip().strip()

data1=x1.strip().split('\n')
data2=x2.strip().split('\n')

userSum=float(0.0)
for x in data1:
        userSum=userSum+float(x)
sysSum=float(0.0)
for x in data2:
        sysSum=sysSum+float(x)
#print userSum/len(data1)
#print sysSum/len(data2)
avgLoad=userSum/len(data1)+sysSum/len(data2)
print '%.2f'%avgLoad

date=os.popen("date +'%y.%m.%d'").read().strip()
with open('/var/log/cpuload','a') as f:
        f.write(date+"  "+str('%.2f'%avgLoad)+"\n")
        f.close()
