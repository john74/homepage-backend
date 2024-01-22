from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class SignOutAPIView(APIView):
    """
    Signs out the currently authenticated user by setting refresh and access tokens with empty values
    and an expiration date of the current datetime minus 100 seconds. This action prompts the browser
    to consider them as expired cookies, leading to their deletion.
    """
    def post(self, request):
        response = Response()
        response.set_cookie(key='thikeeRefreshToken', value="", httponly=True, expires=-100)
        response.set_cookie(key='thikeeAccessToken', value="", httponly=True, expires=-100)
        response.status = status.HTTP_200_OK
        return response