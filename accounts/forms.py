from django import forms
from django.contrib.auth.models import User
from .models import CustomerProfile, ArtistProfile

class UserUpdateForm(forms.ModelForm):
    """Form for updating User model fields"""
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        
class CustomerProfileForm(forms.ModelForm):
    """Form for updating CustomerProfile fields"""
    class Meta:
        model = CustomerProfile
        fields = [
            'phone', 'address_line1', 'address_line2', 
            'city', 'state', 'zip_code', 'country', 'profile_image'
        ]
        
class ArtistProfileForm(forms.ModelForm):
    """Form for updating ArtistProfile fields"""
    class Meta:
        model = ArtistProfile
        fields = [
            'bio', 'location', 'profile_image', 'style', 
            'website', 'social_instagram', 'social_facebook', 'social_twitter'
        ]