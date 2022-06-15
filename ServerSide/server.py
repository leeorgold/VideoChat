from dotenv import load_dotenv
load_dotenv()
import select
import socket
from message_handler import handle_message, search_logged_user, logout
import queue
from client import logged_users
from meeting import meetings
import encryption_manger as em



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


def connection_lost(s):
    print(f'connection with {(ip:=s.getpeername())} is lost')
    session = search_logged_user(ip=ip[0])
    if s in outputs:
        outputs.remove(s)
    inputs.remove(s)
    s.close()

    # Remove message queue
    del message_queues[s]
    del em.encryption_dict[s]

    logout(s, session)


while inputs:

    # Wait for at least one of the sockets to be ready for processing
    # print('waiting for the next event')
    readable, writable, exceptional = select.select(inputs, outputs, inputs)

    # Handle inputs

    for s in readable:
        if s is server:
            # A "readable" server socket is ready to accept a connection
            connection, client_address = s.accept()
            # when you get a new connection
            print(f'new connection from {client_address}')
            # connection.setblocking(False)
            inputs.append(connection)
            em.encryption_dict[connection] = em.EncryptionManger(connection)

            # Give the connection a queue for data we want to send
            message_queues[connection] = queue.Queue()
        else:
            try:
                msg = em.encryption_dict[s].recv()
                if msg is None:
                    raise ConnectionError

                # when you receive a message
                print(f'[{s.getpeername()} -> server]: {msg!r}')
                if msg == b'<SYMMETRIC KEY EXCHANGE>':
                    continue

                # A readable client socket has data
                # print(f'received "{data}" from {s.getpeername()}')
                if (output := handle_message(s, msg)) is not None:
                    if output:
                        message_queues[s].put(output)
                        # Add output channel for response
                        if s not in outputs:
                            outputs.append(s)
                else:
                    # Interpret empty result as closed connection
                    # print(f'closing {client_address} after reading no data')
                    # Stop listening for input on the connection
                    raise ConnectionError

            except ConnectionError:
                connection_lost(s)

    # Handle outputs
    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except queue.Empty:
            # No messages waiting so stop checking for writability.
            # print(f'output queue for {s.getpeername()} is empty')
            outputs.remove(s)
        else:

            # when you send a message to a client
            print(f'[server -> {s.getpeername()}]: {next_msg!r}')
            em.encryption_dict[s].send_aes(next_msg.encode())

    # Handle "exceptional conditions"
    for s in exceptional:
        connection_lost(s)
        # Remove message queue

# from threading import Thread
# import socket
#
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_address = ('0.0.0.0', 10000)
# # server_address = ('192.168.0.115', 10000)
# print(f'starting server on {server_address[0]}:{server_address[1]}')
# server.bind(server_address)
# server.listen(5)