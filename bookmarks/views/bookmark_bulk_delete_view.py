from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer, ShortcutSerializer
from bookmarks.utils import group_bookmarks


class BookmarkBulkDeleteAPIView(APIView):
    bookmark_serializer = BookmarkSerializer
    shortcut_serializer = ShortcutSerializer

    def delete(self, request, *args, **kwargs):
        bookmark_ids = request.data.get('ids', [])

        if not bookmark_ids:
            return Response(data={"error": "No bookmark found"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch all bookmarks
        all_bookmarks = Bookmark.objects.all()

        # Filter bookmarks to be deleted
        bookmarks_to_delete = all_bookmarks.filter(id__in=bookmark_ids)
        bookmarks_to_delete.delete()

        # Exclude the deleted bookmarks from the original queryset
        all_bookmarks = all_bookmarks.exclude(id__in=bookmarks_to_delete.values('id'))
        serialized_bookmarks = self.bookmark_serializer(all_bookmarks, many=True).data
        grouped_bookmarks = group_bookmarks(serialized_bookmarks)

        shortcuts = all_bookmarks.filter(is_shortcut=True)
        serialized_shortcuts = self.shortcut_serializer(shortcuts, many=True).data

        response_data = {
            "message": "Bookmark deleted successfully.",
            "bookmarks": grouped_bookmarks,
            "shortcuts": serialized_shortcuts
        }

        return Response(data=response_data, status=status.HTTP_200_OK)
