from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer, ShortcutSerializer
from bookmarks.utils import group_bookmarks


class ShortcutBulkDeleteAPIView(APIView):
    bookmark_serializer_class = BookmarkSerializer
    shortcut_serializer_class = ShortcutSerializer

    def delete(self, request, *args, **kwargs):
        shortcut_ids = request.data.get('ids', [])

        if not shortcut_ids:
            return Response(data={"error": "No shortcut found"}, status=status.HTTP_400_BAD_REQUEST)

        user_id = request.user.id
        # Fetch all bookmarks
        all_bookmarks = Bookmark.objects.filter(user=user_id)
        # Filter shortcuts to be soft deleted
        try:
            shortcuts_to_delete = all_bookmarks.filter(id__in=shortcut_ids)
        except (ValidationError) as error:
            return Response(data={"error": "No shortcut found"}, status=status.HTTP_400_BAD_REQUEST)

        if not shortcuts_to_delete:
            return Response(data={"error": "No shortcut found"}, status=status.HTTP_400_BAD_REQUEST)

        shortcuts_to_delete.update(is_shortcut=False)

        # Exclude the soft deleted shortcuts from all_bookmarks queryset.
        excluded_shortcuts = all_bookmarks.exclude(id__in=shortcuts_to_delete.values('id'))
        # Filter the remaining records to get only the shortcuts.
        all_shortcuts = excluded_shortcuts.filter(is_shortcut=True)
        serialized_shortcuts = self.shortcut_serializer_class(all_shortcuts, many=True).data

        # Combine shortcuts_to_delete queryset with all_bookmarks, keeping only unique records.
        # That way we update the original all_bookmarks queryset with all the bookmarks that had their is_shortcut attribute set to False.
        # It eliminates the need for an additional database query to retrieve all bookmarks.
        all_bookmarks = shortcuts_to_delete.union(all_bookmarks).order_by("created_at")
        serialized_bookmarks = self.bookmark_serializer_class(all_bookmarks, many=True).data
        grouped_bookmarks = group_bookmarks(serialized_bookmarks)

        response_data = {
            "message": "Shortcut deleted successfully.",
            "bookmarks": grouped_bookmarks,
            "shortcuts": serialized_shortcuts
        }

        return Response(data=response_data, status=status.HTTP_200_OK)