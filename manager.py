from threading import Lock

from eventstack import EventStack


class LogManager(object):
    """
    This class manages finding the stack that
    a given logger or reader is asking for.
    """

    def __init__(self):
        self.stacks = {}

    def getstack(self, priority):
        """ Return the stack corresponding to the given priority """
        if priority is None:
            return None
        stack = self.stacks.get(priority)
        if not stack:
            stack = EventStack(priority)
            self.stacks[priority] = stack
        return stack

    def gettop(self):
        """ Return the highest priority stack """
        for priority in sorted(self.stacks.keys(), reverse=True):
            stack = self.stacks[priority]
            if stack.has_events():
                return stack
        return None

    def reset(self):
        """ Nuke the stacks in this manager """
        self.stacks = {}


# Create singleton instance of log manager
MANAGER = LogManager()

# Create a lock for threads to share
LOCK = Lock()
