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

    def to_representation(self, instance):
        # Create a custom representation for the serialized data
        bookmark = super().to_representation(instance)
        settings = Setting.objects.get(user=instance.user.id)
        show_sub_categories = settings.show_bookmark_sub_categories
        grouping_factor = "sub_category" if show_sub_categories else "category"
        bookmark_category = bookmark.get(grouping_factor)
        return {str(bookmark_category): bookmark}

    def save(self, validated_data):
        bookmark = super().save(**validated_data)
        return self.to_representation(bookmark)

    def update(self, instance, validated_data):
        instance.category = validated_data.get('category', instance.category)
        instance.sub_category = validated_data.get('sub_category', instance.sub_category)
        instance.name = validated_data.get('name', instance.name)
        instance.url = validated_data.get('url', instance.url)
        instance.icon_url = validated_data.get('icon_url', instance.icon_url)
        instance.is_shortcut = validated_data.get('is_shortcut', instance.is_shortcut)
        instance.save()
        return self.to_representation(instance)