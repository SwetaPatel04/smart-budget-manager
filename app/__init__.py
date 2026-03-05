from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from config import Config

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    # Create Flask app
    app = Flask(__name__)
    
    # Load config
    app.config.from_object(Config)
    
    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    # Register blueprints (routes)
    from app.routes.auth import auth_bp
    from app.routes.expenses import expenses_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(expenses_bp, url_prefix='/api/expenses')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
