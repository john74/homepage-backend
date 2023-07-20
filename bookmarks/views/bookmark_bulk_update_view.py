from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkUpdateSerializer


class BookmarkBulkUpdateAPIView(APIView):
    serializer_class = BookmarkUpdateSerializer

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

            serializer = self.serializer_class(data=bookmark)
            if serializer.is_valid():
                updated_bookmark = serializer.update(bookmark_obj, serializer.validated_data)
                updated_bookmarks.append(updated_bookmark)
            else:
                for field, message in serializer.errors.items():
                    errors.append(f'{field} {message[0].lower()}')

        if not errors:
            return Response(data=updated_bookmarks, status=status.HTTP_200_OK)

        if len(errors) < len(bookmarks):
            return Response(data={'bookmarks':updated_bookmarks, 'errors':errors}, status=status.HTTP_206_PARTIAL_CONTENT)

        return Response(data={'errors':errors}, status=status.HTTP_400_BAD_REQUEST)
