creds_json=$(export AWS_ACCESS_KEY_ID=$(env | grep PERSONAL_AWS_TOKEN | awk -F= '{print $2}'); export AWS_SECRET_ACCESS_KEY=$(env | grep PERSONAL_AWS_SECRET | awk -F= '{print $2}'); aws sts get-session-token)

export AWS_ACCESS_KEY_ID=$(echo "$creds_json" | jq .Credentials.AccessKeyId |tr -d '"')
export AWS_SECRET_ACCESS_KEY=$(echo "$creds_json" | jq .Credentials.SecretAccessKey| tr -d '"')
export AWS_SESSION_TOKEN=$(echo "$creds_json" | jq .Credentials.SessionToken|tr -d '"')

> ~/.aws/credentials

echo -e "[personal]" | tee -a ~/.aws/credentials
echo -e "aws_access_key_id=${AWS_ACCESS_KEY_ID}" | tee -a ~/.aws/credentials
echo -e "aws_secret_access_key=${AWS_SECRET_ACCESS_KEY}" | tee -a ~/.aws/credentials
echo -e "aws_session_token=${AWS_SESSION_TOKEN}" | tee -a ~/.aws/credentials
