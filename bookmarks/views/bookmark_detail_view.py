from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer


class BookmarkDetailAPIView(APIView):
    bookmark_serializer_class = BookmarkSerializer

    def get(self, request, bookmark_id, *args, **kwargs):
        user_id = request.user.id
        bookmark = Bookmark.objects.filter(user=user_id, id=bookmark_id).first()
        if not bookmark:
            return Response(data={"errors":"Bookmark not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.bookmark_serializer_class(bookmark)
        return Response(data=serializer.data, status=status.HTTP_200_OK)