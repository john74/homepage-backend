from collections import defaultdict
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer
from bookmarks.utils import group_bookmarks


class BookmarkBulkDeleteAPIView(APIView):
    serializer_class = BookmarkSerializer

    def delete(self, request, *args, **kwargs):
        bookmark_ids = request.data.get('ids', [])

        # Fetch all bookmarks
        all_bookmarks = Bookmark.objects.all()

        # Filter bookmarks to be deleted
        bookmarks_to_delete = all_bookmarks.filter(id__in=bookmark_ids)
        bookmarks_to_delete.delete()

        # Exclude the deleted categories from the original queryset and serialize the remaining categories
        all_bookmarks = all_bookmarks.exclude(id__in=bookmarks_to_delete.values('id'))
        serialized_bookmarks = self.serializer_class(all_bookmarks, many=True).data
        grouped_bookmarks = group_bookmarks(serialized_bookmarks)
        response_data = {'bookmarks': grouped_bookmarks}
        return Response(data=response_data, status=status.HTTP_200_OK)
