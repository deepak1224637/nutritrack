from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ACTIVITY_CHOICES = [
        ('sedentary', 'Sedentary (Office/Desk Job)'),
        ('light', 'Light (Light Exercise 1-3 days/week)'),
        ('moderate', 'Moderate (Gym 3-5 days/week)'),
        ('active', 'Active (Heavy Exercise 6-7 days/week)'),
        ('athlete', 'Athlete (Professional)'),
    ]
    GOAL_CHOICES = [
        ('lose', 'Lose Weight'),
        ('maintain', 'Maintain Weight'),
        ('gain', 'Gain Muscle'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    height_cm = models.FloatField(null=True, blank=True, help_text="Height in cm")
    weight_kg = models.FloatField(null=True, blank=True, help_text="Weight in kg")
    work_type = models.CharField(max_length=100, blank=True, help_text="e.g. Software Engineer, Teacher")
    gym_schedule = models.CharField(max_length=200, blank=True, help_text="e.g. Mon/Wed/Fri 6am-7am")
    address = models.TextField(blank=True)
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_CHOICES, default='moderate')
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES, default='maintain')
    daily_water_goal_ml = models.PositiveIntegerField(default=2500)
    daily_calorie_goal = models.PositiveIntegerField(default=2000)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}'s Profile"

    @property
    def bmi(self):
        if self.height_cm and self.weight_kg:
            h = self.height_cm / 100
            return round(self.weight_kg / (h * h), 1)
        return None

    @property
    def bmi_category(self):
        bmi = self.bmi
        if bmi is None:
            return "Unknown"
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"
