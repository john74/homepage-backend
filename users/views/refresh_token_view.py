from django.conf import settings

from decouple import config
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView


class RefreshTokenAPIView(TokenRefreshView):

    def post(self, request):
        access_token = super().post(request).data["access"]
        response = Response()
        response.set_cookie(key='thikeeAccessToken', value=str(access_token), httponly=True, expires=int(config("ACCESS_TOKEN_LIFETIME")), path='/')
        response.status = status.HTTP_200_OK
        return response
