from manager import MANAGER


def test_getqueue_new():
    queue = MANAGER.getqueue(1)
    assert queue.priority == 1
    MANAGER.queues = {}


def test_getqueue_two():
    MANAGER.reset()
    queue1 = MANAGER.getqueue(1)
    queue2 = MANAGER.getqueue(2)
    assert queue1.priority != queue2.priority
    assert queue2.priority == 2
    MANAGER.reset()


def test_getqueue_existing():
    MANAGER.reset()
    MANAGER.getqueue(1)
    MANAGER.getqueue(1)
    MANAGER.getqueue(1)
    assert len(MANAGER.queues.values()) == 1


def run_tests():
    test_getqueue_new()
    test_getqueue_two()
    test_getqueue_existing()
