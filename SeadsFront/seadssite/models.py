from django.contrib.auth.models import User
from django.db import models

'''
model for SEADS devices like the SEADS plug
'''
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

'''
Relational map between a user and a device
'''
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
		return "User: {} | Owns: {} | DeviceName: {}".format(
			self.user,self.device.device_id,self.device.name)
	'''
	setters
	'''
	def set_user(self, user):
		self.user = user
	def set_device(self, device):
		self.device = device

'''
Model for an extended user profile
'''
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=10)
    cellProvider = models.CharField(max_length=20)
    '''
    getters
    '''
    def get_user(self):
    	return self.user
    def get_phone(self):
    	return self.phone
    def get_cell(self):
    	return self.cellProvider
    def __str__(self):
        return "{}".format(self.user.username)
    '''
    setters
    '''
    def set_user(self, user):
    	self.user = user
    def set_phone(self, phone):
    	self.phone = phone
    def set_cell(self, cell_provider):
    	self.cellProvider = cell_provider

