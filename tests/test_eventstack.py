from eventstack import EventStack


def test_push():
    stack = EventStack(1)
    stack.push("abc")
    assert len(stack.events) == 1
    assert stack.events[0] == "abc"


def test_clear():
    stack = EventStack(1)
    stack.push("abc")
    stack.push("def")
    assert len(stack.events) == 2
    stack.clear()
    assert not len(stack.events)


def test_pop():
    stack = EventStack(1)
    stack.push("abc")
    stack.push("def")
    assert stack.pop() == "def"


def run_tests():
    test_push()
    test_clear()
    test_pop()
