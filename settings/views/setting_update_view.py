from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from settings.models import Setting
from settings.serializers import SettingSerializer


class SettingUpdateAPIView(APIView):
    serializer_class = SettingSerializer

    def put(self, request, *args, **kwargs):
        setting = Setting.objects.first()
        if not setting:
            return Response(data={'errors':"No setting to update"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.update(setting, serializer.validated_data)
            return Response(status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)