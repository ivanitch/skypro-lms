from django.urls import path
from rest_framework.routers import DefaultRouter
from .apps import LmsConfig
from .views import (
    CourseViewSet,
    LessonListAPIView, LessonCreateAPIView,
    LessonRetrieveAPIView, LessonUpdateAPIView, LessonDestroyAPIView
)

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    # Lesson URLs
    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-get'),
    path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
] + router.urls
