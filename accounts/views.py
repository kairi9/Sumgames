from rest_framework import viewsets
from . import serializers
# Create your views here.

class UserInfoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    def get_queryset(self):
        return [self.request.user]