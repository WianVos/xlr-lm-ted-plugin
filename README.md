#XL-Release lm ted plugin


## Preface
This document describes the functionality provide by the `xlr-lm-ted-plugin`, as well as potential future functionality.

## Overview
This module enables users of xl-release to set up integration with ted

## Installation


Copy the plugin JAR file into the `SERVER_HOME/plugins` directory of XL Release.

### Limitations
-

## Supported Tasks

+ ted.PerformBuildNrCheck
    * `TedHost: fqdn for the ted host to perform checks against`
    * `moduleName: name of the module to perform the check for`
    * `environment: Name of the environment to check against`
    * `buildNr: expected buildNr.. not matching will result in an error and a break in the release process`

+ ted.PerformHealthCheck
    * `TedHost: fqdn for the ted host to perform checks against`
    * `moduleName: name of the module to perform the check for`
    * `environment: Name of the environment to check against`


## Example Use Case


