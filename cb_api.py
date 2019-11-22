#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import urllib3


### Cloudbreak API Class
class CBManage():
    # Make sure to set the baseurl
    _urls = {'baseurl': 'https://cloudbreak.example.mysite.com/',
             'identity': 'identity/oauth/authorize',
             'clustercreate': 'cb/api/v2/stacks/user',
             'clusterdelete': 'cb/api/v1/stacks/{}/cluster',
             'clustersinfo': 'cb/api/v2/stacks/account',
             'clusterinfo': 'cb/api/v2/stacks/account/{}',
             'clusterstatus': 'cb/api/v2/stacks/{}/status',
             'cbinfo': 'cb/info'}

    # IMPORTANT: All parameters for cluster creation
    tmpldct = {"rangeradminpassword": "",
               "ambUserName": "",
               "ambPassword": "",
               "krbprincipal": "",
               "krbpassword": "",
               "securityGroupId": "",
               "securityGroupIds": "",
               "subnetId": "",
               "vpcId": "",
               "publicKeyId": "",
               "imageId": "",
               "credentialName": "",
               "instanceProfile": "",
               "name": "",
               "customHostname": "",
               "blueprintName": "",
               "customDomain": "example.mysite.com",
               # Ambari Blueprint variables, create/delete as required, refer cloudbreak json template below
               "atlaskafka": "master-1.example.mysite.com",
               "atlasrest": "master-1.example.mysite.com",
               "metastore1": "master-3.example.mysite.com",
               "metastore2": "master-2.example.mysite.com",
               "rangeradmin": "master-3.example.mysite.com",
               "zoo1": "master-1.example.mysite.com",
               "zoo2": "master-2.example.mysite.com",
               "zoo3": "master-3.example.mysite.com",
               # Kerberos parameters
               "url": "ad.mysite.com",
               "adminUrl": "ad.mysite.com",
               "realm": "AD.MYSITE.COM",
               "ldapUrl": "ldaps://ad.mysite.com",
               "containerDn": "OU=HDP,OU=Service Accts,DC=ad,DC=mysite,DC=com",
               # Ambari parameters, always validateBlueprint
               "validateBlueprint": "true",
               "versionDefinitionFileUrl": "http://repo.example.mysite.com/HDP/centos7/3.x/updates/3.1.0.0/HDP-3.1.0.0/HDP-3.1.0.0-78.xml",
               "baseUrl": "http://repo.example.mysite.com/ambari/centos7/2.x/updates/2.7.3.0/ambari-2.7.3.0",
               "gpgKeyUrl": "http://repo.example.mysite.com/ambari/centos7/2.x/updates/2.7.3.0/RPM-GPG-KEY/RPM-GPG-KEY-Jenkins",
               "recipeNames": ["post-launch-hardenOS", "pre-terminate-cleanup"]}

    def __init__(self, cbusername, cbpassword, verifyCert=True):
        self._verifyCert = verifyCert
        if not self._verifyCert:
            # Also disable warnings, user knows what they are doing
            urllib3.disable_warnings()
        self._token = self._get_token(cbusername, cbpassword)
        self._headers = {'Content-Type': 'application/json',
                         'Accept': 'application/json',
                         'Authorization': 'Bearer {}'.format(self._token)}

    def _get_token(self, cbusername, cbpassword):
        resp = requests.post(url=self._urls['baseurl'] + self._urls['identity'],
                             params={'response_type': 'token',
                                     'client_id': 'cloudbreak_shell',
                                     'scope.0': 'openid',
                                     'source': 'login',
                                     'redirect_uri': 'http://cloudbreak.shell'},
                             headers={'accept': 'application/x-www-form-urlencoded'},
                             verify=self._verifyCert,
                             allow_redirects=False,
                             data=[('credentials',
                                    '{"username":"' + cbusername + '",'
                                    '"password":"' + cbpassword + '"}'),])
        resp.raise_for_status()
        return urllib3.packages.six.moves.urllib.parse.parse_qs(resp.headers["Location"])['access_token'][0]

    # Generic function for GET
    def _getreq(self, url, params=None):
        response = requests.get(self._urls['baseurl'] + url,
                                headers=self._headers,
                                verify=self._verifyCert,
                                params=params)
        return response

    # Generic function for POST
    def _postreq(self, url, msgbody):
        response = requests.post(self._urls['baseurl'] + url,
                                 headers=self._headers,
                                 verify=self._verifyCert,
                                 json=msgbody)
        return response

    # Generic function for DELETE
    def _delreq(self, url, params=None):
        response = requests.delete(self._urls['baseurl'] + url,
                                   headers=self._headers,
                                   verify=self._verifyCert,
                                   params=params)
        return response

    # Get CB version
    def get_cb_info(self, params=None):
        return self._getreq(self._urls['cbinfo'], params)

    # Get status of a cluster
    def get_cluster_status(self, clusterid, params=None):
        return self._getreq(self._urls['clusterstatus'].format(clusterid), params)

    # Get cluster information
    def get_cluster_info(self, clustername, params=None):
        return self._getreq(self._urls['clusterinfo'].format(clustername), params)

    # Get information of all clusters
    def get_allcluster_info(self, params=None):
        return self._getreq(self._urls['clustersinfo'], params)

    # !!!Careful!!!!  Delete a cluster
    def delete_cluster(self, clusterid, params=None):
        return self._delreq(self._urls['clusterdelete'].format(clusterid), params)

    # Create Cluster(stack), builds the cloudbreak json template, set the dictionary values as required
    def create_cluster(self):
        return self._postreq(self._urls['clustercreate'], self._get_msgbody())

    # Cloudbreak json template
    def _get_msgbody(self):
        msgbody = {
                    "general": {
                                "credentialName": self.tmpldct['credentialName'],
                                "name": self.tmpldct['name']
                                },
                    "placement": {
                                "availabilityZone": "us-east-1a",
                                "region": "us-east-1"
                    },
                    "parameters": {},
                    "inputs": {
                                "atlaskafka": self.tmpldct['atlaskafka'],
                                "atlasrest": self.tmpldct['atlasrest'],
                                "metastore1": self.tmpldct['metastore1'],
                                "metastore2": self.tmpldct['metastore2'],
                                "rangeradmin": self.tmpldct['rangeradmin'],
                                "zoo1": self.tmpldct['zoo1'],
                                "zoo2": self.tmpldct['zoo2'],
                                "zoo3": self.tmpldct['zoo3'],
                                "rangeradminpassword": self.tmpldct['rangeradminpassword']
                    },
                "customDomain": {
                            "customDomain": self.tmpldct['customDomain'],
                            "customHostname": self.tmpldct['customHostname'],
                            "clusterNameAsSubdomain": "false",
                            "hostgroupNameAsHostname": "false"
                },
                "tags": {
                            "userDefinedTags": {}
                },
                "instanceGroups": [
                            {
                              "nodeCount": 1,
                              "group": "master2",
                              "type": "CORE",
                              "parameters": {},
                              "template": {
                      "volumeCount": 1,
                      "volumeSize": 100,
                      "rootVolumeSize": 50,
                      "parameters": {
                                 "encrypted": "false",
                                 "platformType": "AWS",
                                 "type": "NONE"
                      },
                      "volumeType": "standard",
                      "instanceType": "m5.xlarge"
                              },
                              "securityGroup": {
                      "securityGroupId": self.tmpldct['securityGroupId'],
                      "securityGroupIds": self.tmpldct['securityGroupIds'],
                      "securityRules": []
                              },
                              "recipeNames": self.tmpldct['recipeNames'],
                              "recoveryMode": "MANUAL"
                            },
                            {
                              "nodeCount": 1,
                              "group": "master1",
                              "type": "GATEWAY",
                              "parameters": {},
                              "template": {
                      "volumeCount": 1,
                      "volumeSize": 100,
                      "rootVolumeSize": 50,
                      "parameters": {
                                 "encrypted": "false",
                                 "platformType": "AWS",
                                 "type": "NONE"
                      },
                      "volumeType": "standard",
                      "instanceType": "m5.xlarge"
                              },
                              "securityGroup": {
                      "securityGroupId": self.tmpldct['securityGroupId'],
                      "securityGroupIds": self.tmpldct['securityGroupIds'],
                      "securityRules": []
                              },
                              "recipeNames": self.tmpldct['recipeNames'],
                              "recoveryMode": "MANUAL"
                            },
                            {
                              "nodeCount": 3,
                              "group": "clients",
                              "type": "CORE",
                              "parameters": {},
                              "template": {
                      "volumeCount": 1,
                      "volumeSize": 100,
                      "rootVolumeSize": 50,
                      "parameters": {
                                 "encrypted": "false",
                                 "platformType": "AWS",
                                 "type": "NONE"
                      },
                      "volumeType": "standard",
                      "instanceType": "m5.xlarge"
                              },
                              "securityGroup": {
                      "securityGroupId": self.tmpldct['securityGroupId'],
                      "securityGroupIds": self.tmpldct['securityGroupIds'],
                      "securityRules": []
                              },
                              "recipeNames": self.tmpldct['recipeNames'],
                              "recoveryMode": "MANUAL"
                            },
                            {
                              "nodeCount": 1,
                              "group": "master3",
                              "type": "CORE",
                              "parameters": {},
                              "template": {
                      "volumeCount": 1,
                      "volumeSize": 100,
                      "rootVolumeSize": 50,
                      "parameters": {
                                 "encrypted": "false",
                                 "platformType": "AWS",
                                 "type": "NONE"
                      },
                      "volumeType": "standard",
                      "instanceType": "m5.xlarge"
                              },
                              "securityGroup": {
                      "securityGroupId": self.tmpldct['securityGroupId'],
                      "securityGroupIds": self.tmpldct['securityGroupIds'],
                      "securityRules": []
                              },
                              "recipeNames": self.tmpldct['recipeNames'],
                              "recoveryMode": "MANUAL"
                            }
                ],
                "stackAuthentication": {
                            "publicKeyId": self.tmpldct['publicKeyId']
                },
                "network": {
                            "parameters": {
                              "subnetId": self.tmpldct['subnetId'],
                              "vpcId": self.tmpldct['vpcId']
                            }
                },
                "imageSettings": {
                            "imageCatalog": "cloudbreak-default",
                            "imageId": self.tmpldct['imageId']
                },
                "cluster": {
                            "rdsConfigNames": [
                              "rangerdb",
                              "hivedb"
                            ],
                            "cloudStorage": {
                              "s3": {
                      "instanceProfile": self.tmpldct['instanceProfile']
                              },
                              "locations": []
                            },
                            "ambari": {
                              "blueprintName": self.tmpldct['blueprintName'],
                              "enableSecurity": "true",
                              "platformVersion": "HDP 3.1",
                              "validateBlueprint": self.tmpldct['validateBlueprint'],
                              "validateRepositories": "false",
                              "userName": self.tmpldct['ambUserName'],
                              "password": self.tmpldct['ambPassword'],
                              "kerberos": {
                                  "url": self.tmpldct['url'],
                                  "adminUrl": self.tmpldct['adminUrl'],
                                  "realm": self.tmpldct['realm'],
                                  "ldapUrl": self.tmpldct['ldapUrl'],
                                  "containerDn": self.tmpldct['containerDn'],
                                  "tcpAllowed": "false",
                                  "principal": self.tmpldct['krbprincipal'],
                                  "password": self.tmpldct['krbpassword']
                              },
                              "ambariStackDetails": {
                                  "stack": "HDP",
                                  "version": "3.1",
                                  "stackRepoId": "HDP",
                                  "enableGplRepo": "false",
                                  "verify": "false",
                                  "repositoryVersion": "3.1.0.0-78",
                                  "versionDefinitionFileUrl": self.tmpldct['versionDefinitionFileUrl'],
                                  "mpacks": []
                              },
                              "ambariRepoDetailsJson": {
                                  "version": "2.7.3.0",
                                  "baseUrl": self.tmpldct['baseUrl'],
                                  "gpgKeyUrl": self.tmpldct['gpgKeyUrl']
                              }
                            }
                            }
                }
        return msgbody


### Set the username and password for cloudbreak
cbuname = 'admin@mysite.com'
cbpwd = 'mycbpassword'
cbobj = CBManage(cbuname, cbpwd, verifyCert=False)


### !!!!Important!!!! Set the template variables before creating the cluster
# uncomment create_cluster as required
cbobj.tmpldct['name'] = "my-cluster-1"
cbobj.tmpldct["customHostname"] = "my-hostname-"
cbobj.tmpldct["blueprintName"] = "myblueprintname"
cbobj.tmpldct["imageId"] = "my-aws-image-id-here"
cbobj.tmpldct["rangeradminpassword"] = "rangeradminpassword"
cbobj.tmpldct["ambUserName"] = "admin"
cbobj.tmpldct["ambPassword"] = "ambariPassword"
cbobj.tmpldct["krbprincipal"] = "mysite-admin@.ad.mysite.com"
cbobj.tmpldct["krbpassword"] = "mysite-admin-password"
cbobj.tmpldct["securityGroupId"] = "sg-awssgid"
cbobj.tmpldct["securityGroupIds"] = ["sg-awssgid1", "sg-awssgid2"]
cbobj.tmpldct["subnetId"] = "subnet-awssubnetid"
cbobj.tmpldct["vpcId"] = "vpc-awsvpcid"
cbobj.tmpldct["publicKeyId"] = "aws-keypair"
cbobj.tmpldct["credentialName"] = "cbcredentialName"
cbobj.tmpldct["instanceProfile"] = "arn:aws:iam::number:my-profile/mysite"
# cbobj.tmpldct["customDomain"] = ""
# cbobj.tmpldct["atlaskafka"] = ""
# cbobj.tmpldct["atlasrest"] = ""
# cbobj.tmpldct["metastore1"] =  ""
# cbobj.tmpldct["metastore2"] = ""
# cbobj.tmpldct["rangeradmin"] =  ""
# cbobj.tmpldct["zoo1"] =  ""
# cbobj.tmpldct["zoo2"] = ""
# cbobj.tmpldct["zoo3"] = ""
# cbobj.tmpldct["url"] =  ""
# cbobj.tmpldct["adminUrl"] = ""
# cbobj.tmpldct["realm"] = ""
# cbobj.tmpldct["ldapUrl"] = ""
# cbobj.tmpldct["containerDn"] = ""
# cbobj.tmpldct["validateBlueprint"] = "false"
# cbobj.tmpldct["versionDefinitionFileUrl"] =  ""
# cbobj.tmpldct["baseUrl"] =  ""
# cbobj.tmpldct["gpgKeyUrl"] = ""
# cbobj.tmpldct["recipeNames"] = ""
#print(cbobj._get_msgbody())
### Create a new cluster, uncomment below
#resp = cbobj.create_cluster()
if resp.ok:
    print(resp.json()['name'], resp.json()['id'])
else:
    print(resp.json())
    resp.raise_for_status()


### To delete the cluster kerberos principals, set withStackDelete=true
### !!!Careful!!! Delete a cluster; uncomment below line
#resp = cbobj.delete_cluster(str(resp.json()['id']), {'withStackDelete':'true'})
#resp = cbobj.delete_cluster('111', {'withStackDelete':'true'})
if resp.ok:
    print('Status:', resp.status_code, ' ', resp.reason)
    print('URL:', resp.url)
else:
    print(resp.json())
    resp.raise_for_status()

### Few GET examples
resp = cbobj.get_cb_info()
print(resp.json())
resp = cbobj.get_allcluster_info()
print(len(resp.text))
resp = cbobj.get_cluster_info('my-cluster-1')
print(resp.json()['name'], resp.json()['id'])
resp = cbobj.get_cluster_status(str(resp.json()['id']))
print(resp.json())
