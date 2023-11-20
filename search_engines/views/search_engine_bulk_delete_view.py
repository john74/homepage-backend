from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from search_engines.models import SearchEngine
from search_engines.serializers import SearchEngineSerializer


class SearchEngineBulkDeleteAPIView(APIView):
    search_engine_serializer_class = SearchEngineSerializer

    def delete(self, request, *args, **kwargs):
        search_engine_ids = request.data.get('ids', [])

        if not search_engine_ids:
            return Response(data={"error": "No search engine found"}, status=status.HTTP_400_BAD_REQUEST)

        user_id = request.user.id
        all_search_engines = SearchEngine.objects.filter(user=user_id)

        try:
            search_engines_to_delete = all_search_engines.filter(id__in=search_engine_ids)
        except (ValidationError) as error:
            return Response(data={"error": "No search engine found"}, status=status.HTTP_400_BAD_REQUEST)

        if not search_engines_to_delete:
            return Response(data={"error": "No search engine found"}, status=status.HTTP_400_BAD_REQUEST)

        search_engines_to_delete.delete()

        all_search_engines = all_search_engines.exclude(id__in=search_engines_to_delete.values('id'))
        default_engine = all_search_engines.get(is_default=True)
        non_default_engines = all_search_engines.filter(is_default=False)

        serialized_default_engine = self.search_engine_serializer_class(default_engine).data
        serialized_non_default_engines = self.search_engine_serializer_class(non_default_engines, many=True).data

        response_data = {
            "message": "Search engine deleted successfully.",
            "default": serialized_default_engine,
            "nonDefault": serialized_non_default_engines,
        }

        return Response(data=response_data, status=status.HTTP_200_OK)
