from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User


class Devices(models.Model):
	user_id = models.CharField(max_length=200, default='DEFAULT USERID')
	device_id = models.IntegerField()
	device_name = models.CharField(max_length=200, default='DEFAULT VALUE')
	device_connectionstatus = models.BooleanField(default=False)
	device_powerstatus = models.BooleanField(default=False)
	def get_id(self):
		return self.DeviceId
	#MetaData
	#url = models.URLField()
	#views = models.IntegerField(default=0) how to associate this with the list of Devices
	#Ali wants on main page


class Map(models.Model):
	user_id = models.ForeignKey(User) #how to get User Id from User sign-in auth
	device_id = models.ForeignKey(Devices)

	def __str__(self):
		return "User: {} | Owns: {}".format(self.user_id,self.device_id.device_id)

	def get_id(self):
		return self.device_id.device_id
	
	#url = models.URLField()
	#views = models.IntegerField(default=0) how to associate this with the list of Devices
	#Ali wants on main page

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

