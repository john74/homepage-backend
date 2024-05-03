from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from settings.models import Setting
from settings.serializers import SettingSerializer


class SettingUpdateAPIView(APIView):

    def put(self, request, *args, **kwargs):
        user_id = request.user.id
        setting = Setting.objects.filter(user=user_id).first()
        if not setting:
            return Response(data={'errors':"No setting to update"}, status=status.HTTP_400_BAD_REQUEST)

        request.data["user"] = user_id
        serializer = SettingSerializer(data=request.data)
        if serializer.is_valid():
            updated_setting = serializer.update(setting, serializer.validated_data)
            serialized_setting = SettingSerializer(updated_setting).data
            response_data = {
                "settings": serialized_setting
            }
            return Response(data=response_data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)