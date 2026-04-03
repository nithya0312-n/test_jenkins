pipeline {
    agent any

    environment {
        IMAGE_NAME = "nithyan12/python-jenkins-app"
        IMAGE_TAG  = "build-${BUILD_NUMBER}"
        CONTAINER_NAME = "python-app"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t $IMAGE_NAME:$IMAGE_TAG .
                docker tag  $IMAGE_NAME:$IMAGE_TAG $IMAGE_NAME:latest
                '''
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-cred',
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
                docker push $IMAGE_NAME:latest
                '''
            }
        }

        stage('Run Container from Image') {
            steps {
                sh '''
                echo "Stopping old container if it exists..."
                docker stop $CONTAINER_NAME || true
                docker rm   $CONTAINER_NAME || true

                echo "Running new container..."
                docker run -d \
                  --name $CONTAINER_NAME \
                  --restart unless-stopped \
                  $IMAGE_NAME:$IMAGE_TAG
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Image built, pushed, and container is running"
        }
        failure {
            echo "❌ Pipeline failed"
        }
    }
}
