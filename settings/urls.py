from django.urls import path

from . import views


app_name = 'settings'

urlpatterns = [
    path('create/', views.SettingCreateAPIView.as_view(), name="create"),
]