from __future__ import print_function
import os, sys, time, json, boto3

# PIP slack client available at https://github.com/slackapi/python-slackclient
from slackclient import SlackClient

# Load base-64 encoded, encrypted key (CiphertextBlob) stored in KMS
ENCRYPTED_TOKEN =  os.environ['kmsEncryptedSlackToken']

# The Slack channel to post the message
SLACK_CHANNEL = os.environ['slackChannel']

# Decrypt Slack Token
token = boto3.client('kms').decrypt(CiphertextBlob=b64decode(ENCRYPTED_TOKEN))['Plaintext']

# Load EC2 details in us-west-2 region
ec2 = boto3.resource('ec2', region_name='us-west-2')

# Function to get instance list without Cost Tags
def get_instances_without_cost_tags(instances):
    idswot = []
    for i in instances:
        if 'Cost Center' not in [t['Key'] for t in i.tags]:
            idswot.append(i.instance_id)
    return idswot

# Main Lambda Function
def lambda_handler(event, context):
    # Get all running instance details
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

    # Get all instance ids without cost tag
    instanceidswot = get_instances_without_cost_tags(instances)

    # Prepare Slack message
    SLACK_MESSAGE = 'InstanceIDs Without Cost Tags: {}'.format(instanceidswot)
    sc = SlackClient(token)
    if sc.rtm_connect():
        print(sc.api_call(
            "chat.postMessage",
            channel=SLACK_CHANNEL,
            text=SLACK_MESSAGE,
            username='awsmessenger'))
    else:
        print("Slack Connection failed, please check whether the given token is valid.")
    return str(datetime.now())

""" For Debugging purpose
instanceidswot = get_instances_without_cost_tags(instances)
print('InstanceIDs Without Cost Tags: {}'.format(instanceidswot))

# To get the list of all currently running instances, we can run manually
#aws ec2 describe-instances --filter "Name=instance-state-name,Values=running" --query 'Reservations[*].Instances[*].[InstanceId]' --output text
"""

