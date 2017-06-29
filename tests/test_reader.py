from logger import Logger
from manager import MANAGER
from reader import Reader


def test_get_empty():
    MANAGER.reset()
    reader = Reader()
    assert not reader.get()


def test_get_empty_priority():
    MANAGER.reset()
    reader = Reader(1)
    assert not reader.get()


def test_get_one_priority():
    MANAGER.reset()
    logger = Logger(1)
    logger.log("abc")
    reader = Reader(1)
    assert reader.get().message == "abc"
    assert not reader.get()


def test_get_one():
    MANAGER.reset()
    logger = Logger(1)
    logger.log("abc")
    reader = Reader()
    assert reader.get().message == "abc"
    assert not reader.get()


def test_get_two_priority():
    MANAGER.reset()
    lo = Logger(1)
    hi = Logger(2)
    lo.log("abc")
    hi.log("def")
    reader = Reader(1)   # read on channel 1
    assert reader.get().message == "abc"
    assert not reader.get()


def test_get_two():
    MANAGER.reset()
    lo = Logger(1)
    hi = Logger(2)
    lo.log("abc")
    hi.log("def")
    reader = Reader()    # no specific channel
    assert reader.get().message == "def"
    assert reader.get().message == "abc"
    assert not reader.get()


def test_get_three_various():
    MANAGER.reset()
    lo = Logger(1)
    mid = Logger(2)
    hi = Logger(3)
    lo.log("1")
    lo.log("2")
    mid.log("3")
    reader = Reader()
    assert reader.get().message == "3"
    assert reader.get().message == "2"
    assert reader.get().message == "1"

    MANAGER.reset()
    lo.log("1")
    hi.log("5")
    lo.log("2")
    mid.log("3")
    mid.log("4")
    assert reader.get().message == "5"
    assert reader.get().message == "4"
    assert reader.get().message == "3"
    assert reader.get().message == "2"
    assert reader.get().message == "1"


def run_tests():
    test_get_empty()
    test_get_empty_priority()
    test_get_one()
    test_get_two()
