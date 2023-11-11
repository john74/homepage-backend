from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    all_users = User.objects.all();

    password = serializers.CharField(
        min_length=8,
        write_only=True,
        error_messages={
            'min_length': 'Password must be at least 8 characters long.',
        }
    )

    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=all_users,
                message='A user with this email already exists.'
            )
        ]
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
