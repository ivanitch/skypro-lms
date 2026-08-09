from django.contrib import admin

from lms.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    ordering = ('title',)
    list_display = ('title', 'description', 'preview')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    ordering = ('title',)
    list_display = ('title', 'preview', 'description', 'video_link', 'course')
