from rest_framework import serializers
from . import models

class GameItemSerializer(serializers.ModelSerializer):
    # host_ratio = serializers.IntegerField(read_only=True)
    # all_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = models.Game
        # 出力したいフィールド名をタプルで(括弧とカンマ)で定義します。
        exclude = ['update_at']
        depth = 1

class TalkItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Talk
        # 出力したいフィールド名をタプルで(括弧とカンマ)で定義します。
        fields = '__all__'

class TalkroomItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Talkroom
        fields = ('id','game', 'recruit_platform', 'recruit_num', 'recruit_gender', 'recruit_context')

    def create(self, validated_data):
        talkroom = models.Talkroom(
            game = validated_data['game'],
           
            recruit_num = validated_data['recruit_num'],
            recruit_gender = validated_data['recruit_gender'],
            recruit_context = validated_data['recruit_context']
        )
        talkroom.save()
        recruit_platform = validated_data['recruit_platform']
        for platform in recruit_platform:
            talkroom.recruit_platform.add(platform)
        talkroom.users_ID.add(self.context['userID'])
        
        return talkroom

    def update(self, instance, validated_data):
        instance.recruit_num = validated_data.get('recruit_num',instance.recruit_num)
        instance.recruit_gender = validated_data.get('recruit_gender',instance.recruit_gender)
        instance.recruit_context = validated_data.get('recruit_context',instance.recruit_context)
        recruit_platform = [models.Platform.objects.get(platform_name=x) for x in validated_data.get('recruit_platform',instance.recruit_platform)]
        instance.recruit_platform.set(recruit_platform)
        instance.users_ID.add(self.context['userID'])
        users_num = instance.users_ID.all().count()
        if users_num >= instance.recruit_num+1:
            instance.under_recruitment = False
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

