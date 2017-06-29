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
        self.init_queue()
        self.transaction = []

    def init_queue(self):
        with self.lock:
            self.queue = MANAGER.getqueue(self.priority)

    def log(self, message):
        """ Log one message to the EventQueue """
        if not self.queue:
            self.init_queue()
        with self.lock:
            event = Event(time.time(), self.priority, message)
            self.queue.push(event)

    def log_t(self, message):
        """ Add the given message to the current transaction """
        self.transaction.append(message)

    def commit(self):
        """ Commit the messages in the transaction to the EventQueue """
        with self.lock:
            self.queue = MANAGER.getqueue(self.priority)
            for message in self.transaction:
                event = Event(time.time(), self.priority, message)
                self.queue.push(event)
        self.transaction = []
