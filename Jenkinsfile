pipeline {
  agent any
 
  options {
    copyArtifactPermission(projectNames: 'horizon-container')
  }

  stages {
    stage('package') {
      environment {
        PBR_VERSION = "${env.BRANCH_NAME}"
      }
      steps {
        dir('dist') {
          deleteDir()
        }
        sh 'python setup.py sdist'
        sh 'find dist -type f -exec cp {} dist/horizon.tar.gz \\;'
        archiveArtifacts(artifacts: 'dist/horizon.tar.gz', onlyIfSuccessful: true)
      }
    }
  }

  post {
    success {
      build(
        job: 'service-containers/master', 
        parameters: [
          string(name: 'JOB_NAME', value: "${env.JOB_NAME}")
        ]
      )
    }
  }
}
