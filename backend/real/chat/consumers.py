import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.timesince import timesince
from .serializers import UserSerializer
from .models import Message,ChatRoom
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
  
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"chat_{self.room_id}"
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Receive message from WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']
        user_serializer = UserSerializer(user)
        email = user_serializer.data['email']
        profile_pic = user_serializer.data['profile_pic']

        new_message = await self.create_message(self.room_id,message,email)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'room_id':self.room_id,
                'sender_email':email,
                'profile_pic':profile_pic,
                'created': timesince(new_message.timestamp)
            }
        )

    async def chat_message(self, event):
        # Receive message from room group
        print(event,"events")
        message = event['message']
        room_id = event['room_id']
        email = event['sender_email']
        profile_pic= event['profile_pic']

        created = event['created']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': message,
                'room_id':room_id,
                'sender_email':email,
                'profile_pic':profile_pic,

                'created': created
        }))


    @sync_to_async
    def create_message(self,room_id,message,email):
        user=User.objects.get(email=email)
        room = ChatRoom.objects.get(id=room_id)
        message = Message.objects.create(content=message,room=room,sender=user)
        message.save()
        return message