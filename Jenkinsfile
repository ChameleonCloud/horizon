pipeline {
  agent any

  options {
    copyArtifactPermission(projectNames: 'horizon*')
  }

  stages {
    stage('package') {
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
}
