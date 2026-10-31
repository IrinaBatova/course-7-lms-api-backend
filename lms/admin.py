from django.contrib import admin
from lms.models import Course, Lesson, CourseSubscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner')
    search_fields = ('title',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course', 'owner')
    search_fields = ('title',)

@admin.register(CourseSubscription)
class CourseSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course')  # Какие колонки показывать в таблице
    search_fields = ('course',)