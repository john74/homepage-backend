from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import (
    Bookmark, BookmarkCategory, BookmarkSubCategory,
)
from bookmarks.serializers import (
    BookmarkSerializer, BookmarkCategorySerializer,
    BookmarkSubCategorySerializer,
)
from users.models import User
from users.serializers import UserSerializer



class UserSettingsListAPIView(APIView):

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.user.id).first()
        if not user:
            return Response(data={"error": "No user found"}, status=status.HTTP_400_BAD_REQUEST)

        serialized_user = UserSerializer(user).data
        user_id = user.id

        all_bookmarks = Bookmark.objects.filter(user=user_id)
        serialized_bookmarks = BookmarkSerializer(all_bookmarks, many=True).data

        all_bookmark_categories = BookmarkCategory.objects.filter(user=user_id)
        serialized_categories = BookmarkCategorySerializer(all_bookmark_categories, many=True).data

        all_bookmark_sub_categories = BookmarkSubCategory.objects.filter(user=user_id)
        serialized_sub_categories = BookmarkSubCategorySerializer(all_bookmark_sub_categories, many=True).data

        response_data = {
            "user": serialized_user,
            "bookmarks": serialized_bookmarks,
            "bookmark_categories": serialized_categories,
            "bookmark_sub_categories": serialized_sub_categories,
        }

        return Response(data=response_data, status=status.HTTP_200_OK)
