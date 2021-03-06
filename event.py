import threading


class Event(object):

    """
    Definition of an event. An event has
        - a priority,
        - timestamp,
        - message,
        - and the name of the thread that created it.
    """

    def __init__(self, timestamp, priority, message):
        self.priority = priority
        self.timestamp = timestamp
        self.message = message
        self.thread = threading.current_thread().name

    def __str__(self):
        return "%f:%s:%d:%s" % (self.timestamp, self.thread, self.priority, self.message)

    @staticmethod
    def from_str(string):
        args = string.split(":")
        event = Event(args[0], args[2], args[3])
        event.thread = args[1]
        return event
