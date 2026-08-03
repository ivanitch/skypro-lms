from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import UserProfileSerializer


class UserProfileAPIView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
