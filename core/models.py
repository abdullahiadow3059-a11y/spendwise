from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

# 1. CATEGORIES
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

# 2. EXPENSES (Corrected with User Link)
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        indexes = [models.Index(fields=['user', 'date'])]

# 3. BUDGETS
class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    monthly_limit = models.DecimalField(max_digits=12, decimal_places=2)
    month_year = models.DateField() # Set to 1st of every month

    class Meta:
        unique_together = ('user', 'category', 'month_year')

# 4. SAVINGS GOALS
class SavingsGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_name = models.CharField(max_length=200)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_savings = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, default='active')
