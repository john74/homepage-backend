from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from base.utils import get_serializer_error
from bookmarks.models import BookmarkCategory
from bookmarks.serializers import BookmarkCategorySerializer


class BookmarkCategoryBulkCreateAPIView(APIView):

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        categories = [
            {**category, "user": user_id} for category in request.data
        ]
        serializer = BookmarkCategorySerializer(data=categories, many=True)

        if not serializer.is_valid():
            error = get_serializer_error(serializer.errors)
            return Response(data={"error": error}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        all_bookmark_categories = BookmarkCategory.objects.filter(user=user_id)
        serialized_categories = BookmarkCategorySerializer(all_bookmark_categories, many=True).data

        response_data = {
            "bookmark_categories": serialized_categories
        }

        return Response(data=response_data, status=status.HTTP_200_OK)
