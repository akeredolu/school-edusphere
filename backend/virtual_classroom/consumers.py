import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from datetime import timedelta
from .models import VirtualAttendance, VirtualClass
from django.contrib.auth.models import AnonymousUser

class ClassPresenceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.class_id = self.scope["url_route"]["kwargs"]["class_id"]
        self.group_name = f"class_{self.class_id}"

        user = self.scope["user"]
        if user is None or isinstance(user, AnonymousUser):
            await self.close()
            return

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        # Record join
        attendance = await self.create_attendance(user)

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "presence_update",
                "message": f"{user.get_full_name()} joined",
            }
        )

    async def disconnect(self, close_code):
        user = self.scope["user"]

        if user and user.is_authenticated:
            await self.update_leave_time(user)

            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "presence_update",
                    "message": f"{user.get_full_name()} left",
                }
            )

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def presence_update(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))

    async def create_attendance(self, user):
        return await VirtualAttendance.objects.acreate(
            virtual_class_id=self.class_id,
            student=user
        )

    async def update_leave_time(self, user):
        attendance = await VirtualAttendance.objects.filter(
            virtual_class_id=self.class_id,
            student=user,
            left_at__isnull=True
        ).afirst()

        if attendance:
            attendance.left_at = timezone.now()
            attendance.duration_seconds = int(
                (attendance.left_at - attendance.joined_at).total_seconds()
            )
            await attendance.asave()


class ClassChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.class_id = self.scope["url_route"]["kwargs"]["class_id"]
        self.group_name = f"class_chat_{self.class_id}"

        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")
        reaction = data.get("reaction")

        user = self.scope["user"]

        if message:
            await ClassChatMessage.objects.acreate(
                virtual_class_id=self.class_id,
                sender=user,
                message=message
            )

            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chat_message",
                    "sender": user.get_full_name(),
                    "message": message,
                }
            )

        if reaction:
            await ClassReaction.objects.acreate(
                virtual_class_id=self.class_id,
                student=user,
                reaction=reaction
            )

            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "reaction_event",
                    "sender": user.get_full_name(),
                    "reaction": reaction,
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def reaction_event(self, event):
        await self.send(text_data=json.dumps(event))
