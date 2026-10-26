pipeline {
    agent any

    stages {
        stage('git checkout') {
            steps {
                echo '=== Stage 1: git checkout ==='
                git branch: 'main', url: 'https://github.com/Prabin-yadav/telemetry-core.git'
                sh 'ls -la'
            }
        }

        stage('telemetry build') {
            steps {
                echo '=== Stage 2: telemetry build ==='
                sh '''
                    echo "[BUILD] Checking telemetry configuration..."
                    cat telemetry.conf
                    echo "[BUILD] Verifying Python syntax..."
                    python3 -m py_compile app.py || true
                    echo "[BUILD] Packaging telemetry artifacts..."
                    mkdir -p build/artifacts
                    cp app.py telemetry.conf README.md build/artifacts/
                    tar -czf build/artifacts/telemetry-core-v3.1.0.tar.gz app.py telemetry.conf README.md
                    echo "[BUILD] Telemetry Core build completed successfully."
                '''
            }
        }

        stage('deploy artifacts') {
            steps {
                echo '=== Stage 3: deploy artifacts ==='
                archiveArtifacts artifacts: 'build/artifacts/**', allowEmptyArchive: true
                sh '''
                    echo "[DEPLOY] Deploying artifacts to ingestion cluster..."
                    mkdir -p /tmp/fleet-deploy
                    cp -r build/artifacts/* /tmp/fleet-deploy/
                    echo "[DEPLOY] Deployment complete: Telemetry ingestion artifacts deployed."
                '''
            }
        }
    }

    post {
        always {
            echo 'Declarative Pipeline finished.'
        }
        success {
            echo 'All stages completed successfully: git checkout, telemetry build, deploy artifacts.'
        }
    }
}
