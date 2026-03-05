from app import db
from datetime import datetime

class Expense(db.Model):
    # Table name in database
    __tablename__ = 'expenses'
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(255))
    
    # Foreign key — links expense to user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'amount': self.amount,
            'category': self.category,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S'),
            'description': self.description,
            'user_id': self.user_id
        }