from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid as uuid_lib

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class CustomUser(AbstractUser):
    """拡張ユーザモデル"""
    id = models.UUIDField(
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False,
    )
    gender_list = [
        ("MA","男性"),
        ("FE","女性"),
        ("EX","その他"),
    ]
    gender = models.CharField(
        max_length=2,
        choices=gender_list,
        default="MA",
    )
    class Meta:
        verbose_name_plural='CustomUser'