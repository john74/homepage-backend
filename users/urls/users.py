from django.urls import path

from users import views


app_name = "users"

urlpatterns = [
    path("sign-up/", views.SignUpAPIView.as_view(), name="sign_up"),
    path("sign-in/", views.SignInAPIView.as_view(), name="sign_in"),
    path("sign-out/", views.SignOutAPIView.as_view(), name="sign_out"),
    path("refresh-token/", views.RefreshTokenAPIView.as_view(), name="refresh_token"),
]