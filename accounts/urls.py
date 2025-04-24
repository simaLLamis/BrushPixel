# accounts/urls.py
from django.urls import path
from .views import *

urlpatterns = [

    path('register/', register, name='register'),  # Add this line
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('settings/', SettingsView.as_view(), name='profile_settings'),
    
    path('settings/update-user/', update_user, name='update_user'),
    path('settings/update-customer/', update_customer_profile, name='update_customer_profile'),
    path('settings/update-artist/', update_artist_profile, name='update_artist_profile'),

]