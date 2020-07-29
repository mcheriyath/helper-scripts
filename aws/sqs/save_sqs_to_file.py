#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Usage: get_sqs_messages.py <QUEUE_URL>
       get_sqs_messages.py -h | --help
"""

import json

import boto3
import docopt


def get_messages_from_queue(queue_url):
"""Generates messages from an SQS queue.

    Note: this continues to generate messages until the queue is empty.
    Every message on the queue will be deleted.

    :param queue_url: URL of the SQS queue to drain.

    """
    sqs_client = boto3.client('sqs')

    while True:
        resp = sqs_client.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=10
        )

        try:
            yield from resp['Messages']
        except KeyError:
            return

        entries = [
            {'Id': msg['MessageId'], 'ReceiptHandle': msg['ReceiptHandle']}
            for msg in resp['Messages']
        ]

        resp = sqs_client.delete_message_batch(
            QueueUrl=queue_url, Entries=entries
        )

        if len(resp['Successful']) != len(entries):
            raise RuntimeError(
                f"Failed to delete messages: entries={entries!r} resp={resp!r}"
            )


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    queue_url = args['<QUEUE_URL>']

    for message in get_messages_from_queue(queue_url):
        print(json.dumps(message))
