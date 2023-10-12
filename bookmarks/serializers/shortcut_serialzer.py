from rest_framework import serializers

from bookmarks.models import Bookmark


class ShortcutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = [
            'id',
            'name',
            'url',
            'icon_url',
            'is_shortcut'
        ]