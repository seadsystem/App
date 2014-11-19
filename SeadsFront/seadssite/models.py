from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink

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

# For the blog 

class Blog(models.Model):
	title = models.CharField(max_length=255, unique=True)
	slug = models.SlugField(max_length=255, unique=True)
	body = models.TextField()
	posted = models.DateField(db_index=True, auto_now_add=True)
	category = models.ForeignKey('seadssite.Category')

	def __unicode__(self):
		return '%s' % self.title

	@permalink
	def get_absolute_url(self):
		return ('view_blog_post', None, {'slug':self.slug})

class Category(models.Model):
	title = models.CharField(max_length=255, db_index=True)
	slug = models.SlugField(max_length=255, db_index=True)

	def __unicode__(self):
		return '%s' % self.title

	@permalink
	def get_absolute_url(self):
		return ('view_blog_category', None, {'slug':self.slug})

class newPost(models.Model):
    title = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=255, default=0)
    body = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)
    posted = models.DateField(db_index=True, auto_now_add=True)


