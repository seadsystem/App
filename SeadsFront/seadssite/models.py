from django.contrib.auth.models import User
from django.db import models

class Devices(models.Model):
	device_id = models.IntegerField()
	name = models.CharField(max_length=200, default='DEFAULT VALUE')
	connection_status = models.BooleanField(default=False)
	power_status = models.BooleanField(default=False)
	'''
	getters
	'''
	def get_id(self):
		return self.device_id
	def get_name(self):
		return self.name
	def get_connection(self):
		return self.connection_status
	def get_power(self):
		return self.power_status
	def __str__(self):
		return "{}".format(self.device_id)
	'''
	setters
	'''
	def set_id(self, device_id):
		self.device_id = device_id
	def set_name(self, name):
		self.name = name
	def set_connection(self, connection_status):
		self.connection_status = connection_status
	def set_power(self, power_status):
		self.power_status = power_status


class Map(models.Model):
	user = models.ForeignKey(User)
	device = models.ForeignKey(Devices)
	'''
	getters
	'''
	def get_user(self):
		return self.user
	def get_device(self):
		return self.device
	def __str__(self):
		return "User: {} | Owns: {} | DeviceName: {}".format(self.user,self.device.device_id,self.device.device_name)

	def get_id(self):
		return self.device.device_id

	def set_id(self, device):
		return "{}".format(self.device)
	'''
	setters
	'''
	def set_user(self, user):
		self.user = user
	def set_device(self, device):
		self.device = device


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

