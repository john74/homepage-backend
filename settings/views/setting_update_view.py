from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from settings.models import Setting
from settings.serializers import SettingSerializer


class SettingUpdateAPIView(APIView):
    setting_serializer_class = SettingSerializer

    def put(self, request, *args, **kwargs):
        setting = Setting.objects.first()
        if not setting:
            return Response(data={'errors':"No setting to update"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.setting_serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.update(setting, serializer.validated_data)
            setting = Setting.objects.first()
            serialized_setting = self.setting_serializer_class(setting).data
            response_data = {'settings': serialized_setting}
            return Response(data=response_data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)