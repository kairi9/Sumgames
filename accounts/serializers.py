from rest_framework import serializers
from matching_app.models import Talkroom
from .models import CustomUser,ExpoPushToken
from django.db import IntegrityError

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

class ExpoPushTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpoPushToken
        # 出力したいフィールド名をタプルで(括弧とカンマ)で定義します。
        fields = ['expo_token']

    def create(self, validated_data):
        user = self.context['userID']
        try:
            token = ExpoPushToken.objects.get(user=user)
            token.expo_token = validated_data['expo_token']
            token.save()
        except ExpoPushToken.DoesNotExist:
            token = ExpoPushToken(
                user = user,
                expo_token = validated_data['expo_token']
            )
            token.save()
        try:
            talkroom = Talkroom.objects.get(host_user = user.pk)
        except Talkroom.DoesNotExist:
            talkroom = Talkroom.objects.get(guest_user__pk = user.pk)
        talkroom.expo_tokens.add(token)
        talkroom.save()
        return token
    
    def update(self, instance, validated_data):
        instance.expo_token = validated_data.get('expo_token', instance.expo_token)
        instance.save()
        return instance
