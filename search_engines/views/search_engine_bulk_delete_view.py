from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from search_engines.models import SearchEngine
from search_engines.serializers import SearchEngineSerializer


class SearchEngineBulkDeleteAPIView(APIView):

    def delete(self, request, *args, **kwargs):
        search_engine_ids = request.data

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
        serialized_search_engines = SearchEngineSerializer(all_search_engines, many=True).data

        response_data = {
            "search_engines": serialized_search_engines,
        }

        return Response(data=response_data, status=status.HTTP_200_OK)
