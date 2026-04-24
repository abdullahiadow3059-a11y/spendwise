from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from database.database import get_dashboard_data

def home(request):
    context = get_dashboard_data(request.user)
    return render(request, 'index.html', context)

@login_required
def add_expense(request):
    if request.method == "POST":
        amount = request.POST.get('amount')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        
        category = Category.objects.get(id=category_id)
        Expense.objects.create(
            user=request.user,
            category=category,
            amount=amount,
            description=description
        )
        return redirect('home')
        
    categories = Category.objects.all()
    return render(request, 'add_expense.html', {'categories': categories})
