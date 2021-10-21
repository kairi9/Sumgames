from django.urls import path

from . import views


app_name = 'matching'
urlpatterns = [
    path('', views.TopPageView.as_view(), name="top"),
    path('login/',views.LoginView.as_view(),name="login"),
    path('signup/',views.SignupView.as_view(),name="signup"),
    path('password/',views.PasswordView.as_view(),name="password"),
    path('verification/',views.VerificationView.as_view(),name="verification"),
    path('hostform/',views.HostformView.as_view(),name="hostform"),
    path('game/',views.GameView.as_view(),name="game"),
    path('guestconfirmation/',views.GuestconfirmationView.as_view(),name="guestconfirmation"),
    path('talkroom/',views.TalkroomView.as_view(),name="talkroom"),
    path('nft-index/',views.NftindexView.as_view(),name="index"),
    path('nft-done/',views.NftdoneView.as_view(),name="done"),
    path('profile/',views.ProfileView.as_view(),name="profile"),
    path('profile_edit/',views.Profile_editView.as_view(),name="profile_edit"),
]
