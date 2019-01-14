## Connecting redshift cluster from Lambda using IAM temporary credentials
This specific lambda was written to run on python3.6

#### Pre-requisite
- Access to AWS Lambda and redshift services
- A redshift admin lambda role
- Existing redshift cluster with master/admin user created
- Existing redshift cluster with table called [sales and some values in it](https://docs.aws.amazon.com/redshift/latest/gsg/rs-gsg-create-sample-db.html)


#### Package installation
```
mkdir packages
cd packages
pip install -r requirements --target .
```

#### Lambda creation
Continuation from above steps:
```
zip -r9 ../function.zip .
cd ../
zip -g function.zip function.py
aws lambda create-function --function-name sampleredshiftconnection --environment Variables="{REDSHIFT_CLUSTER=string,REDSHIFT_ENDPOINT=string,REDSHIFT_PORT=string,REDSHIFT_USER=string,REDSHIFT_PASSWD=password,REDSHIFT_DATABASE=string}" --zip-file fileb://function.zip --handler lambda_handler --runtime python3.6 --role arn:aws:iam::209281865882:role/acct-managed/redshift_admin_lambda_role
```

#### Update Lambda
Make changes to functions.py, zip it and upload.
```
zip -g functions.zip functions.py
aws lambda update-function-code --function-name sampleredshiftconnection --zip-file fileb://function.zip
```
