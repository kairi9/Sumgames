from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    """拡張ユーザモデル"""

    class Meta:
        verbose_name_plural='CustomUser'