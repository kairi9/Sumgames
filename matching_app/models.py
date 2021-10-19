from django.db import models
from django.db.models.fields.related import ForeignKey
from accounts.models import CustomUser

class User(models.Model):
    """ユーザーモデル"""

    user = models.ForeignKey(CustomUser,verbose_name="ユーザー",on_delete=models.PROTECT)
    username = models.CharField(verbose_name="ユーザーネーム",max_length=50)
    Email = models.EmailField(verbose_name="メールアドレス")
    password = models.CharField(verbose_name="パスワード",max_length=50)


class Game(models.Model):
    """ゲームモデル"""

    gameID = models.UUIDField(verbose_name="ID")
    gamename =models.CharField(verbose_name="ゲーム名",max_length=50)
    genre =models.IntegerField(verbose_name="ジャンル")
    detail = models.CharField(verbose_name="説明",max_length=200)
    image = models.ImageField(verbose_name="画像",null = True)
    tags = models.CharField(verbose_name="タグ",max_length=100)
    platform = models.IntegerField(verbose_name="プラットフォーム")
    update_at = models.DateTimeField(verbose_name="更新日時",auto_now=True)

class Talkroom(models.Model):
    """トークルームモデル"""

    talkroom = models.UUIDField(verbose_name="トークルームID")
    create_at = models.TimeField(verbose_name="作成日時",auto_now_add=True)

    class Meta:
        ordering=['-create_at']

class Talk(models.Model):
    """トークモデル"""

    talkID = models.UUIDField(verbose_name="トークID")
    talkroom = models.ForeignKey(Talkroom,on_delete=models.CASCADE)
    username = models.CharField(verbose_name="ユーザー名",max_length=50)
    talktext = models.CharField(verbose_name="内容テキスト",max_length=200,blank=True,null=True)
    talk = models.FileField(verbose_name="内容静的ファイル")
    send_at = models.TimeField(verbose_name="送信日時")

# Create your models here.
