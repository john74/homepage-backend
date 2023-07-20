from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import BookmarkCategory


class BookmarkCategoryBulkDeleteAPIView(APIView):

    def delete(self, request, *args, **kwargs):
        category_ids = request.data.get('ids', [])
        if not category_ids:
            return Response({'message': 'No IDs provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            categories = BookmarkCategory.objects.filter(id__in=category_ids)
        except ValidationError as error:
            return Response(data={"message":error}, status=status.HTTP_400_BAD_REQUEST)

        if not categories:
            return Response({'message': 'No bookmark categories found'}, status=status.HTTP_400_BAD_REQUEST)

        for category in categories:
            category.delete()

        return Response(data={"message":"bookmark categories deleted"}, status=status.HTTP_200_OK)
