#!/usr/bin/python
#I am very sorry to ruin this great puzzel experience for you Brian Jolie ..
# but it is after all friday afternoon ..
#
import urllib
import urllib2
import json



def getJsonDict(host, env):
  """
  Download the TED json for buildnumbers per
  We pull down everything because at this point i do nog give a flying f&*%& about ted's performance
  We will have to worry about that when they start complaining
  :param host: hostname of the ted server
  :param env: wich environment the request the json for
  :return: dict representation of the information provided by ted
  """
  url = "api/build-numbers/all/%s" % env
  url = urllib.quote(url)
  url = "http://%s/%s" % (host, url)

  response = urllib2.urlopen(url)
  return json.loads(response.read())

def getModuleDict(host, env):
  """
  get the info from ted and clean it so we can use it
  :param host: ted host
  :param env: environment to query for
  :return: a dictionary {moduleName: {info}}
  """
  cleanInfo = {}
  rawInput = getJsonDict(host, env)

  for x in rawInput:
    for dep in x['departments']:
        for domain in dep['domains']:
          for module in domain['modules']:
            if module.has_key('error') is False:
                cleanModuleName =  module['moduleName'].split()[0]
                cleanInfo[cleanModuleName] = {}

                if module.has_key('buildNumbers'):
                  cleanInfo[cleanModuleName] = module['buildNumbers']

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

def checkModuleBuildNr(host, env, module, buildNumber):
    """
    check if the buildnr for the given module matches the buildnr from ted
    :param host: ted host
    :param env: env to query for
    :param module: module name
    :param buildNumber: buildnumber to match
    :return: True of False
    """
    actualBuildNumber =  getModuleInfo(host, env, module)['buildNumber']
    if actualBuildNumber != buildNumber:
        print "buildNr: %s does not match up with result from TED: %s" % (buildNumber, actualBuildNumber)
        return False

    return True

if checkModuleBuildNr(tedHost, environment, moduleName, buildNr) == True:
    print "Ted check succeeded"
    sys.exit(0)
else:
    sys.exit(2)
