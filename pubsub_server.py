import asyncio
import json
import websockets
import uuid

# Dictionary to keep track of topics and their subscribers
topic_subscribers = {}

# Dictionary to keep track of authenticated clients and their tokens
authenticated_clients = {}

async def authenticate(websocket):
    # We generate a unique token for each new client connection
    token = str(uuid.uuid4())
    # Store the client's token
    authenticated_clients[websocket] = token
    # Send the token back to the client
    await websocket.send(json.dumps({'token': token}))

async def server(websocket, path):
    await authenticate(websocket)
    
    try:
        async for message in websocket:
            data = json.loads(message)
            if 'token' not in data or data['token'] != authenticated_clients[websocket]:
                await websocket.send(json.dumps({'error': 'Invalid token'}))
                continue

            # Message format: {"action": "subscribe/publish", "topic": "topic_name", "message": "message_content"}
            if data['action'] == 'subscribe':
                if data['topic'] not in topic_subscribers:
                    topic_subscribers[data['topic']] = set()
                topic_subscribers[data['topic']].add(websocket)
            elif data['action'] == 'publish':
                if data['topic'] in topic_subscribers:
                    for subscriber in topic_subscribers[data['topic']]:
                        await subscriber.send(json.dumps({'topic': data['topic'], 'message': data['message']}))
            else:
                await websocket.send(json.dumps({'error': 'Invalid action'}))
    finally:
        # Remove the client from the subscribers of all topics and authenticated clients list
        for subscribers in topic_subscribers.values():
            subscribers.discard(websocket)
        del authenticated_clients[websocket]

start_server = websockets.serve(server, '0.0.0.0', 80)

## print out the external IP address so we can connect to the server
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(s.getsockname()[0])
s.close()

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

