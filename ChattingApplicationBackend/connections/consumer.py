import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer, WebsocketConsumer
# from django.contrib.auth import get_user_model
#
# Users = get_user_model()

class ConnectionHandleConsumer(JsonWebsocketConsumer):
    def connect(self):
        if not self.scope['authenticated']:
            self.close()
        async_to_sync(self.channel_layer.group_add)(f"{self.scope['user']}_connection", self.channel_name)
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(f"{self.scope['user']}_connection", self.channel_name)

    def new_connection(self, event):
        self.send_json({'message': 'new_connection'})
