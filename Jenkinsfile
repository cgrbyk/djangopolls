#!groovy
//@Library('sky-jenkins-utils') _
pipeline {
 agent any
 options { skipDefaultCheckout() }
 environment {
   PACKAGE_TYPE = 'Project'
   APP_URL = 'http://product-ipam-ui-common.apps.skyz.tech/'
 }
 stages {
   stage('Install project requirements') {
     steps {
         withPythonEnv('python') {
           pysh 'pip install virtualenv'
           pysh 'python -m pip install  -r requirements.txt'
         }
     }
   }
   stage('Test') {
        steps{
           withPythonEnv('/python') {
           pysh 'tox'
         }
        }
   }
 }
}