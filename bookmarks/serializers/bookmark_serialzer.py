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

    def to_representation(self, instance):
        # Create a custom representation for the serialized data
        bookmark = super().to_representation(instance)
        bookmark_category = bookmark.pop('category')
        return {str(bookmark_category): bookmark}

    def save(self, validated_data):
        bookmark = super().save(**validated_data)
        return self.to_representation(bookmark)