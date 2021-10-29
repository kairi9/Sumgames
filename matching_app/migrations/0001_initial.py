# Generated by Django 3.2.8 on 2021-10-29 05:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('game_name', models.CharField(max_length=50, unique=True, verbose_name='ゲーム名')),
                ('detail', models.TextField(blank=True, null=True, verbose_name='説明')),
                ('image', models.ImageField(default='images/default.png', upload_to='images/', verbose_name='画像')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('genrename', models.CharField(max_length=50, unique=True, verbose_name='ジャンル名')),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('platform_name', models.CharField(max_length=50, unique=True, verbose_name='プラットフォーム名')),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('tag_name', models.CharField(max_length=50, unique=True, verbose_name='タグ名')),
            ],
        ),
        migrations.CreateModel(
            name='Talkroom',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('recruit_num', models.IntegerField(verbose_name='募集人数')),
                ('recruit_gender', models.CharField(choices=[('AL', '誰でも'), ('MA', '男性'), ('FE', '女性'), ('EX', 'その他')], default='AL', max_length=2)),
                ('recruit_con', models.TextField(default='誰でも気軽に参加してください。', verbose_name='募集内容')),
                ('under_recruitment', models.BooleanField(default=True, verbose_name='募集中')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matching_app.game', verbose_name='ゲーム')),
                ('recruit_platform', models.ManyToManyField(to='matching_app.Platform', verbose_name='プラットフォーム')),
                ('users_ID', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='ユーザーID')),
            ],
            options={
                'ordering': ['-create_at'],
            },
        ),
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('talktext', models.CharField(blank=True, max_length=200, null=True, verbose_name='内容テキスト')),
                ('talkfile', models.FileField(blank=True, null=True, upload_to='', verbose_name='内容静的ファイル')),
                ('send_at', models.DateTimeField(auto_now_add=True, verbose_name='送信日時')),
                ('talkroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matching_app.talkroom', verbose_name='トークルームID')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー名')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='genre',
            field=models.ManyToManyField(to='matching_app.Genre', verbose_name='ジャンル'),
        ),
        migrations.AddField(
            model_name='game',
            name='platform',
            field=models.ManyToManyField(to='matching_app.Platform', verbose_name='プラットフォーム'),
        ),
        migrations.AddField(
            model_name='game',
            name='tags',
            field=models.ManyToManyField(blank=True, to='matching_app.Tags', verbose_name='タグ'),
        ),
    ]
