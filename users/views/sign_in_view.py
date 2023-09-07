from datetime import datetime

from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.utils import create_jwt_pair_for_user


class SignInAPIView(APIView):
    """
    Authenticates the user and returns an access token and
    a refresh token, set as HTTP-only, upon successful authentication.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        user = authenticate(email=data.get('email'), password=data.get('password'))

        # in case we don't delete the users but deactivate them
        if not user or not user.is_active:
            return Response(
                data={
                    "message": "Invalid credentials",
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        tokens = create_jwt_pair_for_user(user)
        response = Response()

        response.set_cookie(key='refreshToken', value=tokens['refresh'], httponly=True)
        response.set_cookie(key='accessToken', value=tokens['access'], httponly=True)

        response.data = {
            "last_login": user.last_login,
        }
        response.status = status.HTTP_200_OK

        user.last_login = datetime.now()
        user.save()
        return response