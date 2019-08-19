#!groovy
pipeline {
 agent any
 options { skipDefaultCheckout() }
 stages {
   stage('Install project requirements') {
     steps {
        checkout scm
            sh 'python --version'
         withPythonEnv('python') {
            sh 'python -m pip install  -r requirements.txt'
         }
     }
   }
   stage('Test') {
     steps{
        withPythonEnv('python') {
            sh 'tox'
        }
     }
   }
 }
}