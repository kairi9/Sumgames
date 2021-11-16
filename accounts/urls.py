from django.urls import path
from rest_framework import routers
from . import views


app_name = 'accounts'
urlpatterns = [
    path('api-token-auth/', views.CustomAuthToken.as_view())
]
router = routers.DefaultRouter()
router.register(r'user', views.UserInfoViewSet,basename='user')

urlpatterns += router.urls