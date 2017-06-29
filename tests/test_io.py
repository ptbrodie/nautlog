import os

from io import StackIO
from logger import Logger
from manager import MANAGER
import settings


def test_flush():
    MANAGER.reset()
    settings.INMEM_EVENT_stack_CAPACITY = 2
    lo = Logger()
    lo.log("1")
    lo.log("2")
    chkpath = StackIO.logfile(lo.stack.priority, lo.stack.events[0].timestamp)
    lo.stack.flush()
    assert os.path.exists(chkpath)
    os.remove(chkpath)


def test_fill():
    MANAGER.reset()
    settings.INMEM_EVENT_stack_CAPACITY = 4
    lo = Logger()
    lo.log("1")
    lo.log("2")
    lo.log("3")
    lo.stack.flush()
    assert not(lo.stack.events)
    lo.stack.fill()
    assert lo.stack.events


def run_tests():
    test_flush()
    test_fill()
