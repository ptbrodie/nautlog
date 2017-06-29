import fnmatch
import os

from event import Event
import settings


class QueueIO(object):

    @staticmethod
    def logfile(priority, timestamp):
        filename = "nautlog_%s_%s.log" % (priority, timestamp)
        return os.path.join(settings.LOGDIR, filename)

    @staticmethod
    def write(fullpath, events):
        if not os.path.exists(settings.LOGDIR):
            os.makedirs(settings.LOGDIR)
        with open(fullpath, "wb") as f:
            for event in events:
                f.write("%s\n" % event)

    @staticmethod
    def get_matches(priority):
        matches = []
        if not os.path.exists(settings.LOGDIR):
            return []
        for file in os.listdir(settings.LOGDIR):
            if fnmatch.fnmatch(file, 'nautlog_%s_*.log' % priority):
                matches.append(file)
        return matches

    @staticmethod
    def read_events(filename):
        events = []
        with open(filename, 'r') as f:
            events = [Event.from_str(e) for e in f.readlines()]
        return events
