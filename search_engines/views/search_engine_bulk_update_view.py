from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from base.utils import get_serializer_error
from search_engines.models import SearchEngine
from search_engines.serializers import SearchEngineSerializer


class SearchEngineBulkUpdateAPIView(APIView):

    def put(self, request, *args, **kwargs):
        user_id = request.user.id
        all_search_engines = SearchEngine.objects.filter(user=user_id)
        updated_engines = []

        for engine in request.data:
            try:
                instance = all_search_engines.get(id=engine['id'])
            except (SearchEngine.DoesNotExist, ValidationError, KeyError) as error:
                return Response(data={"error": "Search engine not found"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = SearchEngineSerializer(data=engine, partial=True)
            if not serializer.is_valid():
                error = get_serializer_error(serializer.errors)
                return Response(data={"error": error}, status=status.HTTP_400_BAD_REQUEST)

            updated_engine = serializer.update(instance, serializer.validated_data)
            updated_engines.append(updated_engine)

        unchanged_engines = []
        for engine in all_search_engines:
            if engine not in updated_engines:
                unchanged_engines.append(engine)

        all_search_engines = unchanged_engines + updated_engines
        serialized_search_engines = SearchEngineSerializer(all_search_engines, many=True).data

        response_data = {
            "search_engines": serialized_search_engines,
        }

        return Response(data=response_data, status=status.HTTP_200_OK)
