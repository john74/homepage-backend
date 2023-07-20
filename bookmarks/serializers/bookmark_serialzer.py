from rest_framework import serializers

from bookmarks.models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = [
            'category',
            'id',
            'name',
            'url',
            'icon_url',
            'is_shortcut',
            'created_at',
            'updated_at'
        ]

    def save(self, validated_data):
        bookmark = super().save(**validated_data)
        return {
            "id": bookmark.id,
            "name": bookmark.name,
            "url": bookmark.url,
            "icon_url": bookmark.icon_url,
            "is_shortcut": bookmark.is_shortcut,
            "created_at": bookmark.created_at,
            "updated_at": bookmark.updated_at
        }