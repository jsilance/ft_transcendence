from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Shape, MapSettings
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
# from .models import ChatMessage, Shape
import json
import math

player_inputs = {}
angle = {}
x = {}
z = {}
userPartyId = {}

def update_player_input(username, key, event):
    # Ensure there's a dictionary for this player
    if event == "keydown":
        player_inputs[username][key] = True
    if event == "keyup":
        player_inputs[username][key] = False

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add the user to a specific group
        await self.channel_layer.group_add("game_room", self.channel_name)
        self.username = self.scope["user"].username if self.scope["user"].is_authenticated else "Anonymous"
        await self.accept()

    async def disconnect(self): 
        # Remove the user from the group
        await self.channel_layer.group_discard("game_room", self.channel_name)

    @staticmethod
    @sync_to_async
    def get_shapes_async(party_id):
        # Fetch shapes in a way that is compatible with async
        return [{"item_id": int(x.item_id), "type": int(x.type), "color": x.color, "posx": int(x.posx), "posy": int(x.posy)} for x in Shape.objects.filter(party_id=party_id)]

    @database_sync_to_async
    def get_map_setting_async(self, party_id):
        return MapSettings.objects.filter(id=party_id).first()

    async def receive(self, text_data):
        
        text_data_json = json.loads(text_data)
    
        # Determine the type of message received.
        message_type = text_data_json.get('type')
    
        if message_type == 'playerPaddleUpdate':
        # Handle the key press event.
            event = text_data_json['event']  # The key that was pressed.
            key = text_data_json['key']  # The key that was pressed.

            update_player_input(self.username, key, event);
        # Prepare a message to broadcast to the group.
            # group_message = {
            # 'type': 'player_paddle_update',
            # 'player': self.username,  # Include the username of the sender.
            # 'event': event,
            # 'key' : key
            # }

            # if event == "keydown":
            #     player_inputs[self.username][key] = True   
            # if event == "keyup":
            #     player_inputs[self.username][key] = False

            # Send the message to the 'threejs_group'.
            # All connected clients in this group will receive it.
            # await self.channel_layer.group_send("game_room", group_message)
        
        if message_type == 'initObject':
                
            party_id = text_data_json['id']
            # Handle the object update event.
            shapes = await self.get_shapes_async(party_id)
            shape_json = json.dumps(shapes)
            map_setting = await self.get_map_setting_async(party_id)
            if map_setting:
                for el in map_setting.listOfPlayer:
                    if el not in player_inputs:
                        player_inputs[self.username] = {'ArrowRight': False, 'ArrowLeft': False}
            # Return the map setting in the desired format
            # Adjust the fields according to your MapSetting model structure
                    radius = (5 / (2 * math.tan(math.pi / int(map_setting.nbPlayer))) * 2 + 3) if int(map_setting.nbPlayer) > 2 else 5
                    angle[el] = (360 / int(map_setting.nbPlayer)) * map_setting.listOfPlayer.index(el) + (360 / int(map_setting.nbPlayer)) / 2
                    x[el] = radius * math.cos(math.radians(angle[el]))
                    z[el] = radius * math.sin(math.radians(angle[el]))
                await self.send(text_data=json.dumps({
                    'type': 'initObject',
                    'shapes': shape_json,
                    'mapSetting': {
                        'radius': radius,
                        'angle': angle,
                        'x': x,
                        'z': z
                    }
                }))


    async def player_paddle_update(self, event):
        # Extract the key pressed (direction) and username from the event.
        x = event['x']
        z = event['z']
        username = event['player']

        # Send a message directly back to the WebSocket client.
        await self.send(text_data=json.dumps({
            'type': 'player_paddle_update',
            'player': username,  # Include the username of the sender.
            "x": x,
            "z": z
        }))

# class MyGameConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Add the user to a specific group
#         await self.channel_layer.group_add("chat_room", self.channel_name)
#         self.username = self.scope["user"].username if self.scope["user"].is_authenticated else "Anonymous"
#         await self.accept()

#     async def disconnect(self):
#         # Remove the user from the group
#         await self.channel_layer.group_discard("game_room", self.channel_name)

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Broadcast the message to the group
#         await self.channel_layer.group_send(
#             "chat_room",
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'username': self.username
#             }
#         )
#         await self.save_message(text_data)

#     # @sync_to_async
#     # def save_message(self, text):
#     #     ChatMessage.objects.create(content=text)

#     async def chat_message(self, event):
#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'username': event['username'],  # Send the username along with the message
#             'message': event['message']
#         }))
