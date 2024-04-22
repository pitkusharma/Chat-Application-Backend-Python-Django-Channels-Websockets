from rest_framework import serializers
from django.contrib.auth import get_user_model


Users = get_user_model()

# class UserSerializer(serializers.Serializer):
#     first_name = serializers.CharField(max_length=20)
#     last_name = serializers.CharField(max_length=20)
#     username = serializers.CharField(max_length=20)
#     password = serializers.CharField(max_length=20)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

    def validate_password(self, value):
        if len(value) <= 4:
            raise serializers.ValidationError('Password needs to be large then 4 letters')
        return value