import boto3
import argparse

profileName = '<awsprofilename>'
serialNumber = 'arn:aws:iam::<awsaccountnumber>:mfa/<awsusername>'

boto3.setup_default_session(profile_name=profileName)

client = boto3.client('sts')

parser = argparse.ArgumentParser()
parser.add_argument('token')
args = parser.parse_args()

new_session_token = client.get_session_token(
	DurationSeconds=129600,
	SerialNumber=serialNumber,
	TokenCode=args.token
)

print "[default]"
print "aws_access_key_id = "+ new_session_token['Credentials']['AccessKeyId']
print "aws_secret_access_key = "+ new_session_token['Credentials']['SecretAccessKey']
print "aws_session_token = "+ new_session_token['Credentials']['SessionToken']
