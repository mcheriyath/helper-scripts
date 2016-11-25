import boto3
import json
import requests

client = boto3.client('sqs')

# Get the Queue URL
response = client.get_queue_url(
    QueueName='samplequeue' # Or the name of your SQS queue
)
url = response['QueueUrl']

messages = client.receive_message(
    QueueUrl=url,
    AttributeNames=['All'],
    MaxNumberOfMessages=1,
    VisibilityTimeout=60,
    WaitTimeSeconds=5
)

if messages.get('Messages'):
    m = messages.get('Messages')[0]
    body = m['Body']
    receipt_handle = m['ReceiptHandle']

print(body)

webhook_url = 'https://hooks.slack.com/services/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'

payload = {
	"text":"",
	"username": "ghost-bot",
	"channel": "#general"
}

payload["text"] ="Message is {body}"

print (payload)

exit()

response = requests.post(
    webhook_url, data=json.dumps(payload),
    headers={'Content-Type': 'application/json'}
)


if response.status_code != 200:
    raise ValueError(
        'Request to slack returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )


response = client.delete_message(
    QueueUrl=url,
    ReceiptHandle=receipt_handle
)
