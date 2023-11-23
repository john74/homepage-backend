from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import BookmarkSubCategory
from bookmarks.serializers import BookmarkSubCategorySerializer
from bookmarks.utils import group_bookmarks


class BookmarkSubCategoryListAPIView(APIView):
    bookmark_sub_category_serializer_class = BookmarkSubCategorySerializer

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        sub_categories = BookmarkSubCategory.objects.filter(user=user_id)
        if not sub_categories:
            return Response(data={"error": "No subcategories found"}, status=status.HTTP_200_OK)

        serialized_sub_categories = self.bookmark_sub_category_serializer_class(sub_categories, many=True).data
        grouped_sub_categories = group_bookmarks(serialized_sub_categories)

        response_data = {"sub_categories": grouped_sub_categories}
        return Response(data=response_data, status=status.HTTP_200_OK)