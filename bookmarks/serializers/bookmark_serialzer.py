from rest_framework import serializers

from base.validators import URLValidator
from bookmarks.models import Bookmark
from settings.models import Setting


class BookmarkSerializer(serializers.ModelSerializer):
    url = serializers.CharField(validators=[URLValidator()])
    icon_url = serializers.CharField(validators=[URLValidator()])

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
            'updated_at',
            'sub_category',
            'user',
        ]

    def save(self, validated_data):
        # return the new bookmark
        return super().save(**validated_data)

    def update(self, instance, validated_data):
        instance.category = validated_data.get('category', instance.category)
        instance.sub_category = validated_data.get('sub_category', instance.sub_category)
        instance.name = validated_data.get('name', instance.name)
        instance.url = validated_data.get('url', instance.url)
        instance.icon_url = validated_data.get('icon_url', instance.icon_url)
        instance.is_shortcut = validated_data.get('is_shortcut', instance.is_shortcut)
        instance.save()
        return instance