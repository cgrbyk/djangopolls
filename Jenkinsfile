#!groovy
pipeline {
 agent any
 options { skipDefaultCheckout() }
 stages {
   stage('Install project requirements') {
     steps {
        checkout scm
         withPythonEnv('python3') {
            sh 'python --version'
            sh 'python -m pip install  -r requirements.txt'
         }
     }
   }
   stage('Test') {
     steps{
        withPythonEnv('python3') {
            sh 'docker-compose up'
            sh 'python manage.py test'
        }
     }
   }
 }
}