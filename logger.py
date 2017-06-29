import time
from threading import Lock

from event import Event
from manager import MANAGER


class Logger(object):
    """
    The logger.
    Implements a threadsafe logger, with transactional capability.
    """

    def __init__(self, priority=1):
        self.priority = priority
        self.lock = Lock()
        self.init_stack()
        self.transaction = []

    def init_stack(self):
        with self.lock:
            self.stack = MANAGER.getstack(self.priority)

    def log(self, message):
        """ Log one message to the EventStack """
        if not self.stack:
            self.init_stack()
        with self.lock:
            event = Event(time.time(), self.priority, message)
            self.stack.push(event)

    def log_t(self, message):
        """ Add the given message to the current transaction """
        self.transaction.append(message)

    def commit(self):
        """ Commit the messages in the transaction to the EventStack """
        with self.lock:
            self.stack = MANAGER.getstack(self.priority)
            for message in self.transaction:
                event = Event(time.time(), self.priority, message)
                self.stack.push(event)
        self.transaction = []

    def commit_whole(self):
        """ Concatenate messages in the transaction and commit them as one event """
        whole_message = "".join(self.transaction)
        self.log(whole_message)
