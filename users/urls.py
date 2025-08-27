# users/urls.py

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterUserView, UserDetailView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('profile/', UserDetailView.as_view(), name='user-profile'),
]