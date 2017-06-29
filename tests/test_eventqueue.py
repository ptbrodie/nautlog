from eventqueue import EventQueue


def test_push():
    queue = EventQueue(1)
    queue.push("abc")
    assert len(queue.events) == 1
    assert queue.events[0] == "abc"


def test_clear():
    queue = EventQueue(1)
    queue.push("abc")
    queue.push("def")
    assert len(queue.events) == 2
    queue.clear()
    assert not len(queue.events)


def test_pop():
    queue = EventQueue(1)
    queue.push("abc")
    queue.push("def")
    assert queue.pop() == "abc"


def run_tests():
    test_push()
    test_clear()
    test_pop()
