from django.contrib import admin
from .models import CustomUser,ExpoPushToken

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(ExpoPushToken)
