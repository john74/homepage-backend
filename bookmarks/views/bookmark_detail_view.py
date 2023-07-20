from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer


class BookmarkDetailAPIView(APIView):
    serializer_class = BookmarkSerializer

    def get(self, request, bookmark_id, *args, **kwargs):
        try:
            bookmark = Bookmark.objects.get(id=bookmark_id)
        except (Bookmark.DoesNotExist, ValidationError):
            return Response(data={"errors":"Bookmark not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(bookmark)
        return Response(data=serializer.data, status=status.HTTP_200_OK)