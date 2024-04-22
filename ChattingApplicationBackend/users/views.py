from rest_framework import views, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from django.conf import settings
from utilities.encryption import Encrypt
from rest_framework.permissions import AllowAny

Users = get_user_model()

class CreateUser(views.APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serialized_data = UserSerializer(data=request.data)
        if serialized_data.is_valid():
            encrypt = Encrypt(serialized_data.validated_data.get('password'))
            serialized_data.validated_data['password'] = encrypt.get_encrypted_string()
            serialized_data.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': f'Invalid data: {serialized_data.errors}'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


