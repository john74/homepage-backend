from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import Bookmark
from bookmarks.serializers import ShortcutSerializer


class ShortcutListAPIView(APIView):
    serializer_class = ShortcutSerializer

    def get(self, request, *args, **kwargs):
        shortcuts = Bookmark.objects.filter(is_shortcut=True)
        serializer = self.serializer_class(shortcuts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)