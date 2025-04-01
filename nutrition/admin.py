# Import Django's admin module for managing models in the admin interface
from django.contrib import admin
# Import the Meal model from the current app's models module
from .models import Meal

# Register the Meal model with the admin site using a decorator
@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    """Custom admin interface configuration for the Meal model."""
    list_display = ('name', 'calories', 'protein', 'carbs', 'fats', 'date', 'user')  # Fields to display in the admin list view
    search_fields = ('name',)  # Fields to enable search functionality (search by meal name)
    list_filter = ('date',)  # Fields to enable filtering (filter meals by date)