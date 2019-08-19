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
            sh 'python manage.py migrate'
        }
     }
    }
   stage('Tox'){
        steps{
            withPythonEnv('python3') {
                sh 'apt-get install python3.6'
                sh 'apt-get install python3.7'
                sh 'tox'
            }
        }
   }
 }
}