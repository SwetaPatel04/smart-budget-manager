from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app import db, bcrypt
from app.models.user import User

# Create blueprint
auth_bp = Blueprint('auth', __name__)

# ── REGISTER ─────────────────────────────────────────────
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Username, email and password are required'}), 400
    
    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already taken'}), 409
    
    # Create new user
    user = User(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    
    # Save to database
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User registered successfully!',
        'user': user.to_dict()
    }), 201


# ── LOGIN ────────────────────────────────────────────────
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    # Find user by email
    user = User.query.filter_by(email=data['email']).first()
    
    # Check if user exists and password is correct
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Create JWT access token
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        'message': 'Login successful!',
        'access_token': access_token,
        'user': user.to_dict()
    }), 200


# ── GET PROFILE ──────────────────────────────────────────
@auth_bp.route('/profile', methods=['GET'])
def profile():
    from flask_jwt_extended import jwt_required, get_jwt_identity
    
    @jwt_required()
    def get_profile():
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
    
    return get_profile()