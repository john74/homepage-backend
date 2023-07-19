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
            'updated_at'
        ]

    def save(self, validated_data):
        category = super().save(**validated_data)
        return {
            "id": category.id,
            "name": category.name,
            "color": category.color,
            "created_at": category.created_at,
            "updated_at": category.updated_at
        }