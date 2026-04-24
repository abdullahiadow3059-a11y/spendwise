from django.shortcuts import render
from django.db.models import Sum
from .models import Expense
from datetime import datetime

def home(request):
    # 1. Get all expenses for the table
    all_expenses = Expense.objects.all().order_by('-date')

    # 2. Calculate Total Spent (This Month)
    current_month = datetime.now().month
    total_spent = Expense.objects.filter(date__month=current_month).aggregate(Sum('amount'))['amount__sum'] or 0

    # 3. Calculate Budget Logic (Assuming a static budget for now)
    # In a full app, you'd pull this from a Budget model
    monthly_budget = 20000 
    remaining_budget = monthly_budget - float(total_spent)
    budget_usage_pct = (float(total_spent) / monthly_budget) * 100 if monthly_budget > 0 else 0

    # 4. Dummy data for Savings (Since your models.py is missing the Savings class)
    savings_goals = [
        {'name': 'New Laptop', 'icon': '💻', 'percent': 45, 'current': 15000, 'target': 35000},
        {'name': 'Emergency Fund', 'icon': '🛡️', 'percent': 80, 'current': 8000, 'target': 10000},
    ]

    context = {
        'transactions': all_expenses,
        'total_spent': total_spent,
        'remaining_budget': remaining_budget,
        'budget_usage_pct': budget_usage_pct,
        'savings_goals': savings_goals,
        'spend_vs_last_month': -5.2, # Hardcoded example
    }

    return render(request, 'index.html', context)
