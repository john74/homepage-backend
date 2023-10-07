from collections import defaultdict

from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer


class BookmarkBulkUpdateAPIView(APIView):
    serializer_class = BookmarkSerializer

    def put(self, request, *args, **kwargs):
        bookmarks = request.data
        updated_bookmarks = []
        errors = []

        for bookmark in bookmarks:
            if 'id' not in bookmark or not bookmark['id']:
                errors.append(f"id not provided for {bookmark}")
                continue

            try:
                bookmark_obj = Bookmark.objects.get(id=bookmark['id'])
            except (Bookmark.DoesNotExist, ValidationError):
                errors.append(f"{bookmark['id']} is not a valid id")
                continue

            serializer = self.serializer_class(instance=bookmark_obj, data=bookmark)
            if serializer.is_valid():
                serializer.update(bookmark_obj, serializer.validated_data)
            else:
                for field, message in serializer.errors.items():
                    errors.append(f'{field} {message[0].lower()}')

        # Group the data by the 'category' field
        grouped_data = defaultdict(list)
        all_bookmarks = Bookmark.objects.all()
        serialized_bookmarks = self.serializer_class(all_bookmarks, many=True).data
        for item in serialized_bookmarks:
            category = list(item.keys())[0]
            grouped_data[category].append(item[category])

        return Response(data={'bookmarks': grouped_data}, status=status.HTTP_200_OK)
