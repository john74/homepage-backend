from django.urls import path

from settings import views


app_name = "settings"

urlpatterns = [
    path("create/", views.SettingCreateAPIView.as_view(), name="create"),
    path("update/", views.SettingUpdateAPIView.as_view(), name="update"),
]