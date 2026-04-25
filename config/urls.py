from django.contrib import admin
from django.urls import path, include # Make sure include is imported

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')), # Your app urls
    path('accounts/', include('django.contrib.auth.urls')), # <--- ADD THIS LINE
]
