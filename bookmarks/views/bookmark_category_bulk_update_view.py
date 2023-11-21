from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from base.utils import get_serializer_error
from bookmarks.models import BookmarkCategory
from bookmarks.serializers import BookmarkCategorySerializer
from bookmarks.utils import group_bookmark_categories


class BookmarkCategoryBulkUpdateAPIView(APIView):
    bookmark_category_serializer_class = BookmarkCategorySerializer

    def put(self, request, *args, **kwargs):
        categories = request.data
        user_id = request.user.id
        categories = [
            {**category, "user": user_id} for category in request.data
        ]

        for category in categories:
            try:
                category_obj = BookmarkCategory.objects.get(id=category['id'])
            except (BookmarkCategory.DoesNotExist, KeyError):
                return Response(data={"error": "Category not found"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.bookmark_category_serializer_class(instance=category_obj, data=category)
            if not serializer.is_valid():
                error = get_serializer_error(serializer.errors)
                return Response(data={"error": error}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

        # Retrieve all categories
        all_categories = BookmarkCategory.objects.filter(user=user_id)
        serialized_categories = self.bookmark_category_serializer_class(all_categories, many=True).data
        grouped_categories = group_bookmark_categories(user_id, serialized_categories)

        response_data = {
            "message": "Category updated successfully.",
            "categories": grouped_categories
        }

        return Response(data=response_data, status=status.HTTP_200_OK)

