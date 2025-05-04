pipeline {
    agent any

    environment {
        IMAGE_NAME = "tharushaoff2001673/authService"
    }

    stages { 
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'firebase-cred', variable: 'FIREBASE_CREDENTIALS_FILE')]) {
                        sh '''
                            cp ${FIREBASE_CREDENTIALS_FILE} ecommerce-microservices.json
                            docker build --build-arg FIREBASE_CREDENTIALS_FILE=ecommerce-microservices.json -t ${IMAGE_NAME}:latest .
                            rm ecommerce-microservices.json
                        '''
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
