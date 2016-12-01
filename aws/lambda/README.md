# AWS EC2 Lambda with Slack Integration
A lambda python script to check EC2 tags and post it on a defined slack channel.

Firstly, Thanks to [Eric Thebeault](https://github.com/thibeault/lambda-slack-birthday-bot/blob/master/run.py) for pointing me in the right direction.

## Primary file lists
lambda_run.py : Main lambda function file.
lambda_ec2_execution-role.txt: Sample Lambda execution policy.
ec2lambdaslack.zip: lambda package to be uploaded for execution.

## Supporting file lists
Vagrantfile: Test machine for creating python virtualenvironment.
get_instance_ids_with_tags.py: Another lame approach.
encrypt_with_kms.py: Sample script to encrypt and decrypt a string with boto3 and AWS KMS.
sortUnique.py: Sample script to sort a list with unique elements.
vagrant.bashrc(encrypted): Bashrc script for the Vagrant machine to configure environment variables.




To Create a [Slack bot user](https://api.slack.com/custom-integrations)
1. Visit https://api.slack.com/custom-integrations
2. Click on Set up a bot user button to continue creating a bot
3. Once created add this user to the desired channel
4. Save the API token to somewhere secured, ideally in an encrypted KMS store

