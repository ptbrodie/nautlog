import time
from threading import Thread
from random import randint
from uuid import uuid4

from logger import Logger
from reader import Reader
from manager import MANAGER


def to_int(value):
    try:
        return int(value)
    except Exception:
        pass


def log_n_times(n):
    logger = Logger()
    for i in xrange(n):
        logger.log("%s" % uuid4())


def test_thread_load():
    MANAGER.reset()
    pool = []
    for i in xrange(10):
        thread = Thread(target=log_n_times, args=(100,))
        pool.append(thread)
        thread.start()

    for thread in pool:
        thread.join()

    reader = Reader()
    for i in xrange(1000):
        assert reader.get()


def test_thread_sequence():
    """
    The way that we test thread safety is as follows:
        0. define a function that logs timestamped events
        1. apply function across threads
        2. sequence should read in reverse chronological order
    """
    MANAGER.reset()
    pool = []
    for i in xrange(4):
        thread = Thread(target=log_n_times, args=(20,))
        pool.append(thread)
        thread.start()

    for thread in pool:
        thread.join()

    reader = Reader()
    event = reader.get()
    while event:
        next = reader.get()
        if next:
            assert str(event.timestamp) >= str(next.timestamp)
        event = next
        next = None


def run_tests():
    test_thread_load()
    test_thread_sequence()
