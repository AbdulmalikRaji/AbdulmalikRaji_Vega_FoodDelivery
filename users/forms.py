from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__'  # This includes all fields
