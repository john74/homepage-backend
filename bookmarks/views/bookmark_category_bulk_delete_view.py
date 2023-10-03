from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import BookmarkCategory
from bookmarks.serializers import BookmarkCategorySerializer


class BookmarkCategoryBulkDeleteAPIView(APIView):
    serializer_class = BookmarkCategorySerializer

    def delete(self, request, *args, **kwargs):
        category_ids = request.data.get('ids', [])

        # Fetch all categories
        all_categories = BookmarkCategory.objects.all()

        # Filter categories to be deleted
        categories_to_delete = all_categories.filter(id__in=category_ids)
        categories_to_delete.delete()

        # Exclude the deleted categories from the original queryset and serialize the remaining categories
        all_categories = all_categories.exclude(id__in=categories_to_delete.values('id'))
        serialized_categories = self.serializer_class(all_categories, many=True).data
        response_data = {'categories': serialized_categories}
        return Response(data=response_data, status=status.HTTP_200_OK)

