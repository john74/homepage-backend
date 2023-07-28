from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from search_engines.models import SearchEngine
from search_engines.serializers import SearchEngineUpdateSerializer


class SearchEngineBulkUpdateAPIView(APIView):
    serializer_class = SearchEngineUpdateSerializer

    def put(self, request, *args, **kwargs):
        search_engines = request.data

        for engine in search_engines:
            serializer = self.serializer_class(data=engine)
            if serializer.is_valid():
                instance = SearchEngine.objects.filter(id=engine['id']).first()
                if instance:
                    serializer.update(instance, serializer.validated_data)
                else:
                    continue
        return Response(status=status.HTTP_200_OK)
