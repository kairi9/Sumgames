from django.db import models
from accounts.models import CustomUser

class Game(models.Model):
    """ゲームモデル"""
    game_name =models.CharField(verbose_name="ゲーム名",max_length=50)
    genre =models.ManyToManyField(Genre,verbose_name="ジャンル")
    detail = models.TextField(verbose_name="説明",null=True)
    image = models.ImageField(verbose_name="画像",null = True)
    tags = models.ManyToManyField(Tags,verbose_name="タグ")
    platform = models.ManyToManyField(Platform,verbose_name="プラットフォーム")
    update_at = models.DateTimeField(verbose_name="更新日時",auto_now=True)

    def __str__(self):
        return self.game_name

class Tags(models.Model):
    tag_name = models.CharField(verbose_name="タグ名",max_length=50)

    def __str__(self):
        return self.tag_name

class Talkroom(models.Model):
    """トークルームモデル"""
    game = models.ForeignKey(Game,verbose_name="ゲーム",on_delete=models.CASCADE)
    recruit_num = models.IntegerField(verbose_name='募集人数')
    gender = [
        ("MA","男性"),
        ("FE","女性"),
        ("EX","その他"),
    ]
    recruit_gender = models.CharField(
        max_length=2,
        choices=gender,
        default="MA",
    )
    recruit_platform = models.ManyToManyField(Platform,verbose_name="プラットフォーム")
    users_ID = models.ManyToManyField(CustomUser,verbose_name="ユーザーID")
    recruit_con = models.TextField(verbose_name='募集内容',null=True)
    under_recruitment = models.BooleanField(verbose_name="募集中",default=True)
    create_at = models.TimeField(verbose_name="作成日時",auto_now_add=True)

    class Meta:
        ordering=['-create_at']

class Platform(models.Model):
    platform_name = models.CharField(verbose_name='プラットフォーム名',max_length=50)
    def __str__(self):
        return self.platform_name

class Talk(models.Model):
    """トークモデル"""
    talkroom = models.ForeignKey(Talkroom,verbose_name="トークルームID",on_delete=models.CASCADE)
    username = models.ForeignKey(CustomUser,verbose_name="ユーザー名",on_delete=models.PROTECT)
    talktext = models.CharField(verbose_name="内容テキスト",max_length=200,blank=True,null=True)
    talkfile = models.FileField(verbose_name="内容静的ファイル")
    send_at = models.TimeField(verbose_name="送信日時")

class Genre(models.Model):
    """ゲームジャンルモデル"""
    genrename = models.CharField(verbose_name='ジャンル名')

    def __str__(self):
        return self.genrename



