from rest_framework import serializers

from search_engines.models import SearchEngine


class SearchEngineSerializer(serializers.ModelSerializer):

    class Meta:
        model = SearchEngine
        fields = [
            'name',
            'url',
            'method',
            'name_attribute',
            'is_default'
        ]