from django.urls import path
from rest_framework import routers
from . import views


app_name = 'matching_app'
router = routers.DefaultRouter()
router.register(r'gameitem', views.GameViewSet,basename='gameitem')
router.register(r'talk', views.TalkViewSet,basename='talk')
router.register(r'talkroom', views.TalkroomViewSet,basename='talkroom')
router.register(r'inquiry', views.InquiryViewSet,basename='inquiry')

urlpatterns = [
    path('',views.TopPageView.as_view(),name="index"),
]
