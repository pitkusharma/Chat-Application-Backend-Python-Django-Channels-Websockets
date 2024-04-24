from rest_framework import serializers
from django.contrib.auth import get_user_model

Users = get_user_model()


# class CreateConnectionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Users
#         fields = ['connection_sent_by', 'connection_sent_to']
#
#     # def validated_connection_sent_by(self, value):
#     #     if Users.objects.filter(username=value).count() != 1:
#     #         raise serializers.ValidationError('Sender username does not exist.')
#     #     return value
#     #
#     # def validated_connection_sent_to(self, value):
#     #     if Users.objects.filter(username=value).count() != 1:
#     #         raise serializers.ValidationError('Receiver username does not exist.')
#     #     return value