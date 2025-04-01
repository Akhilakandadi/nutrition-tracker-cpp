# Import AppConfig base class from Django for app configuration
from django.apps import AppConfig

# Define the configuration class for the 'nutrition' app
class NutritionConfig(AppConfig):
    """Configuration for the nutrition app, specifying settings and initialization."""
    default_auto_field = 'django.db.models.BigAutoField'  # Set the default primary key field type to BigAutoField (supports large integers)
    name = 'nutrition'  # Name of the app, matching the app directory (e.g., 'nutrition/')

    def ready(self):
        """Method called when the app is ready, used to initialize additional components."""
        import nutrition.signals  # Import the signals module to ensure signal handlers are registered