import commands
import threading


class Dispatcher(object):
    COMMAND_PREFIX = "!c:"

    def __init__(self, inc_queue, database_connection, consumer):
        self.inc_queue = inc_queue
        self.data_conn = database_connection
        self.consumer  = consumer
        self.running   = False

    def is_command(self, content):
        return len(content) >= len(Dispatcher.COMMAND_PREFIX) and content[:3] == Dispatcher.COMMAND_PREFIX

    def parse(self, content):
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

    def dispatch(self, command, params, message):
        command_func = commands.identifiers[command]
        return command_func(params, message)

    def store(self, message):
        pass

    def run(self):
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
        self.running = True
        t = threading.Thread(target=self.run)
        t.start()

    def stop(self):
        self.running = False
