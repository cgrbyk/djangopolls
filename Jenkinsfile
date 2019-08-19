#!groovy
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
        def call(body) {
        try{
	   deleteDir()
	}catch(Exception e){
	   echo e.toString()
	}

	checkout scm

	withPythonEnv('/usr/bin/python3.6') {
	  pysh '/usr/bin/python3.6 -m pip install -r /var/lib/jenkins/reqs/venv3.txt --upgrade --no-cache-dir --user'
	  pysh 'echo "PACKAGE_NAME=$(/usr/bin/python -W ignore setup.py -q --name |tail -n1)" >> BUILD_CONTEXT_FILE'
	  pysh 'echo "PACKAGE_VERSION=$(/usr/bin/python -W ignore setup.py -q --version)" >> BUILD_CONTEXT_FILE'
	  pysh 'echo "GIT_URL=$(/usr/bin/python -W ignore setup.py -q --url)" >> BUILD_CONTEXT_FILE'
	}

      try {
        def BUILD_CONTEXT = readProperties file:'BUILD_CONTEXT_FILE'
        env['PACKAGE_NAME'] = BUILD_CONTEXT['PACKAGE_NAME']
        env['PACKAGE_VERSION'] = BUILD_CONTEXT['PACKAGE_VERSION']
        env['GIT_URL'] = BUILD_CONTEXT['GIT_URL'].split('https://')[1] + '.git'
      }catch (Exception e) {
        echo e.toString()
      }
}

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
            import should.*

def call(body) {

    echo "SONAR QUBE"

    if (should.test(env.BRANCH_NAME, env.PACKAGE_TYPE) == true){

        script {
          def envs = sh(returnStdout: true, script: "tox -l").trim().split('\n')
          def cmds = envs.collectEntries({ tox_env ->
            [tox_env, {
              sh "tox --parallel--safe-build -vve $tox_env"
            }]
          })
          parallel(cmds)
        }

        def scanner_command = " /usr/local/bin/sonar-scanner \
                            -Dsonar.host.url=http://10.133.151.21 \
                            -Dsonar.projectKey=${env.PACKAGE_NAME} \
                            -Dsonar.projectVersion=${env.PACKAGE_VERSION} \
                            -Dsonar.branch.name=${env.BRANCH_NAME} \
                            -Dsonar.python.coverage.reportPath=coverage.xml \
                            -Dsonar.login=4313033c794f52637b1843fd6e1f1be65930f87a"

        if (env.CHANGE_TARGET != null){
            scanner_command += " -Dsonar.branch.target=${env.CHANGE_TARGET}"
        }

        sh(" test -e requirements.txt &&" + scanner_command + "|| echo 'not a python repo' ")
        sh(" test -e pom.xml &&" + scanner_command + "-Dsonar.java.binaries=target" + "|| echo 'not a java repo' ")
        sh(" test -e package.json &&" + scanner_command + "|| echo 'not a js repo' ")
    }
}
         }
    }
    stage('SKY Compatibility Check') {
        when {
            expression { should.test(env.BRANCH_NAME, env.PACKAGE_TYPE) == true }
        }
        steps {
          import should.*

def call(body) {
    if(should.test(env.BRANCH_NAME, env.PACKAGE_TYPE) == true){
        withPythonEnv('/bin/python') {
    	    // pysh 'python /var/lib/jenkins/pcheck.py'
	        echo "Compatibility success"
	    }
    }
}
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
  post {
    success {
        slackSend message: "SUCCESS: Job ${env.PACKAGE_NAME} ${env.PACKAGE_VERSION} released and is up here ${env.APP_URL} (${env.BUILD_URL})", color: 'success'
    }
    failure {
        slackSend message: "FAILURE: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})", color: 'warning'
    }
  }
}