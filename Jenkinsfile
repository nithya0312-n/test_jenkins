pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo "Source code checked out automatically by Jenkins"
                sh 'ls -l'
            }
        }

        stage('Run Python Script') {
            steps {
                sh '''
                python3 --version
                python3 file.py
                '''
            }
        }

        stage('Archive Results') {
            steps {
                archiveArtifacts artifacts: 'pipeline_output.log', fingerprint: true
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully"
        }
        failure {
            echo "❌ Pipeline failed"
        }
    }
}
