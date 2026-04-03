pipeline {
    agent any

    environment {
        IMAGE_NAME     = "nithyan12/python-jenkins-app"
        IMAGE_TAG      = "build-${BUILD_NUMBER}"
        CONTAINER_NAME = "python-app"
        KEEP_IMAGES    = 3
        DOCKERHUB_USER = "nithyan12"
        DOCKERHUB_REPO = "python-jenkins-app"
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

        stage('Cleanup Local Images (Keep Latest 3)') {
            steps {
                sh '''
                docker images $IMAGE_NAME --format "{{.Tag}}" \
                  | grep '^build-' \
                  | sort -t- -k2 -nr \
                  | tail -n +$((KEEP_IMAGES + 1)) \
                  | xargs -r -I {} docker rmi -f $IMAGE_NAME:{} || true

                docker images -f dangling=true -q | xargs -r docker rmi -f || true
                '''
            }
        }

        stage('Cleanup Docker Hub Tags (Keep Latest 3)') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-cred',
                    usernameVariable: 'HUB_USER',
                    passwordVariable: 'HUB_PASS'
                )]) {
                    sh '''
                    echo "Authenticating to Docker Hub API..."
                    TOKEN=$(curl -s -X POST https://hub.docker.com/v2/users/login/ \
                      -H "Content-Type: application/json" \
                      -d "{\"username\": \"$HUB_USER\", \"password\": \"$HUB_PASS\"}" \
                      | jq -r .token)

                    echo "Fetching tags from Docker Hub..."
                    TAGS=$(curl -s -H "Authorization: JWT $TOKEN" \
                      https://hub.docker.com/v2/repositories/$DOCKERHUB_USER/$DOCKERHUB_REPO/tags/?page_size=100 \
                      | jq -r '.results[].name' \
                      | grep '^build-' \
                      | sort -t- -k2 -nr)

                    COUNT=0
                    for TAG in $TAGS; do
                        COUNT=$((COUNT+1))
                        if [ $COUNT -le $KEEP_IMAGES ]; then
                            echo "Keeping Docker Hub tag: $TAG"
                        else
                            echo "Deleting Docker Hub tag: $TAG"
                            curl -s -X DELETE \
                              -H "Authorization: JWT $TOKEN" \
                              https://hub.docker.com/v2/repositories/$DOCKERHUB_USER/$DOCKERHUB_REPO/tags/$TAG/
                        fi
                    done
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ CI/CD pipeline completed successfully (local + Docker Hub cleanup done)"
        }
        failure {
            echo "❌ CI/CD pipeline failed"
        }
    }
}
