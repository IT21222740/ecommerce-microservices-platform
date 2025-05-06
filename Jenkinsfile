pipeline {
    agent any

    environment {
        IMAGE_NAME = "tharushaoff2001673/authServicev2" 
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

       
        stage('Build & Tag Docker Image') {
            steps {
                script {
                    withDockerRegistry(credentialsId: 'docker-cred', toolName: 'docker') {
                        sh "docker build -t ${IMAGE_NAME}:latest ."
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    docker.image("${IMAGE_NAME}:latest").inside {
                        sh "pytest"
                    }
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    withDockerRegistry(credentialsId: 'docker-cred', toolName: 'docker') {
                        sh "docker push ${IMAGE_NAME}:latest"
                    }
                }
            }
        }
    }
}
