import pyaudio
import socket

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024



def connecet_to_server_audio(host_ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(b'hello server', (host_ip, port))
    packet, addr = sock.recvfrom(1024)
    while addr != server_addr and packet != b'hello client':
        packet, addr = sock.recvfrom(1024)
    print('connected')
    return sock, (host_ip, port)


# server_addr = ('192.168.0.109', 4444)
# sock, client_addr = connecet_to_server_audio(*server_addr)
audio = pyaudio.PyAudio()


def callback(in_data, frame_count, time_info, status):
    # sock.sendto(in_data, client_addr)
    return None, pyaudio.paContinue


# start Recording
recording_stream = audio.open(format=FORMAT,
                              channels=CHANNELS,
                              rate=RATE,
                              input=True,
                              frames_per_buffer=CHUNK,
                              stream_callback=callback,
                              start=False)
print("recording...")

record = recording_stream.start_stream

playing_stream = audio.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            output=True,
                            frames_per_buffer=CHUNK)


def play():
    while True:
        playing_stream.write(sock.recv(CHUNK))


# print('Shutting down')
# sock.close()
# stream.close()
# audio.terminate()
if __name__ == '__main__':
    record()
    # play()
