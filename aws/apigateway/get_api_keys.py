#!/usr/bin/env/python

import boto3
import os
import argparse

apigateway = boto3.client('apigateway', region_name='us-east-1')

def get_api_keys(apiName):
	message = ""
	if apiName == "all":
	 	api = ""
	else:
		api = apiName
	response = apigateway.get_api_keys(nameQuery=api,includeValues=True)
	if response is not None:
		items = response.get('items')

		for item in items:
			if apiName == "all":
				print(item.get('name') + " \n " + item.get('value'))
			else:
				print(item.get('value'))

def main():
	parser = argparse.ArgumentParser(description='Get API keys')
	parser.add_argument('apiname',
	                   help='Either use all or give the specific apiname to get the key(s)')

	args = parser.parse_args()

	get_api_keys(args.apiname)


if __name__ == "__main__":
	main()
