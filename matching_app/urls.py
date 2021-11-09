from django.urls import path
from rest_framework import routers
from . import views


app_name = 'matching'
# urlpatterns = [
#     path('', views.TopPageView.as_view(), name="top"),
#     path('verification/',views.VerificationView.as_view(),name="verification"),
#     path('hostform/',views.HostformView.as_view(),name="hostform"),
#     path('game/',views.GameView.as_view(),name="game"),
#     #test
#     path('game/ranking/',views.Test.as_view(),name="get_game"),
#     path('guestconfirmation/',views.GuestconfirmationView.as_view(),name="guestconfirmation"),
#     path('talkroom/',views.TalkroomView.as_view(),name="talkroom"),
#     path('nft-index/',views.NftindexView.as_view(),name="index"),
#     path('nft-done/',views.NftdoneView.as_view(),name="done"),
#     path('profile/',views.ProfileView.as_view(),name="profile"),
#     path('profile_edit/',views.Profile_editView.as_view(),name="profile_edit"),
# ]
router = routers.DefaultRouter()
router.register(r'gameitem', views.GameViewSet,basename='gameitem')
router.register(r'talkitem', views.TalkroomViewSet,basename='talkitem')
router.register(r'inquiry', views.InquiryViewSet,basename='InquiryItemSerializeritem')
router.register(r'guestconfirmationitem',views.GuestConfirmationViewSet,basename='guestconfirmationitem')