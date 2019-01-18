# Todo: Export variable name to file
import os

from discord import Gateway
from discord import Consumer
from dispatcher import Dispatcher
from database import Database
import commands
import threading
import time
import queue
import websocket


if os.environ['ENVCHARLOTTE'] == "PROD":
    token = os.environ['DISCORDTOKEN']
    if os.environ['INITDB'] == "TRUE":
        import scripts.init_tables
else:
    with open(".token", "r") as f:
        token = f.read()

message_queue = queue.Queue()

consumer = Consumer(token)
db = Database()
dispatch = Dispatcher(message_queue, db, consumer, commands)


gw = Gateway(token, message_queue, websocket)
gw.connect()

gw.start()
dispatch.start()
