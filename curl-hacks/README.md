## To get stuffs from jenkins using curl

#### Get the username who triggered the build
```bash
curl --silent http://jenkinshost/job/jobname/lastBuild/api/json | jq -r '.actions[].causes[]?.shortDescription? | select(.)'
```
Sample Output
```
Started by user Mithun
```

#### Get the last successful build number
```
curl -s http://jenkinshost/job/jobname/lastSuccessfulBuild/api/json |  jq -r '.actions[].buildsByBranchName | select(. != null)' | grep buildNumber | awk -F, '{print $1}' | awk '{print $2}'
```
Sample Output
```
10
```
