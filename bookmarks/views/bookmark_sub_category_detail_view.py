from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import BookmarkSubCategory
from bookmarks.serializers import BookmarkSubCategorySerializer


class BookmarkSubCategoryDetailAPIView(APIView):
    bookmark_sub_category_serializer_class = BookmarkSubCategorySerializer

    def get(self, request, id, *args, **kwargs):
        user_id = request.user.id
        sub_category = BookmarkSubCategory.objects.filter(user=user_id, id=id).first()
        if not sub_category:
            return Response(data={"errors": "Subcategory not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.bookmark_sub_category_serializer_class(sub_category)
        return Response(data=serializer.data, status=status.HTTP_200_OK)