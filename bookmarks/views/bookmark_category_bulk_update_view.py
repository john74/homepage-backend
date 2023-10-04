from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import BookmarkCategory
from bookmarks.serializers import BookmarkCategorySerializer
from bookmarks.utils import group_bookmark_categories


class BookmarkCategoryBulkUpdateAPIView(APIView):
    serializer_class = BookmarkCategorySerializer

    def put(self, request, *args, **kwargs):
        categories = request.data
        updated_categories = []
        errors = []

        for category_data in categories:
            if 'id' not in category_data or not category_data['id']:
                errors.append(f"id not provided for {category_data}")
                continue

            try:
                category_obj = BookmarkCategory.objects.get(id=category_data['id'])
            except (BookmarkCategory.DoesNotExist, ValidationError):
                errors.append(f"{category_data['id']} is not a valid id")
                continue

            serializer = self.serializer_class(instance=category_obj, data=category_data)
            if serializer.is_valid():
                serializer.save()
                updated_categories.append(serializer.data)
            else:
                errors.extend(serializer.errors)

        # Retrieve all categories
        all_categories = BookmarkCategory.objects.all()
        serialized_categories = self.serializer_class(all_categories, many=True).data
        grouped_categories = group_bookmark_categories(serialized_categories)
        response_data = {'categories': grouped_categories, 'errors': errors}

        if errors:
            status_code = status.HTTP_400_BAD_REQUEST
        elif updated_categories:
            status_code = status.HTTP_200_OK
        else:
            status_code = status.HTTP_204_NO_CONTENT

        return Response(data=response_data, status=status_code)

