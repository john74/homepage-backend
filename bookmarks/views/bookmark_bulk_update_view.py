from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from base.utils import get_serializer_error
from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer, ShortcutSerializer
from bookmarks.utils import group_bookmarks


class BookmarkBulkUpdateAPIView(APIView):
    bookmark_serializer_class = BookmarkSerializer
    shortcut_serializer_class = ShortcutSerializer

    def put(self, request, *args, **kwargs):
        user_id = request.user.id
        bookmarks = [
            {**bookmark, "user": user_id} for bookmark in request.data
        ]
        for bookmark in bookmarks:
            try:
                bookmark_obj = Bookmark.objects.get(user=user_id, id=bookmark['id'])
            except (Bookmark.DoesNotExist, KeyError):
                return Response(data={"error": "Bookmark not found"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.bookmark_serializer_class(instance=bookmark_obj, data=bookmark)
            if not serializer.is_valid():
                error = get_serializer_error(serializer.errors)
                return Response(data={"error": error}, status=status.HTTP_400_BAD_REQUEST)

            serializer.update(bookmark_obj, serializer.validated_data)

        all_bookmarks = Bookmark.objects.filter(user=user_id)
        serialized_bookmarks = self.bookmark_serializer_class(all_bookmarks, many=True).data
        grouped_bookmarks = group_bookmarks(serialized_bookmarks)

        shortcuts = all_bookmarks.filter(is_shortcut=True)
        serialized_shortcuts = self.shortcut_serializer_class(shortcuts, many=True).data

        response_data = {
            "message": "Bookmark updated successfully.",
            "bookmarks": grouped_bookmarks,
            "shortcuts": serialized_shortcuts
        }

        return Response(data=response_data, status=status.HTTP_200_OK)
