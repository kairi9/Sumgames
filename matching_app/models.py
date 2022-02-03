from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import CustomUser,ExpoPushToken
import uuid as uuid_lib

class Genre(models.Model):
    """ゲームジャンルモデル"""
    id = models.UUIDField(
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False,
    )
    genrename = models.CharField(verbose_name='ジャンル名',max_length=150,unique=True)

    def __str__(self):
        return self.genrename

class Tags(models.Model):
    id = models.UUIDField(
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False,
    )
    tag_name = models.CharField(verbose_name="タグ名",max_length=150,unique=True)

    def __str__(self):
        return self.tag_name

class Platform(models.Model):
    id = models.UUIDField(
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False,
    )
    platform_name = models.CharField(verbose_name='プラットフォーム名',max_length=150,unique=True)
    def __str__(self):
        return self.platform_name

class Game(models.Model):
    """ゲームモデル"""
    id = models.UUIDField(
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False,
    )
    game_name =models.CharField(verbose_name="ゲーム名",max_length=150,unique=True)
    genre =models.ManyToManyField(Genre,verbose_name="ジャンル")
    detail = models.TextField(verbose_name="説明",blank=True,null=True)
    image = models.ImageField(verbose_name="画像",upload_to='images/',default='images/default.png')
    tags = models.ManyToManyField(Tags,verbose_name="タグ",blank=True)
    platform = models.ManyToManyField(Platform,verbose_name="プラットフォーム")
    update_at = models.DateTimeField(verbose_name="更新日時",auto_now=True)

    def __str__(self):
        return self.game_name


class Talkroom(models.Model):
    """トークルームモデル"""
    id = models.UUIDField(
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False,
    )
    game = models.ForeignKey(Game,verbose_name="ゲーム",on_delete=models.CASCADE)
    recruit_num = models.IntegerField(verbose_name='募集人数',validators=[MinValueValidator(1,"1人以上募集してください")])
    gender = [
        ("AL","誰でも"),
        ("MA","男性"),
        ("FE","女性"),
    ]
    recruit_gender = models.CharField(
        max_length=2,
        choices=gender,
        default="AL",
    )
    recruit_platform = models.ManyToManyField(Platform,verbose_name="プラットフォーム")
    host_user = models.ForeignKey(CustomUser,verbose_name="ホストユーザー",on_delete=models.PROTECT,related_name='host_user')
    guest_user = models.ManyToManyField(CustomUser,verbose_name="ゲストユーザー",related_name='guest_user',blank=True)
    recruit_context = models.TextField(verbose_name='募集内容',default="誰でも気軽に参加してください。")
    under_recruitment = models.BooleanField(verbose_name="募集中",default=True)
    create_at = models.DateTimeField(verbose_name="作成日時",auto_now_add=True)
    expo_tokens = models.ManyToManyField(ExpoPushToken,verbose_name="EXPOトークン",blank=True)
    class Meta:
        ordering=['-create_at']


class Talk(models.Model):
    """トークモデル"""
    id = models.UUIDField(
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False,
    )
    talkroom = models.ForeignKey(Talkroom,verbose_name="トークルームID",on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,verbose_name="ユーザー名",on_delete=models.PROTECT)
    talktext = models.CharField(verbose_name="内容テキスト",max_length=200,blank=True,null=True)
    talkfile = models.ImageField(verbose_name="内容画像",upload_to='talk_images/',blank=True,null=True)
    send_at = models.DateTimeField(verbose_name="送信日時",auto_now_add=True)
    def __str__(self):
        return str(self.user)+" "+str(self.send_at)
    
class Inquiry(models.Model):
    """お問い合わせモデル"""
    id = models.UUIDField(
        default=uuid_lib.uuid4,
        primary_key=True,
        editable=False,
    )
    userID = models.ForeignKey(CustomUser,verbose_name="ユーザーID",on_delete=models.PROTECT)
    inquiry_title = models.CharField(verbose_name="お問い合わせ要件",max_length=50)
    inquiry_context = models.TextField(verbose_name="お問い合わせ内容")
    send_at = models.DateTimeField(verbose_name="送信日時",auto_now_add=True)
    def __str__(self):
        return self.inquiry_title
