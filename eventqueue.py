import os

from io import QueueIO
import settings


class EventQueue(object):

    def __init__(self, priority, capacity=settings.INMEM_EVENT_QUEUE_CAPACITY):
        self.priority = priority
        self.events = []
        self.capacity = capacity

    def push(self, message):
        self.events.append(message)
        if len(self.events) >= self.capacity:
            self.flush()

    def pop(self):
        # Try to return inmem
        if not self.events:
            # Try to read from disk
            self.events = self.fill()
            if not self.events:
                # Nothing found for this queue
                return None
        return self.events.pop(0)

    def peek(self):
        if not self.events:
            return None
        return self.events[0]

    def clear(self):
        """ Clear all messages in the queue """
        self.events = []

    def flush(self):
        middle = len(self.events) / 2
        first = self.events[:middle]
        last = self.events[middle:]
        firstpath = QueueIO.logfile(self.priority, first[0].timestamp)
        QueueIO.write(firstpath, first)
        lastpath = QueueIO.logfile(self.priority, last[0].timestamp)
        QueueIO.write(lastpath, first)
        self.events = []

    def fill(self):
        matches = QueueIO.get_matches(self.priority)
        if not matches:
            return None
        choice = os.path.join(settings.LOGDIR, sorted(matches, reverse=True)[0])
        self.events = QueueIO.read_events(choice)
        os.remove(choice)
        return self.events

    def has_events(self):
        return len(self.events)
