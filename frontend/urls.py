from django.urls import path

from . import views


app_name = 'frontend'

urlpatterns = [
    path('home/', views.HomeListAPIView.as_view(), name="home"),
]