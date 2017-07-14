Setup Bastion host
==================

Setting up bastion host on AWS-VPC public subnet to reach to all instances in a private subnet

## Contents

* [Setup Environment](#setup-environment)





```bash
  Host 192.168.*.*    
  User ubuntu    
  IdentityFile ~/bastion.pem 
  StrictHostKeyChecking no    
  ForwardAgent yes    
  ProxyCommand ssh -W %h:%p joe@50.23.28.92 -i ~/.ssh/joe.key
```
