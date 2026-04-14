from django.contrib import admin
from .models import MealLog, WaterLog, WeightLog

@admin.register(MealLog)
class MealLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'meal_type', 'food_name', 'calories', 'logged_at']

@admin.register(WaterLog)
class WaterLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'drink_type', 'amount_ml', 'logged_at']

@admin.register(WeightLog)
class WeightLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'weight_kg', 'logged_at']
