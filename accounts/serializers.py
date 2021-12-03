from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # 出力したいフィールド名をタプルで(括弧とカンマ)で定義します。
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'gender','introduction','image')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            gender=validated_data['gender']
        )
        user.set_password(validated_data['password'])
        user.save()
        self.user=user
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.introduction = validated_data.get('introduction', instance.introduction)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance

class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # 出力したいフィールド名をタプルで(括弧とカンマ)で定義します。
        fields = ['password']
        extra_kwargs = {'password': {'write_only': True}}