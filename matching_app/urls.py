from django.urls import path

from . import views


app_name = 'matching'
urlpatterns = [
    path('', views.TopPageView.as_view(), name="top"),
    path('',views.LoginView.as_view(),name="login"),
    path('',views.SignupView.as_view(),name="signup"),
    path('',views.PasswordView.as_view(),name="password"),
    path('',views.VerificationView.as_view(),name="verification"),
    path('',views.HostformView.as_view(),name="hostform"),
    path('',views.GameView.as_view(),name="game"),
    path('',views.GuestconfirmationView.as_view(),name="guestconfirmation"),
    path('',views.TalkroomView.as_view(),name="talkroom"),
    path('',views.NftindexView.as_view(),name="index"),
    path('',views.NftdoneView.as_view(),name="done"),
    path('',views.ProfileView.as_view(),name="profile"),
    path('',views.Profile_editView.as_view(),name="profile_edit"),
]
