import fnmatch
import os

from event import Event
import settings


class QueueIO(object):

    """
    This class implements utilities for queues
    to read and write from files.
    """

    @staticmethod
    def logfile(priority, timestamp):
        """ Get filename corresponding to the given priority and timestamp """
        filename = "nautlog_%s_%s.log" % (priority, timestamp)
        return os.path.join(settings.LOGDIR, filename)

    @staticmethod
    def write(fullpath, events):
        """ Write events to the given file """
        if not os.path.exists(settings.LOGDIR):
            os.makedirs(settings.LOGDIR)
        with open(fullpath, "wb") as f:
            for event in events:
                f.write("%s\n" % event)

    @staticmethod
    def get_matches(priority):
        """ Get log files that were written at the given priority """
        matches = []
        if not os.path.exists(settings.LOGDIR):
            return []
        for file in os.listdir(settings.LOGDIR):
            if fnmatch.fnmatch(file, "nautlog_%s_*.log" % priority):
                matches.append(file)
        return matches

    @staticmethod
    def read_events(filename):
        """ Read events from a file"""
        events = []
        with open(filename, 'r') as f:
            events = [Event.from_str(e) for e in f.readlines()]
        return events
