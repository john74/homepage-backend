from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from base.utils import get_serializer_error
from bookmarks.models import BookmarkSubCategory
from bookmarks.serializers import BookmarkSubCategorySerializer
from bookmarks.utils import group_bookmarks


class BookmarkSubCategoryBulkUpdateAPIView(APIView):
    bookmark_sub_category_serializer_class = BookmarkSubCategorySerializer

    def put(self, request, *args, **kwargs):
        user_id = request.user.id
        sub_categories = [
            {**sub_category, "user": user_id} for sub_category in request.data
        ]
        for sub_category in sub_categories:
            try:
                sub_category_obj = BookmarkSubCategory.objects.get(user=user_id, id=sub_category['id'])
            except (BookmarkSubCategory.DoesNotExist, KeyError):
                return Response(data={"error": "Subcategory not found"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.bookmark_sub_category_serializer_class(instance=sub_category_obj, data=sub_category)
            if not serializer.is_valid():
                error = get_serializer_error(serializer.errors)
                return Response(data={"error": error}, status=status.HTTP_400_BAD_REQUEST)

            serializer.update(sub_category_obj, serializer.validated_data)

        all_sub_categories = BookmarkSubCategory.objects.filter(user=user_id)
        serialized_sub_categories = self.bookmark_sub_category_serializer_class(all_sub_categories, many=True).data
        grouped_sub_categories = group_bookmarks(serialized_sub_categories)

        response_data = {
            "message": "Subcategories updated successfully.",
            "sub_categories": grouped_sub_categories,
        }

        return Response(data=response_data, status=status.HTTP_200_OK)
