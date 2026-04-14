from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum
from datetime import date, timedelta
import json, base64

from django.conf import settings
from .models import MealLog, WaterLog, WeightLog
from accounts.models import UserProfile


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'tracker/landing.html')


@login_required
def dashboard(request):
    today = date.today()
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    meals_today = MealLog.objects.filter(user=request.user, logged_at__date=today)
    water_today = WaterLog.objects.filter(user=request.user, logged_at__date=today)

    totals = meals_today.aggregate(
        cal=Sum('calories'), prot=Sum('protein_g'),
        carb=Sum('carbs_g'), fat=Sum('fat_g')
    )
    total_cal = round(totals['cal'] or 0)
    total_prot = round(totals['prot'] or 0)
    total_carb = round(totals['carb'] or 0)
    total_fat = round(totals['fat'] or 0)
    total_water = water_today.aggregate(total=Sum('amount_ml'))['total'] or 0

    weekly_data = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        day_meals = MealLog.objects.filter(user=request.user, logged_at__date=d)
        day_cal = day_meals.aggregate(cal=Sum('calories'))['cal'] or 0
        weekly_data.append({'date': d.strftime('%a'), 'calories': round(day_cal)})

    meal_breakdown = {}
    for mtype in ['breakfast', 'lunch', 'dinner', 'snack']:
        meal_meals = meals_today.filter(meal_type=mtype)
        meal_cal = meal_meals.aggregate(cal=Sum('calories'))['cal'] or 0
        meal_breakdown[mtype] = round(meal_cal)

    recent_water = water_today.order_by('-logged_at')[:10]
    weight_logs = WeightLog.objects.filter(user=request.user).order_by('-logged_at')[:7]

    return render(request, 'tracker/dashboard.html', {
        'profile': profile,
        'today': today,
        'meals_today': meals_today,
        'total_cal': total_cal,
        'total_prot': total_prot,
        'total_carb': total_carb,
        'total_fat': total_fat,
        'total_water': total_water,
        'weekly_data': json.dumps(weekly_data),
        'meal_breakdown': json.dumps(meal_breakdown),
        'recent_water': recent_water,
        'weight_logs': weight_logs,
        'calorie_goal': profile.daily_calorie_goal,
        'water_goal': profile.daily_water_goal_ml,
        'cal_percent': min(100, round((total_cal / (profile.daily_calorie_goal or 2000)) * 100)),
        'water_percent': min(100, round((total_water / (profile.daily_water_goal_ml or 2500)) * 100)),
    })


@login_required
def log_meal(request):
    if request.method == 'POST':
        meal_type = request.POST.get('meal_type', 'breakfast')
        food_name = request.POST.get('food_name', '')
        image = request.FILES.get('image')
        manual_cal = request.POST.get('calories', '')
        manual_prot = request.POST.get('protein_g', '')
        manual_carb = request.POST.get('carbs_g', '')
        manual_fat = request.POST.get('fat_g', '')

        meal = MealLog(user=request.user, meal_type=meal_type, food_name=food_name)

        if image:
            meal.image = image
            meal.calories = float(request.POST.get('calories') or 0)
            meal.protein_g = float(request.POST.get('protein_g') or 0)
            meal.carbs_g = float(request.POST.get('carbs_g') or 0)
            meal.fat_g = float(request.POST.get('fat_g') or 0)
            meal.save()
            messages.success(request, f'{meal_type.title()} logged successfully!')
        elif manual_cal:
            meal.calories = float(manual_cal or 0)
            meal.protein_g = float(manual_prot or 0)
            meal.carbs_g = float(manual_carb or 0)
            meal.fat_g = float(manual_fat or 0)
            meal.save()
            messages.success(request, f'{meal_type.title()} logged successfully!')
        else:
            meal.save()
            messages.success(request, 'Meal logged!')

        return redirect('dashboard')
    return render(request, 'tracker/log_meal.html')


@login_required
def analyze_food_image(request):
    """Analyze food image using Google Gemini AI"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    image_file = request.FILES.get('image')
    if not image_file:
        return JsonResponse({'error': 'No image provided'}, status=400)

    try:
        api_key = settings.GEMINI_API_KEY

        # Demo mode agar key nahi hai
        if not api_key:
            return JsonResponse({
                'success': True,
                'food_name': 'Demo Food',
                'calories': 350,
                'protein_g': 15,
                'carbs_g': 45,
                'fat_g': 12,
                'fiber_g': 5,
                'sugar_g': 8,
                'sodium_mg': 420,
                'analysis': 'Demo mode: Add GEMINI_API_KEY to use real AI analysis.',
            })

        # Google Gemini AI se analyze karo
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)

        image_bytes = image_file.read()
        content_type = image_file.content_type or 'image/jpeg'

        prompt = """Analyze this food image and provide nutritional information.
Respond ONLY with a valid JSON object. No markdown, no backticks, no extra text.
Use exactly these keys:
{
  "food_name": "name of food",
  "calories": 0,
  "protein_g": 0,
  "carbs_g": 0,
  "fat_g": 0,
  "fiber_g": 0,
  "sugar_g": 0,
  "sodium_mg": 0,
  "analysis": "brief description of the food"
}
All numeric values must be numbers not strings. Estimate for typical serving size visible in image."""

        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type=content_type),
                prompt
            ]
        )

        text = response.text.strip()
        text = text.replace('```json', '').replace('```', '').strip()

        nutrition = json.loads(text)
        nutrition['success'] = True
        return JsonResponse(nutrition)

    except json.JSONDecodeError as e:
        return JsonResponse({'error': f'AI response parse error: {str(e)}'}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def log_water(request):
    if request.method == 'POST':
        drink_type = request.POST.get('drink_type', 'water')
        amount = int(request.POST.get('amount_ml', 250))
        WaterLog.objects.create(user=request.user, drink_type=drink_type, amount_ml=amount)
        return JsonResponse({'success': True, 'amount': amount, 'drink_type': drink_type})
    return JsonResponse({'error': 'POST required'}, status=405)


@login_required
def log_weight(request):
    if request.method == 'POST':
        weight = float(request.POST.get('weight_kg', 0))
        note = request.POST.get('note', '')
        if weight > 0:
            WeightLog.objects.create(user=request.user, weight_kg=weight, note=note)
            profile = request.user.profile
            profile.weight_kg = weight
            profile.save()
            messages.success(request, f'Weight {weight}kg logged!')
        return redirect('dashboard')


@login_required
def meal_history(request):
    meals = MealLog.objects.filter(user=request.user).order_by('-logged_at')
    return render(request, 'tracker/meal_history.html', {'meals': meals})


@login_required
def delete_meal(request, meal_id):
    meal = get_object_or_404(MealLog, id=meal_id, user=request.user)
    meal.delete()
    messages.success(request, 'Meal deleted.')
    return redirect('dashboard')
