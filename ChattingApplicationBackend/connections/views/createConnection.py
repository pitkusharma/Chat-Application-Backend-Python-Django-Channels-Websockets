from rest_framework import views, status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from ..models import Connections
from rest_framework.permissions import IsAuthenticated
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Q


Users = get_user_model()
channel = get_channel_layer()

class CreateConnection(views.APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        connection_sent_by = request.user
        if not request.data.get('connection_sent_to'):
            return Response({'message': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            connection_sent_to = Users.objects.get(username=request.data.get('connection_sent_to'))
        except Users.DoesNotExist:
            return Response({'message': 'To whom you are sending connection doesn\'t exist.'},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        existing_connection = Connections.objects.filter(
            Q(sent_to=connection_sent_to, sent_by=connection_sent_by, status__in=['pending', 'accepted']) |
            Q(sent_to=connection_sent_by, sent_by=connection_sent_to, status__in=['pending', 'accepted'])
        ).count()
        if existing_connection >= 1:
            return Response({'message': 'Connection has been sent already.'},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        new_connection = Connections(sent_to=connection_sent_to,
                                     sent_by=connection_sent_by)
        new_connection.save()
        recipient_channel_name = f"{request.data.get('connection_sent_to')}_connection"
        async_to_sync(channel.group_send)(recipient_channel_name, {
            'type': 'new.connection',
        })
        data = {
            "connection_id": new_connection.id
        }
        return Response({'message': 'Connection sent successfully', "data": data}, status=status.HTTP_201_CREATED)

