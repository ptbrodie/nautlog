import time
from threading import Lock

from event import Event
from manager import MANAGER


class Logger(object):

    def __init__(self, priority=1):
        self.priority = priority
        self.lock = Lock()
        self.init_queue()
        self.transaction = []

    def init_queue(self):
        with self.lock:
            self.queue = MANAGER.getqueue(self.priority)

    def log(self, message):
        if not self.queue:
            self.init_queue()
        with self.lock:
            event = Event(time.time(), self.priority, message)
            self.queue.push(event)

    def log_t(self, message):
        self.transaction.append(message)

    def commit(self):
        with self.lock:
            self.queue = MANAGER.getqueue(self.priority)
            for message in self.transaction:
                event = Event(time.time(), self.priority, message)
                self.queue.push(event)
        self.transaction = []
