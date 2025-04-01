
# nutrition_tracker/urls.py (main project URL configuration)
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from nutrition.views import signup  # import your custom signup view


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Home page shows the login view with a custom template
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    
    # Nutrition app URLs
    path('nutrition/', include('nutrition.urls')),
    
    # Signup URL (accessible via a link from the login page)
    path('signup/', signup, name='signup'),
    
    # Optional: include the built-in auth URLs (password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
]


    








