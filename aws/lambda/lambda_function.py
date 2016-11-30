from __future__ import print_function
import os, sys, time, boto3

ec2 = boto3.resource('ec2', region_name='us-west-2')

def get_instances_with_cost_tags(instances):
    idswt = []
    for i in instances:
        if 'Cost Center' in [t['Key'] for t in i.tags]:
            idswt.append(i.instance_id)
    return idswt

def get_instances_without_cost_tags(instances):
    idswot = []
    for i in instances:
        if 'Cost Center' not in [t['Key'] for t in i.tags]:
            idswot.append(i.instance_id)
    return idswot

instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

instanceidswt = get_instances_with_cost_tags(instances)
print('InstanceIDs With Cost Tags: {}'.format(instanceidswt))

instanceidswot = get_instances_without_cost_tags(instances)
print('InstanceIDs Without Cost Tags: {}'.format(instanceidswot))
