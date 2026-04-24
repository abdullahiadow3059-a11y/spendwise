from django.db import models

class Expense(models.Model):
    name = models.CharField(max_length=100) # This is the description
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.amount}"

class Budget(models.Model):
    category = models.CharField(max_length=50)
    monthly_limit = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.CharField(max_length=7) # Format: YYYY-MM

class SavingsGoal(models.Model):
    name = models.CharField(max_length=100)
    target = models.DecimalField(max_digits=10, decimal_places=2)
    current = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    icon = models.CharField(max_length=10, default="🎯")
