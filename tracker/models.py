from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class MealLog(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meals')
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    image = models.ImageField(upload_to='meals/%Y/%m/%d/', blank=True, null=True)
    food_name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    calories = models.FloatField(default=0)
    protein_g = models.FloatField(default=0)
    carbs_g = models.FloatField(default=0)
    fat_g = models.FloatField(default=0)
    fiber_g = models.FloatField(default=0)
    sugar_g = models.FloatField(default=0)
    sodium_mg = models.FloatField(default=0)
    ai_analysis = models.TextField(blank=True)
    logged_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-logged_at']

    def __str__(self):
        return f"{self.user.username} - {self.meal_type} ({self.logged_at.date()})"

class WaterLog(models.Model):
    DRINK_TYPES = [
        ('water', 'Water'),
        ('milk', 'Milk'),
        ('juice', 'Juice'),
        ('tea', 'Tea'),
        ('coffee', 'Coffee'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='water_logs')
    drink_type = models.CharField(max_length=20, choices=DRINK_TYPES, default='water')
    amount_ml = models.PositiveIntegerField()
    logged_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-logged_at']

    def __str__(self):
        return f"{self.user.username} - {self.drink_type} {self.amount_ml}ml"

class WeightLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weight_logs')
    weight_kg = models.FloatField()
    note = models.CharField(max_length=200, blank=True)
    logged_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-logged_at']
