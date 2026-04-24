from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

# 1. CATEGORIES (Pre-seeded via Django admin or migrations)
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

# 2. EXPENSES (With Indexing for High Performance)
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # This makes the "Recent Transactions" list load instantly
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'date']),
        ]

    def __str__(self):
        return f"{self.user.username} | {self.description} | KSh {self.amount}"

# 3. BUDGETS (With Unique Constraints)
class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    monthly_limit = models.DecimalField(max_digits=12, decimal_places=2)
    # Store the first day of the month (e.g., 2024-05-01) to represent the whole month
    month_year = models.DateField() 

    class Meta:
        unique_together = ('user', 'category', 'month_year')

    def __str__(self):
        return f"{self.user.username} - {self.category.name} ({self.month_year.strftime('%B %Y')})"

# 4. SAVINGS GOALS (With Progress Logic)
class SavingsGoal(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_name = models.CharField(max_length=200)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_savings = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    deadline = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    @property
    def progress_pct(self):
        if self.target_amount <= 0: return 0
        return min(int((self.current_savings / self.target_amount) * 100), 100)

    def __str__(self):
        return f"{self.goal_name} ({self.progress_pct}%)"
