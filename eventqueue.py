import os

from io import QueueIO
import settings


class EventQueue(object):

    """
    This class implements a wrapper for adding, removing, and inspecting events at a given priority.
    """

    def __init__(self, priority, capacity=settings.INMEM_EVENT_QUEUE_CAPACITY):
        self.priority = priority
        self.events = []
        self.capacity = capacity

    def push(self, message):
        """ Add an event to the queue. """
        self.events.append(message)
        if len(self.events) >= self.capacity:
            self.flush()

    def pop(self):
        """ Remove the most recent event from the queue. """
        # Try to return inmem
        if not self.events:
            # Try to read from disk
            self.events = self.fill()
            if not self.events:
                # Nothing found for this queue
                return None
        return self.events.pop(0)

    def peek(self):
        """ Look at the most recent event in the queue, but do not remove """
        if not self.events:
            return None
        return self.events[0]

    def clear(self):
        """ Clear all messages in the queue """
        self.events = []

    def flush(self):
        """ Flush the events in this queue to disk """
        middle = len(self.events) / 2
        first = self.events[:middle]
        last = self.events[middle:]
        firstpath = QueueIO.logfile(self.priority, first[0].timestamp)
        QueueIO.write(firstpath, first)
        lastpath = QueueIO.logfile(self.priority, last[0].timestamp)
        QueueIO.write(lastpath, first)
        self.events = []

    def fill(self):
        """ Fill this queue with events were flushed to disk """
        matches = QueueIO.get_matches(self.priority)
        if not matches:
            return None
        choice = os.path.join(settings.LOGDIR, sorted(matches, reverse=True)[0])
        self.events = QueueIO.read_events(choice)
        os.remove(choice)
        return self.events

    def has_events(self):
        return len(self.events)
