from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from base.utils import get_serializer_error
from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer, ShortcutSerializer
from bookmarks.utils import group_bookmarks


class BookmarkBulkCreateAPIView(APIView):
    bookmark_serializer = BookmarkSerializer
    shortcut_serializer = ShortcutSerializer

    def post(self, request, *args, **kwargs):
        bookmarks = request.data
        serializer = self.bookmark_serializer(data=bookmarks, many=True)
        if not serializer.is_valid():
            error = get_serializer_error(serializer.errors)
            return Response(data={"error": error}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        all_bookmarks = Bookmark.objects.all()
        serialized_bookmarks = self.bookmark_serializer(all_bookmarks, many=True).data
        grouped_bookmarks = group_bookmarks(serialized_bookmarks)

        shortcuts = all_bookmarks.filter(is_shortcut=True)
        serialized_shortcuts = self.shortcut_serializer(shortcuts, many=True).data

        response_data = {
            "message": "Bookmark created successfully.",
            "bookmarks": grouped_bookmarks,
            "shortcuts": serialized_shortcuts
        }
        return Response(data=response_data, status=status.HTTP_201_CREATED)
