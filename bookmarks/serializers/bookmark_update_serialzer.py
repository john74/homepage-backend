from rest_framework import serializers

from bookmarks.models import Bookmark


class BookmarkUpdateSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    def get_category(self, bookmark):
        category = bookmark.get('category')
        if category:
            return category
        return bookmark.category.id

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

    def update(self, bookmark, validated_data):
        updated_bookmark = super().update(bookmark, validated_data)
        return {
            "id": updated_bookmark.id,
            "name": updated_bookmark.name,
            "url": updated_bookmark.url,
            "icon_url": updated_bookmark.icon_url,
            "is_shortcut": updated_bookmark.is_shortcut,
            "created_at": updated_bookmark.created_at,
            "updated_at": updated_bookmark.updated_at
        }