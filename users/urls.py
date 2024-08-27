from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users import views

app_name = "users"

urlpatterns = [
    path("login/", views.UserLoginAPIView.as_view(), name="login-user")
]