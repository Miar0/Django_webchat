import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from core.models import SocialUser
from core.models import Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.group_name = f"room_{self.room_id}"
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        print('New connection')
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        user = SocialUser.objects.get(id=text_data['userId']).username
        if text_data['type'] == 'connected':
            async_to_sync(self.channel_layer.group_send)(
                self.group_name, {
                    'type': 'chat_connected',
                    'message': {
                        'msg': f"{user} is joined to chat"
                    }
                }
            )
        else:
            Message.objects.create(
                room_id=self.room_id,
                user_from_id=text_data['userId'],
                message=text_data['text']
            )
            async_to_sync(self.channel_layer.group_send)(
                self.group_name, {
                    'type': 'chat_message',
                    'message': json.dumps({
                        'text': text_data['text'],
                        'username': user,
                        'userId': text_data['userId']
                    })
                }
            )

    def chat_connected(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message,
            'type': 'connected'
        }))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message,
            'type': 'message'
        }))

    def disconnect(self, text_data=None):
        print('Disconnect')
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
        self.close()
