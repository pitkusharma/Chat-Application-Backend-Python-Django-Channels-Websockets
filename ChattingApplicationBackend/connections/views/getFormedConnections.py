from rest_framework import views, status
from rest_framework.response import Response
from ..models import Connections
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

class GetFormedConnections(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        connection_objects = Connections.objects.filter(
            Q(
                Q(sent_to=request.user) |
                Q(sent_by=request.user)
            ) & Q(status='accepted')
        ).order_by('-sent_at')
        data = []
        for connection in connection_objects:
            connection_with = connection.sent_to \
                if connection.sent_by == request.user else connection.sent_by
            connection_data = {
                "connection_id": connection.id,
                "connection_sent_at": connection.sent_at,
                "connection_with": connection_with.username,
                "full_name": f'{connection_with.first_name} {connection_with.last_name}'
            }
            data.append(connection_data)

        return Response({'message': 'All accpted connection requests.', 'data': data}, status=status.HTTP_200_OK)

