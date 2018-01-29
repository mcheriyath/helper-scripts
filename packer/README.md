## Packer - Automating the creation of the base AMI 

This packer script, will take AWS base Ubuntu Server 14.04 LTS (HVM), SSD Volume Type - (us-east-1) ami-1081b807
* Encrypt the root volume 
* Install essential packages required
* At this time the image will only be available into us-east region. More destinations can be added under value: "ami_regions"

## Configuration info (packer.json)

In the config file you will find 3 sections
* <b>variables</b>, diff environment variables
* <b>builders</b>, where information on what to build
* <b>provisioners</b>, steps to execute on the images

## How to create the AMI

First make sure you have the packer executable installed on your box. This configuration file was created with with packer V0.12.1.
* https://www.packer.io/downloads.html

Make sure to have awscli installed on your box. with AWS_ACCESS_KEY and AWS_SECRET_KEY set in your environment variable or in your aws configure. Packer will first look in your env then look in the config store in your ~/.aws/. 
Your aws user need to have permission to create IAM (Tested with admin role). 

To create the packer.json file we need to run the script which pulls the required details and creates a packer json file from the template.
```bash
sh update-base-packer.sh
```

To create the AMI run the newly created json file with packer command as shown below
```bash
## packer build <your packer json file>
packer build base-packer.json
```
<br>
We can also get the above created Image ID from aws cli using the below command: <br>
For Base Image <br>
```bash
aws --profile default --region us-east-1 ec2 describe-images --owners self --filters Name=tag-value,Values=base-image --query 'Images[*].{ID:ImageId,Name:Name}' --output table
```

### Reference

[packer](https://www.packer.io)


