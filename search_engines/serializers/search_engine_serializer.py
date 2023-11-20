from rest_framework import serializers

from search_engines.models import SearchEngine


class SearchEngineSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchEngine
        fields = [
            'id',
            'name',
            'url',
            'method',
            'name_attribute',
            'is_default',
            'user',
            'created_at',
        ]