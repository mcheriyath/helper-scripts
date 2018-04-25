Sample commands
```
aws route53 list-resource-record-sets --hosted-zone-id <ZONEID> --query "ResourceRecordSets[?ResourceRecords[?Value == 'IPtoSearch']].Name" --output=text
```
