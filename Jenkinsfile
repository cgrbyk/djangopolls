#!groovy
@Library('sky-jenkins-utils') _
pipeline {
 agent any
 options { skipDefaultCheckout() }
 environment {
   PACKAGE_TYPE = 'Project'
   APP_URL = 'http://product-ipam-ui-common.apps.skyz.tech/'
 }
 stages {
   stage('Prepare virtualenv with tools') {
     steps {
       drmPreparePy3Venv()
     }
   }
   stage('Install project requirements') {
     steps {
         withPythonEnv('/bin/python3.6') {
           pysh 'python -m pip install  -r requirements.txt'
         }
     }
   }
   stage('Test') {
       when {
           expression { should.test(env.BRANCH_NAME, env.PACKAGE_TYPE) == true }
       }
        steps{
           drmTestAndAnalysis()
        }
   }
   stage('SKY Compatibility Check') {
       when {
           expression { should.test(env.BRANCH_NAME, env.PACKAGE_TYPE) == true }
       }
       steps {
         drmCompatibilityCheck()
       }
   }
   // Dockerization
   stage('Dockerization') {
     when {
       expression { should.pack(env.BRANCH_NAME, env.PACKAGE_TYPE) == true }
     }
     steps {
       sh "docker build -t registry.sekomy.com/${env.PACKAGE_NAME}:${env.PACKAGE_VERSION} . --no-cache"
       sh "docker push registry.sekomy.com/${env.PACKAGE_NAME}:${env.PACKAGE_VERSION}"
       sh "docker tag registry.sekomy.com/${env.PACKAGE_NAME}:${env.PACKAGE_VERSION} registry.sekomy.com/${env.PACKAGE_NAME}:latest"
       sh "docker push registry.sekomy.com/${env.PACKAGE_NAME}:latest"
     }
   }
   stage('Staging Deploy') {
       when {
           expression { should.deploy(env.BRANCH_NAME, env.PACKAGE_TYPE) == true }
       }
       steps {
           drmStagingDeploy()
       }
   }
 }
}