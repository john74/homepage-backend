from collections import defaultdict

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer


class BookmarkBulkCreateAPIView(APIView):
    serializer_class = BookmarkSerializer

    def post(self, request, *args, **kwargs):
        bookmarks = request.data
        created_bookmarks = []
        errors = []

        for bookmark_data in bookmarks:
            serializer = self.serializer_class(data=bookmark_data)
            try:
                serializer.is_valid(raise_exception=True)
                created_bookmark = serializer.save(serializer.validated_data)
                created_bookmarks.append(created_bookmark)
            except ValidationError as e:
                errors.append({'message': str(e), 'bookmark': bookmark_data})

        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

        # Group the data by the 'category' field
        grouped_data = defaultdict(list)
        for item in created_bookmarks:
            category = list(item.keys())[0]
            grouped_data[category].append(item[category])

        return Response({'bookmarks': grouped_data}, status=status.HTTP_201_CREATED)
