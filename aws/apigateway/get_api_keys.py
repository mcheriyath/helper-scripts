#!/usr/bin/env/python

import boto3
import os
import argparse

# Capture our current directory
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

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
			print(item.get('value'))

def main():
	parser = argparse.ArgumentParser(description='Export some swaggers and postmans.')
	parser.add_argument('apiname',
	                   help='The api name')

	args = parser.parse_args()

	get_api_keys(args.apiname)


if __name__ == "__main__":
		main()
