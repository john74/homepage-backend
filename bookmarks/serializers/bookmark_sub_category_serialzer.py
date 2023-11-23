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

    def to_representation(self, instance):
        # Create a custom representation for the serialized data
        sub_category = super().to_representation(instance)
        category = sub_category.get('category')
        return {str(category): sub_category}

    def save(self, validated_data):
        sub_category = super().save(**validated_data)
        return self.to_representation(sub_category)

    def update(self, instance, validated_data):
        instance.category = validated_data.get('category', instance.category)
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return self.to_representation(instance)