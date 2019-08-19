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
 }