from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'joined_date']
    search_fields = ['user__username', 'user__email', 'location']
    readonly_fields = ['joined_date']