from datetime import datetime
from rest_framework import views, status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from ..models import Connections
from rest_framework.permissions import IsAuthenticated
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.exceptions import ObjectDoesNotExist


Users = get_user_model()
channel = get_channel_layer()


class PerformAction(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, action, connection_id):
        if action.upper() not in ['ACCEPT', 'REJECT', 'CANCEL', 'DELETE']:
            return Response({'message': 'Invalid value in the request.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            connection_obj = Connections.objects.get(id=connection_id)
        except ObjectDoesNotExist:
            return Response({'message': 'Connection request not found.'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        if (action.upper() in ['ACCEPT', 'REJECT'] and connection_obj.sent_to != request.user) or (
            action.upper() in ['CANCEL'] and connection_obj.sent_by != request.user) or (
            action.upper() in ['DELETE'] and (connection_obj.sent_by != request.user and
                                              connection_obj.sent_to != request.user)
        ):
            return Response({'message': 'This connection doesn\'t belong to you.'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        if action.upper() == 'DELETE':
            connection_obj.delete()
            return Response({'message': 'Connection deleted.'}, status=status.HTTP_200_OK)

        action_mapping = {'accept': 'accepted', 'reject': 'rejected', 'cancel': 'cancelled'}

        connection_obj.status = action_mapping[action.lower()]
        connection_obj.status_updated_at = datetime.now()
        connection_obj.save()

        recipient_channel_name = f'{connection_obj.sent_by.username}_connection'
        if action.upper() == 'ACCEPT':
            async_to_sync(channel.group_send)(recipient_channel_name, {
                "type": "connection.accepted",
                "data": {
                    "connection_id": connection_obj.id
                }
            })
            return Response({'message': 'Connection accepted.'}, status=status.HTTP_200_OK)
        elif action.upper() == 'REJECT':
            async_to_sync(channel.group_send)(recipient_channel_name, {
                "type": "connection.rejected",
                "data": {
                    "connection_id": connection_obj.id
                }
            })
            return Response({'message': 'Connection rejected.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Connection cancelled.'}, status=status.HTTP_200_OK)
