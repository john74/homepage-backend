from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer


class BookmarkBulkCreateAPIView(APIView):
    serializer_class = BookmarkSerializer

    def post(self, request, *args, **kwargs):
        bookmarks = request.data
        created_bookmarks = []
        errors = []

        for bookmark in bookmarks:
            serializer = self.serializer_class(data=bookmark)
            if serializer.is_valid():
                created_bookmark = serializer.save(serializer.validated_data)
                created_bookmarks.append(created_bookmark)
            else:
                for field, message in serializer.errors.items():
                    errors.append({'message':f'{field} {message[0].lower()}', 'bookmark':bookmark})

        if not errors:
            return Response(data=created_bookmarks, status=status.HTTP_200_OK)

        if len(errors) < len(bookmarks):
            return Response(data={'bookmarks':created_bookmarks, 'errors':errors}, status=status.HTTP_206_PARTIAL_CONTENT)

        return Response(data={'errors':errors}, status=status.HTTP_400_BAD_REQUEST)
