from rest_framework import serializers

from bookmarks.models import BookmarkCategory


class BookmarkCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookmarkCategory
        fields = [
            'id',
            'name',
            'color',
            'created_at',
            'updated_at',
            'user',
        ]

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name') or instance.name
        instance.color = validated_data.get('color') or instance.color
        instance.save()
        return instance
