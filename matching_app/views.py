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