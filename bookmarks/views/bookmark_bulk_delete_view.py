from collections import defaultdict
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer


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

        # Group the data by the 'category' field
        grouped_data = defaultdict(list)
        for item in serialized_bookmarks:
            category = list(item.keys())[0]
            grouped_data[category].append(item[category])

        response_data = {'bookmarks': grouped_data}
        return Response(data=response_data, status=status.HTTP_200_OK)
