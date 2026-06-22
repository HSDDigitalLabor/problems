import check50
import check50.py

FILE_NAME = "linkedAfter.py"


def to_list(ll):
    """LinkedList -> Python-Liste (mit Zyklus-Schutz)."""
    out = []
    cur = ll.head
    seen = 0
    while cur is not None:
        out.append(cur.value)
        cur = cur.next
        seen += 1
        if seen > 10_000:
            msg = f"Linked list appears to have a cycle (more than {seen} nodes)"
            raise check50.Failure(msg)
    return out


def build_ll(module, values):
    """Erzeugt eine LinkedList über FromPythonlist (wie in der Aufgabe vorgegeben)."""
    ll = module.LinkedList()
    ll.FromPythonlist(values)
    return ll


def a(self, b):
    c = self.head
    while c is not None:
        if c.value == b:
            return c
        c = c.next
    return None


@check50.check()
def exists():
    """linkedAfter.py exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def compiles():
    """linkedAfter.py compiles"""
    check50.py.compile(FILE_NAME)


@check50.check(compiles)
def has_classes_and_method():
    """ListNode, LinkedList and insertAfterNode exist"""
    module = check50.py.import_(FILE_NAME)

    if not hasattr(module, "ListNode"):
        msg = f"Class `ListNode` not found in {FILE_NAME}"
        raise check50.Failure(msg)

    if not hasattr(module, "LinkedList"):
        msg = f"Class `LinkedList` not found in {FILE_NAME}"
        raise check50.Failure(msg)

    if not hasattr(module.LinkedList(), "insertAfterNode"):
        msg = "Method `insertAfterNode` not found in Class `LinkedList`"
        raise check50.Failure(msg)


@check50.check(has_classes_and_method)
def test_frompythonlist_order_is_head_insertion():
    """FromPythonlist: inserts after head (result is reversed input order)"""
    module = check50.py.import_(FILE_NAME)

    ll = build_ll(module, [1, 2, 8, 4])
    expected = [4, 8, 2, 1]  # weil insertAfterHead bei Vorwärtsiteration umdreht
    actual = to_list(ll)

    if actual != expected:
        raise check50.Mismatch(str(expected), str(actual))


@check50.check(has_classes_and_method)
def test_insert_after_middle():
    """insertAfterNode inserts after a middle node (in reversed-built list)"""
    module = check50.py.import_(FILE_NAME)

    ll = build_ll(module, [1, 2, 8, 4])  # Liste: 4 -> 8 -> 2 -> 1
    module.LinkedList.searchValue = a
    node = ll.searchValue(8)
    if node is None:
        msg = "searchValue(8) returned None, but 8 should be in the list"
        raise check50.Failure(msg)

    ll.insertAfterNode(node, module.ListNode(3))

    expected = [4, 8, 3, 2, 1]
    actual = to_list(ll)
    if actual != expected:
        raise check50.Mismatch(str(expected), str(actual))


@check50.check(has_classes_and_method)
def test_insert_after_head():
    """insertAfterNode inserts after head"""
    module = check50.py.import_(FILE_NAME)

    ll = build_ll(module, [10, 20, 30])  # Liste: 30 -> 20 -> 10
    module.LinkedList.searchValue = a
    head = ll.head
    if head is None:
        msg = "Linked list head is None after FromPythonlist"
        raise check50.Failure(msg)

    ll.insertAfterNode(head, module.ListNode(25))

    expected = [30, 25, 20, 10]
    actual = to_list(ll)
    if actual != expected:
        raise check50.Mismatch(str(expected), str(actual))


@check50.check(has_classes_and_method)
def test_insert_after_tail():
    """insertAfterNode inserts after last node (tail)"""
    module = check50.py.import_(FILE_NAME)

    ll = build_ll(module, [10, 20, 30])  # Liste: 30 -> 20 -> 10
    module.LinkedList.searchValue = a
    tail = ll.searchValue(10)  # 10 ist Tail
    if tail is None:
        msg = "searchValue(10) returned None, but 10 should be in the list"
        raise check50.Failure(msg)

    ll.insertAfterNode(tail, module.ListNode(5))

    expected = [30, 20, 10, 5]
    actual = to_list(ll)
    if actual != expected:
        raise check50.Mismatch(str(expected), str(actual))


@check50.check(has_classes_and_method)
def test_insert_after_none_prevnode():
    """insertAfterNode with prevNode=None:
    We expect an exception (ValueError) rather than silently doing nothing."""
    module = check50.py.import_(FILE_NAME)

    ll = build_ll(module, [1, 2, 3])
    module.LinkedList.searchValue = a
    prev = ll.searchValue(999)  # not in list -> None
    new_node = module.ListNode(4)

    threw = False
    try:
        ll.insertAfterNode(prev, new_node)
    except ValueError:
        threw = True

    if not threw:
        msg = "insertAfterNode should raise a ValueError when prevNode is None"
        raise check50.Failure(msg)
