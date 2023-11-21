from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer, ShortcutSerializer
from bookmarks.utils import group_bookmarks


class BookmarkBulkDeleteAPIView(APIView):
    bookmark_serializer_class = BookmarkSerializer
    shortcut_serializer_class = ShortcutSerializer

    def delete(self, request, *args, **kwargs):
        bookmark_ids = request.data.get('ids', [])

        if not bookmark_ids:
            return Response(data={"error": "No bookmark found"}, status=status.HTTP_400_BAD_REQUEST)

        user_id = request.user.id
        # Fetch all bookmarks
        all_bookmarks = Bookmark.objects.filter(user=user_id)

        # Filter bookmarks to be deleted
        try:
            bookmarks_to_delete = all_bookmarks.filter(id__in=bookmark_ids)
        except (ValidationError) as error:
            return Response(data={"error": "No bookmark found"}, status=status.HTTP_400_BAD_REQUEST)

        if not bookmarks_to_delete:
            return Response(data={"error": "No bookmark found"}, status=status.HTTP_400_BAD_REQUEST)

        bookmarks_to_delete.delete()

        # Exclude the deleted bookmarks from the original queryset
        all_bookmarks = all_bookmarks.exclude(id__in=bookmarks_to_delete.values('id'))
        serialized_bookmarks = self.bookmark_serializer_class(all_bookmarks, many=True).data
        grouped_bookmarks = group_bookmarks(serialized_bookmarks)

        shortcuts = all_bookmarks.filter(is_shortcut=True)
        serialized_shortcuts = self.shortcut_serializer_class(shortcuts, many=True).data

        response_data = {
            "message": "Bookmark deleted successfully.",
            "bookmarks": grouped_bookmarks,
            "shortcuts": serialized_shortcuts
        }

        return Response(data=response_data, status=status.HTTP_200_OK)
