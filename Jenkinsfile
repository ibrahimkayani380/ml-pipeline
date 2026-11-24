pipeline {
  agent any
  options { timeout(time: 8, unit: 'MINUTES') }
  environment { IMAGE = 'ibrahimkayani123/ml-app' }
  stages {
    stage('Build and Train') {
      steps { sh 'docker build --build-arg BUILD_COMMIT=$GIT_COMMIT -t $IMAGE:latest .' }
    }
    stage('Test') {
      steps {
        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
          sh 'docker run --rm $IMAGE:latest python -m pytest -q'
        }
      }
    }
    stage('Deploy') {
      steps {
        sh 'docker rm -f ml-app || true'
        sh 'docker run -d --name ml-app --restart unless-stopped -p 8000:8000 $IMAGE:latest'
        sh 'docker run --rm $IMAGE:latest cat artifacts/metrics.json > metrics.json'
      }
    }
    stage('Compare Accuracy') {
      steps {
        sh '''
          NEW=$(python3 -c "import json;print(json.load(open('metrics.json'))['accuracy'])" || echo unknown)
          OLD=$(cat $JENKINS_HOME/prev_acc.txt 2>/dev/null || echo none)
          echo "Previous accuracy: $OLD | New accuracy: $NEW" | tee result.txt
          echo $NEW > $JENKINS_HOME/prev_acc.txt
        '''
      }
    }
    stage('Push to Docker Hub') {
      steps {
        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
          sh 'docker push $IMAGE:latest'
        }
      }
    }
  }
  post {
    always {
      archiveArtifacts artifacts: 'metrics.json,result.txt', allowEmptyArchive: true
      script {
        def r = fileExists('result.txt') ? readFile('result.txt') : ''
        def m = fileExists('metrics.json') ? readFile('metrics.json') : 'Build failed, see console output'
        mail from: 'ibrahimkayani380@gmail.com',
             to: 'qasimalik@gmail.com',
             subject: "MIDTERM FA23-BDS-062 - Build #${env.BUILD_NUMBER}: ${currentBuild.currentResult}",
             body: r + "\n" + m
      }
    }
  }
}
