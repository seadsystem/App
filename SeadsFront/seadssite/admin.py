from django.contrib import admin
from .models import Devices
from .models import Map
from seadssite.models import UserProfile
# Register your models here.
#added below for blog
from django import forms
# from blogs.models import Category, Article

admin.site.register(Devices)
admin.site.register(Map)
admin.site.register(UserProfile)
#both below added for site
# admin.site.register(Categoy, CategoryAdmin)
# admin.site.register(Article, ArticleAdmin)

