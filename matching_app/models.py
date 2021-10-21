from django.db import models
from django.db.models.fields.related import ForeignKey
from accounts.models import CustomUser

class Game(models.Model):
    """ゲームモデル"""
    gamename =models.CharField(verbose_name="ゲーム名",max_length=50)
    genre =models.ForeignKey(verbose_name="ジャンル")
    detail = models.CharField(verbose_name="説明",max_length=200)
    image = models.ImageField(verbose_name="画像",null = True)
    tags = models.CharField(verbose_name="タグ",max_length=100)
    platform = models.ForeignKey(verbose_name="プラットフォーム")
    update_at = models.DateTimeField(verbose_name="更新日時",auto_now=True)

class Talkroom(models.Model):
    """トークルームモデル"""
    create_at = models.TimeField(verbose_name="作成日時",auto_now_add=True)

    class Meta:
        ordering=['-create_at']

class Talk(models.Model):
    """トークモデル"""
    talkroom = models.ForeignKey(Talkroom,on_delete=models.CASCADE)
    username = models.ForeignKey(verbose_name="ユーザー名",max_length=50)
    talktext = models.CharField(verbose_name="内容テキスト",max_length=200,blank=True,null=True)
    talkfile = models.FileField(verbose_name="内容静的ファイル")
    send_at = models.TimeField(verbose_name="送信日時")

# Create your models here.
class Recruit(models.Model):
    """募集テーブルモデル"""
    RecruitNUM = models.IntegerField(verbose_name='募集人数')
    RecruitGender = models.BooleanField(verbose_name='性別')
    RecruitPlatform = models.ForeignKey(verbose_name='プラットフォーム',max_length=5)
    RecruitUserID = models.ForeignKey(verbose_name='ユーザID')
    RecruitCon = models.TextField(verbose_name='募集内容',null=True)
    talkroom =models.UUIDField(verbose_name='トークルームID')
    
    def __str__(self):
        return self.talkroom


class Platform(models.Model):
    """プラットフォームテーブルモデル"""
    platformname = models.CharField(verbose_name='プラットフォーム名',)

    def __str__(self):
        return self.platformname



class Genre(models.Model):
    """ゲームジャンルモデル"""
    genrename = models.CharField(verbose_name='ジャンル名')

    def __str__(self):
        return self.genrename



