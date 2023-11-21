from django.urls import path

from frontend import views


app_name = "frontend"

urlpatterns = [
    path("home/", views.HomeListAPIView.as_view(), name="home"),
    path("weather/", views.WeatherAPIView.as_view(), name="weather"),
]