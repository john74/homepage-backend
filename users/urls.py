from django.urls import path

from . import views


app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUpAPIView.as_view(), name="signup"),
    path('signin/', views.SignInAPIView.as_view(), name="signin"),
]