# Standard Django imports
from django.contrib import messages  # For displaying success/error messages to users
from django.contrib.auth import login, logout as auth_logout  # For user authentication (login/logout)
from django.contrib.auth.decorators import login_required  # Decorator to restrict views to logged-in users
from django.contrib.auth.forms import UserCreationForm  # Built-in form for user registration
from django.contrib.auth.models import User  # Django's User model for authentication
from django.shortcuts import render, redirect  # Utilities for rendering templates and redirecting
from django.utils.timezone import now  # For getting the current date/time in timezone-aware format

# Local app imports
from .forms import SignUpForm, UserProfileForm, WaterIntakeForm, WaterGoalForm, WeightLogForm  # Custom forms for user input
from .models import Meal, UserProfile, WaterIntake, WaterGoal, WeightLog  # Database models for app data
from .utils import get_nutrition  # Utility function to fetch nutritional data (e.g., from USDA API)

# Views

@login_required  # Ensures only authenticated users can access this view
def meal_list(request):
    """Display a list of meals for the logged-in user with total calories."""
    meals = Meal.objects.filter(user=request.user)  # Fetch all meals associated with the current user
    total_calories = sum(meal.calories for meal in meals)  # Calculate total calories from all meals
    return render(request, 'nutrition/meal_list.html', {  # Render the meal list template
        'meals': meals,  # Pass meals QuerySet to template
        'total_calories': total_calories  # Pass total calories to template
    })

@login_required  # Restricts access to logged-in users
def add_meal(request):
    """Handle adding a new meal with nutritional data from an external source."""
    if request.method == "POST":  # Check if the request is a form submission
        food_name = request.POST['food_name']  # Get food name from form input
        nutrition_data = get_nutrition(food_name)  # Fetch nutritional info using utility function

        if nutrition_data:  # If data is successfully retrieved
            if "add_to_meal" in request.POST:  # Check if user clicked "Add to Meal" button
                Meal.objects.create(  # Create a new Meal object in the database
                    user=request.user,  # Associate with current user
                    name=nutrition_data['name'],
                    calories=nutrition_data['calories'],
                    protein=nutrition_data['protein'],
                    carbs=nutrition_data['carbs'],
                    fats=nutrition_data['fats']
                )
                return redirect('meal_list')  # Redirect to meal list after saving
            return render(request, 'nutrition/add_meal.html', {'nutrition_data': nutrition_data})  # Show nutrition data
        else:
            return render(request, 'nutrition/add_meal.html', {"error": "Food not found"})  # Show error if no data

    return render(request, 'nutrition/add_meal.html')  # Render empty form for GET request

@login_required  # Requires user login
def delete_meal(request, meal_id):
    """Delete a specific meal entry for the logged-in user."""
    meal = Meal.objects.get(id=meal_id, user=request.user)  # Fetch the meal by ID, ensuring it belongs to the user
    meal.delete()  # Remove the meal from the database
    return redirect('meal_list')  # Redirect back to meal list

def signup(request):
    """Handle user registration and automatic login."""
    if request.method == 'POST':  # Process form submission
        user_form = SignUpForm(request.POST)  # Form for basic user data
        profile_form = UserProfileForm(request.POST)  # Form for additional profile data
        
        if user_form.is_valid() and profile_form.is_valid():  # Validate both forms
            user = user_form.save()  # Save user to database
            user.set_password(user.password)  # Hash the password
            user.save()  # Save updated user

            profile = profile_form.save(commit=False)  # Prepare profile without saving yet
            profile.user = user  # Link profile to user
            profile.save()  # Save profile to database

            login(request, user)  # Log the user in immediately
            messages.success(request, "Your account has been created and you're now logged in.")  # Success message
            return redirect('meal_list')  # Redirect to meal list
        else:
            messages.error(request, "Please fix the errors below.")  # Error message if forms invalid
    
    else:  # For GET request
        user_form = SignUpForm()  # Empty user form
        profile_form = UserProfileForm()  # Empty profile form

    return render(request, 'registration/signup.html', {  # Render signup template
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required  # Restricts to logged-in users
def profile_info(request):
    """Display the user's profile information."""
    profile, created = UserProfile.objects.get_or_create(user=request.user)  # Get or create user profile
    return render(request, 'nutrition/profile_info.html', {'profile': profile})  # Render profile template

@login_required  # Requires authentication
def edit_profile(request):
    """Allow users to edit their profile information."""
    profile = UserProfile.objects.get(user=request.user)  # Fetch user's existing profile

    if request.method == "POST":  # Handle form submission
        form = UserProfileForm(request.POST, instance=profile)  # Populate form with existing profile data
        if form.is_valid():  # Validate form
            form.save()  # Save updated profile
            return redirect('profile_info')  # Redirect to profile info page
    else:  # For GET request
        form = UserProfileForm(instance=profile)  # Pre-fill form with current profile data

    return render(request, 'nutrition/edit_profile.html', {'form': form})  # Render edit form

@login_required  # Ensures user is logged in
def track_water(request):
    """Track daily water intake and manage hydration goals."""
    # Fetch today's water intake for the user
    water_intakes = WaterIntake.objects.filter(user=request.user, date=now().date())
    total_water = sum(w.amount for w in water_intakes)  # Calculate total water consumed today

    # Get or create user's water goal
    goal, created = WaterGoal.objects.get_or_create(user=request.user)
    daily_goal = goal.daily_goal  # Retrieve daily goal value

    # Calculate progress as a percentage, capped at 100%
    progress = min((total_water / daily_goal) * 100, 100)

    # Warn user if behind on hydration (less than 50% of goal)
    if total_water < daily_goal * 0.5:
        messages.warning(request, "You're behind on your water intake! Stay hydrated. 💧")

    if request.method == "POST":  # Handle form submissions
        if "update_goal" in request.POST:  # If updating the goal
            goal_form = WaterGoalForm(request.POST, instance=goal)
            if goal_form.is_valid():
                goal_form.save()  # Save updated goal
                messages.success(request, "Water intake goal updated! 🎯")
                return redirect('track_water')
        else:  # If logging water intake
            form = WaterIntakeForm(request.POST)
            if form.is_valid():
                water_entry = form.save(commit=False)  # Prepare entry without saving
                water_entry.user = request.user  # Assign to current user
                water_entry.date = now().date()  # Set current date
                water_entry.save()  # Save to database
                return redirect('track_water')

    else:  # For GET request
        form = WaterIntakeForm()  # Empty water intake form
        goal_form = WaterGoalForm(instance=goal)  # Pre-filled goal form

    return render(request, 'nutrition/track_water.html', {  # Render water tracking template
        'form': form,
        'goal_form': goal_form,
        'total_water': total_water,
        'daily_goal': daily_goal,
        'progress': progress,
        'water_intakes': water_intakes
    })

@login_required  # Restricts to authenticated users
def weight_progress(request):
    """Track and display user's weight history."""
    weight_logs = WeightLog.objects.filter(user=request.user).order_by('date')  # Fetch weight logs sorted by date
    
    if request.method == "POST":  # Handle new weight entry
        form = WeightLogForm(request.POST)
        if form.is_valid():
            weight_entry = form.save(commit=False)  # Prepare entry without saving
            weight_entry.user = request.user  # Assign to current user
            weight_entry.date = now().date()  # Set current date
            weight_entry.save()  # Save to database
            return redirect('weight_progress')
    else:  # For GET request
        form = WeightLogForm()  # Empty weight log form
    
    return render(request, 'nutrition/weight_progress.html', {  # Render weight progress template
        'form': form,
        'weight_logs': weight_logs
    })