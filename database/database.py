from core.models import Expense, Category
from django.db.models import Sum
from django.utils import timezone

def get_dashboard_data(user):
    """Safely fetches transactions and totals for the dashboard."""
    now = timezone.now()
    
    if not user.is_authenticated:
        return {'total_spent': 0, 'transactions': []}

    # Fetch all expenses for this specific user
    transactions = Expense.objects.filter(user=user).order_by('-date')
    
    # Calculate total spent this month
    total_spent = transactions.filter(
        date__month=now.month, 
        date__year=now.year
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    return {
        'total_spent': total_spent,
        'transactions': transactions[:5], # Shows last 5
    }

def init_default_categories():
    """Seeds the database with common categories."""
    categories = ['Food', 'Transport', 'Rent', 'Education', 'Entertainment']
    for cat_name in categories:
        Category.objects.get_or_create(name=cat_name)











