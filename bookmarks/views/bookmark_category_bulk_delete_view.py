from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import BookmarkCategory, Bookmark
from bookmarks.serializers import BookmarkCategorySerializer, ShortcutSerializer
from bookmarks.utils import group_bookmark_categories


class BookmarkCategoryBulkDeleteAPIView(APIView):
    bookmark_category_serializer = BookmarkCategorySerializer
    shortcut_serializer = ShortcutSerializer

    def delete(self, request, *args, **kwargs):
        category_ids = request.data.get('ids', [])

        # Fetch all categories
        all_categories = BookmarkCategory.objects.all()

        # Filter categories to be deleted
        categories_to_delete = all_categories.filter(id__in=category_ids)
        categories_to_delete.delete()

        # Exclude categories that need to be deleted from the original 'all_categories' queryset
        all_categories = all_categories.exclude(id__in=categories_to_delete.values('id'))
        serialized_categories = self.bookmark_category_serializer(all_categories, many=True).data
        grouped_categories = group_bookmark_categories(serialized_categories)

        all_shortcuts = Bookmark.objects.filter(is_shortcut=True).order_by("created_at")
        serialized_shortcuts = self.shortcut_serializer(all_shortcuts, many=True).data

        response_data = {'categories': grouped_categories, 'shortcuts': serialized_shortcuts}
        return Response(data=response_data, status=status.HTTP_200_OK)

