from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.expense import Expense

# Create blueprint
expenses_bp = Blueprint('expenses', __name__)

# ── ADD EXPENSE ──────────────────────────────────────────
@expenses_bp.route('/', methods=['POST'])
@jwt_required()
def add_expense():
    data = request.get_json()
    user_id = get_jwt_identity()
    
    # Validate required fields
    if not data or not data.get('title') or not data.get('amount') or not data.get('category'):
        return jsonify({'error': 'Title, amount and category are required'}), 400
    
    # Validate amount is positive number
    if float(data['amount']) <= 0:
        return jsonify({'error': 'Amount must be greater than 0'}), 400
    
    # Create new expense
    expense = Expense(
        title=data['title'],
        amount=float(data['amount']),
        category=data['category'],
        description=data.get('description', ''),
        user_id=user_id
    )
    
    # Save to database
    db.session.add(expense)
    db.session.commit()
    
    return jsonify({
        'message': 'Expense added successfully!',
        'expense': expense.to_dict()
    }), 201


# ── GET ALL EXPENSES ─────────────────────────────────────
@expenses_bp.route('/', methods=['GET'])
@jwt_required()
def get_expenses():
    user_id = get_jwt_identity()
    
    # Get optional filters from query params
    category = request.args.get('category')
    
    # Query expenses for current user
    query = Expense.query.filter_by(user_id=user_id)
    
    # Apply category filter if provided
    if category:
        query = query.filter_by(category=category)
    
    # Order by date descending
    expenses = query.order_by(Expense.date.desc()).all()
    
    return jsonify({
        'expenses': [e.to_dict() for e in expenses],
        'total': len(expenses)
    }), 200


# ── GET SINGLE EXPENSE ───────────────────────────────────
@expenses_bp.route('/<int:expense_id>', methods=['GET'])
@jwt_required()
def get_expense(expense_id):
    user_id = get_jwt_identity()
    
    # Find expense and verify it belongs to current user
    expense = Expense.query.filter_by(
        id=expense_id,
        user_id=user_id
    ).first()
    
    if not expense:
        return jsonify({'error': 'Expense not found'}), 404
    
    return jsonify({'expense': expense.to_dict()}), 200


# ── UPDATE EXPENSE ───────────────────────────────────────
@expenses_bp.route('/<int:expense_id>', methods=['PUT'])
@jwt_required()
def update_expense(expense_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Find expense and verify it belongs to current user
    expense = Expense.query.filter_by(
        id=expense_id,
        user_id=user_id
    ).first()
    
    if not expense:
        return jsonify({'error': 'Expense not found'}), 404
    
    # Update fields if provided
    if data.get('title'):
        expense.title = data['title']
    if data.get('amount'):
        expense.amount = float(data['amount'])
    if data.get('category'):
        expense.category = data['category']
    if data.get('description'):
        expense.description = data['description']
    
    # Save changes
    db.session.commit()
    
    return jsonify({
        'message': 'Expense updated successfully!',
        'expense': expense.to_dict()
    }), 200


# ── DELETE EXPENSE ───────────────────────────────────────
@expenses_bp.route('/<int:expense_id>', methods=['DELETE'])
@jwt_required()
def delete_expense(expense_id):
    user_id = get_jwt_identity()
    
    # Find expense and verify it belongs to current user
    expense = Expense.query.filter_by(
        id=expense_id,
        user_id=user_id
    ).first()
    
    if not expense:
        return jsonify({'error': 'Expense not found'}), 404
    
    # Delete from database
    db.session.delete(expense)
    db.session.commit()
    
    return jsonify({'message': 'Expense deleted successfully!'}), 200


# ── GET SUMMARY ──────────────────────────────────────────
@expenses_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_summary():
    user_id = get_jwt_identity()
    
    # Get all expenses for current user
    expenses = Expense.query.filter_by(user_id=user_id).all()
    
    if not expenses:
        return jsonify({'message': 'No expenses found'}), 200
    
    # Calculate total spending
    total = sum(e.amount for e in expenses)
    
    # Calculate spending by category
    by_category = {}
    for expense in expenses:
        if expense.category not in by_category:
            by_category[expense.category] = 0
        by_category[expense.category] += expense.amount
    
    return jsonify({
        'total_expenses': len(expenses),
        'total_amount': round(total, 2),
        'by_category': by_category
    }), 200