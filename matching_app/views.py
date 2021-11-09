from django.db.models.query import QuerySet
from . import models
from rest_framework import viewsets
from . import serializers
# Create your views here.

class GameViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Game.objects.all()[:10]
    serializer_class = serializers.GameItemSerializer

class TalkroomViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.TalkItemSerializer
    def get_queryset(self):
        talkroom = models.Talkroom.objects.get(users_ID=self.request.user)
        return models.Talk.objects.filter(talkroom=talkroom.id)

class InquiryViewSet(viewsets.ModelViewSet):
    pass

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


