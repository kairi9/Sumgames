from django.urls import path
from rest_framework import routers
from . import views


app_name = 'matching'
router = routers.DefaultRouter()
router.register(r'gameitem', views.GameViewSet,basename='gameitem')
router.register(r'talkroom', views.TalkroomViewSet,basename='talkroom')
router.register(r'inquiry', views.InquiryViewSet,basename='inquiry')
