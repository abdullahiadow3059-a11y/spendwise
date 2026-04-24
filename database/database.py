from core.models import Expense, Category, Budget, SavingsGoal
from django.db.models import Sum
from django.utils import timezone
from decimal import Decimal

def get_dashboard_context(user):
    """Fetches all data for index.html without SQL errors."""
    now = timezone.now()
    
    # 1. Total Spent this month
    total = Expense.objects.filter(
        user=user, 
        date__month=now.month, 
        date__year=now.year
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    # 2. Recent Transactions (Fixes line 211 in your index.html)
    transactions = Expense.objects.filter(user=user).select_related('category').order_by('-date')[:5]

    return {
        'total_spent': total,
        'transactions': transactions,
        'username': user.username
    }

def init_default_categories():
    """Run this to seed your categories safely."""
    defaults = ["Food & Drinks", "Transport", "Accommodation", "Education", "Entertainment"]
    for name in defaults:
        Category.objects.get_or_create(name=name)
