from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from base.utils import get_serializer_error
from bookmarks.models import BookmarkSubCategory
from bookmarks.serializers import BookmarkSubCategorySerializer


class BookmarkSubCategoryBulkCreateAPIView(APIView):

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        sub_categories = [
            {**sub_category, "user": user_id} for sub_category in request.data
        ]

        serializer = BookmarkSubCategorySerializer(data=sub_categories, many=True)
        if not serializer.is_valid():
            error = get_serializer_error(serializer.errors)
            return Response(data={"error": error}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        all_sub_categories = BookmarkSubCategory.objects.filter(user=user_id)
        serialized_sub_categories = BookmarkSubCategorySerializer(all_sub_categories, many=True).data

        response_data = {
            "bookmark_sub_categories": serialized_sub_categories,
        }
        return Response(data=response_data, status=status.HTTP_201_CREATED)
