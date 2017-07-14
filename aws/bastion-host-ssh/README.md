Setup Bastion host
==================

Setting up bastion host on AWS-VPC public subnet to reach to all instances in a private subnet

## Contents

* [Setup Environment](#setup-environment)





```bash
  Host 10.220.*.*
    User ubuntu
    IdentityFile ~/.ssh/aws_keys/ec2deploykeasprod.key
    StrictHostKeyChecking no
    ForwardAgent yes
    ProxyCommand ssh -W %h:%p <your-user-name>@<bastion-prod-ip> -i ~/.ssh/ssh_keys/<personal-privatekey-filename>
```
