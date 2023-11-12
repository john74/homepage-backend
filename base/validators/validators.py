from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from rest_framework import serializers


class URLValidator(URLValidator):
    def __call__(self, value):
        try:
            super().__call__(value)
        except ValidationError as error:
            raise serializers.ValidationError("Please enter a valid URL.")