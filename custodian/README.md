Rules Engine for AWS management
===============================
A great tool to ensure AWS resources are properly tagged and maintained by different IAM users in a company.
Full Credit goes to CapitalOne Team - [Cloud-Custodian](https://github.com/capitalone/cloud-custodian)

## Contents
* [Create IAM Roles](#create-iam-roles)
* [Setup Environement](#setup-environment)
* [Sample Policy](#sample-policy)
* [Troubleshooting](#troubleshooting)
* [Advanced usage of custodian with notification](#advaned-usage-of-custodian-with-notification)
* [References](#references)
* [ToDo](#todo)

## Create IAM Roles



## Setup Environment

#### Install [Virtualbox](https://www.virtualbox.org/wiki/Downloads) and launch vm using [Vagrant](https://www.vagrantup.com/downloads.html) <br>
Sample [Vagrantfile](https://raw.githubusercontent.com/mcheriyath/helper-scripts/master/custodian/Vagrantfile) available in this repo folder
```
$ cd custodian
$ vagrant up
$ vagrant ssh
```

#### Install Cloud Custodian
```
$ virtualenv --python=python2 custodian
$ source custodian/bin/activate
(custodian) $ pip install c7n
```

## Sample Policy
Create a file named custodian.yml with this content:
```
policies:
  - name: ec2-tag-compliance
    mode:
        type: config-rule
        role: <put your lambda execution role arn without quotes>
    resource: ec2
    filters:
      - "tag:Custodian": present
    actions:
      - stop
```


## Advanced usage of custodian with notification
Sample Files:
instanceage.yml - List out all instance information older than 15 days
tagcomplaince.yml - List out all the instance information which does not follow the company policy in using resource tags while creating EC2
post-sqs.py - File use to create message and post it to a given SQS queue
fetch-sqs-post-slack.py - Fetches the message from the SQS queue one by one and post it to defined slack using webhook_url


Better integration options with SQS and Slack with [Zapier](https://zapier.com/zapbook/amazon-sqs/slack/)

Post random message to SQS queue
````ruby
python sqs.py
````

Check whether message is available on Queue
````ruby
aws sqs receive-message --queue-url <SQS URL> --attribute-names All --message-attribute-names All --max-number-of-messages 10
````

After Verifying this we are good to run the custodian script as show below to identify the resources which are not using the recommended tags
````ruby
custodian run -c tagcompliance.yml -s tag -r us-west-2
````

The output will be generated in tag directory 

## TODO
- Once verified the tagcompliance need to update the SQS with the ownerContact details so that a message can be posted on slack or emailed directly to him
- Add a for loop in the fetch-sqs-post-slack.py to get multiple messages and post it to slack
- Proper output if there is no messages in the queue
