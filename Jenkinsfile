pipeline {
  agent any
  environment { IMAGE = 'ibrahimkayani123/ml-app' }
  stages {
    stage('Build and Train') {
      steps { sh 'docker build --build-arg GIT_SHA=$GIT_COMMIT -t $IMAGE:latest .' }
    }
    stage('Compare Accuracy') {
      steps {
        sh '''
          docker run --rm $IMAGE:latest cat metrics.json > metrics.json
          NEW=$(python3 -c "import json;print(json.load(open('metrics.json'))['accuracy'])")
          OLD=$(cat $JENKINS_HOME/prev_acc.txt 2>/dev/null || echo none)
          echo "Previous accuracy: $OLD | New accuracy: $NEW" | tee result.txt
          echo $NEW > $JENKINS_HOME/prev_acc.txt
        '''
      }
    }
    stage('Push to Docker Hub') {
      steps { sh 'docker push $IMAGE:latest' }
    }
    stage('Deploy') {
      steps {
        sh 'docker rm -f ml-app || true'
        sh 'docker run -d --name ml-app -p 8000:8000 $IMAGE:latest'
      }
    }
  }
  post {
    always {
      archiveArtifacts artifacts: 'metrics.json,result.txt', allowEmptyArchive: true
      script {
        try {
          def body = fileExists('result.txt') ? readFile('result.txt') : 'Build failed'
          mail from: 'ibrahimkayani380@gmail.com', to: 'qasimalik@gmail.com',
               subject: "MIDTERM FA23-BDS-062 - Build #${env.BUILD_NUMBER}: ${currentBuild.currentResult}",
               body: body
        } catch (e) {
          echo "Email not sent: ${e}"
        }
      }
    }
  }
}
