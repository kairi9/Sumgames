from typing import Counter
from django.db.models.query import QuerySet
from django.db.models import Count
from rest_framework.response import Response
from . import models
from rest_framework import viewsets
from . import serializers
# Create your views here.

#たける
class GameViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.GameItemSerializer
    def get_queryset(self):
        # game_id = self.kwargs['id']
        return models.Game.objects.all()[:10]
    
    def talk_ratio(self):
        talkroom_people = models.Talkroom.objects.all().aggregate(Count('users_ID'))
        all_talkroom = models.Talkroom.objects.count()
        ratio_data = {
            "all":talkroom_people,
            "host":all_talkroom,
        }
        return ratio_data
    
    def retrieve(self, request, pk=None):
        queryset = models.Game.objects.get(pk=pk)
        ratio_data = self.talk_ratio()
        serializer = serializers.GameItemSerializer(queryset,context={"host_ratio":ratio_data["host"],"all_count":ratio_data["all"]})
        return Response(serializer.data)

#たける
class Talk(viewsets.ModelViewSet):
    pass

#宋
class TalkroomViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TalkItemSerializer
    def get_queryset(self):
        talkroom = models.Talkroom.objects.get(users_ID=self.request.user)
        return models.Talk.objects.filter(talkroom=talkroom.id)

    def create(self,request):
        pass

#宋
class InquiryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.InquiryItemSerializer
    def get_queryset(self):
        inquiry = models.Inquiry.objects.filter(userID=self.request.user)
        return inquiry

#宋
class GuestConfirmationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.GuestConfirmationItemSerializer
    def get_queryset(self):
        user = self.request.user
        gender = user.gender
        if gender == "EX":
            queryset = models.Talkroom.objects.filter(under_recruitment=True,recruit_gender="AL")
        elif gender =="FE":
            queryset = models.Talkroom.objects.filter(under_recruitment=True).exclude(recruit_gender="MA")
        else:
            queryset = models.Talkroom.objects.filter(under_recruitment=True).exclude(recruit_gender="FE")
        return queryset


