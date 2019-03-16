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
import logging
import logging.config
import logging_config
import sys
import traceback


if os.environ['ENVCHARLOTTE'] == "PROD":
    token = os.environ['DISCORDTOKEN']
    if os.environ['INITDB'] == "TRUE":
        import scripts.init_tables
else:
    with open(".token", "r") as f:
        token = f.read()


logging.config.dictConfig(logging_config.config)
logger = logging.getLogger(__name__)
logger.info("Starting with ENVCHARLOTTE=%s." % os.environ['ENVCHARLOTTE'])

# Log exceptions from main thread
def log_exception_hook(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Uncaught exception.", exc_info=(exc_type, exc_value, exc_traceback))
sys.excepthook = log_exception_hook


def install_thread_excepthook():
    """
    Workaround for sys.excepthook thread bug
    (https://sourceforge.net/tracker/?func=detail&atid=105470&aid=1230540&group_id=5470).
    Call once from __main__ before creating any threads.
    If using psyco, call psycho.cannotcompile(threading.Thread.run)
    since this replaces a new-style class method.
    """
    import sys
    run_old = threading.Thread.run
    def run(*args, **kwargs):
        try:
            run_old(*args, **kwargs)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            sys.excepthook(*sys.exc_info())
    threading.Thread.run = run
install_thread_excepthook()


message_queue = queue.Queue()

consumer = Consumer(token)
db = Database()
dispatch = Dispatcher(message_queue, db, consumer, commands)


gw = Gateway(token, message_queue)
gw.start()
dispatch.start()
