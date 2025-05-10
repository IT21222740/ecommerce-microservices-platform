pipeline {
    agent any

    tools {
        jdk 'jdk 17'         
        maven 'maven 3'    
        sonar-scanner 
    }

    environment {
        IMAGE_NAME = "tharushaoff2001673/authservicev3"
        SONAR_TOKEN = credentials('sonarqube')
    }

    stages {
        // Checkout the code from SCM
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // Build and tag the Docker image
        stage('Build & Tag Docker Image') {
            steps {
                script {
                    withDockerRegistry(credentialsId: 'docker-cred', toolName: 'docker') {
                        sh "docker build -t ${IMAGE_NAME}:latest ."
                    }
                }
            }
        }

        // Run tests inside the Docker container
        stage('Run Tests') {
            steps {
                script {
                    docker.image("${IMAGE_NAME}:latest").inside {
                        sh "pytest"
                    }
                }
            }
        }

        // SonarQube Analysis
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube') {  // Ensure this matches the configuration name of your SonarQube server in Jenkins
                    sh '''
                        sonar-scanner \
                          -Dsonar.projectKey=authservice \
                          -Dsonar.sources=. \
                          -Dsonar.host.url=$SONAR_HOST_URL \
                          -Dsonar.login=$SONAR_TOKEN \
                          -Dsonar.python.coverage.reportPaths=coverage.xml
                    '''
                }
            }
        }

        // Push the Docker image to Docker Hub
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

    post {
        // Clean up or notify if the build failed
        failure {
            echo "The pipeline failed."
        }
        success {
            echo "The pipeline completed successfully."
        }
    }
}
