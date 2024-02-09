from channels.testing import WebsocketCommunicator
from django.test import TestCase
from game.routing import application

class MyGameConsumerTest(TestCase):
    async def test_my_consumer(self):
        # Create a communicator for testing your consumer
        communicator = WebsocketCommunicator(application, "")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        
        # Test sending a message to the consumer
        await communicator.send_json_to({"type": "some_message"})
        
        # Test receiving a response from the consumer
        response = await communicator.receive_json_from()
        # Assert the response here
        
        # Close the connection
        await communicator.disconnect()

