import socket

def publish(queue_name, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 8888))

        # Send the push command, followed by the queue name and the message
        s.sendall(b'push\n')
        s.sendall((queue_name + '\n').encode())
        s.sendall((message + '\n').encode())

        # Check the response from the server
        data = s.recv(1024)
        print('Received', repr(data))

publish('test_queue', 'Hello, World!')
