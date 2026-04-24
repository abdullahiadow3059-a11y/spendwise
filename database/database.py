"""
Smart Student Expense Tracker - Database & Logic Module
Group 9 | Optimized for Production (Render)
"""

from core.models import Expense, Category, Budget, SavingsGoal
from django.contrib.auth.models import User
from django.db.models import Sum, F
from django.utils import timezone
from decimal import Decimal

# ──────────────────────────────────────────────
# 1. USER OPERATIONS (Replaces your old SQL registration)
# ──────────────────────────────────────────────

def register_user(full_name, username, password, email=None):
    """Creates a user with secure PBKDF2 hashing (replaces your plain-text SQL)."""
    if User.objects.filter(username=username).exists():
        return None
    user = User.objects.create_user(username=username, password=password, email=email)
    user.first_name = full_name
    user.save()
    return user

# ──────────────────────────────────────────────
# 2. EXPENSE & SUMMARY LOGIC (Replaces your JOIN queries)
# ──────────────────────────────────────────────

def get_monthly_summary(user):
    """
    Returns total spent per category for the current month.
    Equivalent to your old 'get_monthly_summary' SQL.
    """
    now = timezone.now()
    return (
        Expense.objects.filter(user=user, date__month=now.month, date__year=now.year)
        .values('category__name')
        .annotate(total_spent=Sum('amount'))
        .order_by('-total_spent')
    )

def get_total_spent(user):
    """Returns the grand total spent this month."""
    now = timezone.now()
    total = Expense.objects.filter(
        user=user, date__month=now.month, date__year=now.year
    ).aggregate(Sum('amount'))['amount__sum']
    return total or Decimal('0.00')

# ──────────────────────────────────────────────
# 3. BUDGET VS SPENDING (Replaces your complex SQL COALESCE)
# ──────────────────────────────────────────────

def get_budget_performance(user):
    """
    Compares monthly limits to actual spending.
    Matches your 'get_budget_vs_spending' logic.
    """
    now = timezone.now()
    budgets = Budget.objects.filter(user=user, month_year__month=now.month)
    
    results = []
    for b in budgets:
        spent = Expense.objects.filter(
            user=user, category=b.category, date__month=now.month
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        
        results.append({
            'category': b.category.name,
            'limit': b.monthly_limit,
            'spent': spent,
            'remaining': b.monthly_limit - spent,
            'percent': (spent / b.monthly_limit) * 100 if b.monthly_limit > 0 else 0
        })
    return results

# ──────────────────────────────────────────────
# 4. INITIALIZATION (Replaces your 'seed_default_categories')
# ──────────────────────────────────────────────

def init_default_categories():
    """Seeds the database with your group's specific categories."""
    defaults = [
        "Food & Drinks", "Transport", "Accommodation", 
        "Education", "Entertainment", "Healthcare", 
        "Clothing", "Airtime & Data", "Personal Care"
    ]
    for name in defaults:
        Category.objects.get_or_create(name=name)
