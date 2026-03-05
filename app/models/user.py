from app import db, bcrypt

class User(db.Model):
    # Table name in database
    __tablename__ = 'users'
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    # Relationship — one user has many expenses
    expenses = db.relationship('Expense', backref='user', lazy=True)
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        # Hash password before storing — never store plain text!
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        # Check if provided password matches stored hash
        return bcrypt.check_password_hash(self.password, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }