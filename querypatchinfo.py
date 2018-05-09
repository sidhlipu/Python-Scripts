import urllib2
import base64
import json
import sys

try:

  username = sys.argv[1]
  password = sys.argv[2]
  domain = sys.argv[3]
  service = sys.argv[4]
  daasmanagedserver = sys.argv[5]
except IndexError:
 print "Arguments Required....Aborting this Execution"
 print "Usage: python querypatchinfo.py username password domain service daasmanagedserver"
 sys.exit(0)

authtoken = (base64.encodestring('%s:%s' %(username,password)))[:-1]
#print authtoken

req = urllib2.Request('http://%s/data/api/v1/version' %(daasmanagedserver))

req.add_header("Authorization", "Basic %s" % (authtoken))
req.add_header("X-ID-TENANT-NAME", "%s" % (domain))
req.add_header("X-ORACLE-DAAS-SERVICE-NAME", "%s" % (service))
try:
  cont = urllib2.urlopen(req)
  dict = json.loads(cont.read())
  print dict['productVersion']
except urllib2.HTTPError,e:
     print e.code

