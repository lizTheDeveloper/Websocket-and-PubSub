import socket

def receive(queue_name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 8888))

        # Send the pop command, followed by the queue name
        s.sendall(b'pop\n')
        s.sendall((queue_name + '\n').encode())

        # Check the response from the server
        data = s.recv(1024)
        print('Received', repr(data))

receive('test_queue')
