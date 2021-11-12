from django.urls import path
from rest_framework import routers
from rest_framework.authtoken import views as auth_view
from . import views


app_name = 'accounts'
urlpatterns = [
    path('api-token-auth/', auth_view.obtain_auth_token)
]
router = routers.DefaultRouter()
router.register(r'user-info', views.UserInfoViewSet,basename='user-info')

urlpatterns += router.urls