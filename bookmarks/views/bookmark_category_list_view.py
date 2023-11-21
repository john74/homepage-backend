from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import BookmarkCategory
from bookmarks.serializers import BookmarkCategorySerializer
from bookmarks.utils import group_bookmark_categories


class BookmarkCategoryListAPIView(APIView):
    bookmark_category_serializer_class = BookmarkCategorySerializer

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        all_categories = BookmarkCategory.objects.filter(user=user_id)
        serialized_categories = self.bookmark_category_serializer_class(all_categories, many=True).data
        grouped_categories = group_bookmark_categories(user_id, serialized_categories)
        response_data = {'categories': grouped_categories}
        return Response(data=response_data, status=status.HTTP_200_OK)