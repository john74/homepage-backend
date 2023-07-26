from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from search_engines.models import SearchEngine
from search_engines.serializers import SearchEngineSerializer


class SearchEngineBulkCreateAPIView(APIView):
    serializer_class = SearchEngineSerializer

    def post(self, request, *args, **kwargs):
        search_engines = request.data

        for engine in search_engines:
            serializer = self.serializer_class(data=engine)
            if serializer.is_valid():
                SearchEngine.objects.create(**serializer.validated_data)
        return Response(status=status.HTTP_200_OK)