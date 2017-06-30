import os
import shutil

from io import StackIO
from logger import Logger
from reader import Reader
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


def test_log_past_capacity_read_all():
    remove_log_dir()
    MANAGER.reset()
    tmp = settings.INMEM_EVENT_STACK_CAPACITY
    set_capacity(4)
    lo = Logger()
    for i in range(10):
        lo.log("%s" % i)
    r = Reader()
    for i in reversed(range(10)):
        assert r.get().message == "%s" % i
    remove_log_dir()
    set_capacity(tmp)


def test_log_past_capacity_read_all_multi():
    remove_log_dir()
    MANAGER.reset()
    tmp = settings.INMEM_EVENT_STACK_CAPACITY
    set_capacity(4)
    lo = Logger(1)
    hi = Logger(2)
    for i in range(10):
        lo.log("%s" % i)
    for i in range(10, 20):
        hi.log("%s" % i)
    r = Reader()
    for i in reversed(range(20)):
        assert r.get().message == "%s" % i
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
    test_log_past_capacity_read_all()
    test_log_past_capacity_read_all_multi()
    remove_log_dir()
