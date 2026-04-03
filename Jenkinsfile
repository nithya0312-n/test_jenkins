pipeline {
    agent any

    environment {
        IMAGE_NAME = "nithyan12/python-jenkins-app"
        IMAGE_TAG  = "latest"
        CREDS_ID   = "dockerhub-cred"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
                sh 'ls -l'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t $IMAGE_NAME:$IMAGE_TAG .
                '''
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: CREDS_ID,
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    '''
                }
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                sh '''
                docker push $IMAGE_NAME:$IMAGE_TAG
                '''
            }
        }

        stage('Verify Image Locally') {
            steps {
                sh '''
                docker rmi $IMAGE_NAME:$IMAGE_TAG || true
                docker pull $IMAGE_NAME:$IMAGE_TAG
                '''
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker stop python-app || true
                docker rm python-app || true

                docker run -d --name python-app $IMAGE_NAME:$IMAGE_TAG
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Image built, pushed, pulled, and container started successfully"
        }
        failure {
            echo "❌ Pipeline failed"
        }
    }
}
