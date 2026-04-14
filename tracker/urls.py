from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('log/meal/', views.log_meal, name='log_meal'),
    path('log/water/', views.log_water, name='log_water'),
    path('log/weight/', views.log_weight, name='log_weight'),
    path('analyze/food/', views.analyze_food_image, name='analyze_food'),
    path('meals/history/', views.meal_history, name='meal_history'),
    path('meals/delete/<int:meal_id>/', views.delete_meal, name='delete_meal'),
]
