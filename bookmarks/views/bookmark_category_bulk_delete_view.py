from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import BookmarkCategory, Bookmark
from bookmarks.serializers import BookmarkCategorySerializer, ShortcutSerializer
from bookmarks.utils import group_bookmark_categories


class BookmarkCategoryBulkDeleteAPIView(APIView):
    bookmark_category_serializer_class = BookmarkCategorySerializer
    shortcut_serializer_class = ShortcutSerializer

    def delete(self, request, *args, **kwargs):
        category_ids = request.data.get('ids', [])

        if not category_ids:
            return Response(data={"error": "No bookmark categories found"}, status=status.HTTP_400_BAD_REQUEST)

        user_id = request.user.id
        # Fetch all categories
        all_categories = BookmarkCategory.objects.filter(user=user_id)

        # Filter categories to be deleted
        try:
            categories_to_delete = all_categories.filter(id__in=category_ids)
        except (ValidationError) as error:
            return Response(data={"error": "No bookmark category found"}, status=status.HTTP_400_BAD_REQUEST)

        if not categories_to_delete:
            return Response(data={"error": "No bookmark category found"}, status=status.HTTP_400_BAD_REQUEST)

        categories_to_delete.delete()

        # Exclude categories that need to be deleted from the original 'all_categories' queryset
        all_categories = all_categories.exclude(id__in=categories_to_delete.values('id'))
        serialized_categories = self.bookmark_category_serializer_class(all_categories, many=True).data
        grouped_categories = group_bookmark_categories(user_id, serialized_categories)

        all_shortcuts = Bookmark.objects.filter(is_shortcut=True).order_by("created_at")
        serialized_shortcuts = self.shortcut_serializer_class(all_shortcuts, many=True).data

        response_data = {
            "message": "Bookmark category deleted successfully.",
            "categories": grouped_categories,
            "shortcuts": serialized_shortcuts
        }

        return Response(data=response_data, status=status.HTTP_200_OK)

