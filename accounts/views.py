# accounts/views.py
from django.views.generic import TemplateView

class DashboardView(TemplateView):
    template_name = 'registration/dashboard.html'


class SettingsView(TemplateView):
    template_name = 'registration/settings.html'



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ArtistProfile
from .forms import UserUpdateForm, CustomerProfileForm, ArtistProfileForm


from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})



@login_required
def update_user(request):
    """Update User model settings"""
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            
            # Save theme and display preferences
            request.user.theme = request.POST.get('theme', 'dark')
            request.user.text_size = request.POST.get('text_size', 'medium')
            request.user.high_contrast = 'high_contrast' in request.POST
            request.user.reduce_motion = 'reduce_motion' in request.POST
            request.user.save()
            
            messages.success(request, 'Your account settings have been updated.')
            return redirect('profile_settings')
    
    messages.error(request, 'There was an error updating your account. Please try again.')
    return redirect('profile_settings')

@login_required
def update_customer_profile(request):
    """Update CustomerProfile settings"""
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES, instance=request.user.customer_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            
            # Handle profile image if provided
            if 'profile_image' in request.FILES:
                profile.profile_image = request.FILES['profile_image']
            
            # Handle preferences and notification settings
            profile.newsletter_subscribed = 'newsletter_subscribed' in request.POST
            
            # Save notification preferences in user settings
            notification_settings = request.user.notification_settings
            notification_settings.exhibitions = 'exhibitions_notification' in request.POST
            notification_settings.artists = 'artists_notification' in request.POST
            notification_settings.events = 'events_notification' in request.POST
            notification_settings.save()
            
            profile.save()
            messages.success(request, 'Your customer profile has been updated.')
            return redirect('profile_settings')
    
    messages.error(request, 'There was an error updating your profile. Please try again.')
    return redirect('profile_settings')

@login_required
def update_artist_profile(request):
    """Update ArtistProfile settings if it exists"""
    try:
        artist_profile = request.user.artist_profile
    except ArtistProfile.DoesNotExist:
        messages.error(request, 'You do not have an artist profile.')
        return redirect('profile_settings')
    
    if request.method == 'POST':
        form = ArtistProfileForm(request.POST, request.FILES, instance=artist_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            
            # Handle profile image if provided
            if 'profile_image' in request.FILES:
                profile.profile_image = request.FILES['profile_image']
            
            profile.save()
            messages.success(request, 'Your artist profile has been updated.')
            return redirect('profile_settings')
    
    messages.error(request, 'There was an error updating your artist profile. Please try again.')
    return redirect('profile_settings')