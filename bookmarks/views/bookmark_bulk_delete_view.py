from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import Bookmark


class BookmarkBulkDeleteAPIView(APIView):

    def delete(self, request, *args, **kwargs):
        bookmark_ids = request.data.get('ids', [])
        if not bookmark_ids:
            return Response({'message': 'No IDs provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bookmarks = Bookmark.objects.filter(id__in=bookmark_ids)
        except ValidationError as error:
            return Response(data={"message":error}, status=status.HTTP_400_BAD_REQUEST)

        if not bookmarks:
            return Response({'message': 'No bookmarks found'}, status=status.HTTP_400_BAD_REQUEST)

        for bookmark in bookmarks:
            bookmark.delete()

        return Response(data={"message":"bookmarks deleted"}, status=status.HTTP_200_OK)
