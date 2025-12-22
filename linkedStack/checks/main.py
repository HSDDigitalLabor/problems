import check50
import check50.py

FILE_NAME = "linkedStack.py"


@check50.check()
def exists():
    """linkedStack.py exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def compiles():
    """linkedStack.py compiles"""
    check50.py.compile(FILE_NAME)


@check50.check(compiles)
def has_classes_and_methods():
    """Classes ListNode, LinkedList, Stack and methods push, pop, peek exist"""
    module = check50.py.import_(FILE_NAME)

    if not hasattr(module, "ListNode"):
        msg = f"Class `ListNode` not found in {FILE_NAME}"
        raise check50.Failure(msg)

    if not hasattr(module, "LinkedList"):
        msg = f"Class `LinkedList` not found in {FILE_NAME}"
        raise check50.Failure(msg)

    if not hasattr(module, "Stack"):
        msg = f"Class `Stack` not found in {FILE_NAME}"
        raise check50.Failure(msg)

    stack_instance = module.Stack()

    if not hasattr(stack_instance, "push"):
        msg = "Method `push` not found in Class `Stack`"
        raise check50.Failure(msg)
    if not hasattr(stack_instance, "pop"):
        msg = "Method `pop` not found in Class `Stack`"
        raise check50.Failure(msg)
    if not hasattr(stack_instance, "peek"):
        msg = "Method `peek` not found in Class `Stack`"
        raise check50.Failure(msg)


@check50.check(has_classes_and_methods)
def test_push_peek():
    """push adds element and peek returns it"""
    module = check50.py.import_(FILE_NAME)
    stack = module.Stack()

    stack.push(10)
    top = stack.peek()

    if top != 10:
        raise check50.Mismatch(
            "10", str(top), help="peek should return the last pushed value"
        )


@check50.check(has_classes_and_methods)
def test_push_pop():
    """pop removes and returns the top element"""
    module = check50.py.import_(FILE_NAME)
    stack = module.Stack()

    stack.push(20)
    popped = stack.pop()

    if popped != 20:
        raise check50.Mismatch(
            "20", str(popped), help="pop should return the last pushed value"
        )

    if stack.peek() is not None:
        msg = "Stack should be empty after popping the only element"
        raise check50.Failure(msg)


@check50.check(has_classes_and_methods)
def test_lifo_order():
    """Stack follows LIFO (Last-In, First-Out) order"""
    module = check50.py.import_(FILE_NAME)
    stack = module.Stack()

    stack.push(1)
    stack.push(2)
    stack.push(3)

    if stack.pop() != 3:
        msg = "First pop should return 3"
        raise check50.Failure(msg)
    if stack.pop() != 2:
        msg = "Second pop should return 2"
        raise check50.Failure(msg)
    if stack.pop() != 1:
        msg = "Third pop should return 1"
        raise check50.Failure(msg)


@check50.check(has_classes_and_methods)
def test_empty_stack():
    """pop and peek return None on empty stack"""
    module = check50.py.import_(FILE_NAME)
    stack = module.Stack()

    if stack.peek() is not None:
        msg = "peek on empty stack should return None"
        raise check50.Failure(msg)

    if stack.pop() is not None:
        msg = "pop on empty stack should return None"
        raise check50.Failure(msg)


@check50.check(has_classes_and_methods)
def test_mixed_operations():
    """Stack handles mixed push and pop operations correctly"""
    module = check50.py.import_(FILE_NAME)
    stack = module.Stack()

    stack.push(10)
    stack.push(20)
    if stack.pop() != 20:
        msg = "Pop should return 20"
        raise check50.Failure(msg)

    stack.push(30)
    if stack.pop() != 30:
        msg = "Pop should return 30"
        raise check50.Failure(msg)

    if stack.pop() != 10:
        msg = "Pop should return 10"
        raise check50.Failure(msg)

    if stack.pop() is not None:
        msg = "Pop on empty stack should return None"
        raise check50.Failure(msg)


@check50.check(has_classes_and_methods)
def test_peek_idempotent():
    """peek returns the same value multiple times without removing it"""
    module = check50.py.import_(FILE_NAME)
    stack = module.Stack()

    stack.push(42)

    val1 = stack.peek()
    val2 = stack.peek()

    if val1 != 42 or val2 != 42:
        msg = "peek should return 42 consistently"
        raise check50.Failure(msg)

    if stack.pop() != 42:
        msg = "Item should still be on stack after peek"
        raise check50.Failure(msg)


@check50.check(has_classes_and_methods)
def test_independent_stacks():
    """Multiple Stack instances are independent"""
    module = check50.py.import_(FILE_NAME)
    stack1 = module.Stack()
    stack2 = module.Stack()

    stack1.push(1)
    stack2.push(2)

    if stack1.peek() != 1:
        msg = "stack1 should have 1 at top"
        raise check50.Failure(msg)
    if stack2.peek() != 2:
        msg = "stack2 should have 2 at top"
        raise check50.Failure(msg)

    stack1.pop()
    if stack2.peek() != 2:
        msg = "stack2 should still have 2 after popping stack1"
        raise check50.Failure(msg)
