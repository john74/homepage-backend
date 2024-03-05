from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import BookmarkCategory, Bookmark
from bookmarks.serializers import BookmarkCategorySerializer


class BookmarkCategoryBulkDeleteAPIView(APIView):

    def delete(self, request, *args, **kwargs):
        category_ids = request.data

        if not category_ids:
            return Response(data={"error": "No bookmark categories found"}, status=status.HTTP_400_BAD_REQUEST)

        user_id = request.user.id
        # Fetch all categories
        all_categories = BookmarkCategory.objects.filter(user=user_id)

        # Filter categories to be deleted
        try:
            categories_to_delete = all_categories.filter(id__in=category_ids)
        except (ValidationError) as error:
            return Response(data={"error": "No bookmark category found"}, status=status.HTTP_400_BAD_REQUEST)

        if not categories_to_delete:
            return Response(data={"error": "No bookmark category found"}, status=status.HTTP_400_BAD_REQUEST)

        categories_to_delete.delete()

        # Exclude categories that need to be deleted from the original 'all_categories' queryset
        all_categories = BookmarkCategory.objects.filter(user=user_id)
        serialized_categories = BookmarkCategorySerializer(all_categories, many=True).data

        response_data = {
            "bookmark_categories": serialized_categories,
        }

        return Response(data=response_data, status=status.HTTP_200_OK)

