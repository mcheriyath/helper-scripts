## Jenkins related

#### Migrate plugins from one jenkins server to another

Install [Butler](https://github.com/mlabouardy/butler)

- Export plugins
```
./butler plugins export --server jenkins-server1:8080 --username mithun.cheriyath --password $JENKINSPASS
```
- Import plugins
```
./butler plugins import --server jenkins-server2:8080 --username mithun.cheriyath --password $JENKINSPASS
```

#### Migrate plugins from one jenkins server to another
- Export Jobs
```
./butler jobs export --server jenkins-server1:8080 --username mithun.cheriyath --password $JENKINSPASS
```
- Import Jobs
```
./butler jobs import --server jenkins-server2:8080 --username mithun.cheriyath --password $JENKINSPASS
```

#### Migrate views from one jenkins server to another along with the jobs
- Export Views
```
java -jar jenkins-cli.jar -s https://jenkins-server1/ get-view "Tech Reg" --username mithun.cheriyath --password $JENKINSPASS > ci-views/ViewName.xml
```
- Import Views
```
 java -jar jenkins-cli.jar -s http://jenkins-server2/ create-view "Tech Reg" --username mithun.cheriyath --password $JENKINSPASS < ci-views/ViewName.xml
```
