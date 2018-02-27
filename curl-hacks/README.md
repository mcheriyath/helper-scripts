## To get stuffs from jenkins using curl


```bash
curl --silent http://jenkinshost/job/jobname/lastBuild/api/json | jq -r '.actions[].causes[]?.shortDescription? | select(.)'
```
Sample Output
```
Started by user Mithun
```
