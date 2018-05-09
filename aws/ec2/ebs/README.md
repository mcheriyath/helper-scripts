## Create Role
```
aws iam create-role --role-name ebs-backup-worker --assume-role-policy-document file://snapshot-trust.json
```

## Attach policy
```
aws iam put-role-policy --role-name ebs-backup-worker --policy-name TakeSnapshots --policy-document file://snapshot-policy.json
```

Ref: https://serverlesscode.com/post/lambda-schedule-ebs-snapshot-backups/
