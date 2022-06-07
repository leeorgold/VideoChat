import pyaudio
import socket
import time

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096

audio = pyaudio.PyAudio()


def connect_to_client_audio():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('192.168.0.114', 4444))
    serversocket.listen(5)

    client_socket, addr = serversocket.accept()
    return client_socket


def connect_to_server_audio(host_ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sock.connect((host_ip, 4444))
    return sock


sock = connect_to_client_audio()


def callback(in_data, frame_count, time_info, status):
    sock.send(in_data)
    return None, pyaudio.paContinue


# start Recording
recording_stream = audio.open(format=FORMAT,
                              channels=CHANNELS,
                              rate=RATE,
                              input=True,
                              frames_per_buffer=CHUNK,
                              stream_callback=callback)
print("recording...")

playing_stream = audio.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            output=True,
                            frames_per_buffer=CHUNK)
# stream.start_stream()
while True:
    playing_stream.write(sock.recv(CHUNK))


print("finished recording")

serversocket.close()
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
