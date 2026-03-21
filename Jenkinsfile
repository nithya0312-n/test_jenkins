pipeline {
    agent any

    stages {
        stage('Preparation') {
            steps {
                // Pull code from GitHub (replace with your repo)
		  withEnv(['GIT_SSH_COMMAND=ssh -o StrictHostKeyChecking=no']){
                  git branch: 'main', url: 'git@github.com:nithya0312-n/test_jenkins.git' 
           }}
        }

        stage('Run Script') {
            steps {
                // Run the Python file
                sh 'python3 file.py'
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
