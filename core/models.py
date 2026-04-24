from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Expense(models.Model):
    # null=True and blank=True prevent the "non-nullable" build crash
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='expenses', 
        null=True, 
        blank=True
    )
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        db_table = 'core_expense'

    def __str__(self):
        return f"{self.category.name} - {self.amount}"
