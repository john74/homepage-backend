from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import (
    Bookmark,
)
from bookmarks.serializers import (
    BookmarkSerializer,
)
from users.models import User
from users.serializers import UserSerializer



class UserSettingsListAPIView(APIView):

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.user.id).first()
        if not user:
            return Response(data={"error": "No user found"}, status=status.HTTP_200_OK)

        serialized_user = UserSerializer(user).data
        user_id = user.id

        all_bookmarks = Bookmark.objects.filter(user=user_id)
        serialized_bookmarks = BookmarkSerializer(all_bookmarks, many=True).data

        response_data = {
            "user": serialized_user,
            "bookmarks": serialized_bookmarks
        }

        return Response(data=response_data, status=status.HTTP_200_OK)
