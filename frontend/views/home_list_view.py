from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import (
    Bookmark, BookmarkCategory, BookmarkSubCategory
)
from bookmarks.serializers import (
    BookmarkSerializer, BookmarkCategorySerializer,
    ShortcutSerializer, BookmarkSubCategorySerializer
)
from bookmarks.utils import (
    group_bookmarks, group_bookmark_categories,
)
from frontend.utils import retrieve_weather_data
from search_engines.models import SearchEngine
from search_engines.serializers import SearchEngineSerializer
from settings.models import Setting
from settings.serializers import SettingSerializer
from users.models import User
from users.serializers import UserSerializer



class HomeListAPIView(APIView):
    bookmark_serializer_class = BookmarkSerializer
    bookmark_category_serializer_class = BookmarkCategorySerializer
    bookmark_sub_category_serializer_class = BookmarkSubCategorySerializer
    shortcut_serializer_class = ShortcutSerializer
    search_engine_serializer_class = SearchEngineSerializer
    user_serializer_class = UserSerializer
    setting_serializer_class = SettingSerializer

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.user.id).first()
        if not user:
            return Response(data={"error": "No user found"}, status=status.HTTP_200_OK)

        serialized_user = self.user_serializer_class(user).data
        user_id = user.id

        weather_data = retrieve_weather_data(user_id=user_id)

        all_bookmarks = Bookmark.objects.filter(user=user_id)
        serialized_bookmarks = self.bookmark_serializer_class(all_bookmarks, many=True).data
        grouped_bookmarks = group_bookmarks(serialized_bookmarks)

        all_bookmark_categories = BookmarkCategory.objects.filter(user=user_id)
        serialized_categories = self.bookmark_category_serializer_class(all_bookmark_categories, many=True).data
        grouped_categories = group_bookmark_categories(user_id, serialized_categories)

        all_bookmark_sub_categories = BookmarkSubCategory.objects.filter(user=user_id)
        serialized_sub_categories = self.bookmark_sub_category_serializer_class(all_bookmark_sub_categories, many=True).data
        grouped_sub_categories = group_bookmarks(serialized_sub_categories)

        all_shortcuts = all_bookmarks.filter(is_shortcut=True)
        serialized_shortcuts = self.shortcut_serializer_class(all_shortcuts, many=True).data

        all_search_engines = SearchEngine.objects.filter(user=user_id)
        default_engine = all_search_engines.get(is_default=True)
        non_default_engines = all_search_engines.filter(is_default=False)

        serialized_default_engine = self.search_engine_serializer_class(default_engine).data
        serialized_non_default_engines = self.search_engine_serializer_class(non_default_engines, many=True).data

        settings = Setting.objects.filter(user=user_id).first()
        serialized_settings = self.setting_serializer_class(settings).data

        response_data = {
            "user": serialized_user,
            "settings": serialized_settings,
            "bookmarks": grouped_bookmarks,
            "categories": grouped_categories,
            "sub_categories": grouped_sub_categories,
            "shortcuts": serialized_shortcuts,
            "search_engines": {
                "default": serialized_default_engine,
                "nonDefault": serialized_non_default_engines,
            },
            "weather": weather_data,
        }

        return Response(data=response_data, status=status.HTTP_200_OK)
