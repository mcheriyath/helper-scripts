from __future__ import print_function
import os
import sys
import time
import boto3

ec2 = boto3.resource('ec2', region_name='us-west-2')
# Use the filter() method of the instances collection to retrieve all running EC2 instances.
#instances = ec2.instances.filter(
#    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
#for instance in instances:
#    print(instance.id, instance.instance_type, instance.launch_time)

#print("end of first instructions")
#print("\n \n")
print("begin get_instances_without_cost_tags")

def get_instances_without_cost_tags(instances):
    for instance in instances:
        for tag in instance.tags:
            if tag['Key'] != "Cost Center":
                ilist = list.sort(instance.id)
                #sorted(set(('InstanceID: {}, InstanceType: {}, LaunchTime: {}'.format(instance.id, instance.instance_type, instance.launch_time))))
                print(ilist)
    return instances

instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
instancedetails = get_instances_without_cost_tags(instances)


output="Instances: %s" % (instancedetails)
print("Output:")
print(output)

exit()

def get_environments_from_instances(instances):
    """
    Get all the environments available from instances lists
    :param list instances: the list of instance
    :rtype: list
    :return: a list of the environments
    """
    environments = []
    for instance in instances:
        tags = instance.tags
        for tag in tags:
            key = tag.get("Key")
            if key == "Environment":
                environment = tag.get("Value").strip()
                if environment not in environments:
                    environments.append(environment)
    return environments



