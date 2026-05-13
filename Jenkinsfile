pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "hvardhan21/server-health-api"
        DOCKER_TAG = "latest"
        AWS_REGION = "ap-south-1"
        EKS_CLUSTER = "server-health-cluster"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Cloning repository...'
                checkout scm
            }
        }

        stage('Test') {
            steps {
                echo 'Running unit tests...'
                sh '''
                    pip3 install fastapi uvicorn psutil httpx pytest --break-system-packages --quiet
                    python3 -m pytest tests/test_main.py -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing image to Docker Hub...'
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                    sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                echo 'Deploying to EKS...'
                withCredentials([
                    string(credentialsId: 'aws-access-key-id', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-secret-access-key', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh '''
                        export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                        export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
                        aws eks update-kubeconfig --region ap-south-1 --name server-health-cluster
                        kubectl apply -f k8s/deployment.yaml
                        kubectl apply -f k8s/service.yaml
                        kubectl rollout status deployment/server-health-api
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed! API live on EKS.'
        }
        failure {
            echo 'Pipeline failed. Check logs above.'
        }
    }
}