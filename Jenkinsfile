pipeline {
    agent any

    stages {
        stage('Preparation') {
            steps {
                // Pull code from GitHub (replace with your repo)
                git 'https://github.com/your-username/your-python-repo.git'
            }
        }

        stage('Run Script') {
            steps {
                // Run the Python file
                sh 'python3 your_script.py'
            }
        }

        stage('Results') {
            steps {
                // Archive the log file created by the Python script
                archiveArtifacts artifacts: 'pipeline_output.log', allowEmptyArchive: true
            }
        }
    }
}

