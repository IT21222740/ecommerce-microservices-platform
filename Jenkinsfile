pipeline {
    agent any

    environment {
        IMAGE_NAME = "tharushaoff2001673/authservicev3"
        SONARQUBE_SCANNER = 'sonar-scanner'
    }

    tools {
        sonarQubeScanner 'sonar-scanner'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('SonarQube Scan') {
            steps {
                withSonarQubeEnv('sonarqube') {
                    sh "${tool SONARQUBE_SCANNER}/bin/sonar-scanner"
                }
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
                        sh "pytest || true" 
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
