import base64
import urllib2
import json
import sys


def queryAPI(srvr=None,user=None,pwd=None,status=None,domain=None,service=None):

    url=r'http://%s:7005/data/admin/curator/workflowjob/listJobsByStatus/%s' % (srvr,status)
    req=urllib2.Request(url)
    base64string = base64.encodestring('%s:%s' % (user, pwd))[:-1]
    req.add_header("Authorization", "Basic %s" % base64string)
    req.add_header("X-ID-TENANT-NAME", "%s" % domain)
    req.add_header("X-USER-IDENTITY-DOMAIN-NAME", "%s" % domain)
    req.add_header("X-ORACLE-DAAS-SERVICE-NAME", "%s" % service)

    content = urllib2.urlopen(req)
    jsonstring = content.read()
    return jsonstring
    #data = dict()
    #data = json.loads(jsonstring)
    #if(jsonstring != r'null'):
      #print data
      #print data[u'workflowJob'][u'latestWorkflowInstanceStatus']


if( __name__ == '__main__'):

  #queryAPI('slcn09vmf0160.us.oracle.com', 'DATASERVICE_DATASERVICE_CCONSOLE_APPID','rFziv6lg5h_eyp')
  print queryAPI(sys.argv[1], sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])
#queryAPI()
