from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import (
    Bookmark, BookmarkCategory,
)
from bookmarks.serializers import (
    BookmarkSerializer, BookmarkCategorySerializer,
    ShortcutSerializer,
)
from bookmarks.utils import (
    group_bookmarks, group_bookmark_categories,
)
from search_engines.models import SearchEngine
from search_engines.serializers import SearchEngineSerializer
from frontend.utils import retrieve_weather_data


class HomeListAPIView(APIView):
    bookmark_serializer_class = BookmarkSerializer
    bookmark_category_serializer_class = BookmarkCategorySerializer
    shortcut_serializer_class = ShortcutSerializer
    search_engine_serializer_class = SearchEngineSerializer

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        weather_data = retrieve_weather_data(user_id=user_id)

        all_bookmarks = Bookmark.objects.filter(user=user_id)
        serialized_bookmarks = self.bookmark_serializer_class(all_bookmarks, many=True).data
        grouped_bookmarks = group_bookmarks(serialized_bookmarks)

        all_bookmark_categories = BookmarkCategory.objects.filter(user=user_id)
        serialized_categories = self.bookmark_category_serializer_class(all_bookmark_categories, many=True).data
        grouped_categories = group_bookmark_categories(serialized_categories)

        all_shortcuts = all_bookmarks.filter(is_shortcut=True)
        serialized_shortcuts = self.shortcut_serializer_class(all_shortcuts, many=True).data

        all_search_engines = SearchEngine.objects.filter(user=user_id)
        default_engine = all_search_engines.get(is_default=True)
        non_default_engines = all_search_engines.filter(is_default=False)

        serialized_default_engine = self.search_engine_serializer_class(default_engine).data
        serialized_non_default_engines = self.search_engine_serializer_class(non_default_engines, many=True).data

        response_data = {
            'bookmarks': grouped_bookmarks,
            'categories': grouped_categories,
            'shortcuts': serialized_shortcuts,
            'search_engines': {
                "default": serialized_default_engine,
                "nonDefault": serialized_non_default_engines,
            },
            "weather": weather_data,
        }

        return Response(data=response_data, status=status.HTTP_200_OK)
