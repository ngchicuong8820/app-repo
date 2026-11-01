pipeline {
    agent any

    options {
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
    }

    environment {
        // Chỉ dùng một image tổng theo cách bạn cấu hình
        DOCKER_IMAGE = "ngchicuong8820/lab1-app"
        IMAGE_TAG = "v${env.BUILD_NUMBER}"
        GITOPS_REPO = "https://github.com/ngchicuong8820/lab1-gitops.git"
        APP_URL = "http://host.docker.internal:8501" 
        
        DOCKER_CRED_ID = 'docker-creds'
        GITHUB_CRED_ID = 'github-token'
    }

    stages {
        stage('1. Checkout Code') {
            steps { checkout scm }
        }

        stage('1.5. Prepare Tools') {
            steps {
                sh '''
                mkdir -p ./bin
                echo "Đang tải Trivy CLI..."
                curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b ./bin
                
                echo "Đang tải Docker CLI..."
                ARCH=$(uname -m)
                if [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
                    curl -sSL -o docker.tgz https://download.docker.com/linux/static/stable/aarch64/docker-24.0.9.tgz
                else
                    curl -sSL -o docker.tgz https://download.docker.com/linux/static/stable/x86_64/docker-24.0.9.tgz
                fi
                tar -xzf docker.tgz
                mv docker/docker ./bin/
                chmod +x ./bin/docker
                '''
            }
        }

        stage('2. Code & IaC Security (SAST/SCA)') {
            failFast true
            parallel {
                stage('SAST & SCA (Trivy)') {
                    steps {
                        sh './bin/trivy fs ./ --scanners vuln,secret,misconfig --exit-code 0'
                    }
                }
                stage('IaC Scan') {
                    steps {
                        sh './bin/trivy config ./ --exit-code 0 --severity HIGH,CRITICAL'
                    }
                }
            }
        }

        stage('3. Build Image') {
            steps { 
                sh "./bin/docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} ." 
            }
        }

        stage('4. Container Security') {
            steps {
                sh "./bin/trivy image --exit-code 0 --severity HIGH,CRITICAL ${DOCKER_IMAGE}:${IMAGE_TAG}"
            }
        }

        stage('5. Push Registry') {
            steps {
                withCredentials([usernamePassword(credentialsId: env.DOCKER_CRED_ID, passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                    sh """
                    echo \$DOCKER_PASS | ./bin/docker login -u \$DOCKER_USER --password-stdin
                    ./bin/docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
                    """
                }
            }
        }

        stage('6. Update GitOps Manifest') {
            steps {
                withCredentials([string(credentialsId: env.GITHUB_CRED_ID, variable: 'GIT_TOKEN')]) {
                    sh """
                    # Xóa thư mục tạm nếu có và clone repo GITOPS RIÊNG BIỆT
                    rm -rf gitops-temp
                    git clone https://oauth2:\${GIT_TOKEN}@github.com/ngchicuong8820/lab1-gitops.git gitops-temp
                    cd gitops-temp

                    # Thay thế tag mới trong file manifest (Lưu ý: Không còn tiền tố gitops-repo/ nữa)
                    sed -i "s|image: ${DOCKER_IMAGE}:.*|image: ${DOCKER_IMAGE}:${IMAGE_TAG}|g" apps/lab1-app.yaml

                    # Commit và push thay đổi lên repo GitOps riêng
                    git config user.name "Jenkins DevSecOps Bot"
                    git config user.email "jenkins@lab.local"
                    git add apps/lab1-app.yaml
                    git commit -m "chore: release ${IMAGE_TAG} [skip ci]" || echo "Không có thay đổi nào để commit"
                    git push origin HEAD:main
                    """
                }
            }
        }

        stage('7. Dynamic Application Security Testing (DAST)') {
            steps {
                sh """
                echo "Quét DAST vào ứng dụng frontend..."
                ./bin/docker run --rm -t owasp/zap2docker-stable zap-baseline.py -t ${APP_URL} -I || true
                """
            }
        }
    }
    
    post {
        always {
            sh 'rm -rf ./*'
        }
    }
}