import os

from io import StackIO
import settings


class EventStack(object):

    """
    This class implements a wrapper for adding, removing, and inspecting events at a given priority.
    """

    def __init__(self, priority, capacity=settings.INMEM_EVENT_STACK_CAPACITY):
        self.priority = priority
        self.events = []
        self.capacity = capacity

    def push(self, message):
        """ Add an event to the stack. """
        self.events.append(message)
        if len(self.events) >= self.capacity:
            self.flush()

    def pop(self):
        """ Remove the most recent event from the stack. """
        # Try to return inmem
        if not self.events:
            # Try to read from disk
            self.events = self.fill()
            if not self.events:
                # Nothing found for this stack
                return None
        return self.events.pop(len(self.events) - 1)

    def peek(self):
        """ Look at the most recent event in the stack, but do not remove """
        if not self.events:
            return None
        return self.events[0]

    def clear(self):
        """ Clear all messages in the stack """
        self.events = []

    def flush(self):
        """ Flush the events in this stack to disk """
        middle = len(self.events) / 2
        first = self.events[:middle]
        last = self.events[middle:]
        firstpath = StackIO.logfile(self.priority, first[0].timestamp)
        StackIO.write(firstpath, first)
        lastpath = StackIO.logfile(self.priority, last[0].timestamp)
        StackIO.write(lastpath, first)
        self.events = []

    def fill(self):
        """ Fill this stack with events were flushed to disk """
        matches = StackIO.get_matches(self.priority)
        if not matches:
            return None
        choice = os.path.join(settings.LOGDIR, sorted(matches, reverse=True)[0])
        self.events = StackIO.read_events(choice)
        os.remove(choice)
        return self.events

    def has_events(self):
        return len(self.events)
