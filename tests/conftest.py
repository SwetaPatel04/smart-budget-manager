import pytest
from app import create_app, db

@pytest.fixture
def app():
    # Create app with testing config
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'JWT_SECRET_KEY': 'test-jwt-secret'
    })
    
    # Create tables
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    # Create test client
    return app.test_client()

@pytest.fixture
def auth_token(client):
    # Register and login to get token
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@test.com',
        'password': 'password123'
    })
    
    response = client.post('/api/auth/login', json={
        'email': 'test@test.com',
        'password': 'password123'
    })
    
    return response.get_json()['access_token']
