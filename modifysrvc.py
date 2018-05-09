import json
import sys
def Payload(srvctxt,regsrvc,domain,service):

    idname =  service + '-' + domain
    srvcfile = open(srvctxt, "r")
    data = dict()
    data = json.load(srvcfile)
    tofile = open(regsrvc, "w")
    data['id'] = idname
    data['name'] = service
    data['identity_domain_id'] = domain
    data['identity_domain_name'] = domain
    json.dump(data,tofile,sort_keys=True)
    srvcfile.close()
    tofile.close()


if(__name__ == "__main__"):

  Payload(sys.argv[1], sys.argv[2],sys.argv[3],sys.argv[4])
