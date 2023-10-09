from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import Bookmark
from bookmarks.serializers import ShortcutSerializer

class ShortcutBulkDeleteAPIView(APIView):
    serializer_class = ShortcutSerializer

    def delete(self, request, *args, **kwargs):
        shortcut_ids = request.data.get('ids', [])

        # Fetch all shortcuts
        all_shortcuts = Bookmark.objects.filter(is_shortcut=True)

        # Filter shortcuts to be deleted
        shortcuts_to_delete = all_shortcuts.filter(id__in=shortcut_ids)
        shortcuts_to_delete.update(is_shortcut=False)

        # Exclude the deleted shortcuts from the original queryset and serialize the remaining shortcuts
        all_shortcuts = all_shortcuts.exclude(id__in=shortcuts_to_delete.values('id'))
        serialized_shortcuts = self.serializer_class(all_shortcuts, many=True).data

        response_data = {'shortcuts': serialized_shortcuts}
        return Response(data=response_data, status=status.HTTP_200_OK)
