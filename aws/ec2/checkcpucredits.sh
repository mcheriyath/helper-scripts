#!/bin/bash
## https://forums.aws.amazon.com/thread.jspa?messageID=556357
## To generate load
## sudo yum -y --enablerepo=epel install python-psutil python-matplotlib numpy python-twisted-core
## curl -O https://raw.githubusercontent.com/GaetanoCarlucci/CPULoadGenerator/master/CPULoadGenerator.py
## python CPULoadGenerator.py -l 0.9 -d 300
#set -x
if [ -z $MYINSTANCE ]; then
 # if running in EC2, get the instanceId from metadata service
 export IID=http://169.254.169.254/latest/dynamic/instance-identity/document
 curl --connect-timeout 1 -s $IID -so /dev/null
 exitval=$?
 # if curl failed, assume we are not running in EC2
 if [ $exitval -gt 0 ]; then
  echo "Usage: MYINSTANCE=i-abcd1234 $0 "
  echo "This script also requires the AWS CLI http://aws.amazon.com/cli/"
  exit 1
 else
  $(curl -s $IID | grep ': "' | sed -e 's/^[ \t]*/ export /' -e 's/ : /=/' -e 's/,//' |tr -d '"')
  export AWS_DEFAULT_REGION=$region
  MYINSTANCE=$instanceId
 fi
fi
 
if [ -z $MYFREQUENCY ]; then
 MYFREQUENCY=300
fi
 
if [ -z $START ]; then
 START=`date +'%Y-%m-%dT%H:%M:59Z' --utc -d '60 minutes ago' `
fi
if [ -z $END ]; then
 END=`date +'%Y-%m-%dT%H:%M:59Z' --utc `
fi
 
echo "example timestamps:"
echo "export END=`date +'%Y-%m-%dT%H:%M:59Z' --utc -d '60 minutes ago'`"
echo "export END=\`date +'%Y-%m-%dT%H:%M:59Z' --utc -d '60 minutes ago'\`"
 
echo "setting up the API call"
echo "MYFREQUENCY=$MYFREQUENCY"
echo "START=$START"
echo "END=$END"
MYDIMENSION="{\"Name\":\"InstanceId\",\"Value\":\"$MYINSTANCE\"}"
echo "MYDIMENSION=$MYDIMENSION"
 
# http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/viewing_metrics_with_cloudwatch.html
for m in CPUCreditBalance CPUCreditUsage; do
  echo "m=$m"
  aws cloudwatch get-metric-statistics --namespace 'AWS/EC2' --region $AWS_DEFAULT_REGION \
    --period $MYFREQUENCY --start-time $START --end-time $END \
    --metric-name $m --dimensions $MYDIMENSION --statistic Average \
    --query 'Datapoints[*].[Timestamp,Average,Unit]' --output text | sort
done
