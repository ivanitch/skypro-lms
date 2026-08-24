from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Payment, User
from .permissions import IsUserOwner
from .serializers import (
    PaymentSerializer,
    UserProfileSerializer,
    UserRegisterSerializer,
)


class UserCreateAPIView(CreateAPIView):
    """Регистрация нового пользователя (доступна всем)."""
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]


class UserProfileAPIView(RetrieveUpdateAPIView):
    """Просмотр и редактирование профиля пользователя."""
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsUserOwner]

    def get_object(self):
        """
        Если параметр pk/id не передан в URL,
        автоматически возвращаем профиль текущего авторизованного пользователя.
        """
        if 'pk' not in self.kwargs and 'id' not in self.kwargs:
            return self.request.user
        return super().get_object()


class PaymentListAPIView(ListAPIView):
    """Список платежей (доступен только авторизованным пользователям)."""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date', 'amount']
