from collections import defaultdict

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer


class BookmarkListAPIView(APIView):
    serializer_class = BookmarkSerializer

    def get(self, request, *args, **kwargs):
        bookmarks = Bookmark.objects.all()
        serializer = self.serializer_class(bookmarks, many=True)

        # Group the data by the 'category' field
        grouped_data = defaultdict(list)
        for item in serializer.data:
            category = list(item.keys())[0]
            grouped_data[category].append(item[category])

        return Response(data=grouped_data, status=status.HTTP_200_OK)