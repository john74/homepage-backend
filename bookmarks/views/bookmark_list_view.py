from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer
from bookmarks.utils import group_bookmarks


class BookmarkListAPIView(APIView):
    bookmark_serializer_class = BookmarkSerializer

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        bookmarks = Bookmark.objects.filter(user=user_id)
        serialized_bookmarks = self.bookmark_serializer_class(bookmarks, many=True).data

        grouped_bookmarks = group_bookmarks(serialized_bookmarks)
        response_data = {'bookmarks': grouped_bookmarks}
        return Response(data=response_data, status=status.HTTP_200_OK)