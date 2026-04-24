from core.models import Expense
from django.db.models import Sum
from django.utils import timezone

def get_dashboard_data(user):
    now = timezone.now()
    # Safely handle unauthenticated users or empty data
    if not user.is_authenticated:
        return {'transactions': [], 'total_spent': 0}
        
    transactions = Expense.objects.filter(user=user).order_by('-date')
    total_spent = transactions.filter(date__month=now.month).aggregate(Sum('amount'))['amount__sum'] or 0
    
    return {
        'transactions': transactions,
        'total_spent': total_spent,
    }
