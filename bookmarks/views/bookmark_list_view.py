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
        return Response(data=serializer.data, status=status.HTTP_200_OK)