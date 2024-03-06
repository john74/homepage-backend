from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import BookmarkSubCategory
from bookmarks.serializers import BookmarkSubCategorySerializer


class BookmarkSubCategoryBulkDeleteAPIView(APIView):

    def delete(self, request, *args, **kwargs):
        sub_category_ids = request.data

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
        serialized_sub_categories = BookmarkSubCategorySerializer(all_sub_categories, many=True).data

        response_data = {
            "bookmark_sub_categories": serialized_sub_categories,
        }

        return Response(data=response_data, status=status.HTTP_200_OK)
