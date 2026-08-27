from rest_framework import serializers

from .models import Course, Lesson
from .validators import YoutubeUrlValidator


class LessonSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = '__all__',
        validators = [YoutubeUrlValidator(field='video_link')]

    def get_course(self, obj):
        return obj.course.title


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, obj):
        return obj.lessons.count()


