import asyncio

# Our message queues will be stored here
queues = {}

async def handle_client(reader, writer):
    while True:
        # Get a line of input from the client
        data = await reader.readline()
        command = data.decode().strip()

        # If the command is "push", then we expect two more lines: the queue name and the message
        if command == 'push':
            queue_name = await reader.readline()
            queue_name = queue_name.decode().strip()
            message = await reader.readline()
            message = message.decode().strip()

            # If the queue doesn't exist yet, we create it
            if queue_name not in queues:
                queues[queue_name] = []

            queues[queue_name].append(message)
            writer.write(b'OK\n')
            await writer.drain()

        # If the command is "pop", then we expect one more line: the queue name
        elif command == 'pop':
            queue_name = await reader.readline()
            queue_name = queue_name.decode().strip()

            # If the queue exists and it's not empty, we pop a message from it
            if queue_name in queues and queues[queue_name]:
                message = queues[queue_name].pop(0)
                writer.write((message + '\n').encode())
            else:
                writer.write(b'ERROR\n')
            await writer.drain()

        # If the command is "quit", then we break the loop and close the connection
        elif command == 'quit':
            break
        else:
            writer.write(b'ERROR\n')
            await writer.drain()

    writer.close()

async def main():
    server = await asyncio.start_server(handle_client, 'localhost', 8888)

    async with server:
        await server.serve_forever()

asyncio.run(main())
