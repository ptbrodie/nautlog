import os

from io import QueueIO
from logger import Logger
from manager import MANAGER
import settings


def test_flush():
    MANAGER.reset()
    settings.INMEM_EVENT_QUEUE_CAPACITY = 2
    lo = Logger()
    lo.log("1")
    lo.log("2")
    chkpath = QueueIO.logfile(lo.queue.priority, lo.queue.events[0].timestamp)
    lo.queue.flush()
    assert os.path.exists(chkpath)
    os.remove(chkpath)


def test_fill():
    MANAGER.reset()
    settings.INMEM_EVENT_QUEUE_CAPACITY = 4
    lo = Logger()
    lo.log("1")
    lo.log("2")
    lo.log("3")
    lo.queue.flush()
    assert not(lo.queue.events)
    lo.queue.fill()
    assert lo.queue.events


def run_tests():
   test_flush()
   test_fill()
