import os
import shutil

from io import StackIO
from logger import Logger
from manager import MANAGER
import settings


def test_flush():
    remove_log_dir()
    MANAGER.reset()
    tmp = settings.INMEM_EVENT_STACK_CAPACITY
    set_capacity(3)
    lo = Logger()
    lo.log("1")
    lo.log("2")
    lo.stack.flush()
    matches = StackIO.get_matches(1)
    assert matches
    remove_log_dir()
    set_capacity(tmp)


def test_fill():
    remove_log_dir()
    MANAGER.reset()
    tmp = settings.INMEM_EVENT_STACK_CAPACITY
    set_capacity(4)
    lo = Logger()
    lo.log("1")
    lo.log("2")
    lo.log("3")
    lo.stack.flush()
    assert not(lo.stack.events)
    lo.stack.fill()
    assert lo.stack.events
    remove_log_dir()
    set_capacity(tmp)


def test_log_past_capacity():
    remove_log_dir()
    MANAGER.reset()
    tmp = settings.INMEM_EVENT_STACK_CAPACITY
    set_capacity(4)
    lo = Logger()
    for i in range(10):
        lo.log("%s" % i)
    matches = StackIO.get_matches(1)
    assert matches
    remove_log_dir()
    set_capacity(tmp)


def set_capacity(capacity):
    settings.INMEM_EVENT_STACK_CAPACITY = capacity

def remove_log_dir():
    if os.path.exists(settings.LOGDIR):
        shutil.rmtree(settings.LOGDIR)


def run_tests():
    test_flush()
    test_fill()
    test_log_past_capacity()
    remove_log_dir()
