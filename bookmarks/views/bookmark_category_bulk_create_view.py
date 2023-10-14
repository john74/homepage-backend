from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import BookmarkCategory
from bookmarks.serializers import BookmarkCategorySerializer
from bookmarks.utils import group_bookmark_categories


class BookmarkCategoryBulkCreateAPIView(APIView):
    bookmark_category_serializer = BookmarkCategorySerializer

    def post(self, request, *args, **kwargs):
        categories = request.data
        serializer = self.bookmark_category_serializer(data=categories, many=True)

        if not serializer.is_valid():
            return Response(data={}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        all_bookmark_categories = BookmarkCategory.objects.all()
        serialized_categories = self.bookmark_category_serializer(all_bookmark_categories, many=True).data
        grouped_categories = group_bookmark_categories(serialized_categories)

        response_data = {'categories': grouped_categories}
        return Response(data=response_data, status=status.HTTP_200_OK)
