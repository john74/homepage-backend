from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from base.utils import get_serializer_error
from bookmarks.models import BookmarkCategory
from bookmarks.serializers import BookmarkCategorySerializer


class BookmarkCategoryBulkUpdateAPIView(APIView):

    def put(self, request, *args, **kwargs):

        user_id = request.user.id
        categories = [
            {**category, "user": user_id} for category in request.data
        ]

        for category in categories:
            try:
                category_obj = BookmarkCategory.objects.get(id=category['id'])
            except (BookmarkCategory.DoesNotExist, KeyError):
                return Response(data={"error": "Category not found"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = BookmarkCategorySerializer(instance=category_obj, data=category)
            if not serializer.is_valid():
                error = get_serializer_error(serializer.errors)
                return Response(data={"error": error}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

        # Retrieve all categories
        all_categories = BookmarkCategory.objects.filter(user=user_id)
        serialized_categories = BookmarkCategorySerializer(all_categories, many=True).data

        response_data = {
            "bookmark_categories": serialized_categories
        }

        return Response(data=response_data, status=status.HTTP_200_OK)

