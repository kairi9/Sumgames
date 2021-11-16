from rest_framework import viewsets,permissions
from . import serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.authtoken.models import Token
from .models import CustomUser
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
# Create your views here.

class IsAdminOrIsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user or request.user.is_superuser

#ログイン用
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = Token.objects.get(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
        })

#その他ユーザー周り
class UserInfoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'update':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request):
        queryset = request.user
        serializer = serializers.UserSerializer(queryset)
        return Response(serializer.data)

    def create(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        token = Token.objects.get(user=serializer.user)
        data = {
            'token': token.key,
            'user_id': token.user.id,
        }
        return Response(data)

    def retrieve(self, request, pk=None):
        queryset = CustomUser.objects.get(pk=pk)
        serializer = serializers.UserSerializer(queryset)
        return Response(serializer.data)

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        user = CustomUser.objects.get(pk=pk)
        serializer = serializers.UserSerializer(user,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        queryset = CustomUser.objects.get(pk=pk)
        data = queryset.delete()
        return Response(data)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrIsSelf])
    def set_password(self, request, pk=None):
        user = CustomUser.objects.get(pk=pk)
        serializer = serializers.PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response({'status': 'password set'})
