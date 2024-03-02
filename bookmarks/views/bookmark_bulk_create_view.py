from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from base.utils import get_serializer_error
from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer


class BookmarkBulkCreateAPIView(APIView):

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        bookmarks = [
            {**bookmark, "user": user_id} for bookmark in request.data
        ]
        serializer = BookmarkSerializer(data=bookmarks, many=True)
        if not serializer.is_valid():
            error = get_serializer_error(serializer.errors)
            return Response(data={"error": error}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        all_bookmarks = Bookmark.objects.filter(user=user_id)
        serialized_bookmarks = BookmarkSerializer(all_bookmarks, many=True).data

        response_data = {
            "bookmarks": serialized_bookmarks,
        }
        return Response(data=response_data, status=status.HTTP_201_CREATED)
