from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Genre)
admin.site.register(models.Tags)
admin.site.register(models.Platform)
admin.site.register(models.Game)
admin.site.register(models.Talkroom)
admin.site.register(models.Talk)
admin.site.register(models.Inquiry)