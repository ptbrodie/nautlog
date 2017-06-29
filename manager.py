from eventqueue import EventQueue


class LogManager(object):

    def __init__(self):
        self.queues = {}

    def getqueue(self, priority):
        if priority is None:
            return None
        queue = self.queues.get(priority)
        if not queue:
            queue = EventQueue(priority)
            self.queues[priority] = queue
        return queue

    def gettop(self):
        for priority in sorted(self.queues.keys(), reverse=True):
            queue = self.queues[priority]
            if queue.has_events():
                return queue
        return None

    def reset(self):
        self.queues = {}


# Create singleton instance of log manager
MANAGER = LogManager()
