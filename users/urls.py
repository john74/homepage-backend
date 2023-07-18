from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from . import views


app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUpAPIView.as_view(), name="signup"),
    path('signin/', views.SignInAPIView.as_view(), name="signin"),
    path('sign-out/', views.SignOutAPIView.as_view(), name="sign_out"),
    path('refresh-token/', TokenRefreshView.as_view(), name="refresh_token"),
]