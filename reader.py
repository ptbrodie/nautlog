from threading import Lock

from manager import MANAGER


class Reader(object):

    """
    The Reader.
    By default a Reader reads from the log
    by highest priority followed by chronology.
    The default can be overridden by constructing
    a Reader object with a set priority.
    """

    def __init__(self, priority=None):
        self.priority = priority
        self.lock = Lock()

    def get(self):
        """ Read the most recent event from the appropriate queue. """
        with self.lock:
            queue = MANAGER.getqueue(self.priority)
            if not queue:
                queue = MANAGER.gettop()
            return queue.pop() if queue else None

    def get_all(self, limit=1):
        """
        Read greedily from the log `limit` number of times by locking access
        """
        with self.lock:
            queue = MANAGER.gettop()
            for i in xrange(limit):
                yield queue.pop()
                if not queue.has_events():
                    queue = MANAGER.gettop()
