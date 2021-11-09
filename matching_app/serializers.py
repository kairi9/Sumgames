from django.db.models import fields
from rest_framework import serializers
from . import models

""" class GameItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Game
        # 出力したいフィールド名をタプルで(括弧とカンマ)で定義します。
        #fields = ('id', 'game_name', 'genre', 'detail', 'image', 'tags', 'platform')
        exclude = ['update_at']
        depth = 1 """
        
class GameItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Game
        # 出力したいフィールド名をタプルで(括弧とカンマ)で定義します。
        fields = ('game_name', 'genre', 'detail', 'image', 'tags', 'platform')
        depth = 1

class TalkItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Talk
        # 出力したいフィールド名をタプルで(括弧とカンマ)で定義します。
        fields = '__all__'

class TalkroomItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Talkroom
        fields = ('game', 'recruit_platform', 'recruit_num', 'recruit_gender', 'recruit_context', )

class InquiryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Inquiry
        # 出力したいフィールド名をタプルで(括弧とカンマ)で定義します。
        fields = ('inquiry_title', 'inquiry_context')

class GuestConfirmationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Talkroom
        # 出力したいフィールド名をタプルで(括弧とカンマ)で定義します。
        fields = ('id','game','recruit_platform','recruit_context')
        depth=1
    
#class Tallkroom(serializers.ModelSerializer):
  #  class Meta:
 #       model = models.Talkroom
#        fields = ('talktext')
