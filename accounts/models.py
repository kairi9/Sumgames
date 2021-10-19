from typing import AbstractSet
from django.db import models

# Create your models here.

class CustoUser(AbstractUser):
    """拡張ユーザモデル"""

    class Meta:
        verbose_name_plural='CustomUser'