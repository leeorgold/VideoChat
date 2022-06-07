import select
import socket
from message_handler import handle_message
import queue

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setblocking(False)

# Bind the socket to the port
server_address = ('0.0.0.0', 10000)
# server_address = ('192.168.0.115', 10000)
print(f'starting server on {server_address[0]}:{server_address[1]}')
server.bind(server_address)
server.listen(5)

# Sockets from which we expect to read
inputs = [server]

# Sockets to which we expect to write
outputs = []

# Outgoing message queues (socket:Queue)
message_queues = {}

while inputs:

    # Wait for at least one of the sockets to be ready for processing
    print('waiting for the next event')
    readable, writable, exceptional = select.select(inputs, outputs, inputs)

    # Handle inputs
    for s in readable:
        if s is server:
            # A "readable" server socket is ready to accept a connection
            connection, client_address = s.accept()
            print(f'new connection from {client_address}')
            connection.setblocking(False)
            inputs.append(connection)

            # Give the connection a queue for data we want to send
            message_queues[connection] = queue.Queue()
        else:
            length = s.recv(8).decode()
            if length:
                length = int(length)
                msg = s.recv(length).decode()
                worked, info = handle_message(msg)
                response = info
                # A readable client socket has data
                # print(f'received "{data}" from {s.getpeername()}')
                message_queues[s].put(response)
                # Add output channel for response
                if s not in outputs:
                    outputs.append(s)
            else:
                # Interpret empty result as closed connection
                # print(f'closing {client_address} after reading no data')
                # Stop listening for input on the connection
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()

                # Remove message queue
                del message_queues[s]

    # Handle outputs
    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except queue.Empty:
            # No messages waiting so stop checking for writability.
            print(f'output queue for {s.getpeername()} is empty')
            outputs.remove(s)
        else:
            print(f'sending "{next_msg}" to {s.getpeername()}')
            s.send(next_msg.encode())

    # Handle "exceptional conditions"
    for s in exceptional:
        print(f'handling exceptional condition for {s.getpeername()}')
        # Stop listening for input on the connection
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        # Remove message queue
