from eventqueue import EventQueue


class LogManager(object):
    """
    This class manages finding the queue that
    a given logger or reader is asking for.
    """

    def __init__(self):
        self.queues = {}

    def getqueue(self, priority):
        """ Return the queue corresponding to the given priority """
        if priority is None:
            return None
        queue = self.queues.get(priority)
        if not queue:
            queue = EventQueue(priority)
            self.queues[priority] = queue
        return queue

    def gettop(self):
        """ Return the highest priority queue """
        for priority in sorted(self.queues.keys(), reverse=True):
            queue = self.queues[priority]
            if queue.has_events():
                return queue
        return None

    def reset(self):
        """ Nuke the queues in this manager """
        self.queues = {}


# Create singleton instance of log manager
MANAGER = LogManager()
