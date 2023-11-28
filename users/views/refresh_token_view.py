from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView


class RefreshTokenAPIView(TokenRefreshView):

    def post(self, request):
        response = super().post(request)
        response_data = {
            "accessToken": response.data["access"],
            "access_token_lifetime": settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
        }
        return Response(data=response_data, status=status.HTTP_200_OK)
