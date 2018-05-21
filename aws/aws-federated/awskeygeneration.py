#!/usr/bin/python

import sys, re
import boto.sts
import boto.s3
import requests
import getpass
import ConfigParser
import base64
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from os.path import expanduser
from urlparse import urlparse, urlunparse
from requests_ntlm import HttpNtlmAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning) 
##########################################################################
# Variables

# region: The default AWS region that this script will connect
# to for all API calls
region = 'us-east-1'

# output format: The AWS CLI output format that will be configured in the
# saml profile (affects subsequent CLI calls)
outputformat = 'text'

# awsconfigfile: The file where this script will store the temp
# credentials under the saml profile
awsconfigfile = '/.aws/credentials'

# SSL certificate verification: Whether or not strict certificate
# verification is done, False should only be used for dev/test
sslverification = False
# idpentryurl: The initial URL that starts the authentication process.
idpentryurl = 'https://sso.corp.example.com/adfs/ls/IdpInitiatedSignOn?loginToRp=urn:amazon:webservices'

##########################################################################

# Get the federated credentials from the user
username = sys.argv[1] # corp username
password = sys.argv[2] # corp password
account_id = sys.argv[3] # aws accountnumber
role_name = sys.argv[4] # IAM user role

if '@' not in username:
    username += '@corp.ad.example.com'


# Initiate session handler
session = requests.Session()

# Programatically get the SAML assertion
# Set up the NTLM authentication handler by using the provided credential
# session.auth = HttpNtlmAuth(username, password, session)

# Opens the initial AD FS URL and follows all of the HTTP302 redirects
# response = session.get(idpentryurl, verify=False)

# *** New Section ***
formresponse = session.get(idpentryurl, verify=False)
formsoup = BeautifulSoup(formresponse.text.decode('utf8'), "html.parser")
payload = {}
for inputtag in formsoup.find_all(re.compile('(INPUT|input)')):
    name = inputtag.get('name','')
    value = inputtag.get('value','')
    if "user" in name.lower():
        #Make an educated guess that this is the right field for the username
        payload[name] = username
    elif "email" in name.lower():
        #Some IdPs also label the username field as 'email'
        payload[name] = username
    elif "pass" in name.lower():
        #Make an educated guess that this is the right field for the password
        payload[name] = password
    else:
        #Simply populate the parameter with the existing value (picks up hidden fields in the login form)
        payload[name] = value

idpauthformsubmiturl = idpentryurl
response = session.post(
        idpauthformsubmiturl, data=payload, verify=False)

# *** New Section End*** 

# Debug the response if needed
# print (response.text)

# Overwrite and delete the credential variables, just for safety
username = '##############################################'
password = '##############################################'
del username
del password

# Decode the response and extract the SAML assertion
soup = BeautifulSoup(response.text.decode('utf8'), "html.parser")
assertion = ''

# Look for the SAMLResponse attribute of the input tag (determined by
# analyzing the debug print lines above)
for inputtag in soup.find_all('input'):
    if(inputtag.get('name') == 'SAMLResponse'):
        #print(inputtag.get('value'))
        assertion = inputtag.get('value')

# Parse the returned assertion and extract the authorized roles
awsroles = []
role_arn = "arn:aws:iam::" + account_id + ":role/" + role_name
principal_arn = "arn:aws:iam::" + account_id + ":saml-provider/SSOPROD"
root = ET.fromstring(base64.b64decode(assertion))


# Use the assertion to get an AWS STS token using Assume Role with SAML
conn = boto.sts.connect_to_region(region)
token = conn.assume_role_with_saml(role_arn, principal_arn, assertion)

# Write the AWS STS token into the AWS credential file
home = expanduser("~")
filename = home + awsconfigfile

# Read in the existing config file
config = ConfigParser.RawConfigParser()
config.read(filename)

# Put the credentials into a specific profile instead of clobbering
# the default credentials
if not config.has_section('saml'):
    config.add_section('saml')

config.set('saml', 'output', outputformat)
config.set('saml', 'region', region)
config.set('saml', 'aws_access_key_id', token.credentials.access_key)
config.set('saml', 'aws_secret_access_key', token.credentials.secret_key)
config.set('saml', 'aws_session_token', token.credentials.session_token)

# Write the updated config file
with open(filename, 'w+') as configfile:
    config.write(configfile)

# Give the user some basic info as to what has just happened
print '\n\n----------------------------------------------------------------'
print 'Your new access key pair has been stored in the AWS configuration file {0} under the saml profile.'.format(filename)
print 'Note that it will expire at {0}.'.format(token.credentials.expiration)
print 'After this time you may safely rerun this script to refresh your access key pair.'
print 'To use this credential call the AWS CLI with the --profile option (e.g. aws --profile saml ec2 describe-instances).'
print '----------------------------------------------------------------\n\n'


