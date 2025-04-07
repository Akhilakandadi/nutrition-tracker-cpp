# Standard Django imports
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.timezone import now

# Custom library import
from nutrition_tracker_lib import NutritionTracker

# Local app imports
from .forms import SignUpForm, UserProfileForm, WaterIntakeForm, WaterGoalForm, WeightLogForm
from .models import Meal, UserProfile, WaterIntake, WaterGoal, WeightLog

# Views

@login_required
def meal_list(request):
    """Display a list of meals with a summary using NutritionTracker."""
    tracker = NutritionTracker()
    meals = Meal.objects.filter(user=request.user)
    
    # Sync database meals with tracker
    for meal in meals:
        tracker.log_meal(
            food_name=meal.name,
            calories=meal.calories,
            protein=meal.protein,
            carbs=meal.carbs,
            fats=meal.fats
        )
    
    summary = tracker.get_meal_summary()
    return render(request, 'nutrition/meal_list.html', {
        'meals': meals,
        'total_calories': summary['total_calories'],
        'total_meals': summary['total_meals']
    })

@login_required
def add_meal(request):
    """Add a new meal using NutritionTracker to fetch and log data."""
    tracker = NutritionTracker()
    if request.method == "POST":
        food_name = request.POST['food_name']
        nutrition_data = tracker.fetch_nutrition_data(food_name)

        if nutrition_data:
            if "add_to_meal" in request.POST:
                # Save to database
                Meal.objects.create(
                    user=request.user,
                    name=nutrition_data['name'],
                    calories=nutrition_data['calories'],
                    protein=nutrition_data['protein'],
                    carbs=nutrition_data['carbs'],
                    fats=nutrition_data['fats']
                )
                # Log to tracker
                tracker.log_meal(
                    food_name=nutrition_data['name'],
                    calories=nutrition_data['calories'],
                    protein=nutrition_data['protein'],
                    carbs=nutrition_data['carbs'],
                    fats=nutrition_data['fats']
                )
                return redirect('meal_list')
            return render(request, 'nutrition/add_meal.html', {'nutrition_data': nutrition_data})
        else:
            return render(request, 'nutrition/add_meal.html', {"error": "Food not found"})
    
    return render(request, 'nutrition/add_meal.html')

@login_required
def delete_meal(request, meal_id):
    """Delete a meal entry for the logged-in user."""
    meal = Meal.objects.get(id=meal_id, user=request.user)
    meal.delete()
    return redirect('meal_list')

def signup(request):
    """Handle user registration and automatic login."""
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            
            profile, created = UserProfile.objects.get_or_create(user=user, defaults={**profile_form.cleaned_data})
            if created:
                messages.success(request, "Your account has been created and you're now logged in.")
            else:
                messages.warning(request, "UserProfile already existed, updated instead.")

            login(request, user)
            return redirect('meal_list')
        else:
            messages.error(request, "Please fix the errors below.")
    
    else:
        user_form = SignUpForm()
        profile_form = UserProfileForm()

    return render(request, 'registration/signup.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def profile_info(request):
    """Display the user's profile information."""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'nutrition/profile_info.html', {'profile': profile})

@login_required
def edit_profile(request):
    """Allow users to edit their profile information."""
    profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_info')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'nutrition/edit_profile.html', {'form': form})

@login_required
def track_water(request):
    """Track water intake using NutritionTracker."""
    tracker = NutritionTracker()
    water_intakes = WaterIntake.objects.filter(user=request.user, date=now().date())
    
    # Sync database with tracker
    for intake in water_intakes:
        tracker.log_water(intake.amount)
    
    water_summary = tracker.get_water_summary()
    total_water = water_summary['total_water_ml']
    goal, _ = WaterGoal.objects.get_or_create(user=request.user)
    daily_goal = goal.daily_goal
    progress = min((total_water / daily_goal) * 100, 100)

    if total_water < daily_goal * 0.5:
        messages.warning(request, "You're behind on your water intake! Stay hydrated. 💧")

    if request.method == "POST":
        if "update_goal" in request.POST:
            goal_form = WaterGoalForm(request.POST, instance=goal)
            if goal_form.is_valid():
                goal_form.save()
                messages.success(request, "Water intake goal updated! 🎯")
                return redirect('track_water')
        else:
            form = WaterIntakeForm(request.POST)
            if form.is_valid():
                water_entry = form.save(commit=False)
                water_entry.user = request.user
                water_entry.date = now().date()
                water_entry.save()
                tracker.log_water(water_entry.amount)  # Log new entry
                return redirect('track_water')
    else:
        form = WaterIntakeForm()
        goal_form = WaterGoalForm(instance=goal)

    return render(request, 'nutrition/track_water.html', {
        'form': form,
        'goal_form': goal_form,
        'total_water': total_water,
        'daily_goal': daily_goal,
        'progress': progress,
        'water_intakes': water_intakes,
        'water_entries': water_summary['total_entries']
    })

@login_required
def weight_progress(request):
    """Track weight progress using NutritionTracker."""
    tracker = NutritionTracker()
    weight_logs = WeightLog.objects.filter(user=request.user).order_by('date')
    
    # Sync database with tracker
    for log in weight_logs:
        tracker.log_weight(log.weight)
    
    tracker_progress = tracker.get_weight_progress()

    if request.method == "POST":
        form = WeightLogForm(request.POST)
        if form.is_valid():
            weight_entry = form.save(commit=False)
            weight_entry.user = request.user
            weight_entry.date = now().date()
            weight_entry.save()
            tracker.log_weight(weight_entry.weight)  # Log new entry
            return redirect('weight_progress')
    else:
        form = WeightLogForm()
    
    return render(request, 'nutrition/weight_progress.html', {
        'form': form,
        'weight_logs': weight_logs,
        'tracker_progress': tracker_progress
    })
