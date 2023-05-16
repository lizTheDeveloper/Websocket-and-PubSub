import asyncio
import json
import websockets

async def client():
    # Connect to the server
    async with websockets.connect('ws://172.31.128.38:80') as websocket:
        # Get the authentication token from the server
        response = await websocket.recv()
        data = json.loads(response)
        token = data.get('token')

        # Subscribe to a topic
        subscribe_message = json.dumps({
            'action': 'subscribe',
            'topic': 'test_topic',
            'token': token
        })
        await websocket.send(subscribe_message)

        # Publish a message to the topic
        publish_message = json.dumps({
            'action': 'publish',
            'topic': 'test_topic',
            'message': "Hello, I am liz's websocket server!",
            'token': token
        })
        await websocket.send(publish_message)

        # Receive messages
        while True:
            response = await websocket.recv()
            print(f"Received: {response}")

asyncio.get_event_loop().run_until_complete(client())


