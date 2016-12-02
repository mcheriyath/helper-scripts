# AWS EC2 Lambda with Slack Integration
A lambda python script to check EC2 tags and post it on a defined slack channel.

Firstly, Thanks to [Eric Thebeault](https://github.com/thibeault/lambda-slack-birthday-bot/blob/master/run.py) for pointing me in the right direction.

#### Primary file lists
`lambda_run.py` : Main lambda function file.<br>
`lambda_ec2_execution-role.txt`: Sample Lambda execution policy.<br>
`ec2lambdaslack.zip`: lambda package to be uploaded for execution.<br>

#### Supporting file lists
`Vagrantfile`: Test machine for creating python virtualenvironment.<br>
`get_instance_ids_with_tags.py`: Another lame approach.<br>
`encrypt_with_kms.py`: Sample script to encrypt and decrypt a string with boto3 and AWS KMS.<br>
`sortUnique.py`: Sample script to sort a list with unique elements.<br>
`vagrant.bashrc(encrypted)`: Bashrc script for the Vagrant machine to configure environment variables.<br>

### Requirements for Integrating EC2, LAMBDA and Slack
1. Permission to create Slack Channel and invite users to the channel
2. AWS CLI/API access(AccessKey & SecretKey) to services like Lambda, KMS, S3, EC2
3. IAM User with permissions to create policies which enables lambda execution role to access EC2, KMS, Cloudwatch and S3
4. Host machine supporting Ubuntu Vagrant box(optional)

##### To Create a Slack bot user, get the Slack API Token
1. Visit https://api.slack.com/custom-integrations
2. Click on Set up a bot user button to continue creating a bot
3. Once created add this user to the desired channel(Later passed as an environmentvariable in Lambda)
4. Save the API token somewhere securely, ideally in an encrypted KMS store

##### To Create a Lambda Deployment Package
Copy the file lambda_run.py to the vagrant box. <br>
Create a virtualenv, activate the environ, install packages with pip<br>

> vagrant@lambda:~$ virtualenv ~/ec2lambdaslack_venv <br>
> vagrant@lambda:~$ source ~/ec2lambdaslack_venv/bin/activate<br>
> (ec2lambdaslack_venv) vagrant@lambda:~$ pip install slackclient boto3 crypto <br>


Create the lambda bundle/package with the required site-packages and lambda function code <br>
> (ec2lambdaslack_venv) vagrant@lambda:~$ cd ~/ec2lambdaslack_venv/lib/python2.7/site-packages/ <br>
> (ec2lambdaslack_venv) vagrant@lambda:~$ zip -r9 /vagrant/ec2lambdaslack.zip websocket boto3 botocore slackclient requests <br>
> (ec2lambdaslack_venv) vagrant@lambda:~$ zip -r9 /vagrant/ec2lambdaslack.zip lambda_run.py <br>

In the official [deployment-pkg](http://docs.aws.amazon.com/lambda/latest/dg/with-s3-example-deployment-pkg.html) it says we need to compress all the site packages, but that is not required.<br>

Create your lambda function
> aws lambda create-function --region us-west-2 --function-name lambda_run --zip-file fileb:///vagrant/ec2lambdaslack.zip --role arn:aws:iam::awsaccountnumber:role/lambda-execution-role --handler lambda_run.lambda_handler --runtime python2.7 --timeout 4 --memory-size 128

Create KMS key, craete an Alias and Encrypt the Slack token
> aws kms create-key --region us-west-2 --description 'Token  to Send message to Slack based on Ec2 tag complaince' --policy file://lambda_ec2_execution-role.json <br>
> aws kms create-alias --region us-west-2 --alias-name alias/awstoslacktoken --target-key-id ARNFromTheAboveCommand <br>
> aws kms encrypt --key-id ARNFromTheAboveCommand --region us-west-2 --plaintext "SlackTokenCreatedEarlier" <br>

Note down the CiphertextBlob(including the == in the end) as this will be passed as an Environment Variable in Lambda later.

##### Create Lambda environment variables

######Using CLI while creating lambda function as 
> --environment Variables={kmsEncryptedSlackToken='outputofCiphertextBlob',slackChannel='ChannelName'}

######Using AWS Console
Login to your console and go to: Lambda -> Functions -> lambda_run<br>
Under Environment variables:

Key|  Value 
--- | ---
kmsEncryptedSlackToken|outputofCiphertextBlob
slackChannel|ChannelName

Save it<br>

### Testing the lambda function

###### Using CLI for invoking lambda function
````ruby
aws lambda invoke --invocation-type RequestResponse --function-name lambda_run --region us-west-2 --log-type Tail --payload '{"kmsEncryptedSlackToken":"outputofCiphertextBlob","slackChannel":"ChannelName"}' outputfile.txt
````
On sucess Message gets posted onto slack channel and the command line returns a below output
````ruby
{
    "LogResult": "U1RBUlQgUmVxdWVzdElkOiBiNmFhOTUxNy1iOGI2LTExZTYtOTdhZi1lMTgwN2NiMzIzM2YgVmVyc2lvbjogJExBVEVTVAp7dSdtZXNzYWdlJzoge3UndXNlcm5hbWUnOiB1J2F3c21lc3NlbmdlcicsIHUndGV4dCc6IHUiSW5zdGFuY2VJRHMgV2l0aG91dCBDb3N0IFRhZ3M6IFsnaS04YmNlM2E1NycsICdpLTUyNzk5YThlJywgJ2ktMmNlNzJkODInLCAnaS02MjhlN2JiZScsICdpLTIyNzQ5OGZlJywgJ2ktNzdkNDM5YWInLCAnaS03MGQ0MzlhYycsICdpLWNmYjBhZWQ3JywgJ2ktMTBiMGFlMDgnLCAnaS0xN2IwYWUwZicsICdpLTk2YTk3NDM4JywgJ2ktNzU1MDQ0NmQnLCAnaS0wMDUxNDUxOCcsICdpLTFjYzQyOWMwJ10iLCB1J3RzJzogdScxNDgwNzAwNTYwLjAwMDAwMicsIHUnc3VidHlwZSc6IHUnYm90X21lc3NhZ2UnLCB1J3R5cGUnOiB1J21lc3NhZ2UnLCB1J2JvdF9pZCc6IHUnQjM5MVpKQkVaJ30sIHUnb2snOiBUcnVlLCB1J3RzJzogdScxNDgwNzAwNTYwLjAwMDAwMicsIHUnY2hhbm5lbCc6IHUnQzM5S0VHSjZUJ30KTGFtYmRhIHJ1biBTdWNjZXNzIG9uIDIwMTYtMTItMDIgMTc6NDI6NDAKRU5EIFJlcXVlc3RJZDogYjZhYTk1MTctYjhiNi0xMWU2LTk3YWYtZTE4MDdjYjMyMzNmClJFUE9SVCBSZXF1ZXN0SWQ6IGI2YWE5NTE3LWI4YjYtMTFlNi05N2FmLWUxODA3Y2IzMjMzZglEdXJhdGlvbjogMjMwOC40OCBtcwlCaWxsZWQgRHVyYXRpb246IDI0MDAgbXMgCU1lbW9yeSBTaXplOiAxMjggTUIJTWF4IE1lbW9yeSBVc2VkOiA0OSBNQgkK",
    "StatusCode": 200
}
````
The output is saved to outputfile.txt

###### Using AWS Console for invoking lambda function
- Login to your console and go to: Lambda -> Functions -> lambda_run
- Click on Test
- The function should ideally run and post messages onto slack channel if there is any instance without the given tag
- On cloudwatch logs we get the message posted to slack channel as well as an output like
````python
Lambda run Success on 2016-12-01 22:17:10
````

### TO-DO
- null output
