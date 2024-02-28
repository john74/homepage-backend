from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer


class ShortcutBulkCreateAPIView(APIView):
    """
    API endpoint for bulk creation of shortcuts.

    Accepts a list of bookmark IDs and sets their 'is_shortcut' property to True.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for creating shortcuts from bookmarks.

        :return: Response data with the bookmarks or error message.
        """
        bookmark_ids_list = request.data

        if not bookmark_ids_list:
            return Response(data={"error": "No bookmark ids provided"}, status=status.HTTP_400_BAD_REQUEST)

        user_id = request.user.id

        # Fetch only the bookmarks that are currently requested.
        # The condition is_shortcut=False acts as a safeguard to prevent fetching bookmarks
        # that are already shortcuts, even if their IDs were mistakenly included in request.data.
        try:
            non_shortcut_bookmarks = Bookmark.objects.filter(user=user_id, id__in=bookmark_ids_list, is_shortcut=False)
        except (ValidationError) as error:
            return Response(data={"error": error}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure that the update operation is only performed if bookmarks meeting the previous criteria are found.
        if non_shortcut_bookmarks:
            non_shortcut_bookmarks.update(is_shortcut=True)

        all_bookmarks = Bookmark.objects.filter(user=user_id).order_by("created_at")
        serialized_bookmarks = BookmarkSerializer(all_bookmarks, many=True).data

        response_data = {
            "bookmarks": serialized_bookmarks,
        }

        return Response(data=response_data, status=status.HTTP_200_OK)