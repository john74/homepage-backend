from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import BookmarkCategory
from bookmarks.serializers import BookmarkCategorySerializer


class BookmarkCategoryDetailAPIView(APIView):
    bookmark_category_serializer_class = BookmarkCategorySerializer

    def get(self, request, category_id, *args, **kwargs):
        user_id = request.user.id
        category = BookmarkCategory.objects.filter(user=user_id, id=category_id).first()
        if not category:
            return Response(data={"errors":"No category found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.bookmark_category_serializer_class(category)
        return Response(data=serializer.data, status=status.HTTP_200_OK)