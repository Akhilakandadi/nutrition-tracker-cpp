# Import Django's models module for defining database models
from django.db import models
# Import User model from Django's authentication system for linking to users
from django.contrib.auth.models import User
# Import signals for automatic actions after model events (e.g., user creation)
from django.db.models.signals import post_save
# Import receiver decorator to handle signal events
from django.dispatch import receiver
# Re-imported models and User (duplicate, can be removed)
from django.db import models
from django.contrib.auth.models import User
# Import now function for setting default timestamps
from django.utils.timezone import now

class Meal(models.Model):
    """Model to store meal entries with nutritional information for a user."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links meal to a user; CASCADE deletes meals if user is deleted
    name = models.CharField(max_length=200)  # Name of the meal (e.g., "Chicken Salad")
    calories = models.IntegerField()  # Total calories in the meal (in kcal)
    protein = models.FloatField()  # Protein content (in grams)
    carbs = models.FloatField()  # Carbohydrate content (in grams)
    fats = models.FloatField()  # Fat content (in grams)
    date = models.DateField(auto_now_add=True)  # Date meal was added, auto-set to current date

    def __str__(self):
        """String representation of the Meal object."""
        return f"{self.name} - {self.calories} kcal"  # Returns meal name and calories (e.g., "Chicken Salad - 300 kcal")

class UserProfile(models.Model):
    """Model to store additional user information beyond Django's default User model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one link to User; CASCADE deletes profile if user is deleted
    age = models.IntegerField(null=True, blank=True)  # User's age, optional (can be null or blank)
    weight = models.FloatField(null=True, blank=True)  # User's weight in kg, optional
    height = models.FloatField(null=True, blank=True)  # User's height in cm, optional
    medical_conditions = models.TextField(null=True, blank=True)  # Free-text field for medical conditions, optional

    def __str__(self):
        """String representation of the UserProfile object."""
        return self.user.username  # Returns the associated username (e.g., "john_doe")

class WaterIntake(models.Model):
    """Model to track daily water intake for a user."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links water intake to a user; CASCADE deletes entries if user is deleted
    date = models.DateField(default=now)  # Date of water intake, defaults to current date
    amount = models.FloatField()  # Amount of water consumed in milliliters (ml)

    def __str__(self):
        """String representation of the WaterIntake object."""
        return f"{self.user.username} - {self.amount} ml on {self.date}"  # Returns username, amount, and date (e.g., "john_doe - 500 ml on 2025-03-31")

class WaterGoal(models.Model):
    """Model to store a user's daily water intake goal."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one link to User; CASCADE deletes goal if user is deleted
    daily_goal = models.FloatField(default=2000)  # Daily water goal in milliliters, defaults to 2000 ml (2 liters)

    def __str__(self):
        """String representation of the WaterGoal object."""
        return f"{self.user.username} - Goal: {self.daily_goal} ml"  # Returns username and goal (e.g., "john_doe - Goal: 2000 ml")

class WeightLog(models.Model):
    """Model to track a user's weight history over time."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links weight log to a user; CASCADE deletes logs if user is deleted
    date = models.DateField(default=now)  # Date of weight entry, defaults to current date
    weight = models.FloatField()  # Weight in kilograms

    def __str__(self):
        """String representation of the WeightLog object."""
        return f"{self.user.username} - {self.weight} kg on {self.date}"  # Returns username, weight, and date (e.g., "john_doe - 70.5 kg on 2025-03-31")