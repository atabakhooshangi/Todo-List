from django.contrib import admin
from .models import User, Task
from django.contrib.auth.models import Group


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'date_joined', 'is_active', 'is_superuser']
    list_editable = ['is_active', 'is_superuser']
    search_fields = ['username']
    list_filter = ['is_active', 'is_superuser']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'complete', 'created']
    list_editable = ['complete']
    list_filter = ['complete']
    search_fields = ['title', 'user']


admin.site.unregister(Group)
