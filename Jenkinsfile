pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out code from GitHub...'
                git branch: 'main',
                    url: 'https://github.com/SwetaPatel04/smart-budget-manager.git'
                echo 'Code checkout complete! ✅'
            }
        }

        stage('Install Python Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh '''
                    pip install flask --break-system-packages
                    pip install flask-sqlalchemy --break-system-packages
                    pip install flask-jwt-extended --break-system-packages
                    pip install flask-bcrypt --break-system-packages
                    pip install scikit-learn --break-system-packages
                    pip install pandas --break-system-packages
                    pip install numpy --break-system-packages
                    pip install python-dotenv --break-system-packages
                    pip install pytest --break-system-packages
                    pip install pytest-flask --break-system-packages
                '''
                echo 'Python dependencies installed! ✅'
            }
        }

        stage('Run Pytest Tests') {
            steps {
                echo 'Running pytest tests...'
                sh 'python -m pytest tests/test_api.py -v'
                echo 'Pytest tests complete! ✅'
            }
        }

        stage('Install Playwright') {
            steps {
                echo 'Installing Playwright...'
                sh '''
                    npm install @playwright/test
                    npx playwright install chromium
                '''
                echo 'Playwright installed! ✅'
            }
        }

        stage('Run Playwright Tests') {
            steps {
                echo 'Running Playwright E2E tests...'
                sh 'npx playwright test --project=chromium'
                echo 'Playwright tests complete! ✅'
            }
        }

        stage('Results') {
            steps {
                echo 'All tests passed! Pipeline complete! ✅'
            }
        }
    }

    post {
        success {
            echo '🎉 Pipeline succeeded! All 20 tests passed!'
        }
        failure {
            echo '❌ Pipeline failed! Check the logs!'
        }
    }
}
