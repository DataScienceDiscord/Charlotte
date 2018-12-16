import commands
import threading


class Dispatcher(object):
    """A dispatcher to relay the received messages to the appropriate
    commands.

    Args:
        inc_queue: The incoming message queue.
        database_connection: The datanase interface.
        consumer: The discord REST API consumer to send messages through.
    """
    COMMAND_PREFIX = "!c:"

    def __init__(self, inc_queue, database_connection, consumer):
        self.inc_queue = inc_queue
        self.data_conn = database_connection
        self.consumer  = consumer
        self.running   = False

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
            command = content.split(":")[1]
            if command == "":
                raise ValueError("Badly formatted command.")

            # Extract params
            content_start = len(Dispatcher.COMMAND_PREFIX) + len(command)# +:
            if content_start > len(content):
                raise ValueError("Badly formatted command.")
            params = content[content_start:]

            # Getting rid of the ":"
            if len(params) >= 1:
                params = params[1:]

            return command, params
        return None, None

    def dispatch(self, command_id, params, message):
        """Calls the appropriate command with the given parameters.

        Args:
            command_id: The string identifier of the command.
            params: The parameters to be passed to the command.
            message: The full message which contained the command.

        Returns:
            The results of the command.
        """
        command = commands.identifiers[command_id]
        return command(params, message)

    def store(self, message):
        pass

    def run(self):
        """Listens for new messages in the incoming queue and dispatches
        them to the appropriate commands and stores them.
        """
        while self.running:
            message = self.inc_queue.get()

            if message == None:
                self.stop()
                break

            command, params = self.parse(message.content)
            if command:
                response = self.dispatch(command, params, message)
                self.consumer.create_message(response)
            else:
                self.store(message)

    def start(self):
        """Starts listening for incoming messages."""
        self.running = True
        t = threading.Thread(target=self.run)
        t.start()

    def stop(self):
        """Stops listening for incoming messages."""
        self.running = False
