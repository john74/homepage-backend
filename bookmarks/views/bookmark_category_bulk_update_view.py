from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import BookmarkCategory
from bookmarks.serializers import BookmarkCategorySerializer


class BookmarkCategoryBulkUpdateAPIView(APIView):
    serializer_class = BookmarkCategorySerializer

    def put(self, request, *args, **kwargs):
        categories = request.data
        updated_categories = []
        errors = []

        for category in categories:
            if 'id' not in category or not category['id']:
                errors.append(f"id not provided for {category}")
                continue

            try:
                category_obj = BookmarkCategory.objects.get(id=category['id'])
            except (BookmarkCategory.DoesNotExist, ValidationError):
                errors.append(f"{category['id']} is not a valid id")
                continue

            serializer = self.serializer_class(data=category)
            if serializer.is_valid():
                updated_category = serializer.update(category_obj, serializer.validated_data)
                updated_categories.append(updated_category)
            else:
                for field, message in serializer.errors.items():
                    errors.append(f'{field} {message[0].lower()}')

        if not errors:
            return Response(data={'categories':updated_categories}, status=status.HTTP_200_OK)

        if len(errors) < len(categories):
            return Response(data={'categories':updated_categories, 'errors':errors}, status=status.HTTP_206_PARTIAL_CONTENT)

        return Response(data={'errors':errors}, status=status.HTTP_400_BAD_REQUEST)
