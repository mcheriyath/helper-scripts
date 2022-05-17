// alias jcli_env='java -jar ~/jenkins-cli.jar -s http://jenkins.url -auth jenkins_cli_user:user_token' 
// jcli_env groovy = < jenkins-user-creation.groovy testUser testPassword testEmail@testEmail.com

import hudson.model.*
import hudson.security.*
import hudson.tasks.Mailer
import java.util.*
import java.lang.reflect.*


def userId = args[0]
def password = args[1]
def email = args[2]
def fullname = args[3]

def instance = jenkins.model.Jenkins.instance
def existingUser = instance.securityRealm.allUsers.find {it.id == userId}

if (existingUser == null) {
    def user = instance.securityRealm.createAccount(userId, password)
    user.addProperty(new Mailer.UserProperty(email));
	  user.setFullName(fullname);
    instance.save()
} 
