from django.contrib import admin

from lms.models import Course, Lesson
from users.models import Payment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    ordering = ('title',)
    list_display = ('title', 'description', 'preview')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    ordering = ('title',)
    list_display = ('title', 'preview', 'description', 'video_link', 'course')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    ordering = ('amount',)
    list_display = ('id', 'amount', 'user', 'paid_course', 'paid_lesson')
