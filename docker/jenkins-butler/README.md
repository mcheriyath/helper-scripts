#### How to run
```
docker build -t butler .
docker run -v c:/Users/mcheriyath/Work/jenkins-backup:/app butler:latest /usr/local/bin/butler jobs export --server $JENKINS_IP:8080 --username mithun.cheriyath --password $JENKINSUSER_TOKEN
```
