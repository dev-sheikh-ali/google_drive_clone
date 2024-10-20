from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  # Use a date input
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'sirname', 'dob')

class CustomUserChangeForm(UserChangeForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  # Use a date input
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'sirname', 'dob')
