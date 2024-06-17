import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'global'
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        print('New connection')
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        if text_data['type'] == 'connected':
            user = get_user_model().objects.get(id=text_data['userId']).username
            async_to_sync(self.channel_layer.group_send)(
                self.group_name, {
                    'type': 'chat_connected',
                    'message': {
                        'msg': f"{user} is joined to chat"
                    }}

            )

    def chat_connected(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message,
            'type': 'connected'
        }))

    def disconnect(self, text_data=None):
        print('Disconnect')
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
        self.close()
