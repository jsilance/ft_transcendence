from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
# from .models import ChatMessage, Shape
import json

class MyGameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add the user to a specific group
        await self.channel_layer.group_add("chat_room", self.channel_name)
        self.username = self.scope["user"].username if self.scope["user"].is_authenticated else "Anonymous"
        await self.accept()

    async def disconnect(self):
        # Remove the user from the group
        await self.channel_layer.group_discard("game_room", self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Broadcast the message to the group
        await self.channel_layer.group_send(
            "chat_room",
            {
                'type': 'chat_message',
                'message': message,
                'username': self.username
            }
        )
        await self.save_message(text_data)

    # @sync_to_async
    # def save_message(self, text):
    #     ChatMessage.objects.create(content=text)

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'username': event['username'],  # Send the username along with the message
            'message': event['message']
        }))

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add the user to a specific group
        await self.channel_layer.group_add("game_room", self.channel_name)
        self.username = self.scope["user"].username if self.scope["user"].is_authenticated else "Anonymous"
        await self.accept()

    async def disconnect(self): 
        # Remove the user from the group
        await self.channel_layer.group_discard("game_room", self.channel_name)

    async def receive(self, text_data):
        
        text_data_json = json.loads(text_data)
    
        # Determine the type of message received.
        message_type = text_data_json.get('type')
    
        if message_type == 'playerPaddleUpdate':
        # Handle the key press event.
            event = text_data_json['event']  # The key that was pressed.
            key = text_data_json['key']  # The key that was pressed.
        
        # Prepare a message to broadcast to the group.
            group_message = {
            'type': 'player_paddle_update',
            'player': self.username,  # Include the username of the sender.
            'event': event,
            'key' : key
            }
        
            # Send the message to the 'threejs_group'.
            # All connected clients in this group will receive it.
            await self.channel_layer.group_send("game_room", group_message)
        
        # if message_type == 'initObject':
                
        #     party_id = text_data_json['id']
        #     # Handle the object update event.
        #     shapes = await self.get_shapes_async(party_id)
        #     shape_json = json.dumps(shapes)
        #     await self.send(text_data=json.dumps({
        #         'type': 'initObject',
        #         'shapes': shape_json
        #     }))


    async def player_paddle_update(self, event):
        # Extract the key pressed (direction) and username from the event.
        eventkey = event['event']
        key = event['key']
        username = event['player']

        # Send a message directly back to the WebSocket client.
        await self.send(text_data=json.dumps({
            'type': 'playerPaddleUpdate',
            'player': username,  # Include the username of the sender.
            'event': eventkey,
            'key': key
        }))