import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from datetime import datetime, timedelta

class SpendingPredictor:
    
    def __init__(self):
        self.model = LinearRegression()
        self.is_trained = False
    
    def prepare_data(self, expenses):
        """Convert expenses to ML features"""
        if not expenses:
            return None, None
        
        # Convert expenses to numpy arrays
        amounts = []
        days = []
        
        # Get reference date (first expense date)
        first_date = expenses[-1].date
        
        for expense in expenses:
            # Calculate days since first expense
            delta = (expense.date - first_date).days
            days.append(delta)
            amounts.append(expense.amount)
        
        X = np.array(days).reshape(-1, 1)
        y = np.array(amounts)
        
        return X, y
    
    def train(self, expenses):
        """Train model on user's expense history"""
        if len(expenses) < 2:
            self.is_trained = False
            return False
        
        X, y = self.prepare_data(expenses)
        
        if X is None:
            return False
        
        # Train linear regression model
        self.model.fit(X, y)
        self.is_trained = True
        return True
    
    def predict_next_month(self, expenses):
        """Predict total spending for next month"""
        if not expenses:
            return None
        
        # Calculate average daily spending
        total_amount = sum(e.amount for e in expenses)
        
        if not expenses:
            return 0
        
        # Get date range
        dates = [e.date for e in expenses]
        date_range = (max(dates) - min(dates)).days + 1
        
        if date_range == 0:
            date_range = 1
        
        # Calculate daily average
        daily_average = total_amount / date_range
        
        # Predict next 30 days
        predicted_monthly = daily_average * 30
        
        return round(predicted_monthly, 2)
    
    def get_category_insights(self, expenses):
        """Get spending insights by category"""
        if not expenses:
            return {}
        
        # Calculate spending by category
        category_totals = {}
        category_counts = {}
        
        for expense in expenses:
            cat = expense.category
            if cat not in category_totals:
                category_totals[cat] = 0
                category_counts[cat] = 0
            category_totals[cat] += expense.amount
            category_counts[cat] += 1
        
        # Calculate total spending
        total = sum(category_totals.values())
        
        # Build insights
        insights = {}
        for category, amount in category_totals.items():
            insights[category] = {
                'total': round(amount, 2),
                'count': category_counts[category],
                'percentage': round((amount / total) * 100, 1),
                'average_per_expense': round(amount / category_counts[category], 2)
            }
        
        return insights
    
    def get_budget_recommendations(self, expenses):
        """Generate budget recommendations"""
        recommendations = []
        
        if not expenses:
            return recommendations
        
        insights = self.get_category_insights(expenses)
        total = sum(e.amount for e in expenses)
        
        for category, data in insights.items():
            percentage = data['percentage']
            
            # Flag high spending categories
            if percentage > 40:
                recommendations.append({
                    'category': category,
                    'type': 'warning',
                    'message': f'{category} is {percentage}% of your spending — consider reducing!'
                })
            elif percentage > 25:
                recommendations.append({
                    'category': category,
                    'type': 'info',
                    'message': f'{category} is {percentage}% of your spending — monitor closely.'
                })
            else:
                recommendations.append({
                    'category': category,
                    'type': 'good',
                    'message': f'{category} spending looks healthy at {percentage}%.'
                })
        
        return recommendations


# Create a single instance
predictor = SpendingPredictor()