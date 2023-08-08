from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from commons.utils import format_error_message
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
            serializer.create(serializer.validated_data)
            return Response(
                data={
                    "message": "User created successfully",
                    "status": status.HTTP_201_CREATED,
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        error = format_error_message(serializer.errors)
        return Response(
            data={
                "message": error,
                "status": status.HTTP_400_BAD_REQUEST
            },
            status=status.HTTP_400_BAD_REQUEST
        )
