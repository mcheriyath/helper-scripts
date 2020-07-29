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
    ...


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    queue_url = args['<QUEUE_URL>']

    for message in get_messages_from_queue(queue_url):
        print(json.dumps(message))
