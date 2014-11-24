from seadssite.models import UserProfile 
from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

#we should use email validation: http://stackoverflow.com/questions/3217682/checking-validity-of-email-in-django-python


class Meta:
    model = User
    fields = ('username', 'first_name','last_name', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'cellProvider')