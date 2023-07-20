from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import Bookmark


class ShortcutBulkDeleteAPIView(APIView):

    def delete(self, request, *args, **kwargs):
        shortcut_ids = request.data.get('ids', [])
        if not shortcut_ids:
            return Response({'message': 'No IDs provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            shortcuts = Bookmark.objects.filter(id__in=shortcut_ids, is_shortcut=True)
        except ValidationError as error:
            return Response(data={"message":error}, status=status.HTTP_400_BAD_REQUEST)

        if not shortcuts:
            return Response({'message': 'No shortcuts found'}, status=status.HTTP_400_BAD_REQUEST)

        for shortcut in shortcuts:
            shortcut.is_shortcut = False
            shortcut.save()

        return Response(data={"message":"shortcuts deleted"}, status=status.HTTP_200_OK)
