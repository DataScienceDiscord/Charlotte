from discord import Gateway
from discord import Consumer
from dispatcher import Dispatcher
import threading
import time
import queue
import websocket

with open(".token", "r") as f:
    token = f.read()

message_queue = queue.Queue()

consumer = Consumer(token)
dispatch = Dispatcher(message_queue, None, consumer)
dispatch.start()


gw = Gateway(token, message_queue, websocket)
gw.connect()

def stop_in_a_while():
    time.sleep(30)
    gw.stop()
    gw.close()
    dispatch.stop()
    message_queue.put(None)

t = threading.Thread(target=stop_in_a_while)
t.start()

gw.start()
dispatch.start()
