from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    firstName = models.CharField(max_length=50, default='First Name')
    lastName = models.CharField(max_length=50, default='Last Name')
    phone = models.CharField(max_length=10)
    cellProvider = models.CharField(max_length=20)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username