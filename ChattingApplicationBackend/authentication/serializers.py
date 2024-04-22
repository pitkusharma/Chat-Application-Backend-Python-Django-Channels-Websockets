from rest_framework import serializers
from django.contrib.auth import get_user_model


Users = get_user_model()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=20)

    def validated_username(self, value):
        if Users.objects.filter(username='raj').count() != 1:
            raise serializers.ValidationError('Username does not exist.')
        return value

class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=300)