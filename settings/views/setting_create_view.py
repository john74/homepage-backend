from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from settings.models import Setting
from settings.serializers import SettingSerializer


class SettingCreateAPIView(APIView):
    serializer_class = SettingSerializer

    def post(self, request, *args, **kwargs):
        if Setting.objects.exists():
            return Response(data={'errors':"Setting exists. Cannot add another one"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)