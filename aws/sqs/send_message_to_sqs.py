import boto3

# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue
queue = sqs.get_queue_by_name(QueueName='TradeStatus.fifo')

try:
    userInput = raw_input("Please enter file name: ")
except NameError:
    pass

with open(userInput, 'r') as myfile:
    data=myfile.read()

response = queue.send_message(
    MessageBody=data,
    MessageGroupId='messageGroup1'
)

# The response is NOT a resource, but gives you a message ID and MD5
print(response.get('MessageId'))
print(response.get('MD5OfMessageBody'))
