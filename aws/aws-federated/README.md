## Identity Federation

AWS supports identity federation using SAML (Security Assertion Markup Language) 2.0. Using SAML,
With most of the corporate implementations AWS accounts are integrated with on premise identity provider (IdP). This is great if you want to
use the AWS CLI or programmatically call AWS APIs via AD Authentication.

#### Prerequisites: <br>
- A recent version (2.36+) of the AWS Python SDK installed on your local workstation. <br>
- A minimal AWS credentials file (for example, ~/.aws/credentials) with the following contents
adjusted to your preferred region and output format.
```
[default]
 output = json
 region = us-east-1
 aws_access_key_id =
 aws_secret_access_key =
```
- You need to install two of the modules that fall outside the core Python distribution, specifically
beautifulsoup4 and requests-ntlm. <br>
-- pip install beautifulsoup4 <br>
-- pip install requests-ntlm <br>

#### Command syntax:
```
 awsrole.py username password <aws account number> <Role>
```
example 
```
awsrole.py user pass 123123123 Special-User-Group
```
