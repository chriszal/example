pipeline {
    agent any
    environment {
        REGISTRY_HOST = 'relevium-dev.hua.gr:443'
        REG_PASS= "${REGISTRY_PASSWORD}"
        WH_PASS= "${WEBHOOK_PASSWORD}"
        jsonInputApi='{"image":"relevium-dev.hua.gr:443/falcon-api:v1.0", "database":["mongodb","influxdb"],"port":["8081"]}'
        jsonInputReceiver='{"image":"relevium-dev.hua.gr:443/receiver:v1.0", "database":["mongodb","influxdb"],"port":["8000"]}'
    }
    stages {
        stage('Docker Login') {
            steps {
                echo "connecting to local image registry"
                sh 'docker login relevium-dev.hua.gr:443 --username relevium -p ${REG_PASS}'
            }
        }
        stage('create Docker images') {
            steps {
                echo "building docker image version v1.0} ..."
                sh 'docker build -f Dockerfile.api -t relevium-dev.hua.gr:443/falcon-api:v1.0 .'
                dir('receiver') {
                    sh 'docker build -f Dockerfile.receiver -t relevium-dev.hua.gr:443/receiver:v1.0 .'
                }
            }
        }
        stage('tag and push Docker images to registry') {
            steps {
                echo "pushing version v1.0 to registry at ${REGISTRY_HOST} ..."
                sh 'docker push relevium-dev.hua.gr:443/falcon-api:v1.0'
                sh 'docker push relevium-dev.hua.gr:443/receiver:v1.0'
            }
        }
        stage('deploy Docker containers') {
            steps {
                echo "sending request to deploy webhook for api"
                sh "curl -X POST https://relevium-dev.hua.gr/deploy/ -H 'Content-Type: application/json' --user 'relevium:${WH_PASS}' -d '${jsonInputApi}'"
                echo "sending request to deploy webhook for receiver"
                sh "curl -X POST https://relevium-dev.hua.gr/deploy/ -H 'Content-Type: application/json' --user 'relevium:${WH_PASS}' -d '${jsonInputReceiver}'"
            }
        }
    }
}
