from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Devices(models.Model):
	DeviceId = models.IntegerField()
	#MetaData
	#url = models.URLField()
	#views = models.IntegerField(default=0) how to associate this with the list of Devices
	#Ali wants on main page


class UserDevice(models.Model):
	UserId = models.ForeignKey(User) #how to get User Id from User sign-in auth
	DeviceId = models.ForeignKey(Devices)
	#url = models.URLField()
	#views = models.IntegerField(default=0) how to associate this with the list of Devices
	#Ali wants on main page

