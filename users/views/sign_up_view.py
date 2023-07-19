from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.serializers import UserSerializer


class SignUpAPIView(generics.GenericAPIView):
    """
    Creates and saves a new user to the database if the request data
    is valid.
    """
    permission_classes = [AllowAny,]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "User created successfully",
                "data": serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data={"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
