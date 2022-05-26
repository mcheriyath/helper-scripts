// Run from https://JenkinsURL/script

import jenkins.*
import jenkins.model.* 
import hudson.*
import hudson.model.*
def jenkinsCredentials = com.cloudbees.plugins.credentials.CredentialsProvider.lookupCredentials(
        com.cloudbees.plugins.credentials.Credentials.class,
        Jenkins.instance,
        null,
        null
);
for (creds in jenkinsCredentials) {
    println(jenkinsCredentials.id)
    }

for (creds in jenkinsCredentials) {
  if(creds.id == "Jenkins-Creds-ID"){
    println(creds.username)
    println(creds.password)
    }
}
