from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class SignOutAPIView(APIView):
    """
    Logs out the currently authenticated user by deleting the 'refreshToken'
    from the response's HTTP cookies.
    """
    def post(self, request):
        response = Response()
        response.delete_cookie(key='refreshToken')
        return Response({'message': 'Successfully signed out'}, status=status.HTTP_200_OK)