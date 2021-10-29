from rest_framework import serializers
from . import models

class GameItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Game
        # 出力したいフィールド名をタプルで(括弧とカンマ)で定義します。
        #fields = ('id', 'game_name', 'genre', 'detail', 'image', 'tags', 'platform')
        exclude = ['update_at']
        depth = 1

class TalkItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Talk
        # 出力したいフィールド名をタプルで(括弧とカンマ)で定義します。
        fields = '__all__'