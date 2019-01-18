import threading
import queue
import logging


class Dispatcher(object):
    """A dispatcher to relay the received messages to the appropriate
    commands.

    Args:
        inc_queue: The incoming message queue.
        database_connection: The datanase interface.
        consumer: The discord REST API consumer to send messages through.
    """
    COMMAND_PREFIX = "!c/" # Must end with delimiter
    DELIMITER      = "/"

    def __init__(self, inc_queue, database_connection, consumer, commands, queue_timeout=10, logging=logging):
        self.inc_queue = inc_queue
        self.data_conn = database_connection
        self.consumer  = consumer
        self.commands  = commands
        self.running   = False
        self.queue_timeout = queue_timeout
        self.logger = logging.getLogger(__name__)

    def is_command(self, content):
        """Indicates whether a message is a command.

        Args:
            content: The contents of the message.

        Returns:
            A boolean indicating whether the message is a command.
        """
        return len(content) >= len(Dispatcher.COMMAND_PREFIX) and content[:3] == Dispatcher.COMMAND_PREFIX

    def parse(self, content):
        """Parses a message to extract the command and its parameters.

        Args:
            content: The contents of the message.

        Returns:
            A tuple containing the command identifier and the parameters.
        """
        if self.is_command(content):

            # Extract command
            #commands look like:
            # prefix(includes delimiter) command delimiter params
            # without spaces
            command = content.split(Dispatcher.DELIMITER)[1]
            if command == "":
                raise ValueError("Badly formatted command.")

            # Extract params
            content_start = len(Dispatcher.COMMAND_PREFIX) + len(command)
            params = content[content_start:]

            # Getting rid of the delimiter
            if len(params) >= 1:
                params = params[1:]

            return command, params
        return None, None

    def dispatch(self, command_id, message, *args):
        """Calls the appropriate command with the given parameters.

        Args:
            command_id: The string identifier of the command.
            params: The parameters to be passed to the command.
            message: The full message which contained the command.

        Returns:
            The results of the command.
        """
        self.logger.info("Comand called by %s(%s): %s.", message.username, message.author_id, command_id)
        command = self.commands.identifiers[command_id]
        return command(message, self.data_conn, *args)

    def process_message(self, message):
        """Calls the appropriate command with the given parameters.

        Args:
            command_id: The string identifier of the command.
            params: The parameters to be passed to the command.
            message: The full message which contained the command.

        Returns:
            The results of the command.
        """
        command, params = self.parse(message.content)
        if command:
            if command in self.commands.identifiers:
                response = self.dispatch(command, message, params)
            else:
                response = self.dispatch("unknown_command", message)
            self.consumer.create_message(response)
        self.dispatch("store", message)

    def run(self):
        """Listens for new messages in the incoming queue and dispatches
        them to the appropriate commands and stores them.
        """
        self.logger.info("Dispatcher loop started.")
        while self.running:
            try:
                message = self.inc_queue.get(timeout=self.queue_timeout)
            except queue.Empty:
                continue

            if message == None:
                self.stop()
                break

            self.process_message(message)
        self.logger.info("Dispatcher loop ended.")

    def start(self):
        """Starts listening for incoming messages."""
        self.logger.info("Dispatcher thread starting.")
        self.running = True
        t = threading.Thread(target=self.run)
        t.start()
        return t

    def stop(self):
        """Stops listening for incoming messages."""
        self.logger.info("Dispatcher thread stopping.")
        self.running = False
