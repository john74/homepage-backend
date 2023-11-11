from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.serializers import UserSerializer
from base.utils import get_serializer_error


class SignUpAPIView(generics.GenericAPIView):
    """
    Creates and saves a new user to the database if the request data
    is valid.
    """
    permission_classes = [AllowAny,]
    user_serializer_class = UserSerializer

    def post(self, request):
        serializer = self.user_serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(data={"message": "Your account has been created successfully"}, status=status.HTTP_201_CREATED)

        error = get_serializer_error(serializer.errors);
        return Response(data={"error": error}, status=status.HTTP_400_BAD_REQUEST)
