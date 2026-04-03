pipeline {
    agent any

    environment {
        IMAGE_NAME     = "nithyan12/python-jenkins-app"
        IMAGE_TAG      = "build-${BUILD_NUMBER}"
        CONTAINER_NAME = "python-app"
        KEEP_IMAGES    = 3
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
                echo "Building new Docker image..."
                docker build -t $IMAGE_NAME:$IMAGE_TAG .
                docker tag $IMAGE_NAME:$IMAGE_TAG $IMAGE_NAME:latest
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
                echo "Pushing images to Docker Hub..."
                docker push $IMAGE_NAME:$IMAGE_TAG
                docker push $IMAGE_NAME:latest
                '''
            }
        }

        stage('Run Container') {
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

        stage('Cleanup Old Docker Images (Keep Latest 3)') {
            steps {
                sh '''
                echo "🧹 Cleaning up Docker images for $IMAGE_NAME"

                # 1️⃣ Remove old build-* images, keep latest 3 by build number
                docker images $IMAGE_NAME --format "{{.Tag}}" \
                  | grep '^build-' \
                  | sort -t- -k2 -nr \
                  | tail -n +$((KEEP_IMAGES + 1)) \
                  | xargs -r -I {} docker rmi -f $IMAGE_NAME:{} || true

                # 2️⃣ Remove dangling <none> images
                docker images -f "dangling=true" -q \
                  | xargs -r docker rmi -f || true

                # 3️⃣ Remove old images with incorrect repository name
                docker images python-jenkins-app -q \
                  | xargs -r docker rmi -f || true

                echo "✅ Docker image cleanup completed"
                '''
            }
        }
    }

    post {
        success {
            echo "✅ CI/CD pipeline completed successfully"
        }
        failure {
            echo "❌ CI/CD pipeline failed"
        }
    }
}
