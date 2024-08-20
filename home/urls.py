# project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('admin/', admin.site.urls),  # Default Django admin route
    path('user/', include('home.routers.user')),  # Include URLs from app_name/router/user.py
    path('ctv/', include('home.routers.ctv')),  # Include URLs from app_name/router/user.py
]
