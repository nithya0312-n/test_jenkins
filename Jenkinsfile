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
            }
        }

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

        stage('Run Container') {
            steps {
                sh '''
                docker stop $CONTAINER_NAME || true
                docker rm   $CONTAINER_NAME || true

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
                echo "Cleaning up old Docker images (keeping latest ${KEEP_IMAGES})"

                IMAGES=$(docker images $IMAGE_NAME --format "{{.Repository}}:{{.Tag}} {{.CreatedAt}}" \
                         | grep build- \
                         | sort -rk2 \
                         | awk '{print $1}')

                COUNT=0
                for IMAGE in $IMAGES; do
                    COUNT=$((COUNT+1))
                    if [ $COUNT -le $KEEP_IMAGES ]; then
                        echo "Keeping $IMAGE"
                    else
                        echo "Removing $IMAGE"
                        docker rmi -f $IMAGE || true
                    fi
                done
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully (old images cleaned)"
        }
        failure {
            echo "❌ Pipeline failed"
        }
    }
}
