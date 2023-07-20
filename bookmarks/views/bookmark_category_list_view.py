from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import BookmarkCategory
from bookmarks.serializers import BookmarkCategorySerializer


class BookmarkCategoryListAPIView(APIView):
    serializer_class = BookmarkCategorySerializer

    def get(self, request, *args, **kwargs):
        categories = BookmarkCategory.objects.all()
        serializer = self.serializer_class(categories, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)