from django.contrib import admin
from .models import Devices
from .models import Map
from seadssite.models import UserProfile
# Register your models here.
#added below for blog
from django import forms
from seadssite.models import Blog, Category

admin.site.register(Devices)
admin.site.register(Map)
admin.site.register(UserProfile)
#both below added for site

class BlogAdmin(admin.ModelAdmin):
	exclude = ['posted']
	prepopulated_fields = {'slug':('title',)}

class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)



