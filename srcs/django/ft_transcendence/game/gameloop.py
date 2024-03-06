import asyncio
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .consumers import player_inputs, radius, angle, x, z
from .models import MapSettings
import math

class GameLoop:
    offsetX = {player.username: 0 for player in MapSettings.listOfPlayer}
    offsetZ = {player.username: 0 for player in MapSettings.listOfPlayer}

    def __init__(self):
        self.game_running = True
        self.channel_layer = get_channel_layer()

    async def start(self):
        while self.game_running:
            # Update game state here (e.g., move ball, check scores)
            # ...

            # Broadcast updated game state to all clients
            # for player in MapSettings.listOfPlayer:
            #     if player_inputs[player.username]["ArrowLeft"] and self.offset[player.username] < (16 - int(MapSettings.nbPlayer) + 2):
            #         self.offset[player.username] -= 3 / radius
            #     if player_inputs[player.username]["ArrowRight"] and self.offset[player.username] > (-16 + int(MapSettings.nbPlayer) - 2):
            #         self.offset[player.username] += 3 / radius
            #     x[player.name] = radius * math.cos((angle[self.id] + self.offset[self.username]) * math.pi / 180)
            #     z[player.name] = radius * math.sin((angle[self.id] + self.offset[self.username]) * math.pi / 180)


            # Wait a bit before next cycle

            for player in MapSettings.listOfPlayer:
                direction = 0
                if player_inputs[player.username]["ArrowLeft"]:
                    direction -= 1
                if player_inputs[player.username]["ArrowRight"]:
                    direction += 1
                self.offsetX[player.username] += direction * math.cos(angle[self.id])
                self.offsetZ[player.username] += direction * math.sin(angle[self.id])
                if (self.offsetX[player.username] ** 2 + self.offsetZ[player.username] ** 2) ** 0.5 <= 5:
                    x[player.name] = radius * math.cos(math.radians(angle[self.id])) + self.offsetX[player.username]
                    z[player.name] = radius * math.sin(math.radians(angle[self.id])) + self.offsetZ[player.username]

            message = self.generate_game_state_message()
            await self.channel_layer.group_send(
                "game_group",
                {
                    "type": "player_paddle_update",
                    "player" : player.username,
                    "x": x,
                    "z": z
                }
            )
            await asyncio.sleep(1/60)  # Example: 60 updates per second

    def generate_game_state_message(self):
        # Generate a dictionary representing the current game state
        # This could include ball position, player scores, etc.
        return {"type": "update", "data": "Your game state data here"}

# Starting the game loop
game_loop = GameLoop()
asyncio.run(game_loop.start())
