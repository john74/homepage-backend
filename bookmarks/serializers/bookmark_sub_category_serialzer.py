from rest_framework import serializers

from bookmarks.models import BookmarkSubCategory


class BookmarkSubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = BookmarkSubCategory
        fields = [
            'id',
            'category',
            'user',
            'name',
            'created_at',
            'created_by',
            'updated_at',
            'updated_at',
        ]

    def save(self, validated_data):
        return super().save(**validated_data)

    def update(self, instance, validated_data):
        instance.category = validated_data.get('category', instance.category)
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance