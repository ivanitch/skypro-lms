from rest_framework import serializers

from .models import Course, Lesson, Subscription
from .validators import YoutubeUrlValidator


class LessonSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [YoutubeUrlValidator(field='video_link')]

    def get_course(self, obj):
        return obj.course.title


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user if 'request' in self.context else None
        if user and user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False
