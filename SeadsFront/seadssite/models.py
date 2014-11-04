from django.contrib.auth.models import User
from django.db import models

'''
model for SEADS devices like the SEADS plug
'''
class Devices(models.Model):
	device_id = models.IntegerField()
	name = models.CharField(max_length=200, default='DEFAULT VALUE')
	connection = models.BooleanField(default=True)
	power = models.BooleanField(default=False)


'''
Relational map between a user and a device
'''
class Map(models.Model):
	user = models.ForeignKey(User)
	device = models.ForeignKey(Devices)


'''
Model for an extended user profile
'''
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=10)
    cellProvider = models.CharField(max_length=20)

    '''
    getters
    
    def get_user(self):
    	return self.user
    def get_phone(self):
    	return self.phone
    def get_cell(self):
    	return self.cellProvider
    def __str__(self):
        return "{}".format(self.user.username)
    
    setters
    
    def set_user(self, user):
    	self.user = user
    def set_phone(self, phone):
    	self.phone = phone
    def set_cell(self, cell_provider):
    	self.cellProvider = cell_provider
    '''
