import pytest

# ── AUTH TESTS ───────────────────────────────────────────

def test_register_success(client):
    """Test successful user registration"""
    response = client.post('/api/auth/register', json={
        'username': 'newuser',
        'email': 'new@test.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'User registered successfully!'

def test_register_duplicate_email(client):
    """Test registration with duplicate email fails"""
    client.post('/api/auth/register', json={
        'username': 'user1',
        'email': 'same@test.com',
        'password': 'password123'
    })
    response = client.post('/api/auth/register', json={
        'username': 'user2',
        'email': 'same@test.com',
        'password': 'password123'
    })
    assert response.status_code == 409

def test_login_success(client):
    """Test successful login returns token"""
    client.post('/api/auth/register', json={
        'username': 'loginuser',
        'email': 'login@test.com',
        'password': 'password123'
    })
    response = client.post('/api/auth/login', json={
        'email': 'login@test.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.get_json()

def test_login_invalid_password(client):
    """Test login with wrong password fails"""
    client.post('/api/auth/register', json={
        'username': 'user3',
        'email': 'user3@test.com',
        'password': 'correctpassword'
    })
    response = client.post('/api/auth/login', json={
        'email': 'user3@test.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401

# ── EXPENSE TESTS ────────────────────────────────────────

def test_add_expense_success(client, auth_token):
    """Test adding expense successfully"""
    response = client.post('/api/expenses/', 
        json={
            'title': 'Test Expense',
            'amount': 50.00,
            'category': 'Food'
        },
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 201
    assert response.get_json()['expense']['title'] == 'Test Expense'

def test_add_expense_missing_fields(client, auth_token):
    """Test adding expense with missing fields fails"""
    response = client.post('/api/expenses/',
        json={'title': 'Incomplete Expense'},
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 400

def test_get_expenses(client, auth_token):
    """Test getting all expenses"""
    # Add an expense first
    client.post('/api/expenses/',
        json={'title': 'Test', 'amount': 10.00, 'category': 'Food'},
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    response = client.get('/api/expenses/',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 200
    assert len(response.get_json()['expenses']) == 1

def test_get_summary(client, auth_token):
    """Test getting expense summary"""
    client.post('/api/expenses/',
        json={'title': 'Food Item', 'amount': 30.00, 'category': 'Food'},
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    response = client.get('/api/expenses/summary',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['total_amount'] == 30.00
    assert 'Food' in data['by_category']

def test_delete_expense(client, auth_token):
    """Test deleting an expense"""
    # Add expense first
    add_response = client.post('/api/expenses/',
        json={'title': 'To Delete', 'amount': 20.00, 'category': 'Other'},
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    expense_id = add_response.get_json()['expense']['id']
    
    # Delete it
    response = client.delete(f'/api/expenses/{expense_id}',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Expense deleted successfully!'

def test_unauthorized_access(client):
    """Test accessing expenses without token fails"""
    response = client.get('/api/expenses/')
    assert response.status_code == 401
