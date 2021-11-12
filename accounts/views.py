from rest_framework import viewsets
from . import serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import permission_classes
# Create your views here.

class UserInfoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer

    def list(self, request):
        queryset = self.request.user
        serializer = serializers.UserSerializer(queryset)
        return Response(serializer.data)

    @permission_classes([IsAdminUser])
    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        serializer = serializers.UserSerializer(queryset)
        return Response(serializer.data)

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass