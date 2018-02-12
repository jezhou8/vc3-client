#!/bin/bash
source ./standard-common-config.sh

# Node set
#Nodeset( name=lincolnb-htcondor-10-workers state=new owner=lincolnb node_number=10 app_type=htcondor app_role=worker-nodes cores=1 memory_mb=None storage_mb=None app_host=None app_port=None app_sectoken=None environment=None description=None displayname=htcondor-10-workers url=None docurl=None )
RUN_CHECK_CLIENT nodeset-create --owner lincolnb --node_number 10 --app_type htcondor --app_role worker-nodes --displayname="htcondor-10-workers-nodeset" lincolnb-htcondor-10-workers

# Cluster containing that nodeset
# Cluster( name=lincolnb-htcondor-10-workers state=new owner=lincolnb nodesets=[u'lincolnb-htcondor-10-workers'] description=10 HTCondor workers  displayname=htcondor-10-workers url=None docurl=None )
RUN_CHECK_CLIENT cluster-create --owner lincolnb --description "HTCondor with 10 Workers" --displayname="htcondor-10-workers" lincolnb-htcondor-10-workers

# Add the nodeset to the cluster
RUN_CHECK_CLIENT cluster-addnodeset lincolnb-htcondor-10-workers lincolnb-htcondor-10-workers


RUN_CHECK_CLIENT nodeset-create --owner btovar --node_number 51 --app_type htcondor --app_role worker-nodes --displayname="htcondor-51-workers-nodeset" btovar-htcondor-51-workers

