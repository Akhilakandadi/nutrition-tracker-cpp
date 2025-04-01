# Import path function from Django for defining URL patterns
from django.urls import path
# Import specific view functions from the current app's views module
from .views import meal_list, add_meal, delete_meal, signup, edit_profile, profile_info, track_water, weight_progress
# Import the views module as a whole for potential additional references (optional if all views are explicitly imported)
from . import views

# Define URL patterns for the nutrition app
urlpatterns = [
    path('', meal_list, name='meal_list'),  # Root URL (e.g., /nutrition/) maps to meal_list view
    path('add/', add_meal, name='add_meal'),  # URL for adding a meal (e.g., /nutrition/add/)
    path('delete/<int:meal_id>/', delete_meal, name='delete_meal'),  # URL for deleting a meal with dynamic ID (e.g., /nutrition/delete/1/)
    path('signup/', signup, name='signup'),  # URL for user signup (e.g., /nutrition/signup/)
    path('edit/', edit_profile, name='edit_profile'),  # URL for editing user profile (e.g., /nutrition/edit/)
    path('profile/', profile_info, name='profile_info'),  # URL for viewing user profile (e.g., /nutrition/profile/)
    path('track-water/', track_water, name='track_water'),  # URL for water tracking (e.g., /nutrition/track-water/)
    path('weight-progress/', weight_progress, name='weight_progress'),  # URL for weight progress (e.g., /nutrition/weight-progress/)
]