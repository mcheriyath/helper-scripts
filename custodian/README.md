## Sample Rules Engine for AWS management
This is a really good tool to ensure AWS resources are properly tagged and maintained by different IAM users in a company.
Full Credit goes to CapitalOne Team - [Cloud-Custodian](https://github.com/capitalone/cloud-custodian)

Sample Files:
instanceage.yml - List out all instance information older than 15 days
tagcomplaince.yml - List out all the instance information which does not follow the company policy in using resource tags while creating EC2



Better integration options with SQS and Slack with [Zapier](https://zapier.com/zapbook/amazon-sqs/slack/)

Generate Random SQS message
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

