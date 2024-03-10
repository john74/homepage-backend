from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from base.utils import get_serializer_error
from search_engines.models import SearchEngine
from search_engines.serializers import SearchEngineSerializer


class SearchEngineBulkCreateAPIView(APIView):

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        search_engines = [
            {**engine, "user": user_id} for engine in request.data
        ]

        serializer = SearchEngineSerializer(data=search_engines, many=True, partial=True)
        if not serializer.is_valid():
            error = get_serializer_error(serializer.errors)
            return Response(data={"error": error}, status=status.HTTP_400_BAD_REQUEST)

        SearchEngine.objects.bulk_create([
            SearchEngine(**engine) for engine in serializer.validated_data
        ])

        all_search_engines = SearchEngine.objects.filter(user=user_id)
        default_search_engines = all_search_engines.filter(is_default=True)
        if len(default_search_engines) > 1:
            new_default_engine = default_search_engines.latest("created_at")
            rest_default_engines = default_search_engines.exclude(id=new_default_engine.id)
            rest_default_engines.update(is_default=False)

        all_search_engines = SearchEngine.objects.filter(user=user_id)
        serialized_search_engines = SearchEngineSerializer(all_search_engines, many=True).data

        response_data = {
            "search_engines": serialized_search_engines,
        }

        return Response(data=response_data, status=status.HTTP_200_OK)