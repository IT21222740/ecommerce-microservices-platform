pipeline {
    agent any

    environment {
        IMAGE_NAME = "tharushaoff2001673/authservice"
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
                        // Copy the Firebase credentials file to the workspace
                        sh 'cp ${FIREBASE_CREDENTIALS_FILE} ecommerce-microservices.json'

                        // Build the Docker image and pass the credentials file as an argument
                        sh '''
                            docker build --build-arg FIREBASE_CREDENTIALS_FILE=ecommerce-microservices.json -t ${IMAGE_NAME}:latest .

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
