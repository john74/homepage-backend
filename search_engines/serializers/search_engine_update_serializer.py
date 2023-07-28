from rest_framework import serializers

from search_engines.models import SearchEngine


class SearchEngineUpdateSerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        required=False
    )

    url = serializers.URLField(
        required=False
    )

    method = serializers.CharField(
        required=False
    )

    name_attribute = serializers.CharField(
        required=False
    )

    is_default = serializers.BooleanField(
        required=False
    )

    class Meta:
        model = SearchEngine
        fields = [
            'id',
            'name',
            'url',
            'method',
            'name_attribute',
            'is_default'
        ]