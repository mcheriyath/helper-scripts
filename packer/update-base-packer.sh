#!/bin/bash
VPCID=$(aws --profile default ec2 describe-vpcs --filters Name=tag-value,Values=prod --query 'Vpcs[*].{ID:VpcId}' | grep ID| awk -F '"' '{print $4}')

SUBNETID=$(aws --profile default ec2 describe-subnets --filters Name=vpc-id,Values=$VPCID,Name=tag-value,Values=Public | grep SubnetId | awk -F '"' 'NR==1{print $4}')

cp base-packer.json.template base-packer.json
sed -i "s/VPCID/$VPCID/g" base-packer.json
sed -i "s/SUBNETID/$SUBNETID/g" base-packer.json
