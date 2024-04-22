from rest_framework import views, status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .serializers import CreateConnectionSerializer
from .models import Connections
# from rest_framework.permissions import AllowAny, IsAuthenticated


class CreateConnection(views.APIView):

    def post(self, request):
        serialized_data = CreateConnectionSerializer(data=request.data)
        if not serialized_data.is_valid():
            return Response({'message': f'Invalid data: {serialized_data.errors}'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
