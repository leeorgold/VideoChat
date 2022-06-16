from dotenv import load_dotenv

load_dotenv()
import select
import socket
from message_handler import handle_message, search_logged_user, logout
import queue
import encryption_manger as em

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('0.0.0.0', 10000)
print(f'starting server on {server_address}')
server.bind(server_address)
server.listen(5)

# Sockets from which we expect to read
inputs = [server]

# Sockets to which we expect to write
outputs = []

# Outgoing message queues dictionary (socket:Queue)
message_queues = {}


def connection_lost(s):
    """The function handles cases of connection lost"""
    print(f'connection with {(ip := s.getpeername())} is lost')
    session = search_logged_user(ip=ip[0])
    if s in outputs:
        outputs.remove(s)
    inputs.remove(s)
    s.close()

    # Remove message queue
    del message_queues[s]
    # Remove the encryption details
    del em.encryption_dict[s]
    # Log the user out of the system
    logout(s, session)


while inputs:

    # Wait for at least one of the sockets to be ready for processing
    readable, writable, exceptional = select.select(inputs, outputs, inputs)

    # Handle incoming messages
    for s in readable:
        if s is server:
            # A "readable" server socket is ready to accept a connection
            connection, client_address = s.accept()
            print(f'new connection from {client_address}')
            inputs.append(connection)
            # Create an encryption manger to ensure secured communication
            em.encryption_dict[connection] = em.EncryptionManger(connection)

            # Create a message queue for the sever responses
            message_queues[connection] = queue.Queue()
        else:
            # when you receive a message from a client
            try:
                msg = em.encryption_dict[s].recv()
                # if the message cannot be decrypted (it has been interfered), a None is returned
                if msg is None:
                    raise ConnectionError

                print(f'[{s.getpeername()} -> server]: {msg!r}')
                if msg == b'<SYMMETRIC KEY EXCHANGE>':
                    # nothing for the server to handle
                    continue

                # analysed and handle the request from the client
                if (output := handle_message(s, msg)) is None:
                    # if there is no response to the request (illegal request)
                    raise ConnectionError

                elif output:
                    # if there is a response to the request (legal request)
                    message_queues[s].put(output)
                    if s not in outputs:
                        outputs.append(s)

            except ConnectionError:
                # in any ConnectionError disconnect form the client
                connection_lost(s)

    # Handle outgoing responses
    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except queue.Empty:
            # No messages waiting.
            outputs.remove(s)
        else:
            # send response
            print(f'[server -> {s.getpeername()}]: {next_msg!r}')
            em.encryption_dict[s].send_aes(next_msg.encode())

    # Handle exceptional connections (disconnect).
    for s in exceptional:
        connection_lost(s)
