from logger import Logger
from manager import MANAGER


def test_log():
    MANAGER.reset()
    lo = Logger(1)
    lo.log("abc")
    queue = MANAGER.getqueue(1)
    assert len(queue.events) == 1
    event = queue.events[0]
    assert event.message == "abc"


def test_log_two():
    MANAGER.reset()
    lo = Logger(1)
    lo.log("abc")
    hi = Logger(2)
    hi.log("def")
    qlo = MANAGER.getqueue(1)
    qhi = MANAGER.getqueue(2)
    assert len(qlo.events) == 1
    assert len(qhi.events) == 1
    eventlo = qlo.events[0]
    assert eventlo.message == "abc"
    eventhi = qhi.events[0]
    assert eventhi.message == "def"


def test_log_t():
    MANAGER.reset()
    lo = Logger(1)
    lo.log_t("1")
    lo.log_t("2")
    lo.log_t("3")
    lo.commit()
    qlo = MANAGER.getqueue(1)
    assert len(qlo.events) == 3


def run_tests():
    test_log()
    test_log_two()
    test_log_t()
