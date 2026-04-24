from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from database.database import get_dashboard_data

def home(request):
    # This fetches the data prepared in database.py
    context = get_dashboard_data(request.user)
    return render(request, 'index.html', context)
