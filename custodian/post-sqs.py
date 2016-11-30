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
response = queue.send_message(MessageBody='OpsMessage'+ str(random_message))

print(response.get('MessageId'))
