from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from base.utils import get_serializer_error
from settings.models import Setting
from settings.serializers import SettingSerializer


class SettingCreateAPIView(APIView):
    setting_serializer_class = SettingSerializer

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        if Setting.objects.filter(user=user_id):
            return Response(data={"errors": "Setting exists. Cannot add another one"}, status=status.HTTP_400_BAD_REQUEST)

        request.data["user"] = user_id
        serializer = self.setting_serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"message": "Setting created successfully"}, status=status.HTTP_200_OK)

        error = get_serializer_error(serializer.errors)
        return Response(data={"error": error}, status=status.HTTP_400_BAD_REQUEST)