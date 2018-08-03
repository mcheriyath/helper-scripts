#!/bin/bash
# lists all buckets along with their tags in the following format:
# bucket_name | { tag_name: tag_value }
# depends on AWS CLI and JQ

for bucket in `aws s3api list-buckets | jq .Buckets[].Name -r`; do 
    tags=$(aws s3api get-bucket-tagging --bucket $bucket | jq -c '.[][] | {(.Key): .Value}' | tr '\n' '\t')
    echo $bucket '|' $tags
done
