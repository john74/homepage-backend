from django.conf import settings
from django.contrib.auth import authenticate
from django.utils import timezone

from decouple import config
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class SignInAPIView(APIView):
    """
    Authenticates the user and returns an access token and
    a refresh token, set as HTTP-only, upon successful authentication.
    """
    permission_classes = [AllowAny,]

    def post(self, request):
        data = request.data
        user = authenticate(email=data.get('email'), password=data.get('password'))

        # in case we don't delete the users but deactivate them
        if not user or not user.is_active:
            return Response(data={"error": "Invalid credentials. Please check your email and password and try again."}, status=status.HTTP_401_UNAUTHORIZED)

        refresh_token = RefreshToken.for_user(user)

        response = Response()
        response.set_cookie(key='thikeeRefreshToken', value=str(refresh_token), httponly=True, expires=int(config("REFRESH_TOKEN_LIFETIME")))
        response.set_cookie(key='thikeeAccessToken', value=str(refresh_token.access_token), httponly=True, expires=int(config("ACCESS_TOKEN_LIFETIME")))

        response.data = {
            "username": user.username,
            "email": user.email,
            "last_login": user.last_login
        }
        response.status = status.HTTP_200_OK

        user.last_login = timezone.now()
        user.save()
        return response