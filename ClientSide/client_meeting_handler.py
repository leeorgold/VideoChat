import socket
from client_image_handler import ClientImageHandler
from threading import Thread
import time


img_handler = ClientImageHandler('172.19.230.32', 9999)

Thread(target=img_handler.grab_frame, daemon=True).start()
Thread(target=img_handler.send_image, daemon=True).start()
Thread(target=img_handler.receive_json_data, daemon=True).start()
Thread(target=img_handler.display, daemon=True).start()

time.sleep(1000)
