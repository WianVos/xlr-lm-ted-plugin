#!/usr/bin/python
import urllib
import urllib2
import json



def getJsonDict(host, env):
  """
  Download the TED json for health-checkers per environment
  We pull down everything because at this point i do nog give a flying f&*%& about ted's performance
  I just want to make this plugin as robust as i possible can
  :param host: hostname of the ted server
  :param env: wich environment the request the json for
  :return: dict representation of the information provided by ted
  """
  url = "api/health-checker/all/%s" % env
  url = urllib.quote(url)
  url = "http://%s/%s" % (host, url)

  response = urllib2.urlopen(url)
  return json.loads(response.read())

def getModuleDict(host, env):
  cleanInfo = {}
  rawInput = getJsonDict(host, env)

  for x in rawInput:
    for dep in x['departments']:
        for domain in dep['domains']:
          for module in domain['modules']:
            if module.has_key('error') is False:
                cleanModuleName =  module['moduleName'].split()[0]
                cleanInfo[cleanModuleName] = {}

                if module.has_key('endpointHealth'):
                  for eph in module['endpointHealth']:
                    if eph.has_key('isPrimary') and eph['isPrimary'] is True:
                      cleanInfo[cleanModuleName] = eph

  return cleanInfo

def getModuleInfo(host, env, module):
  """

    get specific info for one module
    :param host: ted host
    :param env: env to query for
    :param module: module to get info for
    :return: returns info for a module
  """

  moduleDict = getModuleDict(host, env)

  if moduleDict.has_key(module) is False:
        return False

  return moduleDict[module]

def checkModuleEndpointStatus(host, env, module):
    """
    check if the buildnr for the given module matches the buildnr from ted
    :param host: ted host
    :param env: env to query for
    :param module: module name
    :param buildNumber: buildnumber to match
    :return: True of False
    """
    actualHealthStatus =  getModuleInfo(host, env, module)['httpCode']
    if actualHealthStatus != 200:
        print "httpStatus for endpoint: %s which indicates that there is something wrong with our beloved module: %s" % (actualHealthStatus, module)
        return False

    return True

if checkModuleEndpointStatus(tedHost, environment, moduleName):
    print "Ted check succeeded"
    return True

sys.exit(2)
