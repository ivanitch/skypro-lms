from django.urls import path

from .apps import UsersConfig
from .views import UserProfileAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('profile/<int:pk>/', UserProfileAPIView.as_view(), name='user-profile'),
]
