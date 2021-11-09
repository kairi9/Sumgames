from django.db.models.query import QuerySet
from . import models
from rest_framework import viewsets
from . import serializers
# Create your views here.

""" class GameViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Game.objects.all()[:10]
    serializer_class = serializers.GameItemSerializer """
    
class GameViewSet(viewsets.ModelViewSet):
    queryset = models.Game.objects.all()[:3]
    serializer_class = serializers.GameItemSerializer
    """ def get_queryset(self):
        game = models.Game.objects.get(game_name = self.request.user)
        return models.Game.objects.all(game = game.id) """

class TalkroomViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.TalkItemSerializer
    def get_queryset(self):
        talkroom = models.Talkroom.objects.get(users_ID=self.request.user)
        return models.Talk.objects.filter(talkroom=talkroom.id)

class HostViewSet(viewsets.ModelViewSet):
    queryset = models.Talkroom.objects.all()[:1]
    serializer_class = serializers.TalkroomItemSerializer
    

class InquiryViewSet(viewsets.ModelViewSet):
    serializers_class = serializers.InquiryItemSerializer
    def get_queryset(self):
        inquiry = models.Inquiry.objects.get(users_ID=self.request.user)
        return models.Inquiry.objects.filter(inquiry=inquiry.id)

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


