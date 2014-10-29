from django.contrib import admin
from .models import Devices
from .models import UserDevice
# Register your models here.


admin.site.register(Devices)
admin.site.register(UserDevice)