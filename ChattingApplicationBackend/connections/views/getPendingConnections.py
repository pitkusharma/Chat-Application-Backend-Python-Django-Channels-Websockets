from rest_framework import views, status
from rest_framework.response import Response
from ..models import Connections
from rest_framework.permissions import IsAuthenticated

class GetPendingConnections(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        connection_objects = Connections.objects.filter(
            sent_to=request.user,
            status='pending').order_by('-sent_at')
        data = []
        for connection in connection_objects:
            connection_sent_by = connection.sent_by
            connection_data = {
                "connection_id": connection.id,
                "connection_sent_at": connection.sent_at,
                "connection_sent_by": connection_sent_by.username,
                "full_name": f'{connection_sent_by.first_name} {connection_sent_by.last_name}'
            }
            data.append(connection_data)

        return Response({'message': 'All pending connection requests.', 'data': data}, status=status.HTTP_200_OK)

