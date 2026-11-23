pipeline {
  agent any
  environment { IMAGE = 'ibrahimkayani123/ml-app' }
  stages {
    stage('Build and Train') {
      steps { sh 'docker build --build-arg BUILD_COMMIT=$GIT_COMMIT -t $IMAGE:latest .' }
    }
    stage('Test') {
      steps { sh 'docker run --rm $IMAGE:latest python -m pytest -q' }
    }
    stage('Deploy') {
      steps {
        sh 'docker rm -f ml-app || true'
        sh 'docker run -d --name ml-app --restart unless-stopped -p 8000:8000 $IMAGE:latest'
        sh 'docker run --rm $IMAGE:latest cat artifacts/metrics.json > metrics.json'
      }
    }
    stage('Push to Docker Hub') {
      steps {
        catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
          sh 'docker push $IMAGE:latest'
        }
      }
    }
  }
  post {
    always {
      archiveArtifacts artifacts: 'metrics.json', allowEmptyArchive: true
      script {
        def body = fileExists('metrics.json') ? readFile('metrics.json') : 'Build failed, see console output'
        mail from: 'ibrahimkayani380@gmail.com',
             to: 'qasimalik@gmail.com',
             subject: "MIDTERM FA23-BDS-062 - Build #${env.BUILD_NUMBER}: ${currentBuild.currentResult}",
             body: body
      }
    }
  }
}
