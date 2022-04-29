import select
import socket
import json
from participant import Participant
# from .server_image_handler import ServerImageHandler
# import queue


def is_participant_exists(ip):
    for participant in participants.values():
        if participant.is_same_ip(ip):
            return participant
    return Participant(ip)


def output_data():
    output = {}
    for s, participant in participants.items():
        output[participant.name] = participant.image_handler.frame
    return output


participants = {}

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setblocking(0)

# Bind the socket to the port
server_address = ('127.0.0.1', 10000)
print(f'starting server on {server_address[0]}:{server_address[1]}')
server.bind(server_address)
server.listen(3)

# Sockets from which we expect to read
inputs = [server]

# Sockets to which we expect to write
outputs = []

# Outgoing message queues (socket:Queue)
message_queues = {}

while inputs:

    # Wait for at least one of the sockets to be ready for processing
    # print('waiting for the next event')
    readable, writable, exceptional = select.select(inputs, outputs, inputs)

    # Handle inputs
    for s in readable:
        if s is server:
            # A "readable" server socket is ready to accept a connection
            connection, client_address = s.accept()
            print(f'new connection from {client_address}')
            # participants.append(Participant(client_address))
            # connection.setblocking(False)
            inputs.append(connection)

            part = is_participant_exists(client_address[0])
            participants[connection] = part
            part.set_image_handler(connection)

            # Give the connection a queue for data we want to send
            # message_queues[connection] = queue.Queue()
        else:
            try:
                participants[s].image_handler.handle()
            except Exception as e:
                raise e
                # # Interpret empty result as closed connection
                # print(f'closing {s.getpeername} after reading no data')
                # # Stop listening for input on the connection
                # if s in outputs:
                #     outputs.remove(s)
                # inputs.remove(s)
                # image_handlers.pop(s)
                # s.close()
                #
                # # Remove message queue
                # del message_queues[s]

    # Handle outputs
    output = output_data()
    for s in writable:
        copy = output.copy()
        copy.pop(participants[s].name)
        try:
            # next_msg = message_queues[s].get_nowait()
            s.sendall(json.dumps(copy).encode())
        except Exception as e:
            raise e
        # except queue.Empty:
        #     # No messages waiting so stop checking for writability.
        #     print(f'output queue for {s.getpeername()} is empty')
        #     outputs.remove(s)
        # else:
        #     print(f'sending "{next_msg}" to {s.getpeername()}')
        #     s.send(next_msg)

    # Handle "exceptional conditions"
    for s in exceptional:
        # print(f'handling exceptional condition for {s.getpeername()}')
        # # Stop listening for input on the connection
        # inputs.remove(s)
        # if s in outputs:
        #     outputs.remove(s)
        # participants.pop(s)
        # s.close()
        # # Remove message queue
        # del message_queues[s]
        del participants[s].image_handler
        participants.pop(s)
        s.close()
