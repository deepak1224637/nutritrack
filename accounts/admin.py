from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'age', 'weight_kg', 'height_cm', 'goal', 'activity_level']
    search_fields = ['user__username', 'user__email']
