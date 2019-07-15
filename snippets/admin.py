from django.contrib import admin

# Register your models here.
from snippets.models import CourseUsers

@admin.register(CourseUsers)
class CourseUsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'owner')
