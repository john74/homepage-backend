from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import BookmarkCategory
from bookmarks.serializers import BookmarkCategorySerializer


class BookmarkCategoryDetailAPIView(APIView):
    serializer_class = BookmarkCategorySerializer

    def get(self, request, category_id, *args, **kwargs):
        try:
            category = BookmarkCategory.objects.get(id=category_id)
        except (BookmarkCategory.DoesNotExist, ValidationError):
            return Response(data={"errors":"No category found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(category)
        return Response(data=serializer.data, status=status.HTTP_200_OK)