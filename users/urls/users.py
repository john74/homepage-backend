from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from users import views


app_name = "users"

urlpatterns = [
    path("sign-up/", views.SignUpAPIView.as_view(), name="sign_up"),
    path("sign-in/", views.SignInAPIView.as_view(), name="sign_in"),
    path("sign-out/", views.SignOutAPIView.as_view(), name="sign_out"),
    path("refresh-token/", TokenRefreshView.as_view(), name="refresh_token"),
]