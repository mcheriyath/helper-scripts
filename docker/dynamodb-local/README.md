
Start a DynamoDB Local instance
```
$ docker run -v "$PWD":/dynamodb_local_db -p 8000:8000 cnadiminti/dynamodb-local:latest
Initializing DynamoDB Local with the following configuration:
Port:    8000
InMemory:    false
DbPath:    /dynamodb_local_db
SharedDb:    true
shouldDelayTransientStatuses:    false
CorsParams:    *
```

This will add your current directory as a volume to the container and publish host port to container port.
Verify the DynamoDB Local instance with AWS CLI

Create a Table
```
$ aws dynamodb create-table --table-name myTable --attribute-definitions AttributeName=id,AttributeType=S --key-schema AttributeName=id,KeyType=HASH --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 --endpoint-url http://0.0.0.0:8000
```

List the Tables
```
$ aws dynamodb list-tables --endpoint-url http://0.0.0.0:8000 --output json
{
    "TableNames": [
        "myTable"
    ]
}
```
For complete list of available commands please refer AWS DynamoDB CLI.
Environment Variables
```
JAVA_OPTS
```
This optional environment variable can be used to set JVM options.

Example usage: 
```docker run -v "$PWD":/dynamodb_local_db -p 8000:8000 -e JAVA_OPTS='-Xmx256m' cnadiminti/dynamodb-local:latest```

DYNAMODB_PORT

This optional environment variable can be used to overwrite the default port (8000).

Example usage: 
```docker run -v "$PWD":/dynamodb_local_db -e DYNAMODB_PORT=443 -p 8000:443 cnadiminti/dynamodb-local:latest```
