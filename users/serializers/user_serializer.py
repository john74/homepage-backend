from rest_framework import serializers
from rest_framework.validators import ValidationError
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs['email'])
        if email_exists:
            raise ValidationError('A user with this email already exists')
        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
