#!/usr/bin/python
#DT:07.06.2017
#Next date

import sys,os
import traceback

print "--------------------------------------------------------"
print "    ------------| Next Date Program |-------------"
print "--------------------------------------------------------\n"

def choice():
        answer=raw_input("\nDo you want to calculate again? ")
        if answer in ['Yes','yes','y','YES']:
                print
                main()
        else:
                print "Thank you !!"


def nextDate(y,m,d):
        try:
                mod=y%4
                if mod==0 and m==2 and d < 29:
                        date=str(d+1)+'-'+str(m)+"-"+str(y)
                        print 'Next Date:'+date
                        choice()
                elif mod==0 and m==2 and d == 29:
                        date=str(1)+'-'+str(m+1)+"-"+str(y)
                        print 'Next Date:'+date
                        choice()
                elif m==12 and d<31:
                        date=str(d+1)+'-'+str(m)+"-"+str(y)
                        print 'Next Date:'+date
                        choice()
                elif m==12 and d==31:
                        date=str(1)+'-'+str(1)+"-"+str(y+1)
                        print 'Next Date:'+date
                        choice()
                elif d==31 and m in [1,3,5,7,8,10]:
                        date=str(1)+'-'+str(m+1)+"-"+str(y)
                        print 'Next Date:'+date
                        choice()
                elif d==30 and m in [4,6,9,11]:
                        date=str(1)+'-'+str(m+1)+"-"+str(y)
                        print 'Next Date:'+date
                        choice()
                elif d > 29 and m == 2:
                        print "[WARNING]Invalid date for month=02"
                        choice()
                elif d>30 and m in [4,6,9,11]:
                        print "[WARNING]Invalid date for month="+str(m)
                        choice()
                else:
                        date=str(d+1)+'-'+str(m)+"-"+str(y)
                        print 'Next Date:'+date
                        choice()
        except:
                print "[DEBUG:]"+traceback.format_exc()






def main():
        try:
                date=raw_input("Enter the date in dd.mm.yyyy format: ")
        except ValueError:
                print "\n[ERROR:]Invalid/NULL value provided !!"
                print "[DEBUG:]"+traceback.format_exc()
                print "[INFO:]Input format should be a Integer"
                sys.exit(-1)
        try:
                year=int(date.split('.')[2])
                if year not in range(1812,1913):
                        print "[WARNING]Year range should be from 1812-1912"
                        sys.exit(-1)
                elif len(list(str(year))) != 4:
                        print "[WARNING]Invalid year, should be from 1812-1912 and 4 character long"
                        sys.exit()
                month=int(date.split('.')[1])
                if month not in range(01,13):
                        print "[WARNING]Month is not valid, should be in 01-12"
                        sys.exit()
                elif len(list(str(month))) != 2 and len(list(str(month))) != 1:
                        print "[WARNING]Invalid month, should be from 01-31"
                        sys.exit()
                day=int(date.split('.')[0])
                if day not in range(01,32):
                        print "[WARNING]Date should be in range 01-31"
                        sys.exit()
                elif len(list(str(day))) != 2 and len(list(str(day))) != 1:
                        print "[WARNING]Invalid date, should be from 01-31"
                        sys.exit()
                if isinstance(month, int ) and isinstance(year, int ) and isinstance(day, int ):
                        nextDate(year,month,day)

        except:
                print "\n[ERROR:]Invalid/NULL value provided !!"
                print "[DEBUG:]"+traceback.format_exc()
                print "[INFO:]Input format should only Integer"
                sys.exit(-1)


if( __name__ == '__main__'):
        main()
