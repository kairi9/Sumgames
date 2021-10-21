from django.urls import path

from . import views


app_name = 'matching'
urlpatterns = [
    path('', views.TopPageView.as_view(), name="top")
]
