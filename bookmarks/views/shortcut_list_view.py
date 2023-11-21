from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import Bookmark
from bookmarks.serializers import ShortcutSerializer


class ShortcutListAPIView(APIView):
    shortcut_serializer_class = ShortcutSerializer

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        shortcuts = Bookmark.objects.filter(user=user_id, is_shortcut=True)
        serializer = self.shortcut_serializer_class(shortcuts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)