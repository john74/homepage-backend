from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from search_engines.models import SearchEngine
from search_engines.serializers import SearchEngineSerializer


class SearchEngineListAPIView(APIView):
    serializer_class = SearchEngineSerializer

    def get(self, request, *args, **kwargs):
        search_engines = SearchEngine.objects.all()
        serializer = self.serializer_class(search_engines, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)