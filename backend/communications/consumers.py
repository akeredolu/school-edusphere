import json
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import UntypedToken
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from jwt import decode as jwt_decode
from django.conf import settings

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get token from query params
        self.token = self.scope['query_string'].decode().split("token=")[-1]
        
        try:
            # Validate token
            UntypedToken(self.token)
            decoded_data = jwt_decode(self.token, settings.SECRET_KEY, algorithms=["HS256"])
            self.user = await database_sync_to_async(User.objects.get)(id=decoded_data['user_id'])
        except Exception as e:
            await self.close()
            return

        # Room setup
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "")

        # Save message in DB
        await self.save_message(message)

        # Broadcast
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message(self, message):
        from communications.models import Conversation, Message
        # Get or create class group conversation
        conversation, _ = Conversation.objects.get_or_create(is_group=True, participants__username__in=[self.user.username])
        Message.objects.create(
            conversation=conversation,
            sender=self.user,
            text=message
        )

