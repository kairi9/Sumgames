from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # 出力したいフィールド名をタプルで(括弧とカンマ)で定義します。
        fields = ('username','password', 'first_name', 'last_name', 'email', 'gender')

