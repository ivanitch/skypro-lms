from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentListAPIView, UserCreateAPIView, UserProfileAPIView, PaymentCreateAPIView

app_name = UsersConfig.name

urlpatterns = [
    # Авторизация и регистрация (доступны без токена)
    path('register/', UserCreateAPIView.as_view(), name='user-register'),
    path('login/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # Профиль и платежи
    path('profile/<int:pk>/', UserProfileAPIView.as_view(), name='user-profile'),
    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),
    path('payments/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
]
