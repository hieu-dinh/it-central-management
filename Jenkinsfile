pipeline {
    echo "Hello World! Jenkins pipeline here"
    echo "This is the build number ${BUILD_NUMBER}"
//     agent any
//     environment {
//         REGISTRY = 'hieudinh13'
//         IMAGE = 'it-central-management'
//         SERVER_IP = '192.168.170.50'
//         USER_ADMIN = 'debian'

//     }
//     stages {
//         stage('Build') {
//             steps {
//                 sh 'docker build -t $REGISTRY/$IMAGE:${BUILD_NUMBER} .'
//                 sh 'docker tag $REGISTRY/$IMAGE:${BUILD_NUMBER} $REGISTRY/$IMAGE:latest'
//             }
//         }
//         stage("Push") {
//             steps {
//                 withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'USERNAME', passwordVariable: 'PASS')]) {
//                     sh 'echo $PASS | docker login -u $USERNAME --password-stdin'
//                 }
//                 sh 'docker push $REGISTRY/$IMAGE:${BUILD_NUMBER}'
//                 sh 'docker push $REGISTRY/$IMAGE:latest'
//             }
//         }
//         stage("Deploy") {
//             steps {
//                 sshagent(credentials:['icm'] ) {
//                     sh "scp docker-compose.yml $USER_ADMIN@$SERVER_IP:/opt/inventory-management/docker-compose.yml" 
//                 }
//                 sshagent(credentials: ['icm']) {
//                     sh """
// ssh -A -o StrictHostKeyChecking=no -tt $USER_ADMIN@$SERVER_IP <<EOF
// docker-compose -f /opt/it-central-management/docker-compose.yml pull > /dev/null
// docker-compose -f /opt/it-central-management/docker-compose.yml up -d > /dev/null
// exit
// EOF
//                     """
//                 }
//             }
//         }
//     }
//     post {
//         always {
//             sh 'docker rmi $REGISTRY/$IMAGE:${BUILD_NUMBER} || true'
//             sh 'docker rmi $REGISTRY/$IMAGE:latest || true'
//             sh 'docker image prune -f'
//             sh 'docker logout'
//         }
//     }
}