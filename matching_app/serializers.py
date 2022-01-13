from django.db.models import fields
from rest_framework import serializers
from drf_base64.serializers import ModelSerializer
from . import models
from accounts.models import CustomUser

class GameItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Game
        # 出力したいフィールド名をタプルで(括弧とカンマ)で定義します。
        exclude = ['update_at']
        depth = 1

class TalkItemSerializer(ModelSerializer):
    class Meta:
        model = models.Talk
        # 出力したいフィールド名をタプルで(括弧とカンマ)で定義します。
        fields = '__all__'
        extra_kwargs = {
            'talkroom': {'read_only': True},
            'user': {'read_only': True},
            'send_at': {'read_only': True}
        }
    
    def create(self, validated_data):
        talk = models.Talk(
            talktext = validated_data['talktext'],
            talkfile = validated_data['talkfile'],
        )
        talk.user = self.context['userID']
        talk.talkroom = self.context['talkroom']
        talk.save()
        return talk

class TalkroomTinderUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username','image')

class TalkroomTinderSerializer(serializers.ModelSerializer):
    game = serializers.StringRelatedField()
    recruit_platform = serializers.StringRelatedField(many=True)
    host_user = TalkroomTinderUserSerializer()
    guest_user = TalkroomTinderUserSerializer(many=True)
    class Meta:
        model = models.Talkroom
        fields = ('id','game', 'recruit_platform', 'recruit_num', 'recruit_gender', 'recruit_context','host_user','guest_user')
        extra_kwargs = {
            'id': {'read_only': True},
            'host_user': {'read_only': True},
            'guest_user': {'read_only': True},
        }

class TalkroomItemSerializer(serializers.ModelSerializer):
    game = serializers.StringRelatedField()
    recruit_platform = serializers.StringRelatedField(many=True)
    host_user = TalkroomUserSerializer(read_only=True)
    guest_user = TalkroomUserSerializer(many=True,read_only=True)
    class Meta:
        model = models.Talkroom
        fields = ('id','game', 'recruit_platform', 'recruit_num', 'recruit_gender', 'recruit_context','host_user','guest_user')
        extra_kwargs = {
            'id': {'read_only': True},
            'host_user': {'read_only': True},
            'guest_user': {'read_only': True},
        }

    def create(self, validated_data):
        talkroom = models.Talkroom(
            game = validated_data['game'],
            recruit_num = validated_data['recruit_num'],
            recruit_gender = validated_data['recruit_gender'],
            recruit_context = validated_data['recruit_context'],
            host_user = self.context['userID']
        )
        talkroom.save()
        recruit_platform = validated_data['recruit_platform']
        for platform in recruit_platform:
            talkroom.recruit_platform.add(platform)
        return talkroom

    def update(self, instance, validated_data):
        instance.recruit_num = validated_data.get('recruit_num',instance.recruit_num)
        instance.recruit_gender = validated_data.get('recruit_gender',instance.recruit_gender)
        instance.recruit_context = validated_data.get('recruit_context',instance.recruit_context)
        recruit_platform = [models.Platform.objects.get(platform_name=x) for x in validated_data.get('recruit_platform',instance.recruit_platform)]
        instance.recruit_platform.set(recruit_platform)
        instance.save()
        return instance


class InquiryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Inquiry
        # 出力したいフィールド名をタプルで(括弧とカンマ)で定義します。
        fields = ('inquiry_title','inquiry_context')

    def create(self, validated_data):
        inquiry = models.Inquiry(
            inquiry_title = validated_data['inquiry_title'],
            inquiry_context = validated_data['inquiry_context'] 
        )
        inquiry.userID = self.context['userID']
        inquiry.save()
        return inquiry

