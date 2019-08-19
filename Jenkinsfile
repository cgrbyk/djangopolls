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
           pysh 'python -m pip install  -r requirements.txt'
     }
   }
   stage('Test') {
        steps{
           sh 'tox'
        }
   }
 }
}