from __future__ import print_function
import os
import sys
import time
import boto3

ec2 = boto3.resource('ec2', region_name='us-west-2')

def get_instances_with_cost_tags(instances):
    ids = []
    for instance in instances:
        for tag in instance.tags:
            if tag['Key'] == "Cost Center":
                idlist = f5(instance.id, None) # used only to filter unique instance id
                #print(instance.id) # gets the actual instance id with Cost Center Tag
                ids.append(instance.id)
    return ids

def get_instances_without_cost_tags(instances):
    idwot = []
    for intance in instances:
        for tag in instance.tags:

def f5(seq, idfun=None):
    # order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        # in old Python versions:
        # if seen.has_key(marker)
        # but in new ones:
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result

instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
instanceids = get_instances_with_cost_tags(instances)
print('InstanceIDs: {}'.format(instanceids))

