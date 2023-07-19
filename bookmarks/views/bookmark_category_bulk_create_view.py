from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookmarks.models import BookmarkCategory
from bookmarks.serializers import BookmarkCategorySerializer


class BookmarkCategoryBulkCreateAPIView(APIView):
    serializer_class = BookmarkCategorySerializer

    def post(self, request, *args, **kwargs):
        categories = request.data
        created_categories = []
        errors = []

        for category in categories:
            serializer = self.serializer_class(data=category)
            if serializer.is_valid():
                created_category = serializer.save(serializer.validated_data)
                created_categories.append(created_category)
            else:
                for field, message in serializer.errors.items():
                    errors.append({'message':f'{field} {message[0].lower()}', 'category':category})

        if not errors:
            return Response(data=created_categories, status=status.HTTP_200_OK)

        if len(errors) < len(categories):
            return Response(data={'bookmarks':created_categories, 'errors':errors}, status=status.HTTP_206_PARTIAL_CONTENT)

        return Response(data={'errors':errors}, status=status.HTTP_400_BAD_REQUEST)
