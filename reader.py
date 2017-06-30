from manager import LOCK, MANAGER


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

    def get(self):
        """ Read the most recent event from the appropriate stack. """
        with LOCK:
            stack = MANAGER.getstack(self.priority)
            if not stack:
                stack = MANAGER.gettop()
            return stack.pop() if stack else None

    def get_all(self, limit=1):
        """
        Read greedily from the log `limit` number of times by locking access
        """
        with LOCK:
            stack = MANAGER.gettop()
            for i in xrange(limit):
                yield stack.pop()
                if not stack.has_events():
                    stack = MANAGER.gettop()
