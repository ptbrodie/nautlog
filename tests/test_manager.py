from manager import MANAGER


def test_getstack_new():
    stack = MANAGER.getstack(1)
    assert stack.priority == 1
    MANAGER.stacks = {}


def test_getstack_two():
    MANAGER.reset()
    stack1 = MANAGER.getstack(1)
    stack2 = MANAGER.getstack(2)
    assert stack1.priority != stack2.priority
    assert stack2.priority == 2
    MANAGER.reset()


def test_getstack_existing():
    MANAGER.reset()
    MANAGER.getstack(1)
    MANAGER.getstack(1)
    MANAGER.getstack(1)
    assert len(MANAGER.stacks.values()) == 1


def run_tests():
    test_getstack_new()
    test_getstack_two()
    test_getstack_existing()
