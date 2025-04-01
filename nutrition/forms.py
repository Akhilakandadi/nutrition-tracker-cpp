# Import Django's forms module for creating form classes
from django import forms
# Import User model from Django's authentication system for user-related forms
from django.contrib.auth.models import User
# Import custom models from the current app for form definitions
from .models import WaterIntake, WaterGoal, UserProfile, WeightLog

class SignUpForm(forms.ModelForm):
    """Form for user registration with username, email, and password fields."""
    password = forms.CharField(widget=forms.PasswordInput)  # Password field with masked input for security
    email = forms.EmailField()  # Email field with built-in email validation

    class Meta:
        """Metadata for SignUpForm, defining the model and fields."""
        model = User  # Links form to Django's User model
        fields = ['username', 'email', 'password']  # Fields to include in the form: username, email, and password

class UserProfileForm(forms.ModelForm):
    """Form for capturing additional user profile details."""
    weight_unit = forms.ChoiceField(
        choices=[('kg', 'Kilograms (kg)'), ('lbs', 'Pounds (lbs)')],  # Dropdown options for weight unit
        required=True  # Ensures user selects a unit (no blank option)
    )
    
    class Meta:
        """Metadata for UserProfileForm, defining the model and fields."""
        model = UserProfile  # Links form to UserProfile model
        fields = ['age', 'weight', 'height', 'medical_conditions', 'weight_unit']  # Fields for profile data plus weight unit

class WaterIntakeForm(forms.ModelForm):
    """Form for logging daily water intake."""
    class Meta:
        """Metadata for WaterIntakeForm, defining the model and fields."""
        model = WaterIntake  # Links form to WaterIntake model
        fields = ['amount']  # Single field for water amount in milliliters

class WaterGoalForm(forms.ModelForm):
    """Form for setting or updating a daily water intake goal."""
    class Meta:
        """Metadata for WaterGoalForm, defining the model and fields."""
        model = WaterGoal  # Links form to WaterGoal model
        fields = ['daily_goal']  # Single field for daily water goal in milliliters

class WeightLogForm(forms.ModelForm):
    """Form for logging user weight entries."""
    class Meta:
        """Metadata for WeightLogForm, defining the model and fields."""
        model = WeightLog  # Links form to WeightLog model
        fields = ['weight']  # Single field for weight in kilograms