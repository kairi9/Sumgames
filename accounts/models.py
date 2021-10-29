from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class CustomUser(AbstractUser):
    """拡張ユーザモデル"""
    #host = models.BooleanField(verbose_name="ホスト",default=False)
    #guest = models.BooleanField(verbose_name="ゲスト",default=False)
    class Meta:
        verbose_name_plural='CustomUser'