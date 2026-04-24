from core.models import Expense
from django.db.models import Sum
from django.utils import timezone
from decimal import Decimal

def get_dashboard_data(user):
    """Calculates all stats for index.html without errors."""
    now = timezone.now()
    
    # Safety check: if user isn't logged in, return zeros
    if not user.is_authenticated:
        return {
            'total_spent': Decimal('0.00'),
            'transactions': [],
            'remaining_budget': Decimal('0.00'),
            'savings_goal_pct': 0
        }

    # Fetch transactions (Fixes line 211 error)
    transactions = Expense.objects.filter(user=user).order_by('-date')
    
    # Calculate Total Spent for the current month
    total = transactions.filter(
        date__month=now.month, 
        date__year=now.year
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    return {
        'total_spent': total,
        'transactions': transactions[:10],  # Show latest 10
        'remaining_budget': Decimal('5000.00') - total, # Example static budget
        'savings_goal_pct': 15 # Example static goal
    }
