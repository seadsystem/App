from seadssite.models import UserProfile 
from django.contrib.auth.models import User
from django import forms

#we should use email validation: http://stackoverflow.com/questions/3217682/checking-validity-of-email-in-django-python
#http://stackoverflow.com/questions/20192144/creating-custom-user-registration-form-django

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)
    username = forms.CharField(required = True)
    email = forms.EmailField(required = True)
    phone = forms.CharField(required = True)
    cellProvider = forms.EmailField(required = True)
    class Meta:
    	model = User
    	fields = ('username', 'first_name','last_name', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'cellProvider')