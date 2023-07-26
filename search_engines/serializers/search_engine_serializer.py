from rest_framework import serializers

from search_engines.models import SearchEngine


class SearchEngineSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, search_engine):
        name = search_engine.name
        if name:
            return name.capitalize()

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