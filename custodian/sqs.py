# SQS list all queues
import boto3
import string
import random


sqs = boto3.resource('sqs')
for queue in sqs.queues.all():
    print(queue.url)

#Get the queue
queue = sqs.get_queue_by_name(QueueName='denverdevopsmcqueue')

#Random ID Generator
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))

random_message = id_generator()

#Create a new message
response = queue.send_message(MessageBody='Messagedenverdevopsmc'+ str(random_message))

# The return is NOT a resource, but gives us a message ID 
#print(response.get('MessageId'))
#response = queue.send_messages(Entries=[
#	{
#		'Id': '1',
#		'MessageBody': 'world'
#	},
#	{
#		'Id': '2',
#		'MessageBody': 'boto3',
#		'MessageAttributes': {
#			'Author': {
#				'StringValue': 'Daniel',
#				'DataType': 'String'
#			}
#		}
#	}
#])
print(response.get('MessageId'))
#print(response.get('Failed'))
