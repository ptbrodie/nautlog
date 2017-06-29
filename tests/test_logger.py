from logger import Logger
from reader import Reader
from manager import MANAGER


def test_log():
    MANAGER.reset()
    lo = Logger(1)
    lo.log("abc")
    stack = MANAGER.getstack(1)
    assert len(stack.events) == 1
    event = stack.events[0]
    assert event.message == "abc"


def test_log_two():
    MANAGER.reset()
    lo = Logger(1)
    lo.log("abc")
    hi = Logger(2)
    hi.log("def")
    qlo = MANAGER.getstack(1)
    qhi = MANAGER.getstack(2)
    assert len(qlo.events) == 1
    assert len(qhi.events) == 1
    eventlo = qlo.events[0]
    assert eventlo.message == "abc"
    eventhi = qhi.events[0]
    assert eventhi.message == "def"


def test_log_three():
    MANAGER.reset()
    lo = Logger()
    hi = Logger(2)
    lo.log("abc")
    hi.log("def")
    lo.log("ghi")

    reader = Reader()
    reader.get().message == "def"
    reader.get().message == "ghi"
    reader.get().message == "abc"
    reader.get()


def test_log_t():
    MANAGER.reset()
    lo = Logger(1)
    lo.log_t("1")
    lo.log_t("2")
    lo.log_t("3")
    lo.commit()
    qlo = MANAGER.getstack(1)
    assert len(qlo.events) == 3
    reader = Reader(1)
    assert reader.get().message == "3"


def test_log_t_empty():
    MANAGER.reset()
    lo = Logger(1)
    lo.commit()
    qlo = MANAGER.getstack(1)
    assert not len(qlo.events)


def test_log_t_commit_whole():
    MANAGER.reset()
    lo = Logger(1)
    lo.log_t("1")
    lo.log_t("2")
    lo.log_t("3")
    lo.commit_whole()
    qlo = MANAGER.getstack(1)
    assert len(qlo.events) == 1
    reader = Reader(1)
    assert reader.get().message == "123"


def run_tests():
    test_log()
    test_log_two()
    test_log_three()
    test_log_t()
    test_log_t_empty()
    test_log_t_commit_whole()
