from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import BookmarkSubCategory
from bookmarks.serializers import BookmarkSubCategorySerializer
from bookmarks.utils import group_bookmarks


class BookmarkSubCategoryBulkDeleteAPIView(APIView):
    sub_category_serializer_class = BookmarkSubCategorySerializer

    def delete(self, request, *args, **kwargs):
        sub_category_ids = request.data.get('ids', [])

        if not sub_category_ids:
            return Response(data={"error": "No subcategory found"}, status=status.HTTP_400_BAD_REQUEST)

        user_id = request.user.id
        all_sub_categories = BookmarkSubCategory.objects.filter(user=user_id)

        try:
            sub_categories_to_delete = all_sub_categories.filter(id__in=sub_category_ids)
        except (ValidationError) as error:
            return Response(data={"error": "No subcategory found"}, status=status.HTTP_400_BAD_REQUEST)

        if not sub_categories_to_delete:
            return Response(data={"error": "No subcategory found"}, status=status.HTTP_400_BAD_REQUEST)

        sub_categories_to_delete.delete()

        # Exclude the deleted bookmarks from the original queryset
        all_sub_categories = all_sub_categories.exclude(id__in=sub_categories_to_delete.values('id'))
        serialized_sub_categories = self.sub_category_serializer_class(all_sub_categories, many=True).data
        grouped_sub_categories = group_bookmarks(serialized_sub_categories)

        response_data = {
            "message": "Subcategories deleted successfully.",
            "sub_categories": grouped_sub_categories,
        }

        return Response(data=response_data, status=status.HTTP_200_OK)
