import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer, WebsocketConsumer
from .serializers import CreateConnectionSerializer
from django.contrib.auth import get_user_model
from .models import Connections

Users = get_user_model()

class ConnectionHandleConsumer(JsonWebsocketConsumer):
    def connect(self):
        if not self.scope['authenticated']:
            self.close()
        async_to_sync(self.channel_layer.group_add)(f"{self.scope['user']}_connection", self.channel_name)
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(f"{self.scope['user']}_connection", self.channel_name)

    def receive_json(self, message):
        print(message)
        if message['type'].upper() == 'SENT_CONNECTION':
            try:
                connection_sent_by = Users(username=message['data']['connection_sent_by'])
                connection_sent_to = Users(username=message['data']['connection_sent_to'])
                new_connection = Connections(connection_sent_to=connection_sent_to,
                                             connection_sent_by=connection_sent_by)
                new_connection.save()
                self.send_json({
                    "type": "sent_connection_done",
                    "data": message['data']
                })
            except Exception as e:
                self.send_json({
                    "type": "sent_connection_failed",
                    "data": message['data'],
                    "error": str(e)
                })

        elif message['type'].upper() == 'ACCEPT_CONNECTION':
            pass
        else:
            pass


