#!/usr/bin/env/python

import boto3
import os


# Capture our current directory
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

apigateway = boto3.client('apigateway', region_name='us-east-1')

def get_api_keys():
	message = ""
	response = apigateway.get_api_keys(includeValues=True)
	if response is not None:
		items = response.get('items')


		for item in items:
			print(item.get('name') + "=" + item.get('value'))

get_api_keys()
