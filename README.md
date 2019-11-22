# Cloudbreak API Python utility
Python utility to invoke Cloudera Cloudbreak APIs

## Overview

[Cloudbreak](https://docs.cloudera.com/HDPDocuments/Cloudbreak/Cloudbreak-2.9.1/index.html) is an [open source tool](https://github.com/hortonworks/cloudbreak) to provision and manage Apache Hadoop clusters on cloud environments.
This python utility can be used to invoke the cloudbreak api to manage/query, create or terminate a cluster/stack on AWS. The utility comes with a [json template](https://docs.cloudera.com/HDPDocuments/Cloudbreak/Cloudbreak-2.9.0/install-cli/content/cb_obtain-cluster-json-template-from-the-ui.html) to deploy a Hortonworks Data Platform(HDP3.1) cluster with [kerberos security enabled](https://docs.cloudera.com/HDPDocuments/Cloudbreak/Cloudbreak-2.9.1/advanced-cluster-options/content/cb_enabling-kerberos-security.html) on the HDP cluster. Refer code comments for additional details.
The json template needs to be updated to provision/manage hadoop clusters on Azure, GCP or OpenStack.

### Requires
- [Python](https://www.python.org/downloads/) 3.5 or greater
