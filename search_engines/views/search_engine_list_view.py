from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from search_engines.models import SearchEngine
from search_engines.serializers import SearchEngineSerializer


class SearchEngineListAPIView(APIView):
    search_engine_serializer = SearchEngineSerializer

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        engines = SearchEngine.objects.filter(user=user_id)
        default_engine = engines.filter(is_default=True).first()
        non_default_engines = engines.filter(is_default=False)

        serialized_default_engine = self.search_engine_serializer(default_engine).data
        serialized_non_default_engines = self.search_engine_serializer(non_default_engines, many=True).data

        response_data = {
            "default": serialized_default_engine,
            "nonDefault": serialized_non_default_engines,
        }
        return Response(data=response_data, status=status.HTTP_200_OK)