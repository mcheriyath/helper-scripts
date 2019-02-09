Rules Engine for AWS management
===============================
A great tool to ensure AWS resources are properly tagged and maintained by different IAM users in a company.
Full credit goes to CapitalOne Team - [Cloud-Custodian](https://github.com/capitalone/cloud-custodian)

## Contents
* [Create IAM Roles and Permissions](#create-iam-roles-and-permissions)
* [Setup Environement](#setup-environment)
* [Sample Policy](#sample-policy)
* [Troubleshooting](#troubleshooting)
* [Advanced Usage](#advanced-usage)
* [References](#references)
* [ToDo](#todo)

## Create IAM Roles and Permissions
#### Create an IAM Role
```
aws iam create-role --role-name mcheriyath-lambda-execution-role --assume-role-policy-document file://role-for-mcheriyath.json
```

Note down the arn generated. This will be used later while creating a custodian policy yml.

#### Create policy with permissions and attached to the role 
```
aws iam put-role-policy --role-name mcheriyath-lambda-execution-role --policy-name mcheriyath-lambda-permission-policy --policy-document file://lambda-execution-role.json
```


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
#### Create a file named custodian.yml with this content:
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
#### Run the custodian to create the AWS Config and Lambda function
```
$ custodian run -s . custodian.yml -r us-west-1 --cache-period=10
2017-06-21 19:41:37,610: custodian.policy:INFO Provisioning policy lambda ec2-tag-compliance
2017-06-21 19:41:38,136: custodian.lambda:INFO Publishing custodian policy lambda function custodian-ec2-tag-compliance
```

## Troubleshooting
#### Verify the AWS Config Rule
```
$ aws configservice describe-config-rules
{
    "ConfigRules": [
        {
            "Scope": {
                "ComplianceResourceTypes": [
                    "AWS::EC2::Instance"
                ]
            },
            "Source": {
                "Owner": "CUSTOM_LAMBDA",
                "SourceIdentifier": "arn:aws:lambda:us-west-1:123456789123:function:custodian-ec2-tag-compliance",
                "SourceDetails": [
                    {
                        "MessageType": "ConfigurationItemChangeNotification",
                        "EventSource": "aws.config"
                    }
                ]
            },
            "Description": "cloud-custodian lambda policy",
            "ConfigRuleName": "custodian-ec2-tag-compliance",
            "ConfigRuleArn": "arn:aws:config:us-west-1:123456789123:config-rule/config-rule-qqerl7",
            "ConfigRuleId": "config-rule-qqerl7",
            "ConfigRuleState": "ACTIVE"
        }
    ]
}
```

#### Verify the Lambda function created
```
$ aws lambda list-functions
{
    "Functions": [
        {
            "Role": "arn:aws:iam::123456789123:role/mcheriyath-lambda-execution-role",
            "FunctionName": "custodian-ec2-tag-compliance",
            "Handler": "custodian_policy.run",
            "FunctionArn": "arn:aws:lambda:us-west-1:123456789123:function:custodian-ec2-tag-compliance",
            "Timeout": 60,
            "Version": "$LATEST",
            "LastModified": "2017-06-21T19:41:39.415+0000",
            "MemorySize": 512,
            "Description": "cloud-custodian lambda policy",
            "CodeSize": 1364638,
            "Runtime": "python2.7",
            "CodeSha256": "UqP0ACfwerwerwerwerwerewt1G+Jc4jzIH89ls/gLU="
        }
    ]
}
```

#### Check Lambda logs for any errors

Easiest way to check lambda logs is from amazon [web-console](http://docs.aws.amazon.com/lambda/latest/dg/monitoring-functions-logs.html)


## Advanced Usage
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

## References

* [Custodian Getting Started](http://www.capitalone.io/cloud-custodian/docs/quickstart/index.html) <br>
* [Use Cases](http://www.capitalone.io/cloud-custodian/docs/usecases/index.html) <br>
* [Lambda+AWSConfig](http://www.capitalone.io/cloud-custodian/docs/policy/lambda.html#config-rules) <br>
* [Reported Issues](https://github.com/capitalone/cloud-custodian/issues/1311)

## TODO
- Once verified the tagcompliance need to update the SQS with the ownerContact details so that a message can be posted on slack or emailed directly to the owner
- Add a for loop in the fetch-sqs-post-slack.py to get multiple messages and post the messages to slack
- Proper output if there is no messages in the queue
